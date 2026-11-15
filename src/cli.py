"""cli.py —— review-agent 入口。

用法：
  python -m src.cli bench [--arms single,selfcheck,review] [--limit N] [--workers 4]
  python -m src.cli bench --arms review --limit 3        # 冒烟
"""

import argparse
import json

from . import bench


def main():
    ap = argparse.ArgumentParser(prog="review-agent")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("bench", help="跑三臂对照 bench")
    b.add_argument("--arms", default="single,selfcheck,review",
                   help="逗号分隔：single,selfcheck,review")
    b.add_argument("--limit", type=int, default=None, help="只跑前 N 题")
    b.add_argument("--workers", type=int, default=4, help="题间并发数")
    b.add_argument("--queries", default=None, help="自定义测试集 json")
    b.add_argument("--out", default=None, help="输出目录")
    b.add_argument("--no-judge", action="store_true", help="跳过判官")
    b.add_argument("--judge-model", default=None,
                   help="换判官模型（仍走同一端点）")

    args = ap.parse_args()
    if args.cmd == "bench":
        arms = [a.strip() for a in args.arms.split(",") if a.strip()]
        bad = [a for a in arms if a not in bench.ARMS]
        if bad:
            ap.error(f"unknown arms: {bad}（可选 {list(bench.ARMS)}）")
        queries = bench.load_queries(args.queries) if args.queries else None
        if args.limit:
            queries = (queries or bench.load_queries())[: args.limit]
        judge_conf = None
        if args.judge_model:
            from . import config
            conf = config.model_conf()
            judge_conf = {"base_url": conf["base_url"], "api_key": conf["api_key"],
                          "model": args.judge_model}
        bench.run_bench(
            arms=arms, queries=queries, workers=args.workers,
            judge_conf=judge_conf, out_dir=args.out, do_judge=not args.no_judge,
        )


if __name__ == "__main__":
    main()
