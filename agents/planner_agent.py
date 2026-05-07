from typing import Any, Dict, List

from constants import BONUS_FEATURES, REQUIRED_AGENTIC_LOOP, REQUIRED_VIDEO_SECTIONS
from schemas import AgentResponse
from tools.task_generator import TaskGenerator
from tools.team_allocator import TeamAllocator


class PlannerAgent:
    def __init__(
        self,
        task_generator: TaskGenerator | None = None,
        team_allocator: TeamAllocator | None = None,
    ):
        self.task_generator = task_generator or TaskGenerator()
        self.team_allocator = team_allocator or TeamAllocator()

    def run(self, input_data: dict) -> AgentResponse:
        logs = []

        try:
            requirements = input_data.get("requirements", {})
            intent = input_data.get("intent", "project_design")
            user_context = input_data.get("user_context", {})

            project_topic = user_context.get("selected_topic", "AssignmentPilot")
            group_size = int(user_context.get("group_size", 4))
            available_days = int(user_context.get("available_days", 7))

            logs.append({
                "step": "reason_2",
                "agent": "PlannerAgent",
                "action": "generate_project_plan",
                "status": "started",
            })

            coding_tasks = self.task_generator.generate(project_topic, intent)
            team_allocation = self.team_allocator.allocate(group_size, project_topic)

            plan = {
                "intent": intent,
                "project_topic": project_topic,
                "project_goal": self._project_goal(requirements, project_topic),
                "reasoning_design": self._reasoning_design(intent),
                "functional_modules": self._functional_modules(),
                "coding_tasks": coding_tasks,
                "team_allocation": team_allocation,
                "development_priorities": self._development_priorities(requirements, available_days),
                "human_interaction_plan": self._human_interaction_plan(requirements),
                "responsible_ai_notes": self._responsible_ai_notes(requirements),
                "bonus_feature_strategy": self._bonus_feature_strategy(requirements),
                "video_sections_to_cover": self._video_sections(requirements),
            }

            logs.append({
                "step": "reason_2",
                "agent": "PlannerAgent",
                "action": "generate_project_plan",
                "status": "success",
                "output_summary": f"Generated {len(coding_tasks)} tasks for {project_topic}.",
            })

            return AgentResponse(
                success=True,
                module_name="PlannerAgent",
                data=plan,
                message="Planning completed successfully.",
                warnings=[],
                errors=[],
                logs=logs,
            )

        except Exception as error:
            logs.append({
                "step": "reason_error",
                "agent": "PlannerAgent",
                "action": "handle_exception",
                "status": "failed",
                "error": str(error),
            })

            return AgentResponse(
                success=False,
                module_name="PlannerAgent",
                data={},
                message="Planning failed.",
                warnings=[],
                errors=[str(error)],
                logs=logs,
            )

    def _project_goal(self, requirements: Dict[str, Any], project_topic: str) -> str:
        return requirements.get(
            "project_goal",
            f"Design and demonstrate {project_topic} as a multi-step Agentic AI application.",
        )

    def _reasoning_design(self, intent: str) -> Dict[str, Any]:
        return {
            "stage": "Reason",
            "selected_intent": intent,
            "routing_method": "Rule-based bilingual keyword matching for stable demo behavior.",
            "planning_method": "Template-based decomposition using extracted assignment requirements.",
            "why_it_matches_brief": [
                "Shows intent classification and routing.",
                "Shows complex task breakdown into coding responsibilities.",
                "Prepares structured outputs for Action and Compliance modules.",
            ],
        }

    def _functional_modules(self) -> List[Dict[str, str]]:
        return [
            {
                "module": "IntentRouter",
                "purpose": "Classify the user's current request into a supported intent.",
                "owner": "Member 2",
            },
            {
                "module": "TaskGenerator",
                "purpose": "Break the project into implementation tasks across the agentic stages.",
                "owner": "Member 2",
            },
            {
                "module": "TeamAllocator",
                "purpose": "Map modules and video responsibilities to four team members.",
                "owner": "Member 2",
            },
            {
                "module": "PlannerAgent",
                "purpose": "Combine requirements, intent, tasks, and allocation into a structured plan.",
                "owner": "Member 2",
            },
        ]

    def _development_priorities(
        self,
        requirements: Dict[str, Any],
        available_days: int,
    ) -> List[Dict[str, str]]:
        priorities = [
            {
                "priority": "P1",
                "focus": "End-to-end runnable demo",
                "reason": "The assignment assesses working implementation and clear demonstration.",
            },
            {
                "priority": "P2",
                "focus": "Coverage of Perceive, Reason, Action, and Learn",
                "reason": "The four-stage agentic loop is a core deliverable.",
            },
            {
                "priority": "P3",
                "focus": "Responsible AI, human oversight, logging, and evaluation",
                "reason": "Responsible Agentic AI is worth 25% and supports bonus evidence.",
            },
        ]

        if available_days <= 7:
            priorities.append({
                "priority": "P4",
                "focus": "Keep bonus features lightweight",
                "reason": "Prioritise credible evidence over broad unfinished scope.",
            })

        if requirements.get("bonus_features"):
            priorities.append({
                "priority": "P5",
                "focus": "Use observability and evaluation as practical bonus features",
                "reason": "They can be demonstrated through logs, test cases, and reports.",
            })

        return priorities

    def _human_interaction_plan(self, requirements: Dict[str, Any]) -> List[str]:
        if not requirements.get("human_interaction_required", True):
            return ["Human review is optional for this brief."]

        return [
            "Ask the team to confirm generated plans before writing final outputs.",
            "Show user feedback changing plan scope during the Learn demo.",
            "Keep peer contribution summaries factual and reviewed by all members.",
        ]

    def _responsible_ai_notes(self, requirements: Dict[str, Any]) -> List[str]:
        if not requirements.get("responsible_ai_required", True):
            return ["Responsible AI is not explicit in the brief, but basic honesty checks remain useful."]

        return [
            "Do not fabricate contributions, test results, or assignment compliance.",
            "Declare AI tool usage in the final video slide.",
            "Route unsafe or academically dishonest requests to the Safety Agent.",
            "Use logs and evaluation cases as evidence instead of unsupported claims.",
        ]

    def _bonus_feature_strategy(self, requirements: Dict[str, Any]) -> List[str]:
        extracted_bonus = requirements.get("bonus_features") or BONUS_FEATURES
        selected = [
            feature
            for feature in extracted_bonus
            if feature in ["Agent Observability", "Agent Evaluation", "Prompt Injection Filtering", "PII Masking"]
        ]

        if selected:
            return selected

        return ["Agent Observability", "Agent Evaluation"]

    def _video_sections(self, requirements: Dict[str, Any]) -> List[str]:
        sections = requirements.get("required_video_sections") or REQUIRED_VIDEO_SECTIONS
        stages = requirements.get("required_agentic_stages") or REQUIRED_AGENTIC_LOOP

        merged = list(dict.fromkeys(sections + stages))
        return merged
