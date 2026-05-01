from pathlib import Path
from dataclasses import asdict

from schemas import AgentResponse
from tools.document_reader import DocumentReaderTool
from tools.requirement_extractor import RequirementExtractorTool


class PerceptionAgent:
    def __init__(
        self,
        document_reader: DocumentReaderTool,
        requirement_extractor: RequirementExtractorTool
    ):
        self.document_reader = document_reader
        self.requirement_extractor = requirement_extractor

    def run(self, input_data: dict) -> AgentResponse:
        logs = []

        try:
            brief_path = Path(input_data["brief_path"])
            user_input = input_data.get("user_input", "")

            logs.append({
                "step": "perceive_1",
                "action": "load_assignment_brief",
                "status": "started"
            })

            raw_text = self.document_reader.read(brief_path)

            logs.append({
                "step": "perceive_1",
                "action": "load_assignment_brief",
                "status": "success",
                "output_summary": f"Loaded {len(raw_text)} characters."
            })

            logs.append({
                "step": "perceive_2",
                "action": "extract_requirements",
                "status": "started"
            })

            requirements = self.requirement_extractor.extract(raw_text)

            logs.append({
                "step": "perceive_2",
                "action": "extract_requirements",
                "status": "success",
                "output_summary": "Assignment requirements extracted."
            })

            return AgentResponse(
                success=True,
                module_name="PerceptionAgent",
                data={
                    "user_input": user_input,
                    "raw_text_length": len(raw_text),
                    "requirements": asdict(requirements)
                },
                message="Perception completed successfully.",
                warnings=[],
                errors=[],
                logs=logs
            )

        except Exception as error:
            logs.append({
                "step": "perceive_error",
                "action": "handle_exception",
                "status": "failed",
                "error": str(error)
            })

            return AgentResponse(
                success=False,
                module_name="PerceptionAgent",
                data={},
                message="Perception failed.",
                warnings=[],
                errors=[str(error)],
                logs=logs
            )