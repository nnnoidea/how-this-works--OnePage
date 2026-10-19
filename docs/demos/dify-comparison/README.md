# Dify: Answer and HTW comparison

[Answer original page](answer/index.html) · [HTW original page](htw/index.html) · [Attribution](NOTICE.md)

## Method

One generation per condition, both GPT-6.1 Sol / low, with the same task: explain Dify in one visual page for a developer unfamiliar with it, choose questions independently, support explanations with evidence, and identify the source version. Both read the same raw checkout at `9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206`. Neither had prior studies, the other output, network access, or permission to install or run Dify. Browser review was moved to a shared external phase.

Answer used upstream commit `7acea24024923eaae8647f5988e826062456dc86` (CLI 0.5.5). HTW used the OnePage Skill snapshot on 2026-10-19. The renderer is byte-identical. One Answer help invocation omitted the output-isolation variables; rendering and lint used the required settings. No effect on input or delivery was observed.

Two fresh Agent readers inspected complete rendered pages in opposite orders and tested navigation and diagram enlargement. They read no source code. A separate reviewer first established a raw-source reference, then checked the neutral X/Y drafts. These are Agent reviews, not a human-user study.

## What this supports for OnePage understanding

HTW connects Dify's purpose, main capabilities, a representative RAG use, execution, delivery and adoption conditions. Answer concentrates on the Workflow runtime, with useful version selection, execution details and troubleshooting. For the goal of understanding the whole project on first contact, HTW provides a more balanced overview. Answer offers stronger concrete behavioral explanations in the narrower Workflow path.

Reader preferences were mixed: X→Y preferred HTW for a first introduction; Y→X preferred Answer for predicting Workflow behavior. Both recognized HTW's broader adoption guidance and Answer's runtime depth. Source review found checked factual accuracy broadly tied, without major errors. This does not establish universal superiority or a stable win rate.

Both produced four flow components. Answer's streaming branch is not visually connected back to execution; HTW's publishing and runtime chains lack an explicit bridge. Answer's execution diagram is tall; HTW's wide diagrams have small labels that benefit from enlargement. Original pages retain these limitations.

## Measured author usage

| Condition | Uncached input | Cached input | Output | Total tokens | Elapsed |
|---|---:|---:|---:|---:|---:|
| Answer | 46,822 | 548,608 | 4,992 | 600,422 | 116.1 s |
| HTW | 28,613 | 543,360 | 5,110 | 577,083 | 116.6 s |

Counts come from actual per-response usage, checked against cumulative turn/session counters. Input includes cached tokens; output includes reasoning. Totals are not prices. Time is task start to completion, including tools. Parent preparation and external review are excluded. HTW used about 3.9% fewer total tokens in this run; one run does not establish a general efficiency advantage. Answer rendered once; HTW rendered three times, including a repeated render after a failed text-edit command.

## Screenshots and original pages

The main README displays only the [HTW full-page capture](../../images/dify-comparison/htw-full.jpg), 1265×2465, with an HTML link for Answer. The [Answer capture](../../images/dify-comparison/answer-full.jpg), 1265×3023, remains available here as experiment material. Both are real browser captures at the same width, with original themes and natural page heights; no cropping, stitching or redrawing. Both studies were authored in Chinese.

GitHub's file viewer shows HTML source. Download the HTML to open locally, or use these GitHub Pages links, published from **main / docs**:

- `https://nnnoidea.github.io/how-this-works--OnePage/demos/dify-comparison/answer/`
- `https://nnnoidea.github.io/how-this-works--OnePage/demos/dify-comparison/htw/`

The example bundle includes no source checkout, private session logs or caches.
