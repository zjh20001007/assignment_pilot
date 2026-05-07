from typing import Dict, List


class TaskGenerator:
    def generate(self, project_topic: str, intent: str = "project_design") -> List[Dict[str, str]]:
        topic = project_topic or "AssignmentPilot"

        base_tasks = [
            {
                "id": "T1",
                "stage": "Perceive",
                "task": "Read the assignment brief and extract structured requirements.",
                "owner": "Member 1",
                "priority": "High",
                "output": "AssignmentRequirement data for downstream agents",
            },
            {
                "id": "T2",
                "stage": "Reason",
                "task": "Classify user intent and decide the planning route.",
                "owner": "Member 2",
                "priority": "High",
                "output": "Intent label such as coding_plan or task_allocation",
            },
            {
                "id": "T3",
                "stage": "Reason",
                "task": f"Break {topic} into coding modules and implementation priorities.",
                "owner": "Member 2",
                "priority": "High",
                "output": "Structured project plan and coding task breakdown",
            },
            {
                "id": "T4",
                "stage": "Action",
                "task": "Generate checklist, timeline, files, and observable tool logs.",
                "owner": "Member 3",
                "priority": "Medium",
                "output": "Markdown plan, CSV task table, and JSON demo log",
            },
            {
                "id": "T5",
                "stage": "Learn",
                "task": "Revise the project plan from user feedback.",
                "owner": "Member 4",
                "priority": "Medium",
                "output": "Simplified or adjusted plan based on feedback history",
            },
            {
                "id": "T6",
                "stage": "Responsible Agentic AI",
                "task": "Check coverage of required sections, safety guardrails, and evaluation evidence.",
                "owner": "Member 4",
                "priority": "High",
                "output": "Compliance report and evaluation summary",
            },
            {
                "id": "T7",
                "stage": "Overview",
                "task": "Integrate all modules into a single runnable demo flow.",
                "owner": "Member 1",
                "priority": "High",
                "output": "End-to-end command line demo",
            },
        ]

        if intent == "video_script":
            base_tasks.append({
                "id": "T8",
                "stage": "Conclusions",
                "task": "Prepare a concise video narration plan for each member.",
                "owner": "All Members",
                "priority": "Medium",
                "output": "Video speaking outline",
            })

        if intent == "revision":
            base_tasks.append({
                "id": "T8",
                "stage": "Learn",
                "task": "Reduce scope to an MVP and move optional bonus features after core requirements.",
                "owner": "Member 4",
                "priority": "High",
                "output": "Revised lower-difficulty project scope",
            })

        return base_tasks
