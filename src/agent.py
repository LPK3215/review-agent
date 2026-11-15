"""agent.py —— 通用 FC 工具循环（从 llm-wiki agent_fc.py 改造）。

与 llm-wiki 的差别：循环原地推进传入的 messages 列表并返回之，
使 selfcheck 臂能在作者会话上续跑、review 臂能播种修订会话。
mode ∈ query / review / ingest，工具集相同，写权限由 wikitools 按 mode 把关。
"""

import json
import time

from . import config, store, wikitools
from .schema import SCHEMA_MD


def _tools(mode: str):
    write_desc = (
        "把值得留存的综合答案写成新页到 answers/ 下（可选）。"
        if mode == "query"
        else "写一页 wiki。path 只能落在 source/ entity/ concept/ compare/ 四类目录下。"
    )
    read_raw_desc = (
        "回读 raw 原文核实（限 3 次，每次 200 行）。path 为 raw 文件名如 rag-total.md。"
        if mode in ("query", "review")
        else "分节读 raw 原文（不限次数，每次最多 400 行）。path 为 raw 文件名如 rag-total.md。"
    )
    return [
        {"type": "function", "function": {"name": "read_index", "description": "读取 wiki 的 index.md：全部页面的一句话摘要与路径。", "parameters": {"type": "object", "properties": {}, "required": []}}},
        {"type": "function", "function": {"name": "list_pages", "description": "列出 wiki 全部页面（路径/类型/标题/摘要）。", "parameters": {"type": "object", "properties": {}, "required": []}}},
        {"type": "function", "function": {"name": "read_page", "description": "读一页 wiki（frontmatter+正文）。offset/limit 按行分页。", "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "页面相对路径，如 concept/rag-pipeline.md"}, "offset": {"type": "integer"}, "limit": {"type": "integer", "description": "读多少行，默认 400"}}, "required": ["path"]}}},
        {"type": "function", "function": {"name": "search_wiki", "description": "在 wiki 页面全文里按关键词搜索，返回命中片段。", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "description": "返回条数，默认 8"}}, "required": ["query"]}}},
        {"type": "function", "function": {"name": "read_raw", "description": read_raw_desc, "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "offset": {"type": "integer"}, "limit": {"type": "integer", "description": "默认 200 行"}}, "required": ["path"]}}},
        {"type": "function", "function": {"name": "write_page", "description": write_desc, "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string", "description": "含 frontmatter 的完整 markdown"}}, "required": ["path", "content"]}}},
    ]


def _dispatch(name, args, state, mode):
    fn = {
        "read_index": lambda: wikitools.read_index(state),
        "list_pages": lambda: wikitools.list_pages(state),
        "read_page": lambda: wikitools.read_page(state, **args),
        "search_wiki": lambda: wikitools.search_wiki(state, **args),
        "read_raw": lambda: wikitools.read_raw(state, mode=mode, **args),
        "write_page": lambda: wikitools.write_page(state, mode=mode, **args),
    }.get(name)
    if fn is None:
        return wikitools._err(f"unknown tool: {name}")
    try:
        return fn()
    except Exception as e:  # noqa: BLE001
        return wikitools._err(f"tool exception: {e}")


def fc_loop(messages, mode, max_steps, require_first_index=False, state=None):
    """推进 messages 直到模型给出无工具调用的最终回复或步数耗尽。

    返回 {answer, usage, elapsed_ms, steps, trajectory, finished, state}。
    messages 被原地追加，可继续传给下一段循环（selfcheck/revise 用）。
    """
    store.init_wiki_root()
    state = state if state is not None else {}
    conf = config.model_conf()
    import openai

    client = openai.OpenAI(base_url=conf["base_url"], api_key=conf["api_key"], timeout=180)
    tools = _tools(mode)
    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    elapsed = 0.0
    trajectory = []
    answer = ""
    finished = False
    index_read = state.get("index_read", False)

    for step in range(max_steps):
        t0 = time.time()
        tool_choice = "auto"
        if require_first_index and step == 0 and not index_read:
            tool_choice = {"type": "function", "function": {"name": "read_index"}}
        try:
            resp = client.chat.completions.create(
                model=conf["model"], messages=messages, tools=tools,
                tool_choice=tool_choice, temperature=0.0, max_tokens=4096,
            )
        except Exception:
            if tool_choice == "auto":
                raise
            resp = client.chat.completions.create(
                model=conf["model"], messages=messages, tools=tools,
                tool_choice="auto", temperature=0.0, max_tokens=4096,
            )
        elapsed += (time.time() - t0) * 1000
        u = resp.usage
        if u:
            for k in usage:
                usage[k] += getattr(u, k, 0) or 0
        msg = resp.choices[0].message
        calls = msg.tool_calls or []
        rec = {"step": step, "tool_calls": [c.function.name for c in calls]}
        if not calls:
            answer = msg.content or ""
            finished = True
            messages.append({"role": "assistant", "content": answer})
            trajectory.append(rec)
            break
        messages.append({
            "role": "assistant", "content": msg.content or "",
            "tool_calls": [
                {"id": c.id, "type": "function",
                 "function": {"name": c.function.name, "arguments": c.function.arguments}}
                for c in calls
            ],
        })
        for c in calls:
            try:
                args = json.loads(c.function.arguments or "{}")
            except Exception:
                args = {}
            obs = _dispatch(c.function.name, args, state, mode)
            if c.function.name == "read_index":
                index_read = True
            state["index_read"] = index_read
            rec.setdefault("args", {})[c.function.name] = {k: str(v)[:120] for k, v in args.items()}
            rec.setdefault("observe", {})[c.function.name] = obs[:200]
            messages.append({"role": "tool", "tool_call_id": c.id, "content": obs})
        trajectory.append(rec)
        if step == max_steps - 1:
            messages.append({"role": "user", "content": "已达步数上限，请直接给出当前最佳答案，不要再调工具。"})

    if not finished:
        try:
            resp = client.chat.completions.create(
                model=conf["model"], messages=messages, temperature=0.0, max_tokens=4096,
            )
            u = resp.usage
            if u:
                for k in usage:
                    usage[k] += getattr(u, k, 0) or 0
            answer = resp.choices[0].message.content or answer
            messages.append({"role": "assistant", "content": answer})
        except Exception:  # noqa: BLE001
            pass

    return {
        "answer": answer,
        "usage": usage,
        "elapsed_ms": elapsed,
        "steps": len(trajectory),
        "trajectory": trajectory,
        "finished": finished,
        "state": state,
    }


def query_system() -> str:
    return (
        SCHEMA_MD
        + "\n\n## 本次任务：query 模式\n"
        + "回答用户问题。先用 read_index 拿全部页摘要，再 read_page 精读 2~5 个候选页，"
        + "不够用 search_wiki 或沿 [[链接]] 延伸；需要核实时 read_raw 回读（限 3 次）。"
        + "答案用中文，末尾标注依据页（[[path]] 形式）。"
        + "值得留存的综合答案可用 write_page 写到 answers/ 下。"
        + "当你能给出最终答案时，不要再调用工具，直接输出答案全文。"
    )


def author_answer(question: str, max_steps=None):
    """作者臂：与 llm-wiki query/fc 完全同构的作答会话。"""
    messages = [
        {"role": "system", "content": query_system()},
        {"role": "user", "content": question},
    ]
    return messages, fc_loop(messages, "query", max_steps or config.AUTHOR_MAX_STEPS,
                             require_first_index=True)
