# runs/ · 实验产物说明

| 目录 | 内容 | 说明 |
|---|---|---|
| `smoke-01/` | 单题 review 臂冒烟 | 未入库（.gitignore 默认拦截），仅本地验证用 |
| `bench-01/` | **权威结果**：3 臂 × 50 题全量 | `per_query.jsonl` 逐题增量、`per_query_{arm}.json` 分臂、`per_query.json` 合并、`summary.json` 聚合、`meta.json` 运行参数 |
| `bench-01-rejudge/` | claude-sonnet-4-6 换判官复核 | `summary_rejudge.json`：判分 + 逐题判分理由 |

复现：`python -m src.cli bench --arms single,selfcheck,review --workers 4 --out runs/bench-01`
