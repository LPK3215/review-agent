---
title: 流程控制与可靠性（原文摘要）
type: source
sources: [raw/flow-control.md]
updated: 2026-11-14
summary: 编排模式、错误分层、幂等、检查点与 HITL 的机制总纲，附 D11 断点恢复对照实测数据。
---
# 流程控制与可靠性（原文摘要）

本页把 raw/flow-control.md 十三章压成判断句，覆盖「工作流怎么编排、错误怎么分、重试与幂等怎么写、检查点存在哪、人怎么介入、崩了怎么续」。^[raw/flow-control.md]

## 一、Agent 与普通程序的可靠性差异

普通服务靠「重试 + 事务」就够；Agent 单次执行从秒到小时、有状态、可中途干预、副作用跨外部系统，所以还多一层「可中断、可恢复、副作用可重放」。^[raw/flow-control.md]

失败分四类：瞬时故障（可退避重试）、永久故障（重试只会浪费）、语义故障（模型判断错，要改判断）、编排故障（卡死、循环不收敛，要超时与步数上限兜底）。**只有第一类值得自动重试**，其余丢进重试只会放大延迟与账单。^[raw/flow-control.md]

三道防线「预防 → 检测 → 恢复」必须同时存在：只有预防是赌不出事，只有恢复是每次重跑。^[raw/flow-control.md]

分工边界：检查点底层实现与记忆分层归记忆与上下文管理；工具级超时与沙箱归工具调用；审批与权限归用户与鉴权 4.4；多副本与停机归部署与运维。^[raw/flow-control.md]

## 二、六种编排模式

链式（步骤固定、一步错全链停）、路由（输入类型差异大、分类错就全错）、并行（子任务独立，难点在合并冲突）、协调者/工作者（可拆且异构，协调者是瓶颈）、评估者/优化者（质量要求高、轮数 2–3 轮后收益递减）、自主循环（最灵活最不可控，必须有最大步数、单步超时、总成本上限三条）。^[raw/flow-control.md]

选择路径：步骤固定→有分支则路由否则链式；步骤不固定→任务可拆则协调者/工作者或并行；否则质量要求高走评估者/优化者，再否则自主循环。^[raw/flow-control.md]

## 三、错误分类与三层策略

错误分输入/处理/输出三类，分类的意义是定位：入口错误不该进重试，输出错误不该在模型侧调参数。预防手段是输入校验、工具白名单、输出格式写死、预算约束；检测靠结构校验、合理性、耗时、循环检测；恢复有重试、降级、换路、人工接管、回滚五种，各有代价。^[raw/flow-control.md]

容错三机制：冗余（关键路径有备份）、隔离（单工具失败不拖垮整轮）、监控（成功率/延迟/错误分布）。^[raw/flow-control.md]

## 四、超时、重试、熔断、降级

四种手段分工明确、互不替代：超时解决无限等待但不解决慢而终成功；重试解决瞬时故障但会放大永久故障的损失；熔断解决持续失败还继续打；降级解决依赖不可用但带来质量损失。重试三纪律：只对可恢复异常、次数上限加指数退避带抖动、重试前先判幂等。熔断阈值后要放探针试探；降级必须显式告知用户，否则用户以为拿到完整结果。^[raw/flow-control.md]

LangGraph 1.2 起把这套做进框架：`RetryPolicy(retry_on=..., max_attempts=...)` 挂 `add_node` 只重试指定异常、`TimeoutPolicy(idle_timeout=..., run_timeout=...)` 超时抛 `NodeTimeoutError`、`runtime.heartbeat()` 给长任务续命、`error_handler`（重试耗尽后的补偿路由，可 `Command(goto=...)`）、`set_node_defaults`（图级统一 retry/timeout/error_handler）。关键分界：`interrupt()` 走 `GraphBubbleUp`，**不进 error_handler、不被重试**，中断与报错是两条路。^[raw/flow-control.md]

## 五、幂等

超时后重试与恢复时节点重入都会导致同一逻辑执行两次。三种做法：幂等键（下游按键去重，适合外部写接口）、先查后写（有天然业务唯一键）、状态机（只允许特定态迁移，适合长流程）。落位原则：高风险动作放在确认之后，低风险查询放在确认之前。^[raw/flow-control.md]

## 六、检查点

三个概念钉死：`interrupt()` 是节点内显式业务断点（不是异常处理）；Checkpointer 是状态快照底座，须 `compile(checkpointer=...)` 才生效（不是默认开）；`thread_id` 是检查点主键（不是线程 ID）。不传 checkpointer，interrupt 无处落盘，恢复与记忆全部失效。^[raw/flow-control.md]

粒度是 **super-step**（图的一次 tick，并行节点同一步只产一份快照）；顺序图 START→A→B→END 写四份。pending writes 让同一步里 A 成功 B 失败时只补 B，纠正「检查点之间崩了全丢」的误解。^[raw/flow-control.md]

durability 三档：`exit`（只在退出时写，中间态全无，适合可重跑的长任务）、`async`（默认，异步写，小概率丢最近一步）、`sync`（每步开始前同步写完，用于钱/库存/不可重放的外部调用）。「中途崩溃不会自动快照」只在 `exit` 下成立。存储四档：InMemory（开发）、Sqlite（单机验证）、Postgres（生产默认，多进程共享）、Mongo/Cosmos（已有基础设施）。生产要的是「多进程能访问同一份存储」。^[raw/flow-control.md]

## 七、四类「停下」

① 预设人工断点（代码 `interrupt()`，有检查点、无限等待，resume 同 `thread_id`）；② 正常流转（每 super-step 都有检查点，不需恢复）；③ 外部取消/停机（硬杀无检查点，协作式 drain 有）；④ 异常报错（有上一份，从上一份重跑失败那步）。**只有第一种是「等人」**。^[raw/flow-control.md]

外部停机两种：`kill -9` 来不及写任何东西；协作式 drain 传 `RunControl()` 并 `request_drain()`，在当前 super-step 跑完后写检查点抛 `GraphDrained`，面向滚动发布与 SIGTERM。drain 是「有序地停」不是 HITL。^[raw/flow-control.md]

异常不会自动变人工：未捕获就冒泡终止停在上一份检查点；`error_handler` 是补偿路由，不是停下来等人。一句话分界：**框架负责停在哪、存什么、从哪续；业务负责要不要停、停了问谁、续了会不会重复扣钱**。^[raw/flow-control.md]

## 八、interrupt 四条硬规则

1. 不要用 `try/except` 包它（`GraphInterrupt` 继承 `GraphBubbleUp`，被 `except Exception` 接住就表现为图卡住）。
2. 同一节点多个 interrupt 顺序不能改（恢复值是任务级列表，按下标严格匹配）；并行分支挂起按 interrupt ID 映射、一次性恢复。
3. payload 要简单可序列化，只放审批所需信息，其余用 ID 引用。
4. interrupt 之前的副作用必须幂等（恢复是重入整个节点）。

「出错后问人」的正确写法：执行节点 `except` 具体异常写 `state.error`，条件边进入确认节点再 `interrupt()`；不要直接在 `except` 块里 `interrupt()`。三处最易错：`invoke()` 不抛异常、payload 在 `__interrupt__`；恢复是整节点重跑而非断点续行；重跑范围是节点不是整张图。^[raw/flow-control.md]

## 九、人机协同（HITL）

四种决策：`approve`、`edit`、`reject`、`respond`——第四种最常被漏（用户其实只想让你告诉怎么写，不要真发邮件）。生效三条件：配了 `interrupt_on`、挂了 checkpointer、恢复用同一 `thread_id`。^[raw/flow-control.md]

条件中断（按金额阈值、收件人域、路径敏感度判断）优于按工具名一刀切，后者造成审批疲劳、人盲点同意，护栏等于没有。多代理时子代理也能配中断，主代理汇总时一并拿到；文件系统类工具可配「越权访问自动中断」，比事后报错更早。前端要做三件事：把中断渲染成明确待办、把决策回传、处理超时未决策并告警。^[raw/flow-control.md]

## 十、踩坑清单（13 条）

把 interrupt 当报错、把 thread_id 当线程 ID、以为检查点默认开、以为恢复是断点续行、用 try/except 接 invoke、把 interrupt 包进 try、多个 interrupt 顺序变动、payload 塞复杂对象、以为崩溃不丢状态（分档）、硬杀后指望自动恢复、以为报错自动转人工、换 thread_id 去恢复、把静态断点 `interrupt_before` 当动态中断。^[raw/flow-control.md]

## 十一、演练与 D11 实测

故障注入四点：节点执行到一半杀进程、外部写超时、中断后换进程恢复、连续失败触发熔断。三指标：恢复成功率、重做步骤数、重复副作用次数——第三项最容易漏测，也是唯一造成真实损失的。反直觉结论：**检查点不等于「恰好执行一次」**，它只保证知道从哪继续；副作用只发生一次要靠幂等，两者缺一不可。^[raw/flow-control.md]

D11 实测（2026-11-13，项目 `checkpoint-recovery`，4 场景 × 2 模式 × 3 次重复，基线为无检查点整链重跑，增强为 `SqliteSaver` + durability=sync + 幂等副作用注册表）：^[raw/flow-control.md]

- 重做步骤：baseline 恒 5 步；enhanced 在 crash 场景 2 步、write_fail 1 步、raise 3 步。
- 重复副作用：crash@write_report 场景 baseline 必为 1（报告发布两次），enhanced 幂等拦截为 0，`dup_blocks` 留痕 1 次。
- 耗时：clean 场景 enhanced 略慢（34 vs 11ms，写放大约 3 倍），崩溃场景因少重做反而更快（3891 vs 4144ms）。
- durability 同现场对照：sync 崩溃后只重做 2 步；exit 硬杀后快照全无只能整链重做 5 步；默认 async 小概率丢最近一步，依赖调度时序，未量化。
- 失效条件：单步任务、或可整体重跑且无副作用的场景，检查点收益接近于零。

证据：项目 `runs/20261113-022608-experiment/report.md`；机制自测 11/11、端到端 LLM 3/3。^[raw/flow-control.md]

## 十三、与引擎手册的分界

本文件讲「该用哪种编排、失败怎么处理」；`工作流引擎手册/`（8 份，约 10100 行）讲各引擎怎么装怎么配：Temporal（重工作流、持久化执行、代码即流程）、Prefect（数据流水线、Python 装饰器风格）、Inngest（事件驱动、Serverless 友好）、Hatchet（轻量任务队列、Go 实现）、Windmill（脚本与内部应用、自带 UI）、n8n 两份（可视化节点式）、ControlFlow（以 Agent 为中心的任务编排）。选型看本页第二章，动手翻手册。^[raw/flow-control.md]
