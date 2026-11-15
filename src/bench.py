"""bench.py —— D12 三臂对照：single / selfcheck / review。

- single   ：作者 Agent 直接作答（= llm-wiki query/fc 同构基线）
- selfcheck：同一作者会话续跑一轮自查（同预算对照，无独立角色）
- review   ：作者草稿 → 独立复核 Agent（只读、查 wiki）→ 作者据意见修订

每臂跑前把 wiki 重置为建 bench 时的快照，保证三臂起点一致；
answers/ 回写在臂内自然累积（与 llm-wiki bench 同口径）。
判官与 llm-wiki 同 prompt 同模型（gold 块原文做参考）。

产出 runs/<ts>-review/:
  per_query.jsonl  逐题增量（每题完成即追加，防中断丢进度）
  summary.json     分臂分类型聚合 + 相对 single 的改对/错改统计
  meta.json        模型、臂、测试集、时间戳
"""

import json
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from . import agent, config, judge, review, store


def load_queries(path=None):
    p = Path(path) if path else config.QUERIES_PATH
    return json.loads(p.read_text(encoding="utf-8"))["queries"]


def load_gold_texts():
    return json.loads(config.GOLD_PATH.read_text(encoding="utf-8"))


def snapshot_pristine():
    """首次建 bench 时把 wiki-root 整体快照；之后每臂重置用。"""
    if config.PRISTINE_DIR.exists():
        return
    shutil.copytree(config.WIKI_ROOT, config.PRISTINE_DIR)


def reset_wiki():
    if config.WIKI_ROOT.exists():
        shutil.rmtree(config.WIKI_ROOT)
    shutil.copytree(config.PRISTINE_DIR, config.WIKI_ROOT)


def _merge_usage(*recs):
    out = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    for r in recs:
        for k in out:
            out[k] += (r.get("usage") or {}).get(k, 0) or 0
    return out


def _sum_ms(*recs):
    return sum(r.get("elapsed_ms", 0) or 0 for r in recs)


def _sum_steps(*recs):
    return sum(r.get("steps", 0) or 0 for r in recs)


def run_single(q):
    messages, rec = agent.author_answer(q["text"])
    return {
        "final": rec["answer"],
        "usage": rec["usage"], "elapsed_ms": rec["elapsed_ms"], "steps": rec["steps"],
        "finished": rec["finished"], "trajectory": rec["trajectory"],
    }


def run_selfcheck(q):
    messages, rec = agent.author_answer(q["text"])
    draft = rec["answer"]
    messages.append({"role": "user", "content": review.SELF_CHECK_PROMPT})
    rec2 = agent.fc_loop(messages, "query", config.SELF_CHECK_MAX_STEPS,
                         require_first_index=False, state=rec["state"])
    return {
        "draft": draft,
        "final": rec2["answer"],
        "usage": _merge_usage(rec, rec2), "elapsed_ms": _sum_ms(rec, rec2),
        "steps": _sum_steps(rec, rec2), "finished": rec["finished"] and rec2["finished"],
        "trajectory": rec["trajectory"] + rec2["trajectory"],
    }


def run_review(q):
    messages, rec = agent.author_answer(q["text"])
    draft = rec["answer"]
    crit = review.review_critique(q["text"], draft)
    rev = review.revise_answer(q["text"], draft, crit["text"])
    return {
        "draft": draft,
        "critique": crit["text"],
        "verdict": crit["verdict"],
        "final": rev["answer"],
        "usage": _merge_usage(rec, crit, rev), "elapsed_ms": _sum_ms(rec, crit, rev),
        "steps": _sum_steps(rec, crit, rev), "finished": rec["finished"] and rev["finished"],
        "trajectory": rec["trajectory"] + crit["trajectory"] + rev["trajectory"],
    }


ARMS = {"single": run_single, "selfcheck": run_selfcheck, "review": run_review}


def _judge_row(judge_conf, q, gold_texts, row):
    """给该题所有臂的最终答案判分；review 臂额外判草稿分。"""
    for arm in row.get("arms", {}):
        a = row["arms"][arm]
        targets = [("final", a["final"])]
        if arm == "review" and a.get("draft") is not None:
            targets.append(("draft", a["draft"]))
        a["judge"] = {}
        for tag, ans in targets:
            jr = judge.judge_answer(q["text"], gold_texts, ans, conf=judge_conf)
            a["judge"][tag] = {"score": jr["score"], "reason": jr["reason"]}
            a["judge_usage"] = jr["judge_usage"]


def run_arm(arm, queries, gold_map, judge_conf, do_judge, workers, on_done):
    fn = ARMS[arm]
    rows = [None] * len(queries)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fn, q): i for i, q in enumerate(queries)}
        for fut in as_completed(futs):
            i = futs[fut]
            try:
                res = fut.result()
            except Exception as e:  # noqa: BLE001 —— 单题失败不拖垮整批
                res = {"error": f"{type(e).__name__}: {e}", "final": "", "usage": {},
                       "elapsed_ms": 0, "steps": 0, "finished": False}
            q = queries[i]
            gold_texts = [gold_map.get(g, "") for g in q["gold"]]
            row = {"id": q["id"], "type": q["type"], "text": q["text"],
                   "gold": q["gold"], "arms": {arm: res}}
            if do_judge:
                _judge_row(judge_conf, q, gold_texts, row)
            rows[i] = row
            on_done(i, row)
            print(f"[bench] {arm} {q['id']} done", flush=True)
    return [r for r in rows if r is not None]


def run_bench(arms=("single", "selfcheck", "review"), queries=None, workers=4,
              judge_conf=None, out_dir=None, do_judge=True):
    config.ensure_dirs()
    store.init_wiki_root()
    snapshot_pristine()
    queries = queries or load_queries()
    gold_map = load_gold_texts()

    out = Path(out_dir) if out_dir else config.RUNS_DIR / time.strftime("%Y%m%d-%H%M%S") + "-review"
    out.mkdir(parents=True, exist_ok=True)
    jsonl = out / "per_query.jsonl"
    jsonl.write_text("", encoding="utf-8")

    all_rows = []

    def on_done(i, row):
        with open(jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    for arm in arms:
        print(f"[bench] === arm {arm} ===", flush=True)
        reset_wiki()
        rows = run_arm(arm, queries, gold_map, judge_conf, do_judge,
                       workers, on_done)
        all_rows.extend(rows)
        (out / f"per_query_{arm}.json").write_text(
            json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    # 汇总：按题聚合三臂
    by_q = {}
    for r in all_rows:
        by_q.setdefault(r["id"], {"id": r["id"], "type": r["type"], "text": r["text"], "gold": r["gold"], "arms": {}})
        by_q[r["id"]]["arms"].update(r["arms"])
    merged = list(by_q.values())
    (out / "per_query.json").write_text(json.dumps(merged, ensure_ascii=False, indent=1), encoding="utf-8")

    summary = _summarize(merged, list(arms))
    meta = {
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "model": config.model_conf()["model"],
        "base_url": config.model_conf()["base_url"],
        "judge_model": (judge_conf or {}).get("model") or config.model_conf()["model"],
        "queries": len(queries),
        "arms": list(arms),
        "workers": workers,
        "judge": do_judge,
        "wiki_pages": len(store.list_pages()),
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[bench] done -> {out}", flush=True)
    return out, merged, summary


def _pct(vals, p):
    if not vals:
        return None
    s = sorted(vals)
    return s[min(len(s) - 1, int(p * len(s)))]


def _arm_score(row, arm, tag="final"):
    try:
        return row["arms"][arm]["judge"][tag]["score"]
    except Exception:
        return None


def _summarize(merged, arms):
    out = {}
    for arm in arms:
        for qtype in ("exact", "semantic", "all"):
            rows = [r for r in merged if qtype == "all" or r["type"] == qtype]
            if not rows:
                continue
            scored = [s for r in rows if (s := _arm_score(r, arm)) is not None]
            tokens = [r["arms"][arm]["usage"].get("total_tokens", 0) for r in rows if arm in r["arms"]]
            calls = [r["arms"][arm].get("steps", 0) for r in rows if arm in r["arms"]]
            lat = [r["arms"][arm].get("elapsed_ms", 0) for r in rows if arm in r["arms"]]
            out[f"{arm}/{qtype}"] = {
                "n": len(rows),
                "judge_mean": round(sum(scored) / len(scored), 3) if scored else None,
                "judge_n": len(scored),
                "tokens_mean": round(sum(tokens) / len(tokens), 1) if tokens else None,
                "calls_mean": round(sum(calls) / len(calls), 2) if calls else None,
                "lat_mean_ms": round(sum(lat) / len(lat), 1) if lat else None,
                "lat_p50_ms": round(_pct(lat, 0.5) or 0, 1),
            }

    # 相对 single 的逐题变化（all 口径；分类型在分析时再切）
    if "single" in arms:
        for arm in arms:
            if arm == "single":
                continue
            diff = {"improved": 0, "degraded": 0, "same": 0, "unscored": 0}
            for r in merged:
                a, b = _arm_score(r, "single"), _arm_score(r, arm)
                if a is None or b is None:
                    diff["unscored"] += 1
                elif b > a:
                    diff["improved"] += 1
                elif b < a:
                    diff["degraded"] += 1
                else:
                    diff["same"] += 1
            out[f"delta/{arm}_vs_single"] = diff

        # review 臂：复核者 verdict 分布 + 草稿 vs 终稿判分变化
        if "review" in arms:
            verdicts = {}
            draft_vs_final = {"draft_better": 0, "final_better": 0, "tie": 0, "unscored": 0}
            for r in merged:
                a = r["arms"].get("review")
                if not a:
                    continue
                v = a.get("verdict") or "unparsed"
                verdicts[v] = verdicts.get(v, 0) + 1
                ds = _arm_score(r, "review", "draft")
                fs = _arm_score(r, "review", "final")
                if ds is None or fs is None:
                    draft_vs_final["unscored"] += 1
                elif fs > ds:
                    draft_vs_final["final_better"] += 1
                elif fs < ds:
                    draft_vs_final["draft_better"] += 1
                else:
                    draft_vs_final["tie"] += 1
            out["review/verdict_dist"] = verdicts
            out["review/draft_vs_final_judge"] = draft_vs_final
    return out
