# Visual format

Adapted from [Answer Me with HTML](https://github.com/QingYunA/answer-me-with-html), under its [MIT license](../vendor/answer-me-with-html/LICENSE). This is the output syntax reference, not a research procedure.

```markdown
---
template: doc
theme: paper
lang: en
title: Project study
subtitle: Optional summary
---
Opening explanation.

## A The reader's question
Markdown paragraphs, links, code, and components.

## B Another question
More content.
```

`doc` is a linear reading page; `sheet` arranges panels as an overview. Themes include `paper`, `blueprint`, and `shadcn`. `##` starts a panel; explicit letter IDs give links such as `#panel-A`. Choose the page's size from the material, without a fixed panel quota.

Use section anchors for navigation within the page, for example `[How it runs](#panel-B)`. Keep the draft beside its HTML. Retain the filename and panel IDs when revising so existing links remain usable; the page checker can catch broken local targets after changes.

## Components

Use fenced blocks with the component name as the language:

| Information | Component | Example content |
|---|---|---|
| Relationships, branching | `flow` or `flow LR` | `A -> B: label`, `{Ready?} -> B: yes`, `A --> C` |
| Messages between actors | `sequence num` | `Caller -> Worker: request`, `Worker --> Caller: result` |
| Hierarchy | `tree` | Indentation for levels; `name \| description` |
| Dated changes | `timeline` or `timeline v` | `date \| event \| explanation` |
| Measured values | `chart line`, `chart bar`, `chart pie` | `label \| number`; `unit=ms` is optional |
| Entities and relationships | `er` | `User 1--* Order: places` with indented fields |
| Comparisons | Markdown table | Normal table syntax |
| Highlighted explanation | `callout info` | Markdown body; also `ok`, `warn`, `err` |

Example:

````markdown
```flow
Request -> {Cached?}
{Cached?} -> Result: yes
{Cached?} -> Compute: no
Compute -> Result
```
````

The CLI has the complete component reference:

```sh
node SKILL_DIR/vendor/answer-me-with-html/am.mjs help flow
node SKILL_DIR/vendor/answer-me-with-html/am.mjs help sequence
node SKILL_DIR/vendor/answer-me-with-html/am.mjs help format
```

## Code and diagnostics

Existing code can be embedded by the renderer with an empty fenced block such as `python src=src/worker.py lines=18-30 hl=22`. Paths resolve within `render.mjs --source-dir DIRECTORY`, or the working directory if omitted. This reads local files, not the commit named in a citation. Select the intended checkout; Git citation validation is a separate check and does not certify embedded snippets. For illustrative code, use a normal fence with `title="Example · sketch"`.

The CLI reports malformed component syntax and writing warnings. Syntax errors require correction. Writing warnings are advisory; preserve necessary conditions and meaning. Render again to the same destination after edits. Generated HTML embeds its Markdown in `#am-source`, but retaining the `.md` makes future changes simpler.
