"""judge.py —— LLM 判官：按 gold 原文给答案打 0/1/2。

判官与答题同一模型、temperature 0；参考材料是 gold 块原文（截断），
不是我们写的「标准答案」，避免把判官引向我们自己的概括。
"""

import json
import re

from . import llm

PROMPT = """你是严格的问答评审。给你一个问题、参考资料（从知识库检索出的相关原文）和一份候选答案。

按下面标准打分，只输出 JSON：
- 2：答案覆盖参考资料的核心要点，没有实质性错误或编造
- 1：部分覆盖，或有明显遗漏/轻微偏差
- 0：未回答、答非所问，或编造了参考资料里没有的内容

{{ "score": 0|1|2, "reason": "一句话理由" }}

问题：{question}

参考资料：
{reference}

候选答案：
{answer}
"""


def judge_answer(question: str, gold_texts: list, answer: str, conf=None, max_tokens=1024):
    ref = "\n\n---\n\n".join(t[:1500] for t in gold_texts)[:6000]
    ans = answer[:4000] if answer else "(空)"
    messages = [{"role": "user", "content": PROMPT.format(question=question, reference=ref, answer=ans)}]
    text, usage, ms = llm.chat(messages, temperature=0.0, max_tokens=max_tokens, conf=conf)
    m = re.search(r"\{.*\}", text, re.S)
    score, reason = None, text[:200]
    if m:
        try:
            obj = json.loads(m.group(0))
            score = int(obj.get("score"))
            reason = str(obj.get("reason", ""))[:300]
        except Exception:
            pass
    if score not in (0, 1, 2):
        # 兜底：从文本里抠数字
        m2 = re.search(r'"score"\s*:\s*([012])', text)
        score = int(m2.group(1)) if m2 else None
    return {"score": score, "reason": reason, "judge_usage": usage, "judge_ms": ms}
