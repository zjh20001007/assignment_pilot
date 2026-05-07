import argparse
import json
from pathlib import Path

from agents.context_agent import ContextAgent
from config import ASSIGNMENT_BRIEF_PATH, ensure_project_directories
from agents.intent_router import IntentRouter
from agents.planner_agent import PlannerAgent
from tools.document_reader import DocumentReaderTool


DEFAULT_PERCEPTION_USER_INPUT = (
    "Please help me to extract the project requirements."
)

DEFAULT_REASON_USER_INPUT = (
    "Please generate a project architecture and design plan for AssignmentPilot."
)

DEFAULT_GROUP_SIZE = 4

DEFAULT_AVAILABLE_DAYS = 7

DEFAULT_TOPIC = "AssignmentPilot"


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
        description="AssignmentPilot Perception + Context + Reason Demo"
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
        default=None,
        help="Optional user request. If not provided, each stage will use its own default user_input."
    )

    parser.add_argument(
        "--reason_only",
        action="store_true",
        help="Run only Member 2 Reason stage without calling the LLM-based Perception stage."
    )

    parser.add_argument(
        "--group_size",
        type=int,
        default=None,
        help="Optional number of team members. If not provided, ContextAgent will infer it from the assignment brief."
    )

    parser.add_argument(
        "--available_days",
        type=int,
        default=None,
        help="Optional estimated available development days. If not provided, ContextAgent will infer it from the assignment deadline."
    )

    parser.add_argument(
        "--topic",
        type=str,
        default=DEFAULT_TOPIC,
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
    group_size: int | None = None,
    available_days: int | None = None,
    selected_topic: str | None = None,
    print_output: bool = True,
) -> dict:
    ensure_project_directories()

    group_size = group_size or DEFAULT_GROUP_SIZE
    available_days = available_days or DEFAULT_AVAILABLE_DAYS
    selected_topic = selected_topic or DEFAULT_TOPIC

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
        print(json.dumps(
            intent_response.logs + plan_response.logs,
            indent=2,
            ensure_ascii=False
        ))

    return {
        "intent_response": intent_response,
        "plan_response": plan_response,
    }


if __name__ == "__main__":
    args = parse_args()

    custom_brief_path = Path(args.brief)

    # Resolve stage-specific user input.
    if args.user_input is not None:
        perception_user_input = args.user_input
        reason_user_input = args.user_input
    else:
        perception_user_input = DEFAULT_PERCEPTION_USER_INPUT
        reason_user_input = DEFAULT_REASON_USER_INPUT

    # Reason-only mode does not have Perception requirements.
    # Therefore ContextAgent is not used here.
    if args.reason_only:
        resolved_group_size = (
            args.group_size
            if args.group_size is not None
            else DEFAULT_GROUP_SIZE
        )

        resolved_available_days = (
            args.available_days
            if args.available_days is not None
            else DEFAULT_AVAILABLE_DAYS
        )

        print(f"the group size is {resolved_group_size}")
        print(f"the resolved_available_days is {resolved_available_days}")

        run_reasoning_demo(
            user_input=reason_user_input,
            group_size=resolved_group_size,
            available_days=resolved_available_days,
            selected_topic=args.topic,
        )

    # Full mode: Perception -> Context -> Reason.
    else:
        perception_response = run_perception_demo(
            brief_path=custom_brief_path,
            user_input=perception_user_input,
        )

        if perception_response.success:
            requirements = perception_response.data.get("requirements", {})

            # ContextAgent resolves group_size and available_days.
            context_agent = ContextAgent()

            context_response = context_agent.run({
                "requirements": requirements,
                "group_size_override": args.group_size,
                "available_days_override": args.available_days,
                "default_group_size": DEFAULT_GROUP_SIZE,
                "default_available_days": DEFAULT_AVAILABLE_DAYS,
            })

            if context_response.success:
                resolved_group_size = context_response.data.get(
                    "group_size",
                    DEFAULT_GROUP_SIZE
                )

                resolved_available_days = context_response.data.get(
                    "available_days",
                    DEFAULT_AVAILABLE_DAYS
                )
            else:
                resolved_group_size = DEFAULT_GROUP_SIZE
                resolved_available_days = DEFAULT_AVAILABLE_DAYS

            print(f"the group size is {resolved_group_size}")
            print(f"the resolved_available_days is {resolved_available_days}")

            print("\nContext Agent Result:")
            print(json.dumps(
                context_response.data,
                indent=2,
                ensure_ascii=False
            ))

            print("\nContext Logs:")
            print(json.dumps(
                context_response.logs,
                indent=2,
                ensure_ascii=False
            ))

            run_reasoning_demo(
                user_input=reason_user_input,
                requirements=requirements,
                group_size=resolved_group_size,
                available_days=resolved_available_days,
                selected_topic=args.topic,
            )