import csv
import json
from pathlib import Path
from typing import Dict, Any, List

from tools.timeline_generator import TimelineGenerator
from tools.checklist_generator import ChecklistGenerator

class ActionAgent:
    """
    Core Agent for the Action stage. Responsible for evaluating the plan and orchestrating tool executions.
    """

    def __init__(self):
        self.timeline_gen = TimelineGenerator()
        self.checklist_gen = ChecklistGenerator()
        self.step_counter = 1
        
        # Internal memory log to replace the buggy external logger for clean demo output.
        self.logs = []
        
        # Resolve project root for strict reproducibility.
        self.project_root = Path(__file__).resolve().parent.parent
        self.output_dir = self.project_root / "outputs"

    def record_internal_trace(self, step: int, agent: str, action: str, status: str, details: dict) -> None:
        """
        Records an in-memory execution trace to fulfill Agent Observability requirements.
        
        Args:
            step: The current execution step number.
            agent: The name of the agent performing the action.
            action: A descriptive, human-readable name of the action being performed.
            status: The current status of the action (e.g., 'started', 'success', 'failed').
            details: A dictionary containing specific observation data related to the action.

        Returns:
            None. The trace is appended to the internal 'self.logs' list.

        Example usage:
            self.record_internal_trace(
                step=1,
                agent="ActionAgent",
                action="generate_timeline",
                status="success",
                details={"file": "outputs/project_plan.md"}
            )
        """
        self.logs.append({
            "step": step,
            "agent": agent,
            "action": action,
            "status": status,
            "observation": details
        })

    def execute_planned_tool_actions(self, planner_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parses the structured output from the Reasoning stage and triggers physical tool actions.
        Adheres to best practices by returning file paths instead of large file contents to prevent LLM context swamping.

        Args:
            planner_output: A dictionary containing the structured project plan. Expected keys include:
                'coding_tasks': A list of dictionaries detailing daily coding assignments.
                'video_sections_to_cover': A list of strings outlining required video content.
                'team_allocation': A dictionary mapping team members to their assigned tasks.
                'development_priorities': A list of dictionaries defining project priorities.

        Returns:
            A dictionary detailing the execution status and generated artifacts. Expected keys include:
                'status': A string indicating the overall success or completion message.
                'generated_files': A dictionary mapping artifact identifiers to their saved file paths on disk.

        Example return value:
            {
                'status': 'Action stage completed successfully',
                'generated_files': {
                    'project_plan': 'Q:\\path\\outputs\\project_plan.md',
                    'compliance_checklist': 'Q:\\path\\outputs\\compliance_report.md',
                    'task_breakdown': 'Q:\\path\\outputs\\task_breakdown.csv',
                    'development_priorities': 'Q:\\path\\outputs\\priorities.csv'
                }
            }
        """
        results = {}
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.record_internal_trace(
            self.step_counter, "ActionAgent", "init_action_sequence", "success", 
            {"input_keys": list(planner_output.keys())}
        )
        self.step_counter += 1
        
        # Phase 1: Generate Markdown Timeline
        if "coding_tasks" in planner_output and isinstance(planner_output["coding_tasks"], list):
            safe_file_name = "project_plan.md"
            if self._is_safe_path(safe_file_name):
                plan_path = str(self.output_dir / safe_file_name)
                final_path = self.timeline_gen.generate_markdown_timeline_with_gantt(
                    planner_output["coding_tasks"], output_path=plan_path
                )
                results["project_plan"] = final_path
                self.record_internal_trace(self.step_counter, "ActionAgent", "generate_timeline", "success", {"file": final_path})
            self.step_counter += 1

        # Phase 2: Generate Compliance Checklist
        if "video_sections_to_cover" in planner_output and isinstance(planner_output["video_sections_to_cover"], list):
            safe_file_name = "compliance_report.md"
            if self._is_safe_path(safe_file_name):
                chk_path = str(self.output_dir / safe_file_name)
                final_path = self.checklist_gen.generate_human_verification_checklist(
                    planner_output["video_sections_to_cover"], output_path=chk_path
                )
                results["compliance_checklist"] = final_path
                self.record_internal_trace(self.step_counter, "ActionAgent", "generate_checklist", "success", {"file": final_path})
            self.step_counter += 1

        # Phase 3: Export CSV Task Breakdown
        if "team_allocation" in planner_output and isinstance(planner_output["team_allocation"], dict):
            safe_file_name = "task_breakdown.csv"
            if self._is_safe_path(safe_file_name):
                csv_path = self.output_dir / safe_file_name
                try:
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Member", "Assigned Tasks"])
                        for member, tasks in planner_output["team_allocation"].items():
                            if isinstance(tasks, list):
                                tasks_str = ", ".join(tasks)
                            elif isinstance(tasks, dict) and "modules" in tasks:
                                tasks_str = ", ".join(tasks["modules"])
                            else:
                                tasks_str = str(tasks)
                            writer.writerow([member, tasks_str])
                    results["task_breakdown"] = str(csv_path)
                    self.record_internal_trace(self.step_counter, "ActionAgent", "export_task_csv", "success", {"file": str(csv_path)})
                except Exception as e:
                    self.record_internal_trace(self.step_counter, "ActionAgent", "export_task_csv", "failed", {"error": str(e)})
            self.step_counter += 1

        # Phase 4: Export CSV Priorities Breakdown
        if "development_priorities" in planner_output and isinstance(planner_output["development_priorities"], list):
            safe_file_name = "priorities.csv"
            if self._is_safe_path(safe_file_name):
                csv_path = self.output_dir / safe_file_name
                try:
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Priority", "Focus", "Reason"])
                        for item in planner_output["development_priorities"]:
                            writer.writerow([item.get("priority", ""), item.get("focus", ""), item.get("reason", "")])
                    results["development_priorities"] = str(csv_path)
                    self.record_internal_trace(self.step_counter, "ActionAgent", "export_priorities_csv", "success", {"file": str(csv_path)})
                except Exception as e:
                    self.record_internal_trace(self.step_counter, "ActionAgent", "export_priorities_csv", "failed", {"error": str(e)})
            self.step_counter += 1

        return {
            "status": "Action stage completed successfully",
            "generated_files": results
        }

    def _is_safe_path(self, target_filename: str) -> bool:
        """
        Validates if a given filename resolves to a path securely within the designated output directory sandbox.

        Args:
            target_filename: The name of the file to be validated (e.g., 'project_plan.md').

        Returns:
            A boolean value. Returns True if the path is safely contained within the output directory, 
            and False if a Path Traversal Attack is detected or an error occurs.

        Example return value:
            True
        """
        try:
            target_path = (self.output_dir / target_filename).resolve()
            return self.output_dir in target_path.parents or self.output_dir == target_path.parent
        except Exception:
            return False

    def run_actions(self, planner_output: Any) -> Any:
        """
        Integration wrapper that processes the reasoning output and formats the final action response.

        Args:
            planner_output: The data structure from the Reasoning stage. Can be an object with a '.data' attribute, 
            a JSON string, or a dictionary.

        Returns:
            A Response-like object containing execution success status, payload data, logs, and a status message. 
            Expected attributes include:
                'success': Boolean indicating if the run was successful.
                'data': The dictionary returned by 'execute_planned_tool_actions'.
                'logs': The internal execution trace list.
                'message': The final execution status string.

        Example return value:
            <Response object with success=True, data={'generated_files': {...}}, message='Action stage completed successfully'>
        """
        data_to_process = planner_output
        if hasattr(planner_output, 'data'):
            data_to_process = planner_output.data
        elif isinstance(planner_output, str):
            data_to_process = json.loads(planner_output)

        execution_results = self.execute_planned_tool_actions(data_to_process)

        return type('Response', (object,), {
            "success": True,
            "data": execution_results,
            "logs": self.logs,
            "message": execution_results.get("status", "Action stage completed")
        })