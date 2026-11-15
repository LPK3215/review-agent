"""llm.py —— OpenAI 兼容 chat completions 薄封装，带 token 记账。

不用 langchain：agent 循环是自写的 JSON-action 协议，openai SDK 足够，
依赖面小、行为可控。每次调用返回 (text, usage)，usage 由调用方累计。
"""

import json
import time

from . import config

_clients = {}


def _get_client(conf=None):
    conf = conf or config.model_conf()
    key = (conf["base_url"], conf["model"])
    if key not in _clients:
        from openai import OpenAI

        _clients[key] = OpenAI(base_url=conf["base_url"], api_key=conf["api_key"] or "none", timeout=180)
    return _clients[key]


def chat(messages, temperature=0.0, max_tokens=4096, retries=2, conf=None):
    """返回 (text, usage_dict, elapsed_ms)。失败重试 retries 次，仍失败抛错。

    conf 可传 {"base_url","api_key","model"} 覆盖默认端点（换判官用）。
    """
    c = conf or config.model_conf()
    last = None
    for attempt in range(retries + 1):
        try:
            t0 = time.time()
            r = _get_client(c).chat.completions.create(
                model=c["model"],
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            ms = (time.time() - t0) * 1000
            u = r.usage
            usage = {
                "prompt_tokens": getattr(u, "prompt_tokens", 0) or 0,
                "completion_tokens": getattr(u, "completion_tokens", 0) or 0,
                "total_tokens": getattr(u, "total_tokens", 0) or 0,
            }
            return (r.choices[0].message.content or ""), usage, ms
        except Exception as e:  # noqa: BLE001 —— 记账型封装，重试后如实抛
            last = e
            time.sleep(2 * (attempt + 1))
    raise last


def parse_action(text):
    """从模型回复里抠出 {"action":..., "args":{...}} JSON。

    模型偶尔带解释文字，取第一个平衡的 {...} 块；解析失败返回 None。
    """
    if not text:
        return None
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(text[start : i + 1])
                except Exception:
                    return None
                if isinstance(obj, dict) and "action" in obj:
                    return obj
                return None
    return None
