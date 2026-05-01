from typing import Dict, List


class TeamAllocator:
    def allocate(self, group_size: int = 4, project_topic: str = "AssignmentPilot") -> Dict[str, Dict[str, List[str] or str]]:
        if group_size != 4:
            return self._allocate_generic(group_size, project_topic)

        return {
            "Member 1": {
                "role": "Project Lead and Perception Owner",
                "agentic_stage": "Perceive + Overview",
                "modules": [
                    "Main Orchestrator",
                    "Document Reader",
                    "Requirement Extractor",
                    "Perception Agent",
                    "Integration",
                ],
                "video_focus": "Explain the project background, architecture, and how the brief is converted into structured requirements.",
            },
            "Member 2": {
                "role": "Reasoning and Planning Owner",
                "agentic_stage": "Reason",
                "modules": [
                    "Intent Router",
                    "Planner Agent",
                    "Task Generator",
                    "Team Allocation",
                ],
                "video_focus": "Explain how user intent is classified and how requirements become a coding plan, task breakdown, and team allocation.",
            },
            "Member 3": {
                "role": "Tool Execution and Output Owner",
                "agentic_stage": "Action",
                "modules": [
                    "Checklist Generator",
                    "Timeline Generator",
                    "Output Writer",
                    "Logger",
                ],
                "video_focus": "Explain tool-calling, generated files, timeline, checklist, and execution logs.",
            },
            "Member 4": {
                "role": "Feedback, Safety, and Evaluation Owner",
                "agentic_stage": "Learn + Responsible AI",
                "modules": [
                    "Feedback Agent",
                    "Safety Agent",
                    "Compliance Checker",
                    "Evaluator",
                ],
                "video_focus": "Explain feedback-based revision, human oversight, guardrails, compliance checking, and evaluation.",
            },
        }

    def _allocate_generic(self, group_size: int, project_topic: str) -> Dict[str, Dict[str, List[str] or str]]:
        size = max(1, group_size)
        allocation = {}

        for index in range(1, size + 1):
            allocation[f"Member {index}"] = {
                "role": f"{project_topic} contributor",
                "agentic_stage": "To be assigned",
                "modules": [],
                "video_focus": "Explain assigned implementation work and evidence.",
            }

        return allocation
