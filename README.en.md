# How This Works

**OnePage to understand how a project works.**

[简体中文](README.md) · **English**

Give your Agent a code repository, a Skill, or a documentation project. How This Works (HTW) turns it into one illustrated, source-backed explanation: **what it is, which needs it suits, how it works with external systems, and how its architecture and key mechanisms cooperate.** It builds an overall understanding for developers encountering the project for the first time, delivered as an HTML page and an editable Markdown draft.

## See the result: Dify on one page

[Open the complete page](https://nnnoidea.github.io/how-this-works--OnePage/demos/dify-comparison/htw/) · [HTML file](docs/demos/dify-comparison/htw/index.html)

![How This Works: a complete OnePage explanation of Dify](docs/images/dify-comparison/htw-full.jpg)

*Real full-page screenshot; click to enlarge. This example is in Chinese; studies can be authored directly in your requested language. Open the live page or download the HTML to read offline.*

## Compared with using the Answer Skill directly

Same Dify source, **GPT-6.1 Sol / low**. The direct Answer Skill result focuses more on execution details; HTW connects project uses, external relationships, internal architecture, key mechanisms and a concrete scenario in OnePage.

[Open the original Answer page](https://nnnoidea.github.io/how-this-works--OnePage/demos/dify-comparison/answer/) · [Answer HTML file](docs/demos/dify-comparison/answer/index.html)

| Author condition | Uncached input tokens | Cached input tokens | Output tokens | Total tokens | Generation time |
| --- | ---: | ---: | ---: | ---: | ---: |
| Answer | 46,822 | 548,608 | 4,992 | 600,422 | 116.1 s |
| HTW | 59,840 | 842,752 | 6,989 | 909,581 | 187.9 s |

Measured generation usage; total tokens include cached input. [View the data](docs/demos/dify-comparison/README.md)

## Use it

Ask your Agent to install the [Skill folder](skills/how-this-works-onepage), then ask:

> Use How This Works to explain `<repository URL or local path>` in one visual page.

## Credits

HTW is adapted from [Answer Me with HTML](https://github.com/QingYunA/answer-me-with-html). Answer supplies the page layout, themes, diagram components and interactions. HTW adapts the research objective and visual requirements for OnePage project understanding, and adds source-reference and page-link checks. The bundled renderer is unmodified; its copyright notice and [MIT license](skills/how-this-works-onepage/vendor/answer-me-with-html/LICENSE) are retained.
