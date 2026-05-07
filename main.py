import argparse
import json
from pathlib import Path

from agents.context_agent import ContextAgent
from config import ASSIGNMENT_BRIEF_PATH, ensure_project_directories
from agents.intent_router import IntentRouter
from agents.planner_agent import PlannerAgent
from agents.action_agent import ActionAgent
from agents.perception_agent import PerceptionAgent
from tools.document_reader import DocumentReaderTool
from tools.requirement_extractor import RequirementExtractorTool


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


# Member 3 standalone mock data for Action stage testing.
DEFAULT_PLANNER_OUTPUT = {
    "coding_tasks": [
        {
            "day": "Day 1",
            "task": "Complete system architecture design and Perception Agent"
        },
        {
            "day": "Day 2",
            "task": "Implement Intent Router and Planner Agent (Reasoning Stage)"
        },
        {
            "day": "Day 3",
            "task": "Develop toolchain and Action Agent (Tool-calling)"
        },
        {
            "day": "Day 4",
            "task": "Integrate Safety and Feedback modules (Learn & Responsible AI)"
        },
        {
            "day": "Day 5",
            "task": "System integration and test case execution"
        },
        {
            "day": "Day 6",
            "task": "Record the 12-minute final demo video"
        }
    ],
    "video_sections_to_cover": [
        "Video duration is strictly within 12 minutes",
        "Overview stage and assignment motivation are clearly demonstrated",
        "Four core cycles (Perceive, Reason, Action, Learn) are covered",
        "Responsible Agentic AI guardrails are explicitly declared",
        "Data visualization and Agent Observability are showcased via Timeline and Logs",
        "All source code is compressed and ready for submission"
    ],
    "team_allocation": {
        "Member 1": [
            "Perception Agent",
            "main.py architecture",
            "Document Extraction Tool"
        ],
        "Member 2": [
            "Intent Router",
            "Planner Agent",
            "Task Breakdown Logic"
        ],
        "Member 3": [
            "Action Agent",
            "Tool-calling execution",
            "MD/CSV Generation & Logging"
        ],
        "Member 4": [
            "Feedback Agent",
            "Safety Guardrails",
            "Compliance Checking"
        ]
    },
    "development_priorities": [
        {
            "priority": "P1",
            "focus": "End-to-end runnable demo",
            "reason": "The assignment assesses working implementation."
        },
        {
            "priority": "P2",
            "focus": "Responsible AI guardrails",
            "reason": "Worth 25% of grade and supports bonus evidence."
        }
    ]
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="AssignmentPilot Perception + Context + Reason + Action Demo"
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
        "--action_only",
        action="store_true",
        help="Run only Member 3 Action stage with mock planner output."
    )

    parser.add_argument(
        "--reason_only",
        action="store_true",
        help="Run only Member 2 Reason stage without calling Perception or Context."
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


def run_context_demo(
    requirements: dict,
    group_size_override: int | None = None,
    available_days_override: int | None = None,
):
    ensure_project_directories()

    context_agent = ContextAgent()

    context_response = context_agent.run({
        "requirements": requirements,
        "group_size_override": group_size_override,
        "available_days_override": available_days_override,
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

    return {
        "context_response": context_response,
        "group_size": resolved_group_size,
        "available_days": resolved_available_days,
    }


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


def run_action_demo(planner_output: dict | None = None):
    """
    Run Member 3 ActionAgent.

    If planner_output is None, use DEFAULT_PLANNER_OUTPUT for standalone testing.
    Otherwise, use the real PlannerAgent output from the Reason stage.
    """
    ensure_project_directories()

    if planner_output is None:
        data_to_process = DEFAULT_PLANNER_OUTPUT
    else:
        data_to_process = planner_output

    action_agent = ActionAgent()
    response = action_agent.run_actions(data_to_process)

    print("\n" + "=" * 60)
    print("AssignmentPilot - Action / Tool-calling Demo")
    print("=" * 60)

    if hasattr(response, "data"):
        results = response.data
        status_msg = response.message
    else:
        results = response
        status_msg = response.get("status")

    print(f"\nFinal Execution Status: {status_msg}")
    print("\nArtifacts Successfully Generated (Saved to ./outputs/):")
    print("-" * 60)

    generated_files = results.get("generated_files", {})

    for key, path in generated_files.items():
        filename = Path(path).name
        print(f"  {key:<25} ->  ./outputs/{filename}")

    print("-" * 60 + "\n")

    return response


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

    # Action-only mode uses mock planner output and does not call Perception or Reason.
    if args.action_only:
        run_action_demo()

    # Reason-only mode does not have Perception requirements.
    # Therefore ContextAgent is not used here.
    elif args.reason_only:
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

    # Full mode: Perception -> Context -> Reason -> Action.
    else:
        perception_response = run_perception_demo(
            brief_path=custom_brief_path,
            user_input=perception_user_input,
        )

        if perception_response.success:
            requirements = perception_response.data.get("requirements", {})

            context_results = run_context_demo(
                requirements=requirements,
                group_size_override=args.group_size,
                available_days_override=args.available_days,
            )

            reasoning_results = run_reasoning_demo(
                user_input=reason_user_input,
                requirements=requirements,
                group_size=context_results["group_size"],
                available_days=context_results["available_days"],
                selected_topic=args.topic,
            )

            plan_data = reasoning_results["plan_response"].data

            run_action_demo(planner_output=plan_data)