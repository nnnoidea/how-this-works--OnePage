---
template: doc
theme: paper
lang: zh-CN
title: Dify：把模型、资料和工具接成应用
subtitle: 面向第一次接触 Dify 的开发者 · langgenius/dify · 源码 9aebf35e945c
---

Dify 是带有可视化工作台和后端 API 的大语言模型应用开发平台。开发者在这里配置模型、提示词、知识库和执行流程，再把应用交给用户或接入自己的产品。模型推理由接入的服务提供，Dify 负责把这些能力组织成可运行、可观察的应用。

阅读路线：[能做什么](#panel-A) → [与谁协作](#panel-B) → [内部结构](#panel-C) → [流程与知识库](#panel-D) → [一次问答](#panel-F)。研究版本固定为 [9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206](https://github.com/langgenius/dify/commit/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206)。

## A 你能用它交付什么？

```flow LR
提示词与模型配置 -> 对话应用: 调整回答方式
业务步骤与输入 -> 工作流: 连接处理节点
业务资料 -> 知识库问答: 先检索再生成
工具与任务描述 -> Agent: 按任务调用能力
对话应用 -> 用户界面或业务 API: 交付
工作流 -> 用户界面或业务 API: 交付
知识库问答 -> 用户界面或业务 API: 交付
Agent -> 用户界面或业务 API: 交付
```

这四种需求体现不同的工作分配：提示词应用把重点放在模型交互；工作流由开发者明确安排步骤；知识库问答把资料检索放到回答之前；Agent 则允许系统围绕任务使用工具。

Dify 内置编排、知识处理和日志能力，模型及工具通过集成接入。开发者仍须提供模型连接、资料、提示词和业务规则，并根据日志和实际结果迭代应用。[功能范围](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L92-L114)

## B Dify 与哪些人和系统交换什么？

```flow LR
开发者 -> 应用配置: 模型、资料与流程
应用配置 -> 应用运行: 配置好的应用
使用者或自有产品 -> 应用运行: 问题或任务
应用运行 -> 使用者或自有产品: 回答与运行结果
应用运行 -> 模型服务: 提示词与上下文
模型服务 -> 应用运行: 生成内容
应用运行 --> 外部工具: 配置后调用
外部工具 --> 应用运行: 工具结果
group Dify: 应用配置, 应用运行
```

框内是 Dify 的主要责任。模型服务可以来自供应商，也可以是你自建的推理服务；工具可以来自插件、MCP 或自己的 API。即使它们部署在同一台机器上，这些服务也需要独立配置。虚线连接按需接入的工具，每次请求可以使用不同路径。[模型、工具和 API](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L97-L114)

## C 打开 Dify：编辑、执行与存储如何分工？

```flow
Web 工作台 -> API 应用服务: 编辑配置或发起调试
业务 API 调用方 -> API 应用服务: 应用输入
API 应用服务 -> 应用生成器: 按应用类型分派
应用生成器 -> 工作流入口: 工作流及运行状态
工作流入口 -> Graphon 图引擎: 图、变量池与执行限制
Graphon 图引擎 -> 节点实现: 执行检索、模型等节点
API 应用服务 -> Worker: 流式工作流执行任务
Worker -> 应用生成器: 执行应用
Worker -> 知识索引服务: 文档处理任务
API 应用服务 -> 数据库与文件存储: 配置与数据
Worker -> 数据库与文件存储: 任务状态与资料
```

Web 是配置入口，API 服务按应用类型选择生成器。对工作流类应用，工作流入口把图和运行状态交给 Graphon 引擎，并增加步数、耗时限制；Graphon 在该版本是锁定为 0.7.0 的依赖包。Dify 的知识检索节点与模型适配把执行引擎接回应用能力。[分派](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/app_generate_service.py#L182-L246) · [入口和限制](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/workflow_entry.py#L138-L185) · [依赖版本](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/pyproject.toml#L48) · [模型节点适配](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/llm_node.py#L1-L44)

耗时任务可交给 Worker：例如文档索引，以及这里展示的流式工作流执行。流式路径通过事件把结果送回调用方；阻塞路径则同步运行并返回结果。部署层把 API、Worker 和 Web 分为服务，并配有数据库、Redis 与文件存储；图省略了 Redis 的缓存和事件传递细节。[执行分支](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/app_generate_service.py#L244-L301) · [部署服务](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docker/docker-compose.yaml#L227-L265) · [Worker](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docker/docker-compose.yaml#L309-L342) · [Web 与数据服务](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docker/docker-compose.yaml#L390-L514)

## D 画布上的连线如何变成一次执行？

```flow LR
开始节点 -> 模型节点: query 变量
模型节点 -> 结束节点: 生成结果
提示词模板 -> 模型节点: 引用开始节点的 query
模型配置 -> 模型节点: 供应商与模型名
```

节点规定“做什么”，边规定“接下来到哪里”，变量把一个节点的结果交给另一个节点。源码中的最小工作流样例将开始节点的 `query` 引入模型提示词，再连接结束节点。画布因此同时表达执行关系和数据引用；只画连线，还需要为节点配置正确的输入。[最小图与输入](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/tests/fixtures/workflow/basic_llm_chat_workflow.yml#L29-L93)

工作流入口持有变量池和运行状态，启动引擎后持续产出运行事件。Dify 对这些事件加过滤层，以维持应用侧的流式响应语义。这使“运行图”和“向用户输出内容”能够分别处理。[事件过滤](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/workflow_entry.py#L56-L79) · [运行事件](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/workflow_entry.py#L187-L199)

```flow LR
Graphon 图引擎 -> 原始运行事件: 执行节点
原始运行事件 -> Dify 事件过滤层: 处理响应流
Dify 事件过滤层 -> 应用运行方: 兼容的输出事件
```

## E 知识库怎样让回答用上你的资料？

```flow LR
上传资料 -> 提取文本: 建库阶段
提取文本 -> 切分片段
切分片段 -> 保存片段并建立索引
用户问题 -> 知识检索节点: 问答阶段
保存片段并建立索引 -> 知识检索节点: 可检索资料
知识检索节点 -> 相关片段
相关片段 -> 模型提示词: 开发者配置上下文引用
模型提示词 -> 模型回答
```

RAG（检索增强生成）把“准备资料”和“回答问题”分开。索引服务提取文本、转换为片段、保存片段，再加载到索引后端；段落索引实现可创建向量索引，用于按内容相关性查找资料。文档处理以后台任务运行，并记录解析或错误状态。[索引阶段](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/knowledge/indexing/execution.py#L104-L138) · [向量加载](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/rag/index_processor/processor/paragraph_index_processor.py#L138-L152) · [后台索引](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/tasks/document_indexing_task.py#L96-L129)

运行时，检索节点从变量池读取问题，并把检索结果放到 `result` 输出。开发者需要把这些片段接入后续模型的上下文。模型节点配置含上下文变量选择器，Dify 从变量池读取关联片段。资料能否被正确提取、切分和检索，会直接影响回答可用的依据；接上知识库并不等于每个问题都能找到充分材料。[节点输入输出](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py#L103-L148) · [上下文读取](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/node_factory.py#L690-L718) · [检索配置](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py#L195-L277)

## F 例子：用户问“报销要交哪些材料？”

下面是说明用的知识库问答流程，不是仓库内置应用。前提是开发者已导入制度文档、等待索引完成，并配置“开始 → 检索 → 模型 → 回答”的流程。

```sequence num
用户 -> API 应用服务: 提交报销问题
API 应用服务 -> Worker: 派发流式应用执行
Worker -> 工作流入口: 加载图与输入
工作流入口 -> 知识检索节点: 用问题查询知识库
知识检索节点 --> 工作流入口: 相关制度片段
工作流入口 -> 模型服务: 按配置发送问题、片段和提示词
模型服务 --> 工作流入口: 生成回答
工作流入口 --> API 应用服务: 运行输出事件
API 应用服务 --> 用户: 流式显示回答
```

这里的“工作流入口”概括了引擎与节点的协作，模型请求通过模型节点及适配层发出。检索只负责提供片段，模型负责组织回答；开发者可在提示词中约定资料不足时如何答复。运行后再检查日志，定位是检索未命中、提示词不清楚，还是模型结果需要改进。图按已介绍的执行、检索与模型连接组合，未声称所有应用都走这条路径。[流式执行](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/app_generate_service.py#L244-L277) · [模型接入](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/model_manager.py#L850-L861) · [日志迭代](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L110-L114)

## G 开始使用前，需要决定什么？

```flow LR
先试应用开发 -> Dify Cloud: 使用托管服务
需要自己部署 -> Docker Compose: 管理服务与存储
Docker Compose -> 配置模型及资料: 部署后仍需配置
Dify Cloud -> 配置模型及资料: 按需求准备
配置模型及资料 -> 测试并检查日志: 确认业务结果
```

仓库提供 Cloud 与社区版自部署入口。自部署快速启动要求至少 2 核 CPU、4 GiB 内存及 Docker Compose 2.24.0；这是启动门槛，不是业务负载容量承诺。部署 Dify 后仍需准备所需模型和外部服务。[使用方式](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L66-L84) · [Cloud 与社区版](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/README.md#L116-L126)

采用前还需阅读仓库许可证：它基于 Apache 2.0 增加条件，涉及多租户服务及前端标识。此处只提示原文位置，不代替许可判断。[LICENSE](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/LICENSE#L3-L18)

本页基于指定提交的静态源码阅读；未运行 Dify，未验证部署性能、云服务现状或模型回答质量。机制说明聚焦工作流与知识库；Agent 的沙箱、工具调度和完整部署选项可在后续深入。
