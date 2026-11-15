"""config.py —— 路径、环境变量、LLM 端点配置。

语料与 wiki 复用 llm-wiki 项目的产物（raw 6 篇 + 已编译 wiki 32 页），
拷贝进本项目 data/ 保持独立仓可复现。gold 参考文本用 gold_texts.json
（84 个 gold 块原文，由 queries_50.json 的 gold id 映射）。
"""

import io
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
WIKI_ROOT = DATA_DIR / "wiki-root"
WIKI_DIR = WIKI_ROOT / "wiki"
INDEX_PATH = WIKI_ROOT / "index.md"
LOG_PATH = WIKI_ROOT / "log.md"
SCHEMA_PATH = WIKI_ROOT / "AGENTS.md"
QUERIES_PATH = DATA_DIR / "queries_50.json"
GOLD_PATH = DATA_DIR / "gold_texts.json"
PRISTINE_DIR = DATA_DIR / ".wiki-pristine"
RUNS_DIR = ROOT / "runs"

# Agent 硬上限：防失控循环
AUTHOR_MAX_STEPS = 15
REVIEW_MAX_STEPS = 8
REVISE_MAX_STEPS = 6
SELF_CHECK_MAX_STEPS = 6
QUERY_MAX_RAW_READS = 3


def load_env(path=None):
    if path is None:
        path = ROOT / ".env"
    path = Path(path)
    if not path.exists():
        return None
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    return path


def model_conf() -> dict:
    load_env()
    return {
        "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("OPENAI_MODEL", "deepseek-v4.1-flash"),
    }


def ensure_dirs():
    for d in (DATA_DIR, RAW_DIR, WIKI_ROOT, RUNS_DIR):
        Path(d).mkdir(parents=True, exist_ok=True)
