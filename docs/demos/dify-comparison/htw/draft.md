---
template: doc
theme: paper
lang: zh-CN
title: Dify：把模型能力接成可运行的应用
subtitle: 从知识问答出发，理解构建、运行与交付的分工
---
Dify 是一个 LLM 应用开发平台：把模型、提示词、知识、工具和运行记录放进同一套构建与交付流程。它适合希望通过可视化方式组装 AI 应用、又需要接入自己业务系统的开发者。

研究对象：**langgenius/dify · 固定提交 `9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206`**。以下是源码与仓库说明的静态研究，示例不代表预装应用，也未验证实际运行表现。

## A 你在 Dify 里构建什么？

```flow LR
开发者 -> 可视化工作流: 编排步骤与分支
提示词与模型配置 -> 可视化工作流: 定义生成行为
知识库 -> 可视化工作流: 提供可检索资料
工具与 Agent -> 可视化工作流: 扩展行动能力
可视化工作流 -> 应用与 API: 交付给用户或业务系统
应用与 API -> 日志与性能观察: 获取运行反馈
日志与性能观察 -> 开发者: 调整提示词、知识与模型
```

这张图是能力关系图。画布组织处理过程；Prompt IDE 支持提示词编辑与模型比较；RAG 覆盖资料导入到检索；Agent 可以在沙箱中处理开放任务，并连接工具、MCP 或自有 API。发布后的能力可通过 API 集成，日志则支持后续迭代。

**模型负责生成，Dify 负责组织应用所需的上下文、步骤与交付方式。**

证据：[平台定位与主要能力](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L64-L114)。图中反馈环表示开发者的改进过程，不是自动训练循环。

## B 一次知识问答，资料如何参与回答？

下面是说明性的应用设计：给内部产品手册做问答。并非每个 Dify 应用都必须使用 RAG，也并非每次问答都需要 Agent。

```flow LR
产品手册 -> 知识库: 导入与处理资料
用户问题 -> 检索步骤: 作为查询
知识库 -> 检索步骤: 候选内容
检索配置 -> 检索步骤: 方法、top_k、阈值与可选重排
检索步骤 -> 相关片段: 返回选中内容
相关片段 -> 模型生成: 配合提示词与问题
模型生成 -> 回答: 返回用户
```

RAG 的关键是先找资料，再把选出的内容用于生成。它让应用能够引用业务资料；回答质量仍取决于资料、检索配置、提示词与模型。

源码中的单知识库检索会读取 `top_k`；经济索引使用关键词搜索，其他索引使用配置的搜索方法；重排模型仅在启用时传入，分数阈值也由配置控制。因此，**接上知识库并不等于每条相关资料都会进入回答**。

证据：[资料导入与 RAG 能力](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L102-L108)、[检索参数如何进入 RetrievalService](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/rag/retrieval/dataset_retrieval.py#L736-L772)。图中“相关片段 → 模型”是示例应用的编排意图，不宣称所有检索节点都自动接到模型。

## C 画布上的流程，如何变成一次运行？

```flow LR
草稿图与变量 -> 发布校验: 检查图结构等
发布校验 -> 发布版本: 复制图与变量并分配版本号
图与运行状态 -> GraphEngine: 初始化一次执行
GraphEngine -> 执行限制层: 限定步数与时间
GraphEngine -> 事件流: 运行产生事件
事件流 -> 响应过滤: 适配 Dify 输出语义
响应过滤 -> 调用方: 返回事件
```

上半条关系解释“保存设计”和“发布版本”的区别。发布先查找草稿并校验，再创建新的 Workflow，复制图及相关变量。

下半条解释运行入口：`WorkflowEntry` 接收图、变量池和运行状态，创建 GraphEngine，并叠加执行限制；运行事件经过 Dify 的过滤层输出。**画布不仅是流程示意，它保存的图会成为运行时输入。**

发布侧证据：[校验和创建版本](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/workflow_service.py#L690-L748)。运行侧证据：[引擎构造与限制层](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/workflow_entry.py#L138-L198)、[事件过滤](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/workflow_entry.py#L56-L79)。这里没有展开 Graphon 内部调度，也不表示所有节点都沿直线执行。

## D 采用它，意味着接管哪些事情？

```flow LR
采用 Dify -> Dify Cloud: 托管服务
采用 Dify -> 自托管: 自己维护部署
自托管 -> Web 与 API: 界面和后端
自托管 -> Worker: 后台任务进程
自托管 -> 数据与运行配套: 数据库、Redis、存储及相关服务
商业使用方式 -> 许可证条件: 核对多租户与前端标识条款
```

如果希望先体验平台，仓库提供托管 Cloud；如果需要把服务部署到自己的环境，仓库提供 Docker Compose。后者涉及 Web、API、Worker 与数据服务等多个进程，不能只按一个前端页面估算维护工作。模型与工具的接入也需要相应配置。

选择它的主要理由是复用整套应用构建和运营流程；相应代价是接受平台的运行设施与配置体系。这是由其能力范围和部署组成得到的判断。

证据：[托管与自托管入口](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L116-L126)、[API 依赖和文件存储](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docker/docker-compose.yaml#L227-L265)、[Worker](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docker/docker-compose.yaml#L309-L342)、[Web 的 API 配置](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docker/docker-compose.yaml#L390-L402)。图是部署职责概括，不是全部服务清单或网络拓扑。

许可证也影响适用性。该提交采用带附加条件的 Apache 2.0 修改版。它规定了多租户服务授权，以及前端 LOGO 和版权信息限制。商业采用应直接核对[仓库许可证原文](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/LICENSE#L3-L18)。此处只呈现该版本文本，不提供法律适用判断。
