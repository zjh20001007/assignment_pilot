import json
from typing import Dict, Any, List

from openai import OpenAI

from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    MAX_BRIEF_CHARS,
)
from schemas import AssignmentRequirement


class RequirementExtractorTool:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            raise ValueError(
                "DEEPSEEK_API_KEY is missing. Please add it to your .env file."
            )

        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )

        self.model = DEEPSEEK_MODEL

    def extract(self, raw_text: str) -> AssignmentRequirement:
        trimmed_text = raw_text[:MAX_BRIEF_CHARS]

        extracted_json = self._extract_with_llm(trimmed_text)

        # Add a deterministic post-processing step.
        # This helps fix cases where the LLM misses obvious Responsible AI signals.
        extracted_json = self._post_process_extracted_json(
            extracted_json,
            trimmed_text
        )

        requirement = self._convert_json_to_requirement(extracted_json)

        return requirement

    def _extract_with_llm(self, raw_text: str) -> Dict[str, Any]:
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(raw_text)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0.1,
            max_tokens=4000,
        )

        content = response.choices[0].message.content

        if not content or not content.strip():
            raise ValueError("DeepSeek returned empty content.")

        try:
            return json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError(f"Failed to parse DeepSeek JSON output: {error}")

    def _build_system_prompt(self) -> str:

        return """
You are an information extraction assistant for university assignment briefs.

Your task is to extract assignment requirements from the user's document.

You must output only valid JSON.
Do not output markdown.
Do not add explanations outside the JSON object.

The JSON object must follow this exact schema:

{
  "project_goal": "string",
  "course_name": "string",
  "video_limit_minutes": 0,
  "required_video_sections": ["string"],
  "required_agentic_stages": ["string"],
  "submission_requirements": {
    "deliverables": ["string"],
    "format": ["string"],
    "submission_platform": "string",
    "group_requirements": "string",
    "special_requirements": ["string"]
  },
  "grading_criteria": {
    "criterion_name": 0
  },
  "deadlines": {
    "assignment_submission": "string",
    "peer_evaluation": "string"
  },
  "bonus_features": ["string"],
  "human_interaction_required": false,
  "responsible_ai_required": false,
  "originality_requirements": ["string"],
  "peer_evaluation_requirements": ["string"]
}

Extraction rules:

1. Extract information only from the provided document.
2. Do not invent course names, deadlines, grading criteria, or submission requirements.
3. If a field is not explicitly mentioned, use an empty string, empty list, empty object, 0, or false.
4. The grading_criteria field must use the actual criterion names and percentages from the document.
5. Do not reuse any example grading criteria unless they appear in the document.
6. If the document mentions slides, reports, code, notebooks, videos, or presentations, extract them into submission_requirements.deliverables.
7. If the document mentions slide count, page count, video length, file type, or format, extract them into submission_requirements.format.
8. If the document mentions NTUlearn, Blackboard, Canvas, Moodle, GitHub, YouTube, or another platform, extract it into submission_requirements.submission_platform.
9. If the document mentions whether the assignment is individual or group-based, extract it into submission_requirements.group_requirements.
10. If the document mentions special requirements such as title slides, content slides, member appearance, voice, captions, originality, or AI usage declarations, extract them into submission_requirements.special_requirements.
11. If the assignment requires a video and gives a time limit, extract the number into video_limit_minutes.
12. If no video time limit is mentioned, set video_limit_minutes to 0.
13. If the assignment is about Agentic AI workflow, agents, Perceive, Reason, Action, Learn, or multi-agent systems, extract the relevant stages into required_agentic_stages.
14. If the assignment requires video sections such as Overview, Perceive, Reason, Action, Learn, Human Interaction, Responsible AI, or Conclusions, extract them into required_video_sections.
15. If the assignment topic involves ethics, risk mitigation, governance, compliance, safety, fairness, privacy, accountability, responsible AI, or harmful AI incidents, set responsible_ai_required to true.
16. If the assignment explicitly requires human review, human approval, human supervision, peer evaluation, or human-in-the-loop design, set human_interaction_required to true.
17. If the document mentions peer evaluation, extract the details into peer_evaluation_requirements and deadlines.peer_evaluation if a deadline is provided.
18. Preserve important dates, time limits, submission formats, slide counts, grading weights, and group size requirements.
19. Keep the output concise but complete.
20. The output must be valid JSON.
"""

    def _build_user_prompt(self, raw_text: str) -> str:
        return f"""
Please extract the assignment requirements from the following document.

Remember:
- Output only valid JSON.
- Do not output markdown.
- Do not add explanations outside the JSON object.
- Use the exact schema required by the system message.

DOCUMENT:
{raw_text}
"""

    def _post_process_extracted_json(
        self,
        data: Dict[str, Any],
        raw_text: str
    ) -> Dict[str, Any]:
        text_lower = raw_text.lower()

        responsible_ai_keywords = [
            "ethical",
            "ethics",
            "risk mitigation",
            "risk management",
            "governance",
            "compliance",
            "responsible ai",
            "safety",
            "fairness",
            "privacy",
            "accountability",
            "harm",
            "incident",
        ]

        if any(keyword in text_lower for keyword in responsible_ai_keywords):
            data["responsible_ai_required"] = True

        human_interaction_keywords = [
            "human-in-the-loop",
            "human supervision",
            "human approval",
            "peer evaluation",
            "all members",
            "team members",
        ]

        if any(keyword in text_lower for keyword in human_interaction_keywords):
            data["human_interaction_required"] = True

        # Make sure submission_requirements exists and has stable keys.
        submission_requirements = data.get("submission_requirements")

        if not isinstance(submission_requirements, dict):
            submission_requirements = {}

        submission_requirements.setdefault("deliverables", [])
        submission_requirements.setdefault("format", [])
        submission_requirements.setdefault("submission_platform", "")
        submission_requirements.setdefault("group_requirements", "")
        submission_requirements.setdefault("special_requirements", [])

        data["submission_requirements"] = submission_requirements

        return data

    def _convert_json_to_requirement(self, data: Dict[str, Any]) -> AssignmentRequirement:
        return AssignmentRequirement(
            project_goal=self._safe_str(data.get("project_goal")),
            course_name=self._safe_str(data.get("course_name")),
            video_limit_minutes=self._safe_int(
                data.get("video_limit_minutes"),
                default=0
            ),

            required_video_sections=self._safe_list(
                data.get("required_video_sections")
            ),
            required_agentic_stages=self._safe_list(
                data.get("required_agentic_stages")
            ),

            submission_requirements=self._safe_dict(
                data.get("submission_requirements")
            ),
            grading_criteria=self._safe_dict(
                data.get("grading_criteria")
            ),
            deadlines=self._safe_dict(
                data.get("deadlines")
            ),

            bonus_features=self._safe_list(
                data.get("bonus_features")
            ),

            human_interaction_required=self._safe_bool(
                data.get("human_interaction_required")
            ),
            responsible_ai_required=self._safe_bool(
                data.get("responsible_ai_required")
            ),

            originality_requirements=self._safe_list(
                data.get("originality_requirements")
            ),
            peer_evaluation_requirements=self._safe_list(
                data.get("peer_evaluation_requirements")
            ),
        )

    def _safe_str(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value)

    def _safe_int(self, value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _safe_bool(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.lower() in ["true", "yes", "1"]

        if isinstance(value, int):
            return value != 0

        return False

    def _safe_list(self, value: Any) -> List[str]:
        if value is None:
            return []

        if isinstance(value, list):
            return [str(item) for item in value]

        return [str(value)]

    def _safe_dict(self, value: Any) -> Dict[str, Any]:
        if isinstance(value, dict):
            return value

        return {}