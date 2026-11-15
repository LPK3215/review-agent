"""review.py —— 独立复核 Agent 与修订会话（D12 的核心变量）。

复核者是**独立会话**：新 system、新 messages、不带作者轨迹，
只看到「问题 + 候选答案」，要自己用工具回 wiki 查证。
与作者同模型同工具集，差别只在角色提示词与只读权限（mode=review）。
"""

import re

from . import config
from .agent import fc_loop, query_system

REVIEWER_SYSTEM = """你是独立答案评审，不是答案作者。另一个 Agent 已经针对用户问题给出候选答案，你的任务是核对它。

工作方式：
1. 先用 read_index 拿目录，必要时 read_page / search_wiki / read_raw（限 3 次）回 wiki 查证候选答案里的事实性声明。
2. 只评审「事实与覆盖」，不改写答案、不补全答案。
3. 你处于只读模式，不能写 wiki。

输出格式（严格遵守，先 verdict 行，再 issues 列表，最后 suggestion 段）：
VERDICT: correct | partial | wrong
ISSUES:
- <问题1：错在哪/漏了什么，指明 wiki 依据页>
- <问题2；没有就写「无」>
SUGGESTION:
<一段话：作者修订时应优先处理什么；若 correct 则写「答案可用，无需修改」>
"""

SELF_CHECK_PROMPT = (
    "请自查刚才的答案：对照你查到的 wiki 依据，检查有没有事实性错误、"
    "关键遗漏或编造内容。可以再调工具补充核实（raw 回读额度已用完的除外）。"
    "自查完直接输出修订后的最终答案全文，不要输出自查过程。"
)

REVISE_SYSTEM = (
    query_system()
    + "\n\n## 本次任务：修订模式\n"
    + "你是答案作者。对话中给出了你的草稿答案和一位独立复核者的评审意见。"
    + "请核实评审意见（可用工具补充查证，raw 回读限 3 次），然后输出修订后的最终答案全文。"
    + "如果评审意见有误或不成立，保留原答案并说明理由；不要因为复核而改错。"
)


def _parse_verdict(text: str) -> str:
    m = re.search(r"VERDICT\s*:\s*(correct|partial|wrong)", text or "", re.I)
    return m.group(1).lower() if m else "unparsed"


def review_critique(question: str, draft: str, max_steps=None):
    """独立复核会话：返回 {text, verdict, usage, elapsed_ms, steps, finished}。"""
    messages = [
        {"role": "system", "content": REVIEWER_SYSTEM},
        {"role": "user", "content": f"用户问题：\n{question}\n\n候选答案：\n{draft}"},
    ]
    rec = fc_loop(messages, "review", max_steps or config.REVIEW_MAX_STEPS,
                  require_first_index=True)
    return {
        "text": rec["answer"],
        "verdict": _parse_verdict(rec["answer"]),
        "usage": rec["usage"],
        "elapsed_ms": rec["elapsed_ms"],
        "steps": rec["steps"],
        "finished": rec["finished"],
        "trajectory": rec["trajectory"],
    }


def revise_answer(question: str, draft: str, critique: str, max_steps=None):
    """修订会话：播种 [草稿 + 评审意见]，允许补充工具查证后输出终稿。"""
    messages = [
        {"role": "system", "content": REVISE_SYSTEM},
        {"role": "user", "content": question},
        {"role": "assistant", "content": draft},
        {"role": "user", "content": "【独立复核意见】\n" + (critique or "（复核者未给出有效意见）")
         + "\n\n请输出修订后的最终答案全文。"},
    ]
    rec = fc_loop(messages, "query", max_steps or config.REVISE_MAX_STEPS,
                  require_first_index=False)
    return {
        "answer": rec["answer"],
        "usage": rec["usage"],
        "elapsed_ms": rec["elapsed_ms"],
        "steps": rec["steps"],
        "finished": rec["finished"],
        "trajectory": rec["trajectory"],
    }
