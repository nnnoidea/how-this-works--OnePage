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

## Project boundary template

Use this structure for the external-relationships view. Keep the boundary convention stable while adapting the participants and exchanges to the evidence.

- Draw one `group` box named for the studied project. Put only its main outward-facing responsibilities inside. Keep users, host applications, and separately supplied services outside.
- Connect each participant to the relevant responsibility. Label arrows with the request, material, action, or result being exchanged. Show requests and returns separately when both matter.
- Use solid arrows for the main exchanges. Use dashed arrows for optional integrations and label their condition. Keep enough participants to explain the actual boundary; omit unsupported roles.
- Treat the box as a responsibility boundary. Briefly clarify ownership or deployment distinctions when needed: a service can run on the same machine and still be an external dependency. For libraries and Skills, exchanges can be function calls, files, instructions, or artifacts rather than network messages.
- Let the following architecture view expand the responsibilities inside the box. The boundary view should remain readable as a project and its surroundings.

The example below demonstrates syntax, not a mandatory set of components. Replace the names and labels with project-specific terms in the reader's language:

````markdown
```flow LR
Caller -> Request handling: task and input
Request handling -> Work coordination: accepted task
Work coordination -> External service: service request
External service -> Work coordination: service result
Work coordination -> Caller: completed output
Maintainer -> Configuration: settings and resources
Configuration -> Work coordination: configured behavior
group Project name: Request handling, Work coordination, Configuration
```
````

Inspect the rendered box and labels at normal reading size. Automatic layout determines positions; the invariant is visible enclosure and correctly directed exchanges, not exact left/right coordinates. If the view is crowded, combine related responsibilities or separate an optional interaction while retaining the same named project boundary.

## Code and diagnostics

Existing code can be embedded by the renderer with an empty fenced block such as `python src=src/worker.py lines=18-30 hl=22`. Paths resolve within `render.mjs --source-dir DIRECTORY`, or the working directory if omitted. This reads local files, not the commit named in a citation. Select the intended checkout; Git citation validation is a separate check and does not certify embedded snippets. For illustrative code, use a normal fence with `title="Example · sketch"`.

The CLI reports malformed component syntax and writing warnings. Syntax errors require correction. Writing warnings are advisory; preserve necessary conditions and meaning. Render again to the same destination after edits. Generated HTML embeds its Markdown in `#am-source`, but retaining the `.md` makes future changes simpler.
