# AssignmentPilot

AssignmentPilot is an Agentic AI assistant for course assignment planning and requirement extraction.

The current version covers the **Perceive stage** and the **Reason stage** of the Agentic AI workflow. It reads an assignment brief provided by the user, uses a DeepSeek large language model to extract structured requirements, and returns the result in a unified `AgentResponse` format. The Reason stage classifies user intent, generates a project plan, breaks coding work into tasks, and allocates work across four members.

---

## 1. Current Completed Work

### 1.1 Completed Module

The currently completed part is:

```text
Perception Agent / Perceive Stage
```

This module supports the following functions:

1. Read an assignment brief from a `.txt` file.
2. Support both a default assignment brief and a custom user-provided brief.
3. Use DeepSeek LLM to extract structured assignment requirements.
4. Convert the extracted JSON result into an `AssignmentRequirement` data object.
5. Return the final result through a standard `AgentResponse`.
6. Print the extracted requirements and execution logs in the terminal.
7. Provide a stable input format for later modules, such as Intent Router, Planner Agent, Compliance Checker, and Feedback Agent.

### 1.2 Input

The current program accepts an assignment brief text file as input.

Default input file:

```text
data/assignment_brief.txt
```

Custom input file example:

```text
data/Assignment_Brief_Responsible_AI_Deployment.txt
```

The input file should be a `.txt` file containing assignment instructions, project requirements, grading criteria, submission requirements, deadlines, or similar course project information.

Example command with a custom brief file:

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt
```

The `--brief` argument tells the program which assignment brief file to read.

### 1.3 Output

At the current stage, the main output is printed directly in the terminal.

The terminal output includes:

1. Whether the Perception Agent ran successfully.
2. The input brief file path.
3. The length of the raw input text.
4. The extracted structured assignment requirements.
5. Execution logs from the Perception Agent.

Example extracted requirement output:

```json
{
  "project_goal": "Research, analyse, and present a recent real-world case or incident involving a Generative AI-powered system.",
  "course_name": "",
  "video_limit_minutes": 0,
  "required_video_sections": [],
  "required_agentic_stages": [],
  "submission_requirements": {
    "deliverables": ["slides"],
    "format": ["8-10 slides, excluding title slide and content slide"],
    "submission_platform": "NTUlearn",
    "group_requirements": "Individual or group of 4-6",
    "special_requirements": []
  },
  "grading_criteria": {
    "Case Description": 20,
    "Impact Analysis": 25,
    "Root Cause Analysis": 25,
    "Organisational Response or Resolution": 20,
    "Presentation Structure": 10
  },
  "deadlines": {
    "assignment_submission": "22 March 2026, 1159pm",
    "peer_evaluation": ""
  },
  "bonus_features": [],
  "human_interaction_required": false,
  "responsible_ai_required": true,
  "originality_requirements": [],
  "peer_evaluation_requirements": []
}
```

Currently, the extracted result is not automatically saved to a file. Later modules can extend the program to save generated outputs into:

```text
outputs/project_plan.md
outputs/task_breakdown.csv
outputs/compliance_report.md
outputs/demo_log.json
```

---

## 2. Current Data Structures

The shared data structures are defined in:

```text
schemas.py
```

These structures define how different modules exchange information. Later members should reuse these structures instead of creating incompatible formats.

### 2.1 `AssignmentRequirement`

`AssignmentRequirement` stores structured information extracted from an assignment brief.

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

#### Field explanation

| Field | Type | Meaning |
|---|---|---|
| `project_goal` | `str` | The main goal of the assignment. It describes what students are expected to do, such as building an Agentic AI application, analysing a case study, preparing a report, or giving a presentation. |
| `course_name` | `str` | The course name if explicitly mentioned in the brief. If the course name is not found, this field can remain empty. |
| `video_limit_minutes` | `int` | The maximum video duration in minutes if the assignment requires a video. If no video limit is mentioned, the value can be `0`. |
| `required_video_sections` | `List[str]` | Sections that must appear in a video presentation, such as `Overview`, `Perceive`, `Reason`, `Action`, `Learn`, `Responsible AI`, or `Conclusions`. If there is no video requirement, this list can be empty. |
| `required_agentic_stages` | `List[str]` | Required Agentic AI stages, such as `Perceive`, `Reason`, `Action`, and `Learn`. This is useful for Agentic AI project briefs. If the assignment is not about Agentic AI workflow, this list can be empty. |
| `submission_requirements` | `Dict[str, str]` | A dictionary describing what students need to submit, including deliverables, formats, submission platform, group requirements, and special requirements. |
| `grading_criteria` | `Dict[str, float]` | A dictionary of grading criteria and their weights. Example: `{"Case Description": 20, "Impact Analysis": 25}`. |
| `deadlines` | `Dict[str, str]` | Important deadlines, such as assignment submission deadline and peer evaluation deadline. |
| `bonus_features` | `List[str]` | Bonus features or optional advanced requirements mentioned in the brief, such as Agentic RAG, Agent Evaluation, MCP, A2A, or PII Masking. |
| `human_interaction_required` | `bool` | Whether the assignment explicitly requires human supervision, human approval, peer evaluation, human-in-the-loop design, or human participation in the workflow. |
| `responsible_ai_required` | `bool` | Whether the assignment involves Responsible AI topics such as ethics, governance, compliance, risk mitigation, fairness, privacy, safety, accountability, or harmful AI incidents. |
| `originality_requirements` | `List[str]` | Requirements related to originality, academic integrity, plagiarism, or AI tool usage declaration. |
| `peer_evaluation_requirements` | `List[str]` | Requirements related to peer evaluation, teamwork review, peer assessment criteria, or peer evaluation deadlines. |

#### Details of `submission_requirements`

Although `submission_requirements` is stored as a dictionary, the current LLM extraction prompt expects it to contain these subfields:

```json
{
  "deliverables": ["string"],
  "format": ["string"],
  "submission_platform": "string",
  "group_requirements": "string",
  "special_requirements": ["string"]
}
```

| Subfield | Meaning |
|---|---|
| `deliverables` | The main items students need to submit, such as slides, report, code, notebook, video, or presentation. |
| `format` | Format requirements, such as slide count, page count, video length, file type, or notebook format. |
| `submission_platform` | Where the assignment should be submitted, such as NTUlearn, Blackboard, GitHub, YouTube, or another platform. |
| `group_requirements` | Whether the assignment is individual or group-based, and how many members are allowed or required. |
| `special_requirements` | Additional requirements, such as title slide exclusion, AI usage statement, member appearance, own voice, captions, or originality declaration. |

### 2.2 `UserContext`

`UserContext` stores user-specific project information.

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

#### Field explanation

| Field | Type | Meaning |
|---|---|---|
| `user_input` | `str` | The current user request. Example: `"Help us plan the coding part of AssignmentPilot."` |
| `group_size` | `int` | Number of team members. The default is `4` because the current team has four members. |
| `available_days` | `int` | Estimated number of days available before the deadline. This can later help the Planner Agent generate a realistic timeline. |
| `selected_topic` | `str` | The selected project topic. The default is `AssignmentPilot`. |
| `preferred_difficulty` | `str` | The user's preferred implementation difficulty, such as `low`, `medium`, or `high`. This can later help simplify or expand the project scope. |
| `current_progress` | `str` | A short description of the current project progress. Example: `"Perception Agent completed."` |
| `target_bonus_features` | `List[str]` | Bonus features the team wants to include, such as Agentic RAG, observability, or evaluation. |
| `feedback_history` | `List[str]` | A list of previous user feedback. This can later support the Learn stage and Feedback Agent. |

### 2.3 `AgentResponse`

`AgentResponse` is the standard response format for all agents and tools.

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

#### Field explanation

| Field | Type | Meaning |
|---|---|---|
| `success` | `bool` | Whether the module ran successfully. `True` means success, while `False` means failure. |
| `module_name` | `str` | The name of the agent or tool returning the response, such as `PerceptionAgent`. |
| `data` | `Dict[str, Any]` | The main result returned by the module. For the Perception Agent, this includes `user_input`, `raw_text_length`, and `requirements`. |
| `message` | `str` | A short human-readable message explaining the result. Example: `"Perception completed successfully."` |
| `warnings` | `List[str]` | Non-fatal issues. The module can still succeed even if warnings exist. |
| `errors` | `List[str]` | Error messages if the module fails. Example: missing file path, empty file, missing API key, or LLM response parsing failure. |
| `logs` | `List[Dict[str, Any]]` | Step-by-step execution logs. These logs support debugging and can later be used for agent observability. |

---

## 3. LLM Model and API Key Storage

### 3.1 LLM Used

The current program uses **DeepSeek** as the LLM provider.

The model name is configured in the `.env` file:

```text
DEEPSEEK_MODEL=deepseek-v4-flash
```

The LLM is called through the OpenAI-compatible SDK interface.

Relevant file:

```text
tools/requirement_extractor.py
```

Core client setup:

```python
self.client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)
```

### 3.2 API Key Storage

The DeepSeek API key should be stored in a `.env` file located in the project root:

```text
assignment_pilot/.env
```

Example `.env` file:

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-v4-flash
MAX_BRIEF_CHARS=60000
```

The `.env` file is loaded in `config.py`.

Important:

```text
Do not upload the .env file to GitHub or any public repository.
```

Recommended `.gitignore` entry:

```text
.env
__pycache__/
```

---

## 4. How to Run the Program

### 4.1 Install Dependencies

Run the following command in the project root directory:

```bash
pip install -r requirements.txt
```

Current `requirements.txt`:

```text
openai>=1.0.0
python-dotenv>=1.0.0
```

### 4.2 Prepare the API Key

Create a `.env` file in the project root:

```text
assignment_pilot/.env
```

Add the following content:

```text
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-v4-flash
MAX_BRIEF_CHARS=60000
```

### 4.3 Run with the Default Brief

Default brief path:

```text
data/assignment_brief.txt
```

Command:

```bash
python main.py
```

### 4.4 Run with a Custom Brief

Example:

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt
```

### 4.5 Run with a Custom User Input

Example:

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt --user_input "Please extract the key assignment requirements."
```

---

## 5. Current Program Flow

The current program flow is:

```text
main.py
  ↓
parse command-line arguments
  ↓
create DocumentReaderTool
  ↓
create RequirementExtractorTool
  ↓
create PerceptionAgent
  ↓
read assignment brief file
  ↓
send raw text to DeepSeek
  ↓
extract structured requirements
  ↓
convert JSON into AssignmentRequirement
  ↓
wrap result in AgentResponse
  ↓
print extracted data and logs
```

---

## 6. Tasks for the Next Three Members

### 6.1 Member 2: Intent Router and Planner Agent

Member 2 should focus on the **Reason** stage.

Suggested files:

```text
agents/intent_router.py
agents/planner_agent.py
tools/task_generator.py
```

Main tasks:

1. Implement user intent classification.
2. Identify whether the user wants topic generation, project design, coding plan, task allocation, compliance check, video script, risk review, or revision.
3. Generate a project plan based on extracted requirements.
4. Break the project into smaller coding tasks.
5. Generate a rough team task allocation plan.
6. Prepare structured output for the Action Agent.

### 6.2 Member 3: Tool Executor and Output Generation

Member 3 should focus on the **Action** stage.

Suggested files:

```text
tools/checklist_generator.py
tools/timeline_generator.py
tools/logger.py
outputs/project_plan.md
outputs/task_breakdown.csv
outputs/demo_log.json
```

Main tasks:

1. Generate assignment checklists based on the extracted requirements.
2. Generate a project development timeline.
3. Save outputs into files.
4. Improve logging and observability.
5. Export project plan to Markdown.
6. Export task breakdown to CSV.
7. Save demo logs to JSON.

### 6.3 Member 4: Compliance, Safety, Feedback, and Evaluation

Member 4 should focus on **Learn**, **Responsible AI**, and **Evaluation**.

Suggested files:

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

Main tasks:

1. Implement Compliance Checker.
2. Check whether the generated plan covers all rubric items.
3. Implement Safety Agent.
4. Prevent unsafe or dishonest requests, such as fabricating team contributions, faking test results, hiding AI usage, or guaranteeing grades.
5. Implement Feedback Agent.
6. Revise the project plan based on user feedback.
7. Implement test cases.
8. Generate an evaluation report.

---

## 7. Current Status

| Module | Status |
|---|---|
| Project folder structure | Completed |
| Config file | Completed |
| Shared schemas | Completed |
| Document reader | Completed |
| DeepSeek-based requirement extractor | Completed |
| Perception Agent | Completed |
| Custom brief file input | Completed |
| Terminal output | Completed |
| Intent Router | Completed |
| Planner Agent | Completed |
| Task Generator | Completed |
| Team Allocator | Completed |
| Checklist Generator | Not started |
| Compliance Checker | Not started |
| Safety Agent | Not started |
| Feedback Agent | Not started |
| Evaluation | Not started |

Current version can be considered:

```text
Perception Agent v1.0 + Reason Agent v1.0
```

### 7.1 Member 2 Completed Work

Member 2 has completed the core Reason-stage modules:

```text
agents/intent_router.py
agents/planner_agent.py
tools/task_generator.py
tools/team_allocator.py
tests/test_member2_reasoning.py
```

Run the local tests:

```bash
python -m unittest tests.test_member2_reasoning -v
```

Run the Reason-only demo:

```bash
python main.py --reason_only --user_input "帮我考虑 coding 的部分，生成四个人分工和项目计划"
```
