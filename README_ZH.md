# AssignmentPilot 中文说明文档

AssignmentPilot 是一个面向课程作业规划与要求抽取的 Agentic AI 助手。

当前版本主要完成了 Agentic AI 工作流中的 **Perceive 阶段**。程序可以读取用户提供的作业 brief 文件，调用 DeepSeek 大模型抽取结构化作业要求，并以统一的 `AgentResponse` 格式返回结果。

---

## 1. 目前已经完成的内容

### 1.1 已完成模块

目前已经完成的部分是：

```text
Perception Agent / Perceive 阶段
```

该模块目前支持以下功能：

1. 从 `.txt` 文件中读取作业 brief。
2. 支持默认作业 brief，也支持用户自定义输入 brief 文件。
3. 使用 DeepSeek LLM 自动抽取作业要求。
4. 将 LLM 返回的 JSON 结果转换为 `AssignmentRequirement` 数据对象。
5. 通过统一的 `AgentResponse` 返回最终结果。
6. 在终端中打印抽取结果和执行日志。
7. 为后续模块提供稳定输入，例如 Intent Router、Planner Agent、Compliance Checker 和 Feedback Agent。

### 1.2 输入是什么

当前程序接收一个作业 brief 文本文件作为输入。

默认输入文件：

```text
data/assignment_brief.txt
```

自定义输入文件示例：

```text
data/Assignment_Brief_Responsible_AI_Deployment.txt
```

输入文件应该是 `.txt` 文件，里面可以包含作业说明、项目要求、评分标准、提交方式、截止时间等内容。

使用自定义 brief 文件的命令示例：

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt
```

其中，`--brief` 参数用于告诉程序这次要读取哪个作业说明文件。

### 1.3 输出结果在哪里获取

当前阶段，程序的主要输出会直接显示在终端中。

终端输出包括：

1. Perception Agent 是否运行成功。
2. 输入的 brief 文件路径。
3. 原始输入文本长度。
4. 抽取出的结构化作业要求。
5. Perception Agent 的执行日志。

当前版本还没有自动把抽取结果保存成文件。后续模块可以继续扩展，将生成结果保存到以下位置：

```text
outputs/project_plan.md
outputs/task_breakdown.csv
outputs/compliance_report.md
outputs/demo_log.json
```

---

## 2. 程序目前定义的数据结构

共享数据结构定义在：

```text
schemas.py
```

这些结构非常重要，因为它们规定了不同 Agent 和工具之间如何传递数据。后续成员应该尽量复用这些结构，避免每个模块自己定义一套不兼容的数据格式。

### 2.1 `AssignmentRequirement`

`AssignmentRequirement` 用于保存从作业 brief 中抽取出的结构化要求。

```python
@dataclass
class AssignmentRequirement:
    project_goal: str = ""
    course_name: str = ""
    video_limit_minutes: int = 12

    required_video_sections: List[str] = field(default_factory=list)
    required_agentic_stages: List[str] = field(default_factory=list)

    submission_requirements: Dict[str, str] = field(default_factory=dict)
    grading_criteria: Dict[str, float] = field(default_factory=dict)
    deadlines: Dict[str, str] = field(default_factory=dict)

    bonus_features: List[str] = field(default_factory=list)

    human_interaction_required: bool = True
    responsible_ai_required: bool = True

    originality_requirements: List[str] = field(default_factory=list)
    peer_evaluation_requirements: List[str] = field(default_factory=list)
```

#### 字段详细解释

| 字段 | 类型 | 含义 |
|---|---|---|
| `project_goal` | `str` | 作业的核心目标。例如：要求学生开发一个 Agentic AI 应用、分析一个真实案例、提交一份报告等。 |
| `course_name` | `str` | 课程名称。如果 brief 中明确写了课程名，就抽取到这里；如果没有写，可以为空字符串。 |
| `video_limit_minutes` | `int` | 视频时长限制。如果作业要求提交视频并给出时长限制，就记录分钟数；如果没有视频要求，可以设为 `0`。 |
| `required_video_sections` | `List[str]` | 视频中必须展示的章节。例如 `Overview`、`Perceive`、`Reason`、`Action`、`Learn`、`Responsible AI`、`Conclusions` 等。如果作业不要求视频，该列表可以为空。 |
| `required_agentic_stages` | `List[str]` | 作业要求展示的 Agentic AI 阶段，例如 `Perceive`、`Reason`、`Action`、`Learn`。如果作业不是 Agentic AI 工作流相关任务，该列表可以为空。 |
| `submission_requirements` | `Dict[str, str]` | 作业提交要求。里面可以包含提交物、格式要求、提交平台、组队要求和特殊要求等。 |
| `grading_criteria` | `Dict[str, float]` | 评分标准及其权重。例如：`{"Case Description": 20, "Impact Analysis": 25}`。 |
| `deadlines` | `Dict[str, str]` | 重要截止时间，例如作业提交时间、互评截止时间等。 |
| `bonus_features` | `List[str]` | brief 中提到的加分项或可选高级功能，例如 Agentic RAG、Agent Evaluation、PII Masking 等。 |
| `human_interaction_required` | `bool` | 作业是否明确要求人类监督、人类审批、互评、human-in-the-loop 或人工参与流程。 |
| `responsible_ai_required` | `bool` | 作业是否涉及 Responsible AI 相关内容，例如伦理、治理、合规、风险缓解、公平性、隐私、安全、问责或 AI 事故分析等。 |
| `originality_requirements` | `List[str]` | 与原创性、学术诚信、抄袭、AI 工具使用声明等相关的要求。 |
| `peer_evaluation_requirements` | `List[str]` | 与同伴互评相关的要求，例如互评内容、互评维度、互评截止时间等。 |

#### `submission_requirements` 的内部字段

虽然 `submission_requirements` 在数据结构中是一个字典，但当前 LLM 抽取时希望它包含以下子字段：

```json
{
  "deliverables": ["string"],
  "format": ["string"],
  "submission_platform": "string",
  "group_requirements": "string",
  "special_requirements": ["string"]
}
```

| 子字段 | 含义 |
|---|---|
| `deliverables` | 需要提交的主要内容，例如 slides、report、code、notebook、video、presentation 等。 |
| `format` | 格式要求，例如 slides 数量、页数、视频时长、文件类型、Notebook 格式等。 |
| `submission_platform` | 提交平台，例如 NTUlearn、Blackboard、GitHub、YouTube 或其他平台。 |
| `group_requirements` | 组队要求，例如个人完成、4-6 人小组、所有成员都要参与等。 |
| `special_requirements` | 其他特殊要求，例如 title slide 不计入页数、必须声明 AI 使用、成员必须出镜、必须使用本人声音、需要原创性声明等。 |

### 2.2 `UserContext`

`UserContext` 用于保存用户当前项目相关信息。

```python
@dataclass
class UserContext:
    user_input: str = ""
    group_size: int = 4
    available_days: int = 10
    selected_topic: str = "AssignmentPilot"
    preferred_difficulty: str = "medium"

    current_progress: str = ""
    target_bonus_features: List[str] = field(default_factory=list)
    feedback_history: List[str] = field(default_factory=list)
```

#### 字段详细解释

| 字段 | 类型 | 含义 |
|---|---|---|
| `user_input` | `str` | 用户当前输入的请求。例如：`"Help us plan the coding part of AssignmentPilot."` |
| `group_size` | `int` | 小组人数。当前默认值是 `4`，因为本项目小组共有四人。 |
| `available_days` | `int` | 距离截止日期大约还有多少天。后续 Planner Agent 可以用它生成更现实的时间安排。 |
| `selected_topic` | `str` | 当前选择的项目题目。默认是 `AssignmentPilot`。 |
| `preferred_difficulty` | `str` | 用户希望项目实现的难度，例如 `low`、`medium` 或 `high`。后续可用于控制项目范围。 |
| `current_progress` | `str` | 当前项目进度描述。例如：`"Perception Agent completed."` |
| `target_bonus_features` | `List[str]` | 小组希望加入的加分项，例如 Agentic RAG、observability、evaluation 等。 |
| `feedback_history` | `List[str]` | 用户历史反馈列表。后续可用于实现 Learn 阶段和 Feedback Agent。 |

### 2.3 `AgentResponse`

`AgentResponse` 是所有 Agent 和工具推荐使用的统一返回格式。

```python
@dataclass
class AgentResponse:
    success: bool
    module_name: str
    data: Dict[str, Any]
    message: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    logs: List[Dict[str, Any]] = field(default_factory=list)
```

#### 字段详细解释

| 字段 | 类型 | 含义 |
|---|---|---|
| `success` | `bool` | 模块是否成功运行。`True` 表示成功，`False` 表示失败。 |
| `module_name` | `str` | 返回结果的模块名称，例如 `PerceptionAgent`。 |
| `data` | `Dict[str, Any]` | 模块返回的核心数据。对于 Perception Agent 来说，里面包括 `user_input`、`raw_text_length` 和 `requirements`。 |
| `message` | `str` | 给用户或开发者看的简短说明。例如：`"Perception completed successfully."` |
| `warnings` | `List[str]` | 非致命警告。即使有 warning，模块也可以继续成功运行。 |
| `errors` | `List[str]` | 错误信息。如果模块运行失败，例如文件不存在、文件为空、API key 缺失，就会记录在这里。 |
| `logs` | `List[Dict[str, Any]]` | 执行日志，用于调试和后续 agent observability 展示。 |

---

## 3. 使用的大模型以及 Key 存放位置

### 3.1 使用的大模型

当前程序使用 **DeepSeek** 作为大模型服务提供方。

模型名称在 `.env` 文件中配置：

```text
DEEPSEEK_MODEL=deepseek-v4-flash
```

当前通过 OpenAI-compatible SDK 接口调用 DeepSeek。

相关文件：

```text
tools/requirement_extractor.py
```

核心客户端初始化代码：

```python
self.client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)
```

### 3.2 API Key 存放位置

DeepSeek API key 应该存放在项目根目录下的 `.env` 文件中：

```text
assignment_pilot/.env
```

`.env` 示例：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-v4-flash
MAX_BRIEF_CHARS=60000
```

`.env` 文件由 `config.py` 加载。

注意：

```text
不要把 .env 文件上传到 GitHub 或任何公开仓库。
```

建议 `.gitignore` 中加入：

```text
.env
__pycache__/
```

---

## 4. 程序运行方法

### 4.1 安装依赖

在项目根目录运行：

```bash
pip install -r requirements.txt
```

当前 `requirements.txt` 内容：

```text
openai>=1.0.0
python-dotenv>=1.0.0
```

### 4.2 准备 API Key

在项目根目录创建 `.env` 文件：

```text
assignment_pilot/.env
```

写入：

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-v4-flash
MAX_BRIEF_CHARS=60000
```

### 4.3 使用默认 brief 运行

默认 brief 路径：

```text
data/assignment_brief.txt
```

运行命令：

```bash
python main.py
```

### 4.4 使用自定义 brief 运行

示例：

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt
```

### 4.5 使用自定义用户输入运行

示例：

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt --user_input "Please extract the key assignment requirements."
```

---

## 5. 当前程序流程

当前程序运行流程如下：

```text
main.py
  ↓
解析命令行参数
  ↓
创建 DocumentReaderTool
  ↓
创建 RequirementExtractorTool
  ↓
创建 PerceptionAgent
  ↓
读取作业 brief 文件
  ↓
将原始文本发送给 DeepSeek
  ↓
抽取结构化作业要求
  ↓
转换为 AssignmentRequirement
  ↓
包装为 AgentResponse
  ↓
在终端打印抽取结果和日志
```

---

## 6. 接下来三个 Member 需要完成的大致任务

### 6.1 Member 2：Intent Router 和 Planner Agent

Member 2 主要负责 **Reason 阶段**。

建议负责文件：

```text
agents/intent_router.py
agents/planner_agent.py
tools/task_generator.py
```

主要任务：

1. 实现用户意图分类。
2. 判断用户请求属于 topic generation、project design、coding plan、task allocation、compliance check、video script、risk review 或 revision。
3. 基于 Perception Agent 抽取出的 requirements 生成项目计划。
4. 将项目拆解成更小的 coding tasks。
5. 生成初步团队任务分配方案。
6. 为 Action Agent 准备结构化输出。

### 6.2 Member 3：Tool Executor 和输出生成

Member 3 主要负责 **Action 阶段**。

建议负责文件：

```text
tools/checklist_generator.py
tools/timeline_generator.py
tools/logger.py
outputs/project_plan.md
outputs/task_breakdown.csv
outputs/demo_log.json
```

主要任务：

1. 根据抽取出的作业要求生成 checklist。
2. 生成项目开发时间表。
3. 将输出结果保存成文件。
4. 改进日志系统和 observability。
5. 将项目计划导出为 Markdown。
6. 将任务拆解导出为 CSV。
7. 将 demo logs 保存为 JSON。

### 6.3 Member 4：Compliance、Safety、Feedback 和 Evaluation

Member 4 主要负责 **Learn、Responsible AI 和 Evaluation**。

建议负责文件：

```text
agents/compliance_agent.py
agents/safety_agent.py
agents/feedback_agent.py
memory/feedback_memory.py
memory/example_memory.py
evaluation/test_cases.py
evaluation/evaluator.py
evaluation/eval_report.py
```

主要任务：

1. 实现 Compliance Checker。
2. 检查生成的项目计划是否覆盖所有评分项。
3. 实现 Safety Agent。
4. 拦截不安全或不诚信请求，例如编造成员贡献、伪造测试结果、隐瞒 AI 使用或保证分数。
5. 实现 Feedback Agent。
6. 根据用户反馈修改项目计划。
7. 实现测试用例。
8. 生成 evaluation report。

---

## 7. 当前项目状态

| 模块 | 状态 |
|---|---|
| 项目文件结构 | 已完成 |
| 配置文件 | 已完成 |
| 共享数据结构 | 已完成 |
| 文档读取工具 | 已完成 |
| 基于 DeepSeek 的要求抽取工具 | 已完成 |
| Perception Agent | 已完成 |
| 自定义 brief 文件输入 | 已完成 |
| 终端输出 | 已完成 |
| Intent Router | 未开始 |
| Planner Agent | 未开始 |
| Checklist Generator | 未开始 |
| Compliance Checker | 未开始 |
| Safety Agent | 未开始 |
| Feedback Agent | 未开始 |
| Evaluation | 未开始 |

当前版本可以视为：

```text
Perception Agent v1.0
```
