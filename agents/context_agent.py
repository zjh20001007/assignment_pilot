import json
import re
from datetime import date

from openai import OpenAI

from schemas import AgentResponse
from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)


class ContextAgent:
    def __init__(self):
        if not DEEPSEEK_API_KEY:
            raise ValueError(
                "DEEPSEEK_API_KEY is missing. Please set it in your .env file."
            )

        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )

    def run(self, input_data: dict) -> AgentResponse:
        logs = []

        try:
            requirements = input_data.get("requirements", {})

            group_size_override = input_data.get("group_size_override")
            available_days_override = input_data.get("available_days_override")

            default_group_size = input_data.get("default_group_size", 4)
            default_available_days = input_data.get("default_available_days", 7)

            logs.append({
                "step": "context_1",
                "action": "resolve_group_size",
                "status": "started"
            })

            group_context = self._resolve_group_size(
                requirements=requirements,
                group_size_override=group_size_override,
                default_group_size=default_group_size,
            )

            logs.append({
                "step": "context_1",
                "action": "resolve_group_size",
                "status": "success",
                "output_summary": (
                    f"Resolved group_size as {group_context['group_size']} "
                    f"from {group_context['group_size_source']}."
                )
            })

            logs.append({
                "step": "context_2",
                "action": "resolve_available_days",
                "status": "started"
            })

            available_days_context = self._resolve_available_days(
                requirements=requirements,
                available_days_override=available_days_override,
                default_available_days=default_available_days,
            )

            logs.append({
                "step": "context_2",
                "action": "resolve_available_days",
                "status": "success",
                "output_summary": (
                    f"Resolved available_days as "
                    f"{available_days_context['available_days']} "
                    f"from {available_days_context['available_days_source']}."
                )
            })

            context_data = {
                **group_context,
                **available_days_context,
            }

            return AgentResponse(
                success=True,
                module_name="ContextAgent",
                data=context_data,
                message="Context resolved successfully.",
                warnings=[],
                errors=[],
                logs=logs
            )

        except Exception as error:
            logs.append({
                "step": "context_error",
                "action": "handle_exception",
                "status": "failed",
                "error": str(error)
            })

            return AgentResponse(
                success=False,
                module_name="ContextAgent",
                data={},
                message="Context resolution failed.",
                warnings=[],
                errors=[str(error)],
                logs=logs
            )

    def _resolve_group_size(
        self,
        requirements: dict,
        group_size_override: int | None,
        default_group_size: int,
    ) -> dict:
        if group_size_override is not None:
            return {
                "group_size": int(group_size_override),
                "group_size_source": "user_override",
                "group_requirement_found": "",
                "group_size_reason": "The user manually provided group_size."
            }

        inferred_group_size, group_requirement_found = (
            self._infer_group_size_from_requirements(requirements)
        )

        if inferred_group_size is not None:
            return {
                "group_size": inferred_group_size,
                "group_size_source": "requirements_inferred",
                "group_requirement_found": group_requirement_found,
                "group_size_reason": (
                    "The group size was inferred from extracted assignment requirements."
                )
            }

        return {
            "group_size": default_group_size,
            "group_size_source": "default_fallback",
            "group_requirement_found": group_requirement_found,
            "group_size_reason": (
                "No reliable group size was found. Used default value."
            )
        }

    def _infer_group_size_from_requirements(
        self,
        requirements: dict,
    ) -> tuple[int | None, str]:
        if not requirements:
            return None, ""

        direct_group_size = requirements.get("group_size")
        if isinstance(direct_group_size, int) and direct_group_size > 0:
            return direct_group_size, "requirements.group_size"

        submission_requirements = requirements.get("submission_requirements", {})
        if not isinstance(submission_requirements, dict):
            return None, ""

        group_text = str(
            submission_requirements.get("group_requirements", "")
        ).strip()

        if not group_text:
            return None, ""

        group_text_lower = group_text.lower()

        # Individual work
        if "individual" in group_text_lower and not re.search(r"\d", group_text_lower):
            return 1, group_text

        # Exact patterns: "Group of 5", "team of 5", "5 members"
        exact_patterns = [
            r"group\s+of\s+(\d+)",
            r"team\s+of\s+(\d+)",
            r"(\d+)\s+members?",
            r"(\d+)\s+students?",
            r"(\d+)\s+people",
        ]

        for pattern in exact_patterns:
            match = re.search(pattern, group_text_lower)
            if match:
                return int(match.group(1)), group_text

        # Range patterns: "4-6", "4 to 6", "4–6"
        range_patterns = [
            r"(\d+)\s*[-–]\s*(\d+)",
            r"(\d+)\s+to\s+(\d+)",
        ]

        for pattern in range_patterns:
            match = re.search(pattern, group_text_lower)
            if match:
                min_size = int(match.group(1))

                # No actual team roster is known, so choose the minimum valid size.
                return min_size, group_text

        return None, group_text

    def _resolve_available_days(
        self,
        requirements: dict,
        available_days_override: int | None,
        default_available_days: int,
    ) -> dict:
        if available_days_override is not None:
            return {
                "available_days": int(available_days_override),
                "available_days_source": "user_override",
                "deadline_found": "",
                "available_days_reason": (
                    "The user manually provided available_days."
                )
            }

        inferred_context = self._infer_available_days_with_deepseek(requirements)

        if inferred_context.get("available_days") is not None:
            return {
                "available_days": int(inferred_context["available_days"]),
                "available_days_source": "deepseek_inferred",
                "deadline_found": inferred_context.get("deadline_found", ""),
                "available_days_reason": inferred_context.get("reason", "")
            }

        return {
            "available_days": default_available_days,
            "available_days_source": "default_fallback",
            "deadline_found": inferred_context.get("deadline_found", ""),
            "available_days_reason": inferred_context.get(
                "reason",
                "DeepSeek could not infer a reliable available_days value."
            )
        }

    def _infer_available_days_with_deepseek(self, requirements: dict) -> dict:
        today = date.today().isoformat()

        system_prompt = """
You are a strict date calculation assistant.

Your task is to infer available_days from assignment requirements.

Rules:
1. Use the provided today's date.
2. Find the assignment submission deadline from the requirements.
3. Calculate available_days as: deadline_date - today_date.
4. Do not add one extra day.
5. If today is 2026-05-07 and the deadline is 2026-05-22, available_days must be 15.
6. If the deadline is missing, unclear, or already passed, return null.
7. Return JSON only.

Return format:
{
  "available_days": 15,
  "deadline_found": "2026-05-22",
  "reason": "short explanation"
}
"""

        user_prompt = f"""
Today's date:
{today}

Extracted assignment requirements:
{json.dumps(requirements, ensure_ascii=False, indent=2)}

Please infer available_days.
"""

        response = self.client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        available_days = data.get("available_days")

        if isinstance(available_days, int) and available_days > 0:
            return {
                "available_days": available_days,
                "deadline_found": data.get("deadline_found", ""),
                "reason": data.get("reason", "")
            }

        return {
            "available_days": None,
            "deadline_found": data.get("deadline_found", ""),
            "reason": data.get("reason", "No reliable deadline was found.")
        }