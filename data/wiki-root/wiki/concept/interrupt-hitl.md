---
title: interrupt 四条硬规则与人机协同（HITL）
type: concept
sources: [raw/flow-control.md]
updated: 2026-11-09
summary: interrupt 不得被 try/except 吞、多断点顺序锁定、payload 可序列化、前置副作用幂等；HITL 四种决策与条件中断优于一刀切。
---
# interrupt 四条硬规则与人机协同

## 四条硬规则

1. **不要用 try/except 包它**：它靠抛异常实现（`GraphInterrupt` 继承 `GraphBubbleUp`），被 `except Exception` 接住就再也传不回图，表现为「图卡住不动」。正确写法是 interrupt 单独一行，易错代码另放 try 且只捕具体异常类型。
2. **同一节点多个 interrupt 顺序不能改**：恢复值是任务级列表、按下标严格匹配；顺序一变、条件跳过或不确定循环，第一个就会吃掉本该给第二个的值。并行分支同时挂起是另一套：按 interrupt ID 映射，一次性恢复。
3. **payload 要简单可序列化**：不塞自定义对象与大块二进制；只放审批要用的信息（做什么、影响什么、能不能撤回），其余用 ID 引用。
4. **interrupt 之前的副作用必须幂等**：恢复是重入整个节点，高风险动作放到 interrupt 之后（见 [[concept-idempotency]]）。

^[raw/flow-control.md]

## 「出错后问人」的正确写法

执行节点 `try` 干活 → `except` 具体异常 → 把错误写进 `state.error`；条件边进入确认节点，`state` 里有 error 才 `interrupt({"error": ..., "retry": ...})`。不要在 `except` 块里直接 `interrupt()`——当前能跑，但下一次改动很容易把它挪进 try。^[raw/flow-control.md]

三处最容易错：`invoke()` 不抛中断异常，payload 在返回值的 `__interrupt__`；恢复不是断点续行，是整个节点重跑；重跑范围是节点，不是整张图。^[raw/flow-control.md]

## HITL 四种决策

| 决策 | 含义 |
|---|---|
| `approve` | 照原样执行 |
| `edit` | 改参数后执行 |
| `reject` | 拒绝，附带理由 |
| `respond` | 不进工具，直接给用户回话 |

第四种最常被漏：用户问「能帮我发邮件吗」，模型准备调工具，人其实想说「不用发，告诉我怎么写就行」。^[raw/flow-control.md]

生效三件事同时成立：配了 `interrupt_on`、挂了 checkpointer、恢复时用同一 `thread_id`。条件中断（金额超阈值、收件人在外域、路径在受保护目录才中断）优于按工具名一刀切——后者造成审批疲劳，人盲点同意，护栏等于没有。多代理时子代理也能配中断，主代理汇总时一并拿到。^[raw/flow-control.md]

## 生命周期与前端职责

`启动 → 节点执行 → 命中中断 → 存检查点 → 返回 interrupts → 人决策 → resume → 重入节点 → 继续`。前端要做三件事：把中断渲染成明确待办、把决策回传、处理超时未决策（会话过期要能告警）。^[raw/flow-control.md]

断点写下来之后怎么存、怎么续，见 [[concept-checkpoint-recovery]]。原文另附 13 条踩坑清单，逐条列在 [[source-flow-control]]。^[raw/flow-control.md]
