import json
from pathlib import Path
import argparse

from config import ASSIGNMENT_BRIEF_PATH, ensure_project_directories
from agents.intent_router import IntentRouter
from agents.planner_agent import PlannerAgent
from agents.action_agent import ActionAgent
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

# Member 3 Addition: Mock data for standalone Action stage testing
DEFAULT_PLANNER_OUTPUT = {
    "coding_tasks": [
        {"day": "Day 1", "task": "Complete system architecture design and Perception Agent"},
        {"day": "Day 2", "task": "Implement Intent Router and Planner Agent (Reasoning Stage)"},
        {"day": "Day 3", "task": "Develop toolchain and Action Agent (Tool-calling)"},
        {"day": "Day 4", "task": "Integrate Safety and Feedback modules (Learn & Responsible AI)"},
        {"day": "Day 5", "task": "System integration and test case execution"},
        {"day": "Day 6", "task": "Record the 12-minute final demo video"}
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
        "Member 1": ["Perception Agent", "main.py architecture", "Document Extraction Tool"],
        "Member 2": ["Intent Router", "Planner Agent", "Task Breakdown Logic"],
        "Member 3": ["Action Agent", "Tool-calling execution", "MD/CSV Generation & Logging"],
        "Member 4": ["Feedback Agent", "Safety Guardrails", "Compliance Checking"]
    },
    "development_priorities": [
        {"priority": "P1", "focus": "End-to-end runnable demo", "reason": "The assignment assesses working implementation."},
        {"priority": "P2", "focus": "Responsible AI guardrails", "reason": "Worth 25% of grade and supports bonus evidence."}
    ]
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
        "--action_only",
        action="store_true",
        help="Run only Member 3 Action stage (Tool-calling & File generation)."
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

def run_action_demo(planner_output=None):
    """
    Member 3 Demo Runner. Handles the ActionAgent response format.
    """
    from agents.action_agent import ActionAgent

    if planner_output is None:
        data_to_process = DEFAULT_PLANNER_OUTPUT
    else:
        data_to_process = planner_output

    action_agent = ActionAgent()
    response = action_agent.run_actions(data_to_process)

    print("\n" + "="*60)
    print("AssignmentPilot - Action / Tool-calling Demo")
    print("="*60)

    if hasattr(response, 'data'):
        results = response.data
        status_msg = response.message
    else:
        results = response
        status_msg = response.get("status")

    print(f"\nFinal Execution Status: {status_msg}")
    print("\nArtifacts Successfully Generated (Saved to ./outputs/):")
    print("-" * 60)
    
    generated_files = results.get('generated_files', {})
    
    for key, path in generated_files.items():
        filename = Path(path).name 
        print(f"  {key:<25} ->  ./outputs/{filename}")
    
    print("-" * 60 + "\n")


if __name__ == "__main__":
    args = parse_args()

    custom_brief_path = Path(args.brief)

    if args.action_only:
        run_action_demo()
        
    elif args.reason_only:
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
            reasoning_results = run_reasoning_demo(
                user_input=args.user_input,
                requirements=perception_response.data.get("requirements", {}),
                group_size=args.group_size,
                available_days=args.available_days,
                selected_topic=args.topic,
            )
            
            plan_data = reasoning_results["plan_response"].data
            run_action_demo(planner_output=plan_data)