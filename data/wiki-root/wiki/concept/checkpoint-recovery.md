---
title: 检查点与断点恢复：super-step、durability 与四类「停下」
type: concept
sources: [raw/flow-control.md]
updated: 2026-11-09
summary: super-step 粒度、pending writes、durability 三档与存储四档的四类「停下」，以及 D11 实测中重做步骤与重复副作用的变化。
---
# 检查点与断点恢复

## 三个概念先钉死

| 概念 | 是什么 | 不是什么 |
|---|---|---|
| `interrupt()` | 节点内显式的业务断点，payload 要能 JSON 序列化 | 异常处理、通用暂停 |
| Checkpointer | 状态快照底座，`compile(checkpointer=...)` 才生效 | 默认开启 |
| `thread_id` | 检查点主键，复用即续同一条线 | 操作系统线程 ID |

不传 checkpointer，interrupt 无处落盘，恢复与记忆全部失效。^[raw/flow-control.md]

## 粒度是 super-step

一个 super-step 是图的一次 tick：这一步里被调度的节点（可能并行）全部跑完，才写一份完整快照。顺序图 `START → A → B → END` 写四份，看起来像节点边界，本质是 super-step 边界；并行节点在同一步里只产出一份。^[raw/flow-control.md]

**pending writes**：super-step 内部每个节点跑完先把写入落到 task 级，不等整步结束——同一步里 A 成功、B 失败，恢复时 A 不重跑、只补 B。这纠正了「检查点之间崩了全丢」的误解：丢的只是失败节点自己那部分。^[raw/flow-control.md]

## durability 三档与存储四档

| 模式 | 何时写 | 崩溃代价 | 适用 |
|---|---|---|---|
| `exit` | 只在退出时 | 中间态全无 | 长任务、性能优先、可重跑 |
| `async`（默认） | 下一步执行期间异步写 | 小概率丢最近一步 | 绝大多数场景 |
| `sync` | 下一步开始前同步写完 | 每步都有 | 钱、库存、不可重放的外部调用 |

「中途崩溃不会自动快照」只在 `exit` 下成立；默认 `async` 是有快照的，只是可能少最后一步。存储分 InMemorySaver（开发测试）、SqliteSaver（单机验证）、PostgresSaver（生产默认，多进程共享）、MongoDBSaver/Cosmos（已有基础设施）——生产要的是「多个执行进程能访问同一份存储」，而不是「用了 checkpointer」这句话本身。^[raw/flow-control.md]

## 四类「停下」

| # | 场景 | 谁触发 | 有没有检查点 | 怎么继续 |
|---|---|---|---|---|
| ① | 预设人工断点 | 代码里的 `interrupt()` | 有，无限期等待 | resume 加同一 `thread_id` |
| ② | 正常流转 | 运行时 | 每个 super-step 都有 | 不需要 |
| ③ | 外部取消/停机 | 信号、运维 | 硬杀没有；协作式 drain 有 | drain 后可续，SIGKILL 不可 |
| ④ | 异常/报错 | 代码或依赖 | 有上一份 | 从上一份重跑失败那步 |

**只有第一种是「等人」**。异常默认不会自动变人工：未捕获就冒泡终止、状态停在上一份检查点；`error_handler` 是重试耗尽后的补偿路由，做的是处理不是停下来等人。^[raw/flow-control.md]

外部停机两种：硬杀（`kill -9`）来不及写任何东西，async 下最多剩上一步的检查点；协作式 drain 传 `RunControl()`、另起线程 `request_drain()`，在当前 super-step 跑完后停下、写检查点、抛 `GraphDrained`，面向滚动发布与 SIGTERM。drain 是「有序地停」，不是HITL。^[raw/flow-control.md]

一句话分界：**框架负责停在哪、存什么、从哪续；业务负责要不要停、停了问谁、续了会不会重复扣钱。**^[raw/flow-control.md]

## 一个反直觉结论与实测

检查点不等于「恰好执行一次」：它只保证「知道从哪继续」，不保证「副作用只发生一次」，后者要靠 [[concept-idempotency]]，两者缺一不可。^[raw/flow-control.md]

D11 实测（`checkpoint-recovery`，2026-11-13，4 场景 × 2 模式 × 3 次重复）：基线无检查点、恢复即整链重跑恒 5 步；增强为 SqliteSaver（durability=sync）+ 幂等注册表后，crash 场景重做 2 步、write_fail 1 步、raise 3 步，重复副作用全部为 0（基线 crash 场景为 1）。耗时上 clean 场景增强版略慢（34 vs 11ms），崩溃场景因少重做反而更快（3891 vs 4144ms）。durability 同现场对照：sync 崩后重做 2 步，exit 硬杀后快照全无、整链重做 5 步，async 丢最近一步依赖调度时序、未量化。失效条件：单步任务、或可整体重跑且无副作用的场景，收益接近于零。^[raw/flow-control.md]

落盘之前的断点本身怎么写，见 [[concept-interrupt-hitl]]；失败分类与重试纪律见 [[concept-agent-reliability]]。
