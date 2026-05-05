# AssignmentPilot

AssignmentPilot is an Agentic AI assistant designed for course assignment planning and requirement extraction.

The current version has completed the  **Perceive stage** ,  **Reason stage** , and **Action stage** within the Agentic AI workflow. The program can read assignment brief files provided by the user, invoke the DeepSeek large language model to extract structured assignment requirements, and return results in a unified `AgentResponse` format. The Reason stage identifies user intent and generates project plans, task breakdowns, and four-person team allocations.

---

## 2. Current Data Structures

## 1. Currently Completed Content

### 1.1 Completed Modules

The currently completed parts are:

```plaintext
Perception Agent / Perceive Stage
Reasoning / Planning Agent / Reason Stage
Action Agent / Action Stage
```

The module currently supports the following functions:

1. Reading assignment briefs from `.txt` files.
2. Supporting both default assignment briefs and user-defined custom brief files.
3. Automatically extracting assignment requirements using the DeepSeek LLM.
4. Converting JSON results returned by the LLM into `AssignmentRequirement` data objects.
5. Clarifying user intent and generating development task breakdowns, timelines, and team allocations.
6. Printing clean extraction results, execution logs, and file generation paths in the terminal.
7. Automatically outputting reasoning results into multiple physical deliverables (Markdown, CSV).
8. Providing a solid foundation for subsequent Learn and Responsible AI modules (Compliance Checker and Feedback Agent).

### 1.2 Input Specifications

The current program receives an assignment brief text file as input.

Default input file:

```plaintext
data/assignment_brief.txt
```

Example of a custom input file:

```plaintext
data/Assignment_Brief_Responsible_AI_Deployment.txt
```

Input files should be `.txt` files containing assignment descriptions, project requirements, grading criteria, submission methods, deadlines, etc.

Command example for using a custom brief file:

```bash
python main.py --brief data/Assignment_Brief_Responsible_AI_Deployment.txt
```

The `--brief` parameter tells the program which assignment description file to read for the current run.

### 1.3 Where to Obtain Output Results

In the current stage, the main execution status of the program is printed clearly in the terminal, while the actual physical output files are automatically saved in the `outputs/` folder at the root directory.

Terminal output includes:

1. Whether the Perception Agent ran successfully.
2. The file path of the input brief.
3. Original input text length.
4. Structured assignment requirements extracted.
5. Execution logs of the Perception Agent.
6. Final execution status and generated file paths from the Action Agent.

Physical files generated upon execution include:

```plaintext
outputs/project_plan.md      # Project schedule containing a Mermaid Gantt chart
outputs/task_breakdown.csv   # Specific task allocation table for the four-person team
outputs/priorities.csv       # Project development priority table
outputs/demo_log.json        # System execution trace log
outputs/compliance_report.md # Compliance audit report containing human verification and reserved machine verification areas
```

---

## 2. Currently Defined Data Structures

Shared data structures are defined in:

```plaintext
schemas.py
```

These structures are crucial as they govern how data is passed between different Agents and tools. Subsequent members should reuse these structures whenever possible to avoid incompatible data formats.

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

| Field                            | Type                 | Meaning                                                                                                                                                                                                                     |
| -------------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `project_goal`                 | `str`              | The main goal of the assignment. It describes what students are expected to do, such as building an Agentic AI application, analysing a case study, preparing a report, or giving a presentation.                           |
| `course_name`                  | `str`              | The course name if explicitly mentioned in the brief. If the course name is not found, this field can remain empty.                                                                                                         |
| `video_limit_minutes`          | `int`              | The maximum video duration in minutes if the assignment requires a video. If no video limit is mentioned, the value can be `0`.                                                                                           |
| `required_video_sections`      | `List[str]`        | Sections that must appear in a video presentation, such as `Overview`, `Perceive`, `Reason`, `Action`, `Learn`, `Responsible AI`, or `Conclusions`. If there is no video requirement, this list can be empty. |
| `required_agentic_stages`      | `List[str]`        | Required Agentic AI stages, such as `Perceive`, `Reason`, `Action`, and `Learn`. This is useful for Agentic AI project briefs. If the assignment is not about Agentic AI workflow, this list can be empty.          |
| `submission_requirements`      | `Dict[str, str]`   | A dictionary describing what students need to submit, including deliverables, formats, submission platform, group requirements, and special requirements.                                                                   |
| `grading_criteria`             | `Dict[str, float]` | A dictionary of grading criteria and their weights. Example:`{"Case Description": 20, "Impact Analysis": 25}`.                                                                                                            |
| `deadlines`                    | `Dict[str, str]`   | Important deadlines, such as assignment submission deadline and peer evaluation deadline.                                                                                                                                   |
| `bonus_features`               | `List[str]`        | Bonus features or optional advanced requirements mentioned in the brief, such as Agentic RAG, Agent Evaluation, MCP, A2A, or PII Masking.                                                                                   |
| `human_interaction_required`   | `bool`             | Whether the assignment explicitly requires human supervision, human approval, peer evaluation, human-in-the-loop design, or human participation in the workflow.                                                            |
| `responsible_ai_required`      | `bool`             | Whether the assignment involves Responsible AI topics such as ethics, governance, compliance, risk mitigation, fairness, privacy, safety, accountability, or harmful AI incidents.                                          |
| `originality_requirements`     | `List[str]`        | Requirements related to originality, academic integrity, plagiarism, or AI tool usage declaration.                                                                                                                          |
| `peer_evaluation_requirements` | `List[str]`        | Requirements related to peer evaluation, teamwork review, peer assessment criteria, or peer evaluation deadlines.                                                                                                           |

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

| Subfield                 | Meaning                                                                                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `deliverables`         | The main items students need to submit, such as slides, report, code, notebook, video, or presentation.                                         |
| `format`               | Format requirements, such as slide count, page count, video length, file type, or notebook format.                                              |
| `submission_platform`  | Where the assignment should be submitted, such as NTUlearn, Blackboard, GitHub, YouTube, or another platform.                                   |
| `group_requirements`   | Whether the assignment is individual or group-based, and how many members are allowed or required.                                              |
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

| Field                     | Type          | Meaning                                                                                                                                             |
| ------------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_input`            | `str`       | The current user request. Example:`"Help us plan the coding part of AssignmentPilot."`                                                            |
| `group_size`            | `int`       | Number of team members. The default is `4` because the current team has four members.                                                             |
| `available_days`        | `int`       | Estimated number of days available before the deadline. This can later help the Planner Agent generate a realistic timeline.                        |
| `selected_topic`        | `str`       | The selected project topic. The default is `AssignmentPilot`.                                                                                     |
| `preferred_difficulty`  | `str`       | The user's preferred implementation difficulty, such as `low`, `medium`, or `high`. This can later help simplify or expand the project scope. |
| `current_progress`      | `str`       | A short description of the current project progress. Example:`"Perception Agent completed."`                                                      |
| `target_bonus_features` | `List[str]` | Bonus features the team wants to include, such as Agentic RAG, observability, or evaluation.                                                        |
| `feedback_history`      | `List[str]` | A list of previous user feedback. This can later support the Learn stage and Feedback Agent.                                                        |

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

| Field           | Type                     | Meaning                                                                                                                                    |
| --------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `success`     | `bool`                 | Whether the module ran successfully.`True` means success, while `False` means failure.                                                 |
| `module_name` | `str`                  | The name of the agent or tool returning the response, such as `PerceptionAgent`.                                                         |
| `data`        | `Dict[str, Any]`       | The main result returned by the module. For the Perception Agent, this includes `user_input`, `raw_text_length`, and `requirements`. |
| `message`     | `str`                  | A short human-readable message explaining the result. Example:`"Perception completed successfully."`                                     |
| `warnings`    | `List[str]`            | Non-fatal issues. The module can still succeed even if warnings exist.                                                                     |
| `errors`      | `List[str]`            | Error messages if the module fails. Example: missing file path, empty file, missing API key, or LLM response parsing failure.              |
| `logs`        | `List[Dict[str, Any]]` | Step-by-step execution logs. These logs support debugging and can later be used for agent observability.                                   |

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
Parse CLI Arguments
  ↓
Create DocumentReaderTool
  ↓
Create RequirementExtractorTool
  ↓
Create PerceptionAgent
  ↓
Read Assignment Brief
  ↓
Send text to DeepSeek
  ↓
Extract structured requirements
  ↓
Convert to AssignmentRequirement
  ↓
Wrap as AgentResponse
  ↓
Print results/logs in terminal
  ↓
Generate structured plan/allocation
  ↓
Pass plan to Action Agent
  ↓
Safety path validation & field mapping
  ↓
Invoke tools to generate MD/CSV files
  ↓
Print final execution status/paths in terminal
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

| Module                               | Status                                                               |
| ------------------------------------ | -------------------------------------------------------------------- |
| Project folder structure             | Completed                                                            |
| Config file                          | Completed                                                            |
| Shared schemas                       | Completed                                                            |
| Document reader                      | Completed                                                            |
| DeepSeek-based requirement extractor | Completed                                                            |
| Perception Agent                     | Completed                                                            |
| Custom brief file input              | Completed                                                            |
| Terminal output                      | Completed                                                            |
| Intent Router                        | Completed                                                            |
| Planner Agent                        | Completed                                                            |
| Task Generator                       | Completed                                                            |
| Team Allocator                       | Completed                                                            |
| Checklist Generator                  | Completed                                                            |
| Compliance Checker                   | Human area (Member 3 Completed), Machine area (Member 4 Not Started) |
| Safety Agent                         | Not started                                                          |
| Feedback Agent                       | Not started                                                          |
| Evaluation                           | Not started                                                          |

Current version can be considered:

```text
Perception Agent v1.0 + Reason Agent v1.0 + Action Agent v1.0
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
python main.py --reason_only --user_input "Help us plan the coding part of AssignmentPilot."
```

### 7.2 Member 3 Completed Content

Member 3 has completed the core modules for the Action stage:

```plaintext
agents/action_agent.py
tools/timeline_generator.py
tools/checklist_generator.py
tools/logger.py
outputs/project_plan.md
outputs/task_breakdown.csv
outputs/demo_log.json
outputs/compliance_report.md
outputs/priorities.csv
```

Core Function Implementation:

1. Automated Deliverable Generation : Automatically generates Markdown project plans and CSV task/priority tables based on reasoning results.
2. Compliance Warning Framework : Generates audit reports via `ChecklistGenerator`. Completed "Human Verification" area rendering and reserved slots for Member 4’s automated audit.
3. System-level Observability : Introduced `ActionLogger` to record Agent execution steps, statuses, and I/O traces via `record_internal_trace`, saving traces as structured JSON.
4. Defensive Programming : Added path security validation `_is_safe_path` in `ActionAgent` to prevent path traversal risks.

Run Demo: Run the Action stage individually using mock data:

```bash
python main.py --action_only
```
