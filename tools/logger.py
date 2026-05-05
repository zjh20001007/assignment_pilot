import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ActionLogger:
    """
    Tool suite for Agent system observability and audit logging.
    """

    def __init__(self, log_filename: str = "demo_log.json"):
        # Design Consideration: Ensure the log file is robustly placed in the outputs directory
        # regardless of where the main script is executed from.
        self.project_root = Path(__file__).resolve().parent.parent
        self.log_dir = self.project_root / "outputs"
        self.log_file = self.log_dir / log_filename
            
        self.log_dir.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump({"trace_id": "session_" + datetime.now().strftime("%Y%m%d%H%M%S"), "logs": []}, f)

    def record_tool_execution_trace(self, step: int, agent_name: str, action: str, status: str, details: Dict[str, Any] = None) -> bool:
        """
        Appends a detailed execution trace of an agent's tool call to a JSON log file.

        Args:
            step: The sequential integer indicating the order of the action.
            agent_name: The name of the agent executing the action.
            action: A specific, descriptive string identifying the tool executed.
            status: The execution outcome status.
            details: A dictionary containing tool inputs, outputs, or error traces. Defaults to an empty dictionary.

        Returns:
            A boolean value indicating successful write operation.

        Example return value:
            True
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "execution_step": step,
            "agent_context": agent_name,
            "tool_action": action,
            "execution_status": status,
            "io_traces": details or {}
        }
        
        try:
            # Design Consideration: Use r+ to efficiently append to the JSON array without rewriting the whole file.
            with open(self.log_file, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data["logs"].append(entry)
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()
            return True
        except Exception as e:
            print(f"[Observability Error] Failed to write trace to log file: {str(e)}")
            return False