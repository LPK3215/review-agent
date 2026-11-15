"""wikitools.py —— FC 工具实现（从 llm-wiki 移植，query/review 共用）。

read_index / list_pages / read_page / search_wiki / read_raw / write_page
全部落到 store 的确定性操作上；LLM 只负责决定何时调谁。
state 为会话级 dict：raw_reads 计数、pages_written 记录。

与 llm-wiki 的差别：新增 mode="review"——复核 Agent 只读不写，
write_page 对 review 模式一律拒绝，防止评审过程污染 wiki。
"""

import json

from . import config, store


def _ok(payload) -> str:
    return "OBSERVE " + json.dumps(payload, ensure_ascii=False)


def _err(msg: str) -> str:
    return "ERROR " + msg


def read_index(state):
    text = config.INDEX_PATH.read_text(encoding="utf-8") if config.INDEX_PATH.exists() else ""
    return _ok({"index": text})


def list_pages(state):
    pages = [(rel, m["type"], m["title"], m["summary"]) for rel, m in store.list_pages()]
    return _ok({"count": len(pages), "pages": pages})


def read_page(state, path, offset=0, limit=400):
    text = store.read_page(path)
    if text is None:
        return _err(f"page not found: {path}")
    lines = text.splitlines()
    chunk = "\n".join(lines[int(offset) : int(offset) + int(limit)])
    return _ok({"path": path, "lines": f"{int(offset) + 1}-{min(int(offset) + int(limit), len(lines))}/{len(lines)}", "content": chunk})


def search_wiki(state, query, limit=8):
    hits = store.search_wiki(query, limit=int(limit))
    return _ok({"hits": hits})


def read_raw(state, path, offset=0, limit=200, mode="query"):
    state["raw_reads"] = state.get("raw_reads", 0) + 1
    if mode in ("query", "review") and state["raw_reads"] > config.QUERY_MAX_RAW_READS:
        return _err(f"raw 回读额度已用完（上限 {config.QUERY_MAX_RAW_READS}）")
    text, total, more = store.read_raw(path, int(offset), int(limit))
    if text is None:
        return _err("raw file not found")
    return _ok({"content": text, "total_lines": total, "has_more": more})


def write_page(state, path, content, mode="query"):
    norm = str(path).replace("\\", "/").lstrip("/")
    if norm.startswith("wiki/"):
        norm = norm[5:]
    if mode == "review":
        return _err("review 模式只读：复核 Agent 不允许写 wiki")
    if mode == "query" and not norm.startswith("answers/"):
        return _err("query 模式只允许写 wiki/answers/ 下的新页")
    if mode == "ingest" and not any(norm.startswith(t) for t in ("source/", "entity/", "concept/", "compare/")):
        return _err("ingest 只允许写 source/entity/concept/compare 四类目录")
    try:
        meta = store.write_page(path, content)
    except Exception as e:  # noqa: BLE001
        return _err(f"write failed: {e}")
    state.setdefault("pages_written", []).append(path)
    return _ok({"written": path, "title": meta["title"], "type": meta["type"]})
