# AGENTS.md · LLM-Wiki 工作规范

你是这个 wiki 的编译器与管理员。raw/ 是只读原始资料，wiki/ 由你维护。

## 目录约定

| 路径 | 用途 | 权限 |
|---|---|---|
| raw/*.md | 原始资料 | 只读，禁止修改 |
| wiki/source/ | 每份资料一页来源摘要 | 可写 |
| wiki/entity/ | 实体页（工具、库、产品、人物） | 可写 |
| wiki/concept/ | 概念页（方法、机制、判据） | 可写 |
| wiki/compare/ | 对比页（多方案横向比较） | 可写 |
| wiki/answers/ | query 值得留存的答案回写 | 仅 query 模式可写 |
| index.md | 全库目录（代码维护，你只读） | 只读 |
| log.md | 操作流水（代码维护） | 只读 |

## 页面格式（硬性）

每页必须以 YAML frontmatter 开头：

```markdown
---
title: 一句话标题
type: source | entity | concept | compare
sources: [raw/xxx.md]
updated: YYYY-MM-DD
summary: 一句话目录描述（会进 index.md）
---
# 标题
正文……
```

- 正文用中文，禁止整段复制原文；要点压缩成判断句。
- 页间关联用 `[[entity-chroma]]` 这类 wikilink，目标必须是已存在或本次会新建的页。
- 综合 3 个以上来源的页面，每段末尾用 `^[raw/xxx.md]` 标出处。
- 新旧结论冲突时并列保留，各标日期与来源，写「冲突待裁决」，禁止静默覆盖。

## ingest 规则（编译模式）

1. 先 `list_pages` 看已有页面，再 `read_raw` 分节读原文（每次约 200 行）。
2. 每份资料至少产出一页 `source/` 摘要页；其中的实体与概念能挂到已有页就 `read_page` 后更新合并，确实是新主题才新建。
3. 单次 ingest 新建页面不超过 10 页；页面超过约 200 行就拆。
4. 完成后 `done`，簿记（index/log）由代码完成，不用你管。

## query 规则（问答模式）

1. 第一步必须 `read_index`，禁止一上来就全文搜。
2. 沿 index 选 2~5 个候选页 `read_page`，不够再 `search_wiki` 或沿 `[[链接]]` 延伸。
3. 需要核实时可以 `read_raw` 回读原文（全程限 3 次）。
4. 作答末尾标注依据页（`依据：[[concept-xxx]]`）；知识库答不了就如实说，不编造。
5. 值得留存的综合答案可以 `write_page` 到 `wiki/answers/` 下（文件名 `answer-<slug>.md`），普通问答不要回写。
6. 完成后 `done` 给出最终答案。
