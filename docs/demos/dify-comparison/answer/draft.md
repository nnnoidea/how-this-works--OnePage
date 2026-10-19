---
title: Dify：把 AI 流程变成可运行的应用
subtitle: 从一个知识问答场景，看懂配置、执行与运行记录
lang: zh
template: doc
theme: blueprint
source: langgenius/dify · 9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206
---
Dify 是 LLM 应用开发平台。它把流程配置、知识检索、模型接入和运行管理放在同一套系统中。

## A 开发者交付的是什么？
设想你要做一个“根据公司文档回答问题”的应用。下面是讲解场景，并非仓库自带流程。

```flow LR
用户问题 -> 知识检索: 查找相关材料
知识检索 -> LLM: 将检索结果配置为上下文
LLM -> 输出: 生成答案
```

画布负责表达步骤和连接。运行时负责执行这些步骤。检索节点只返回材料；模型是否使用材料，取决于后续节点配置。

[项目定位与功能：中文 README](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/docs/zh-CN/README.md#L65-L96)。

## B 为什么修改画布后，线上结果可能没变？
工作流配置有草稿和发布版本。请求入口会选择其中一份。

```flow LR
运行请求 -> {指定 workflow_id?}
{指定 workflow_id?} -> 指定发布版本: 是
{指定 workflow_id?} -> {来自调试器?}: 否
{来自调试器?} -> 草稿: 是
{来自调试器?} -> 当前发布版本: 否
```

没有草稿会报“未初始化”。没有发布版本会报“未发布”。所以排查结果差异时，先确认请求实际选中了哪份配置。

[版本选择：app_generate_service.py:505–548](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/app_generate_service.py#L505-L548)。[保存与发布：workflow_service.py:403、681](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/workflow_service.py#L403)。

## C 一次 Workflow 请求怎样走到执行器？
这里仅展开 Workflow 应用分支。聊天应用另有分支。

```flow
AppGenerateService -> 选择工作流版本
选择工作流版本 -> {streaming?}
{streaming?} -> Celery任务: 是，订阅后提交
Celery任务 -> 事件订阅: 按运行 ID 接收
{streaming?} -> WorkflowAppGenerator: 否，直接生成
WorkflowAppGenerator -> 工作线程
工作线程 -> WorkflowAppRunner
WorkflowAppRunner -> WorkflowEntry
WorkflowEntry -> Graphon引擎
```

流式分支把执行任务与接收事件拆开。非流式分支也会创建工作线程。不能把“非流式”理解成所有工作都在请求线程里执行。

[请求分支：app_generate_service.py:302–355](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/services/app_generate_service.py#L302-L355)。[线程与 Runner：app_generator.py:354–410、670–686](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/app/apps/workflow/app_generator.py#L354-L410)。

## D 节点之间如何传递数据？
Runner 为一次新运行建立 VariablePool。它放入系统变量、环境变量和入口输入，再用图配置创建执行图。

| 对象 | 作用 | 读代码时要分清 |
|---|---|---|
| Workflow.graph_dict | 保存的图配置 | 描述要执行什么 |
| VariablePool | 本次运行的变量池 | 提供节点读取的数据 |
| GraphRuntimeState | 本次运行的状态 | 持有变量池并交给引擎 |
| 知识检索节点的 result | 检索得到的对象数组 | 是材料，不是最终答案 |

知识检索节点用变量选择器读取问题。问题类型不是字符串时，它返回失败结果。检索成功后，它把材料写入 `result` 输出。

[运行初始化：app_runner.py:117–162](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/app/apps/workflow/app_runner.py#L117-L162)。[检索输入与输出：knowledge_retrieval_node.py:101–153](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/nodes/knowledge_retrieval/knowledge_retrieval_node.py#L101-L153)。

## E 谁执行流程，谁留下记录？
Dify 的 WorkflowEntry 构造 Graphon 的 GraphEngine。它配置工作线程数，并添加步数和运行时间限制。

```flow LR
WorkflowAppRunner -> WorkflowEntry: 图与运行状态
WorkflowEntry -> GraphEngine: 构造执行器
GraphEngine -> 持久化层: 执行期间记录
GraphEngine -> 运行事件: 经兼容过滤器输出
运行事件 -> Runner事件处理
```

Runner 向引擎挂载 WorkflowPersistenceLayer。该层拿到流程与节点执行仓储。因此，“流程定义”和“执行记录”是不同对象。

本版本依赖 `graphon==0.7.0`。仓库注释仍提到旧版兼容语义；这里以依赖声明为版本依据。未读取 Graphon 包内部，不能据此断言其具体调度算法。

[引擎构造与限制：workflow_entry.py:152–198](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/workflow/workflow_entry.py#L152-L198)。[持久化接入：app_runner.py:198–232](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/core/app/apps/workflow/app_runner.py#L198-L232)。[依赖版本：pyproject.toml:48](https://github.com/langgenius/dify/blob/9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206/api/pyproject.toml#L48)。

## F 遇到问题，先看哪一层？
| 现象 | 首先检查 | 对应证据 |
|---|---|---|
| 调试正确，发布调用却不同 | 草稿、当前发布版、指定版本 | B：版本选择 |
| 检索节点失败 | 变量选择器和输入类型 | D：检索节点 |
| 流程在运行中被限制 | 最大步数和最大运行时间 | E：执行限制 |
| 流式调用一直没有事件 | 订阅后任务提交与运行 ID | C：流式分支 |

这些是源码引导的排查入口，不是对具体故障的诊断。检索质量和模型回答质量还需要实际输入验证。

## G 研究边界与下一步阅读
研究版本固定为 `9aebf35e945ce0bc2d2cb2f76a7b0ee4dfccc206`。本页基于离线源码静态阅读，未启动项目或验证部署行为。

下一步可以沿 `api/services/app_generate_service.py` 进入请求分流，再沿 `api/core/app/apps/workflow/app_runner.py` 阅读运行准备，最后看 `api/core/workflow/workflow_entry.py` 的引擎接入。

本页没有展开文档入库、插件协议、权限体系和聊天记忆。示例中的知识材料需要预先准备；本页并未验证其入库链路。
