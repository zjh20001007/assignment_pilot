import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv() -> None:
        return None


# Load environment variables from .env file.
load_dotenv()


# Project root directory.
PROJECT_ROOT = Path(__file__).resolve().parent

# Main folders.
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
LOG_DIR = PROJECT_ROOT / "logs"

# Data files.
ASSIGNMENT_BRIEF_PATH = DATA_DIR / "assignment_brief.txt"
GRADING_RUBRIC_PATH = DATA_DIR / "grading_rubric.json"
FEW_SHOT_EXAMPLES_PATH = DATA_DIR / "few_shot_examples.json"

# Output files.
PROJECT_PLAN_OUTPUT_PATH = OUTPUT_DIR / "project_plan.md"
TASK_BREAKDOWN_OUTPUT_PATH = OUTPUT_DIR / "task_breakdown.csv"
COMPLIANCE_REPORT_OUTPUT_PATH = OUTPUT_DIR / "compliance_report.md"
DEMO_LOG_PATH = OUTPUT_DIR / "demo_log.json"


# DeepSeek settings.
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

# To avoid sending extremely long documents during the demo.
MAX_BRIEF_CHARS = int(os.getenv("MAX_BRIEF_CHARS", "60000"))


def ensure_project_directories() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
