# How This Works

**OnePage，看懂一个项目如何运作。**

**简体中文** · [English](README.en.md)

给 Agent 一个代码仓库、Skill 或文档项目，How This Works（HTW）将它解析成一页有图解、有源码依据的讲解：**项目有什么用、主要能力如何配合、哪些前提与限制影响使用。** 为第一次接触项目的开发者建立整体认识，并交付可打开的 HTML 与可编辑的 Markdown 草稿。

## 实际效果：一页理解 Dify

[打开完整网页](https://nnnoidea.github.io/how-this-works--OnePage/demos/dify-comparison/htw/) · [HTML 文件](docs/demos/dify-comparison/htw/index.html)

![How This Works：一页理解 Dify，完整长截图](docs/images/dify-comparison/htw-full.jpg)

*真实页面完整长截图，点击可放大。示例正文为中文；生成内容可直接使用你请求的语言。可打开在线网页，也可下载 HTML 文件离线阅读。*

## 与直接使用 Answer Skill 对比

同一份 Dify 源码、同一任务、同样的 **GPT-6.1 Sol / low**。这次直接使用 Answer Skill 的结果过于侧重 Workflow 内部执行与排障细节，未能形成 OnePage 对整个项目的理解；HTW 则连起了主要能力、运行方式与采用条件。

[查看 Answer 原网页](https://nnnoidea.github.io/how-this-works--OnePage/demos/dify-comparison/answer/) · [Answer HTML 文件](docs/demos/dify-comparison/answer/index.html)

| 作者组 | 未缓存输入 token | 缓存输入 token | 输出 token | 总 token |
| --- | ---: | ---: | ---: | ---: |
| Answer | 46,822 | 548,608 | 4,992 | 600,422 |
| HTW | 28,613 | 543,360 | 5,110 | 577,083 |

两组均约 116 秒，正文和图解保留首次交付。总 token 包含缓存，不等于费用；不含外部评审开销。这是单次对比，不代表普遍效果或成本优势。[实验方法与完整结果](docs/demos/dify-comparison/README.md)

## 使用

将 [Skill 文件夹](skills/how-this-works-onepage) 交给你的 Agent 安装，然后直接提问：

> 用 How This Works 帮我理解 `<仓库地址或本地路径>`，生成一页中文图解。

## 致谢与来源

HTW 基于 [Answer Me with HTML](https://github.com/QingYunA/answer-me-with-html) 修改。页面布局、主题、图表组件和交互来自 Answer；HTW 针对 OnePage 理解项目调整研究目标与图解要求，并增加源码引用和页面链接校验。内置渲染器保持原样，保留上游版权声明、MIT 许可证和[第三方声明](skills/how-this-works-onepage/THIRD_PARTY_NOTICES.md)。
