# review-agent

> **所属专项**：多智能体协作（D12 独立复核 Agent）
> **设计与实验文档**：笔记库 `02-AI/AI专项/多智能体协作/`（待回填）
> **语料来源**：复用 llm-wiki 项目的 6 篇 raw + 已编译 wiki（32 页）与 50 题标注集，拷贝于 `data/`，本仓可独立复现。

## 要回答的问题

多一个「独立复核 Agent」到底值不值？D12 的最小实验：

- **single**：作者 Agent 直接作答（基线，与 llm-wiki query/fc 同构）
- **selfcheck**：同一作者会话续跑一轮自查——同预算对照，没有独立角色
- **review**：作者草稿 → **独立复核 Agent**（新会话、只读权限、自己回 wiki 查证）→ 作者据评审意见修订

比较：判官分（0/1/2，gold 块原文做参考）、逐题改对/错改、token、时延、调用数。

## 结构

```
data/
  raw/            6 篇原始语料（llm-wiki 拷贝，只读）
  wiki-root/      已编译 wiki（32 页，拷贝自 llm-wiki ingest 产物）
  queries_50.json 50 题标注集（exact 30 / semantic 20，gold=块 id）
  gold_texts.json 84 个 gold 块原文（判官参考，已按需裁剪）
src/
  agent.py        通用 FC 工具循环（在 llm-wiki agent_fc 基础上改为可续跑）
  review.py       复核者 prompt/解析 + 修订会话
  wikitools.py    6 个 wiki 工具（review 模式只读）
  store.py        wiki 文件层（frontmatter/index 簿记）
  judge.py        LLM 判官（0/1/2，gold 原文参考）
  bench.py        三臂编排 + 逐题判分 + 汇总
runs/
  bench-01/       权威结果（见 过程文档.md）
```

## 运行

```bash
pip install -r requirements.txt
cp .env.example .env   # 填 OpenAI 兼容端点三件套

# 冒烟（1 题 review 臂）
python -m src.cli bench --arms review --limit 1 --workers 1 --out runs/smoke-01

# 全量（3 臂 × 50 题）
python -m src.cli bench --arms single,selfcheck,review --workers 4 --out runs/bench-01

# 换判官复核
python -m src.cli bench --arms single,selfcheck,review --judge-model <model> --out runs/bench-01-rejudge
```

每臂跑前 wiki 自动重置为 `data/.wiki-pristine` 快照（三臂同一起点）；
`per_query.jsonl` 逐题增量落盘，中断不丢已完成题。

## 结果（2026-11-15，`runs/bench-01/` + `bench-01-rejudge/`）

**阴性结果：独立复核 Agent 不值。**

| 臂 | judge 均分（deepseek / claude） | token/题 | 调用/题 |
|---|---|---|---|
| single | **1.78 / 1.84** | 25.8k | 4.3 |
| selfcheck | 1.78 / 1.78 | 45.3k | 6.1 |
| review | 1.74 / 1.74 | 92.2k（3.6×） | 12.3 |

review 逐题 vs single：+6/−10（deepseek）、+3/−9（claude）——两个判官方向一致为负。机理：复核者挑刺触发无门禁重写，高基线答案被改偏；详见 `过程文档.md` 与笔记库《独立复核Agent实测》。
