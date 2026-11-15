"""store.py —— wiki 文件层：页面读写、index/log 簿记、链接图、检索。

设计口径：LLM 只产出页面内容，index.md 与 log.md 由代码从 frontmatter
确定性重建——簿记不交给模型，保证目录永远与文件系统一致（lint 的
index 漂移检查才有意义）。
"""

import hashlib
import re
from datetime import date
from pathlib import Path

from . import config

PAGE_TYPES = ("source", "entity", "concept", "compare", "answer")

_FM = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)
_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


def today():
    return date.today().isoformat()


def slugify(name: str) -> str:
    s = re.sub(r"[^0-9A-Za-z一-鿿_-]+", "-", name.strip().lower())
    return re.sub(r"-{2,}", "-", s).strip("-") or "untitled"


def list_raw():
    return sorted(p.name for p in config.RAW_DIR.glob("*.md"))


def read_raw(rel_path: str, offset: int = 0, limit: int = 200):
    """按行切片读 raw 文件；返回 (text, total_lines, has_more)。"""
    p = (config.RAW_DIR / Path(rel_path).name).resolve()
    if config.RAW_DIR.resolve() not in p.parents or not p.exists():
        return None, 0, False
    lines = p.read_text(encoding="utf-8").splitlines()
    total = len(lines)
    offset = max(0, offset)
    limit = max(1, min(limit, 400))
    chunk = lines[offset : offset + limit]
    header = f"# {p.name} 行 {offset + 1}-{min(offset + limit, total)} / {total}\n"
    return header + "\n".join(chunk), total, offset + limit < total


def list_pages():
    """返回 [(rel_path, meta)]，rel_path 相对 wiki/。"""
    out = []
    if not config.WIKI_DIR.exists():
        return out
    for p in sorted(config.WIKI_DIR.rglob("*.md")):
        rel = p.relative_to(config.WIKI_DIR).as_posix()
        meta = parse_page(p.read_text(encoding="utf-8"))
        out.append((rel, meta))
    return out


def page_path(rel: str) -> Path:
    """把 'concept/chroma.md' 规整为 wiki 内绝对路径，防目录逃逸。"""
    rel = rel.replace("\\", "/").lstrip("/")
    if rel.startswith("wiki/"):
        rel = rel[5:]
    if not rel.endswith(".md"):
        rel += ".md"
    p = (config.WIKI_DIR / rel).resolve()
    if config.WIKI_DIR.resolve() not in p.parents:
        raise ValueError(f"path escapes wiki dir: {rel}")
    return p


def parse_page(text: str):
    """拆 frontmatter；返回 dict(title/type/sources/updated/summary/links/body_len)。"""
    m = _FM.match(text)
    meta = {"title": "", "type": "", "sources": [], "updated": "", "summary": "", "links": [], "raw_len": len(text)}
    body = text
    if m:
        fm, body = m.group(1), m.group(2)
        for line in fm.splitlines():
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k, v = k.strip(), v.strip()
            if k == "sources":
                meta["sources"] = re.findall(r"[\w./-]+\.md", v)
            elif k in meta:
                meta[k] = v.strip('"')
    meta["links"] = sorted(set(_WIKILINK.findall(body)))
    return meta


def read_page(rel: str, max_chars: int = 12000):
    p = page_path(rel)
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    if len(text) > max_chars:
        return text[:max_chars] + f"\n\n…(截断，全文 {len(text)} 字符，用 offset 续读)"
    return text


def write_page(rel: str, content: str):
    """写页面并返回 meta。要求 frontmatter 齐全；缺字段自动补。"""
    p = page_path(rel)
    p.parent.mkdir(parents=True, exist_ok=True)
    meta = parse_page(content)
    if not meta["title"]:
        meta["title"] = Path(rel).stem
    if not meta["type"]:
        meta["type"] = p.parent.name if p.parent.name in PAGE_TYPES else "concept"
    if not meta["updated"]:
        meta["updated"] = today()
    if not meta["summary"]:
        meta["summary"] = meta["title"]
    # 重建 frontmatter，保证字段顺序与格式统一
    fm = [
        "---",
        f"title: {meta['title']}",
        f"type: {meta['type']}",
        f"sources: [{', '.join(meta['sources'])}]" if meta['sources'] else "sources: []",
        f"updated: {meta['updated']}",
        f"summary: {meta['summary']}",
        "---",
    ]
    body = _FM.match(content)
    body_text = body.group(2) if body else content
    p.write_text("\n".join(fm) + "\n" + body_text.lstrip("\n"), encoding="utf-8")
    return meta


def rebuild_index():
    """从页面 frontmatter 重建 index.md；返回写入的条目数。"""
    pages = list_pages()
    groups = {}
    for rel, meta in pages:
        groups.setdefault(meta["type"] or "misc", []).append((rel, meta))
    lines = ["# Wiki Index", "", "> 由代码从页面 frontmatter 重建，勿手改。", ""]
    order = [t for t in PAGE_TYPES if t in groups] + sorted(set(groups) - set(PAGE_TYPES))
    for t in order:
        lines.append(f"## {t}（{len(groups[t])}）")
        lines.append("")
        for rel, meta in groups[t]:
            name = rel[:-3] if rel.endswith(".md") else rel
            lines.append(f"- [[{name}]] {meta['summary'] or meta['title']}")
        lines.append("")
    config.INDEX_PATH.write_text("\n".join(lines), encoding="utf-8")
    return len(pages)


def append_log(kind: str, detail: str):
    config.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    stamp = f"## [{today()}] {kind} | {detail}"
    if config.LOG_PATH.exists():
        with open(config.LOG_PATH, "a", encoding="utf-8") as f:
            f.write("\n" + stamp + "\n")
    else:
        config.LOG_PATH.write_text("# Wiki Log\n\n" + stamp + "\n", encoding="utf-8")


def search_wiki(query: str, limit: int = 8):
    """大小写不敏感子串搜索全部 wiki 页，返回 'path:行号 — 片段' 列表。"""
    q = query.lower()
    hits = []
    for rel, _meta in list_pages():
        p = page_path(rel)
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            if q in line.lower():
                hits.append(f"{rel}:{i} — {line.strip()[:120]}")
                if len([h for h in hits if h.startswith(rel)]) >= 3:
                    break
        if len(hits) >= limit:
            break
    return hits[:limit]


def raw_hashes():
    """raw/*.md 的 sha256 清单，ingest 时记录、lint 时比对。"""
    out = {}
    for p in sorted(config.RAW_DIR.glob("*.md")):
        out[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def init_wiki_root():
    """建骨架：目录 + 空 index/log + AGENTS.md schema。"""
    config.ensure_dirs()
    for t in ("source", "entity", "concept", "compare", "answers"):
        (config.WIKI_DIR / t).mkdir(parents=True, exist_ok=True)
    if not config.SCHEMA_PATH.exists():
        from .schema import SCHEMA_MD

        config.SCHEMA_PATH.write_text(SCHEMA_MD, encoding="utf-8")
    if not config.INDEX_PATH.exists():
        config.INDEX_PATH.write_text("# Wiki Index\n\n> 由代码从页面 frontmatter 重建，勿手改。\n", encoding="utf-8")
    if not config.LOG_PATH.exists():
        config.LOG_PATH.write_text("# Wiki Log\n", encoding="utf-8")
    return True
