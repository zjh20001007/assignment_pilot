from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AssignmentRequirement:
    project_goal: str = ""
    course_name: str = ""
    video_limit_minutes: int = 12

    required_video_sections: List[str] = field(default_factory=list)
    required_agentic_stages: List[str] = field(default_factory=list)

    submission_requirements: Dict[str, str] = field(default_factory=dict)
    grading_criteria: Dict[str, float] = field(default_factory=dict)
    deadlines: Dict[str, str] = field(default_factory=dict)

    bonus_features: List[str] = field(default_factory=list)

    human_interaction_required: bool = True
    responsible_ai_required: bool = True

    originality_requirements: List[str] = field(default_factory=list)
    peer_evaluation_requirements: List[str] = field(default_factory=list)


@dataclass
class UserContext:
    user_input: str = ""
    group_size: int = 4
    available_days: int = 10
    selected_topic: str = "AssignmentPilot"
    preferred_difficulty: str = "medium"

    current_progress: str = ""
    target_bonus_features: List[str] = field(default_factory=list)
    feedback_history: List[str] = field(default_factory=list)


@dataclass
class AgentResponse:
    success: bool
    module_name: str
    data: Dict[str, Any]
    message: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    logs: List[Dict[str, Any]] = field(default_factory=list)