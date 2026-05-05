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

    def record_internal_trace(self, step: int, agent: str, action: str, status: str, details: dict):
        """
        Maintains an in-memory execution trace to fulfill Agent Observability requirements.
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

        Args:
            planner_output: A dictionary containing the structured project plan including timeline, 
            checklist, and team_allocation.

        Returns:
            A dictionary detailing the execution status and generated artifacts. Expected keys include:
            'status': A string indicating the overall success or completion message.
            'generated_files': A dictionary mapping artifact identifiers to their saved file paths.

        Example return value:
            {
                'status': 'Action stage completed successfully',
                'generated_files': {
                    'project_plan': 'outputs/project_plan.md',
                    'compliance_checklist': 'outputs/compliance_report.md',
                    'task_breakdown': 'outputs/task_breakdown.csv'
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
        if "timeline" in planner_output and isinstance(planner_output["timeline"], list):
            safe_file_name = "project_plan.md"
            if self._is_safe_path(safe_file_name):
                plan_path = str(self.output_dir / safe_file_name)
                final_path = self.timeline_gen.generate_markdown_timeline_with_gantt(
                    planner_output["timeline"], output_path=plan_path
                )
                results["project_plan"] = final_path
                self.record_internal_trace(self.step_counter, "ActionAgent", "generate_timeline", "success", {"file": final_path})
            self.step_counter += 1

        # Phase 2: Generate Compliance Checklist
        if "checklist" in planner_output and isinstance(planner_output["checklist"], list):
            safe_file_name = "compliance_report.md"
            if self._is_safe_path(safe_file_name):
                chk_path = str(self.output_dir / safe_file_name)
                final_path = self.checklist_gen.generate_human_verification_checklist(
                    planner_output["checklist"], output_path=chk_path
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
                            tasks_str = ", ".join(tasks) if isinstance(tasks, list) else str(tasks)
                            writer.writerow([member, tasks_str])
                    results["task_breakdown"] = str(csv_path)
                    self.record_internal_trace(self.step_counter, "ActionAgent", "export_csv", "success", {"file": str(csv_path)})
                except Exception as e:
                    self.record_internal_trace(self.step_counter, "ActionAgent", "export_csv", "failed", {"error": str(e)})
            self.step_counter += 1

        return {
            "status": "Action stage completed successfully",
            "generated_files": results
        }

    def _is_safe_path(self, target_filename: str) -> bool:
        """
        Advanced Guardrail: Prevents Path Traversal Attacks.

        Args:
            target_filename: The name of the file to be validated against the sandbox.

        Returns:
            A boolean indicating if the path is safely contained within the output directory.
        """
        try:
            target_path = (self.output_dir / target_filename).resolve()
            return self.output_dir in target_path.parents or self.output_dir == target_path.parent
        except Exception:
            return False

    def run_actions(self, planner_output: Any) -> Any:
        """
        Integration Wrapper for main.py execution loop.

        Args:
            planner_output: The data structure from the Reasoning stage.

        Returns:
            An object containing execution success, data, logs, and status message.
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