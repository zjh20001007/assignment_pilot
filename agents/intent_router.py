from typing import Dict, List

from constants import INTENT_TYPES
from schemas import AgentResponse


class IntentRouter:
    def __init__(self):
        self.intent_keywords: Dict[str, List[str]] = {
            "revision": [
                "简化",
                "修改",
                "调整",
                "太复杂",
                "改进",
                "revise",
                "revision",
                "simplify",
                "too complex",
                "change",
                "improve",
            ],
            "coding_plan": [
                "coding",
                "code",
                "代码",
                "实现",
                "开发",
                "模块",
                "program",
                "implementation",
                "build",
            ],
            "task_allocation": [
                "分工",
                "成员",
                "四个人",
                "组员",
                "负责",
                "allocate",
                "allocation",
                "team",
                "member",
                "responsibility",
                "responsibilities",
            ],
            "compliance_check": [
                "检查",
                "满足要求",
                "合规",
                "评分",
                "rubric",
                "compliance",
                "check",
                "requirement",
                "criteria",
            ],
            "video_script": [
                "视频",
                "讲稿",
                "演示",
                "presentation",
                "video",
                "script",
                "demo",
                "slide",
            ],
            "risk_review": [
                "风险",
                "问题",
                "安全",
                "guardrail",
                "risk",
                "safety",
                "responsible",
                "weakness",
            ],
            "topic_generation": [
                "题目",
                "选题",
                "主题",
                "topic",
                "idea",
                "brainstorm",
            ],
            "project_design": [
                "架构",
                "设计",
                "workflow",
                "architecture",
                "design",
                "project",
                "plan",
            ],
        }

    def classify(self, user_input: str) -> str:
        text = (user_input or "").strip().lower()

        if not text:
            return "unknown"

        for intent, keywords in self.intent_keywords.items():
            if any(keyword.lower() in text for keyword in keywords):
                return intent

        return "project_design"

    def run(self, input_data: dict) -> AgentResponse:
        logs = []

        try:
            user_input = input_data.get("user_input", "")

            logs.append({
                "step": "reason_1",
                "agent": "IntentRouter",
                "action": "classify_user_intent",
                "status": "started",
            })

            intent = self.classify(user_input)

            logs.append({
                "step": "reason_1",
                "agent": "IntentRouter",
                "action": "classify_user_intent",
                "status": "success",
                "output_summary": f"Intent classified as {intent}.",
            })

            warnings = []
            if intent not in INTENT_TYPES:
                warnings.append(f"Intent '{intent}' is not listed in constants.INTENT_TYPES.")

            return AgentResponse(
                success=True,
                module_name="IntentRouter",
                data={
                    "user_input": user_input,
                    "intent": intent,
                    "available_intents": INTENT_TYPES,
                },
                message="Intent classification completed successfully.",
                warnings=warnings,
                errors=[],
                logs=logs,
            )

        except Exception as error:
            logs.append({
                "step": "reason_error",
                "agent": "IntentRouter",
                "action": "handle_exception",
                "status": "failed",
                "error": str(error),
            })

            return AgentResponse(
                success=False,
                module_name="IntentRouter",
                data={},
                message="Intent classification failed.",
                warnings=[],
                errors=[str(error)],
                logs=logs,
            )
