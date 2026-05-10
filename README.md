# AssignmentPilot

AssignmentPilot is a course assignment planning assistant built as an Agentic AI demo for CA6123.

The project currently covers:

- **Perceive**: reads the assignment brief and extracts structured requirements with DeepSeek.
- **Reason**: classifies user intent, generates a project plan, breaks coding work into tasks, and allocates work across four members.

## Member 2: Reasoning / Planning

Member 2 is responsible for the Reason stage.

Implemented files:

- `agents/intent_router.py`
- `agents/planner_agent.py`
- `tools/task_generator.py`
- `tools/team_allocator.py`
- `tests/test_member2_reasoning.py`

The Reason stage can be tested without calling the LLM:

```bash
python -m unittest tests.test_member2_reasoning -v
```

Run the standalone Reason demo:

```bash
python main.py --reason_only --user_input "帮我考虑 coding 的部分，生成四个人分工和项目计划"
```

Run the full Perceive + Reason flow after installing dependencies and preparing `.env`:

```bash
pip install -r requirements.txt
python main.py
```

## Local Demo Console

This branch also includes a Streamlit demo console for presenting the merged group project in a more visual way:

```bash
pip install -r requirements.txt
python -m streamlit run demo_dashboard.py
```

The console runs the deterministic Reason and Action stages by default, so it can be shown without spending LLM calls. It is designed as a group presentation screen:

- `Flow`: explains how Perceive, Context, Reason, Action, and Learn map to the assignment stages.
- `Member 2 Plan`: highlights IntentRouter, PlannerAgent, TaskGenerator, and TeamAllocator.
- `Generated Files`: shows ActionAgent outputs from `outputs/`.
- `Logs`: shows observability evidence for the demo flow.
- `Raw Data`: keeps the structured JSON outputs available for technical questions.

For a Member 2 presentation, use this path:

1. Select a 4, 5, or 6-member scenario in the sidebar.
2. Click `Run Planning Demo`.
3. Open `Member 2 Plan` and explain the generated intent, team allocation, coding task timeline, and how this structured plan feeds ActionAgent.

## Notes

- `.env` should not be committed to GitHub.
- `member2_private_notes/` is a local-only folder for personal video notes and push checklists.
