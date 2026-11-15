"""rejudge.py —— 换判官复核 bench 结果。

读 runs/<bench>/per_query.json，对每臂 final（review 臂加 draft）
用另一个模型重判，输出 runs/<bench>-rejudge/summary_rejudge.json。
用法：python -m scripts.rejudge --bench runs/bench-01 --judge-model auto/claude-sonnet-4-6
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import config, judge  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", required=True)
    ap.add_argument("--judge-model", required=True)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    bench_dir = Path(args.bench)
    rows = json.loads((bench_dir / "per_query.json").read_text(encoding="utf-8"))
    gold = json.loads(config.GOLD_PATH.read_text(encoding="utf-8"))
    conf = config.model_conf()
    jconf = {"base_url": conf["base_url"], "api_key": conf["api_key"], "model": args.judge_model}

    tasks = []
    for r in rows:
        gold_texts = [gold.get(g, "") for g in r["gold"]]
        for arm, a in r["arms"].items():
            for tag in ("final", "draft"):
                ans = a.get(tag)
                if ans is None or not isinstance(ans, str):
                    continue
                if tag == "draft" and arm != "review":
                    continue
                tasks.append((r["id"], r["text"], arm, tag, ans, gold_texts))

    results = {}
    done = [0]

    def work(t):
        qid, qtext, arm, tag, ans, gold_texts = t
        jr = judge.judge_answer(qtext, gold_texts, ans, conf=jconf)
        return (qid, arm, tag, jr["score"], jr["reason"])

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(work, t) for t in tasks]
        for fut in as_completed(futs):
            qid, arm, tag, score, reason = fut.result()
            results.setdefault(qid, {}).setdefault(arm, {})[tag] = {"score": score, "reason": reason}
            done[0] += 1
            if done[0] % 20 == 0:
                print(f"[rejudge] {done[0]}/{len(tasks)}", flush=True)

    # 汇总
    summary = {}
    for arm in ("single", "selfcheck", "review"):
        for qtype in ("exact", "semantic", "all"):
            sel = [r for r in rows if qtype == "all" or r["type"] == qtype]
            scores = []
            for r in sel:
                s = results.get(r["id"], {}).get(arm, {}).get("final", {}).get("score")
                if s is not None:
                    scores.append(s)
            if scores:
                summary[f"{arm}/{qtype}"] = round(sum(scores) / len(scores), 3)

    for arm in ("selfcheck", "review"):
        diff = {"improved": 0, "degraded": 0, "same": 0, "unscored": 0}
        for r in rows:
            a = results.get(r["id"], {}).get("single", {}).get("final", {}).get("score")
            b = results.get(r["id"], {}).get(arm, {}).get("final", {}).get("score")
            if a is None or b is None:
                diff["unscored"] += 1
            elif b > a:
                diff["improved"] += 1
            elif b < a:
                diff["degraded"] += 1
            else:
                diff["same"] += 1
        summary[f"delta/{arm}_vs_single"] = diff

    # review 草稿 vs 终稿
    d = {"draft_better": 0, "final_better": 0, "tie": 0, "unscored": 0}
    for r in rows:
        ds = results.get(r["id"], {}).get("review", {}).get("draft", {}).get("score")
        fs = results.get(r["id"], {}).get("review", {}).get("final", {}).get("score")
        if ds is None or fs is None:
            d["unscored"] += 1
        elif fs > ds:
            d["final_better"] += 1
        elif fs < ds:
            d["draft_better"] += 1
        else:
            d["tie"] += 1
    summary["review/draft_vs_final_judge"] = d

    out = bench_dir.parent / (bench_dir.name + "-rejudge")
    out.mkdir(parents=True, exist_ok=True)
    payload = {"judge_model": args.judge_model, "created": time.strftime("%Y-%m-%d %H:%M:%S"),
               "summary": summary, "per_question": results}
    (out / "summary_rejudge.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print(f"[rejudge] done -> {out}", flush=True)


if __name__ == "__main__":
    main()
