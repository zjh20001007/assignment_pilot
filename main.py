import argparse
import json
from pathlib import Path

from config import ASSIGNMENT_BRIEF_PATH, ensure_project_directories
from agents.perception_agent import PerceptionAgent
from tools.document_reader import DocumentReaderTool
from tools.requirement_extractor import RequirementExtractorTool


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

    return parser.parse_args()


def run_perception_demo(brief_path: Path, user_input: str) -> None:
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


if __name__ == "__main__":
    args = parse_args()

    custom_brief_path = Path(args.brief)

    run_perception_demo(
        brief_path=custom_brief_path,
        user_input=args.user_input
    )