import unittest

from agents.intent_router import IntentRouter
from agents.planner_agent import PlannerAgent
from schemas import AgentResponse
from tools.task_generator import TaskGenerator
from tools.team_allocator import TeamAllocator


class IntentRouterTests(unittest.TestCase):
    def test_classifies_coding_plan_from_mixed_language_input(self):
        router = IntentRouter()

        intent = router.classify("帮我考虑 coding 的部分，给一个代码实现计划")

        self.assertEqual(intent, "coding_plan")

    def test_revision_has_priority_over_general_project_design(self):
        router = IntentRouter()

        intent = router.classify("这个 project plan 太复杂了，可以帮我简化吗")

        self.assertEqual(intent, "revision")

    def test_run_returns_agent_response(self):
        router = IntentRouter()

        response = router.run({"user_input": "请帮我们做四个人分工"})

        self.assertIsInstance(response, AgentResponse)
        self.assertTrue(response.success)
        self.assertEqual(response.data["intent"], "task_allocation")


class TaskGeneratorTests(unittest.TestCase):
    def test_generates_reasoning_tasks_with_owners_and_outputs(self):
        generator = TaskGenerator()

        tasks = generator.generate("AssignmentPilot", "coding_plan")

        self.assertGreaterEqual(len(tasks), 6)
        self.assertEqual(tasks[0]["stage"], "Perceive")
        self.assertIn("owner", tasks[0])
        self.assertIn("output", tasks[0])


class TeamAllocatorTests(unittest.TestCase):
    def test_allocates_four_members_to_agentic_stages(self):
        allocator = TeamAllocator()

        allocation = allocator.allocate(group_size=4, project_topic="AssignmentPilot")

        self.assertEqual(len(allocation), 4)
        self.assertIn("Intent Router", allocation["Member 2"]["modules"])
        self.assertEqual(allocation["Member 2"]["agentic_stage"], "Reason")


class PlannerAgentTests(unittest.TestCase):
    def test_generates_structured_plan_from_requirements_and_intent(self):
        requirements = {
            "project_goal": "Design and demonstrate an Agentic AI application.",
            "required_agentic_stages": ["Perceive", "Reason", "Action", "Learn"],
            "required_video_sections": [
                "Overview",
                "Perceive",
                "Reason",
                "Action",
                "Learn",
                "AI-Human Interaction",
                "Responsible Agentic AI",
                "Conclusions",
            ],
            "grading_criteria": {
                "Technical Competency": 25,
                "Correctness & Clarity": 25,
                "Responsible Agentic AI": 25,
                "Novelty and Originality": 10,
                "Bonus Features": 15,
            },
            "bonus_features": ["Agent Observability", "Agent Evaluation"],
            "human_interaction_required": True,
            "responsible_ai_required": True,
        }
        planner = PlannerAgent()

        response = planner.run(
            {
                "requirements": requirements,
                "intent": "coding_plan",
                "user_context": {
                    "group_size": 4,
                    "selected_topic": "AssignmentPilot",
                    "available_days": 7,
                },
            }
        )

        self.assertTrue(response.success)
        self.assertEqual(response.module_name, "PlannerAgent")
        self.assertEqual(response.data["intent"], "coding_plan")
        self.assertIn("reasoning_design", response.data)
        self.assertIn("team_allocation", response.data)
        self.assertIn("development_priorities", response.data)
        self.assertEqual(
            response.data["team_allocation"]["Member 2"]["agentic_stage"],
            "Reason",
        )


class MainReasoningDemoTests(unittest.TestCase):
    def test_reason_only_demo_returns_intent_and_plan_without_llm_dependency(self):
        from main import run_reasoning_demo

        result = run_reasoning_demo(
            user_input="帮我考虑 coding 的部分",
            requirements={
                "project_goal": "Design and demonstrate an Agentic AI application.",
                "required_agentic_stages": ["Perceive", "Reason", "Action", "Learn"],
                "required_video_sections": ["Overview", "Reason", "Action", "Learn"],
                "human_interaction_required": True,
                "responsible_ai_required": True,
            },
            group_size=4,
            available_days=7,
            selected_topic="AssignmentPilot",
            print_output=False,
        )

        self.assertEqual(result["intent_response"].data["intent"], "coding_plan")
        self.assertTrue(result["plan_response"].success)
        self.assertEqual(result["plan_response"].data["team_allocation"]["Member 2"]["agentic_stage"], "Reason")


if __name__ == "__main__":
    unittest.main()
