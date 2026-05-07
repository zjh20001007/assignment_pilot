import argparse
import json
from pathlib import Path

from config import ASSIGNMENT_BRIEF_PATH, ensure_project_directories
from agents.intent_router import IntentRouter
from agents.planner_agent import PlannerAgent
from tools.document_reader import DocumentReaderTool


DEFAULT_REASONING_REQUIREMENTS = {
    "project_goal": "Design and demonstrate an Agentic AI application for a realistic multi-step reasoning scenario.",
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


def parse_args():
    parser = argparse.ArgumentParser(
        description="AssignmentPilot Perception Agent Demo"
    )

    parser.add_argument(
        "--brief",
        type=str,
        default=str(ASSIGNMENT_BRIEF_PATH),
        help="Path to the assignment brief text file."
    )

    parser.add_argument(
        "--user_input",
        type=str,
        default="We are a four-member team. Help us plan the coding part of AssignmentPilot.",
        help="User request for the agent."
    )

    parser.add_argument(
        "--reason_only",
        action="store_true",
        help="Run only Member 2 Reason stage without calling the LLM-based Perception stage."
    )

    parser.add_argument(
        "--group_size",
        type=int,
        default=4,
        help="Number of team members."
    )

    parser.add_argument(
        "--available_days",
        type=int,
        default=7,
        help="Estimated available development days."
    )

    parser.add_argument(
        "--topic",
        type=str,
        default="AssignmentPilot",
        help="Selected project topic."
    )

    return parser.parse_args()


def run_perception_demo(brief_path: Path, user_input: str):
    ensure_project_directories()

    from agents.perception_agent import PerceptionAgent
    from tools.requirement_extractor import RequirementExtractorTool

    document_reader = DocumentReaderTool()
    requirement_extractor = RequirementExtractorTool()

    perception_agent = PerceptionAgent(
        document_reader=document_reader,
        requirement_extractor=requirement_extractor
    )

    response = perception_agent.run({
        "brief_path": brief_path,
        "user_input": user_input
    })

    print("=" * 60)
    print("AssignmentPilot - Perception Agent Demo")
    print("=" * 60)

    print("\nInput Brief File:")
    print(brief_path)

    print("\nSuccess:")
    print(response.success)

    print("\nMessage:")
    print(response.message)

    if response.errors:
        print("\nErrors:")
        for error in response.errors:
            print(f"- {error}")

    print("\nExtracted Data:")
    print(json.dumps(response.data, indent=2, ensure_ascii=False))

    print("\nLogs:")
    print(json.dumps(response.logs, indent=2, ensure_ascii=False))

    return response


def run_reasoning_demo(
    user_input: str,
    requirements: dict | None = None,
    group_size: int = 4,
    available_days: int = 7,
    selected_topic: str = "AssignmentPilot",
    print_output: bool = True,
) -> dict:
    ensure_project_directories()

    intent_router = IntentRouter()
    planner_agent = PlannerAgent()

    intent_response = intent_router.run({
        "user_input": user_input
    })

    plan_response = planner_agent.run({
        "requirements": requirements or DEFAULT_REASONING_REQUIREMENTS,
        "intent": intent_response.data.get("intent", "project_design"),
        "user_context": {
            "group_size": group_size,
            "available_days": available_days,
            "selected_topic": selected_topic,
        }
    })

    if print_output:
        print("=" * 60)
        print("AssignmentPilot - Reasoning / Planning Demo")
        print("=" * 60)

        print("\nUser Input:")
        print(user_input)

        print("\nIntent Router Result:")
        print(json.dumps(intent_response.data, indent=2, ensure_ascii=False))

        print("\nPlanner Agent Result:")
        print(json.dumps(plan_response.data, indent=2, ensure_ascii=False))

        print("\nReasoning Logs:")
        print(json.dumps(intent_response.logs + plan_response.logs, indent=2, ensure_ascii=False))

    return {
        "intent_response": intent_response,
        "plan_response": plan_response,
    }


if __name__ == "__main__":
    args = parse_args()

    custom_brief_path = Path(args.brief)

    if args.reason_only:
        run_reasoning_demo(
            user_input=args.user_input,
            group_size=args.group_size,
            available_days=args.available_days,
            selected_topic=args.topic,
        )
    else:
        perception_response = run_perception_demo(
            brief_path=custom_brief_path,
            user_input=args.user_input
        )

        if perception_response.success:
            run_reasoning_demo(
                user_input=args.user_input,
                requirements=perception_response.data.get("requirements", {}),
                group_size=args.group_size,
                available_days=args.available_days,
                selected_topic=args.topic,
            )
