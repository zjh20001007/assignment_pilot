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

## Notes

- `.env` should not be committed to GitHub.
- `member2_private_notes/` is a local-only folder for personal video notes and push checklists.
