import os
from typing import List, Dict

class TimelineGenerator:
    """
    Tool suite for generating visual project timelines and schedules.
    """

    def generate_markdown_timeline_with_gantt(self, plan_data: List[Dict[str, str]], output_path: str = "outputs/project_plan.md") -> str:
        """
        Generates a Markdown document containing a project schedule and a visual Mermaid Gantt chart.
        Stores the generated file externally to avoid returning large responses that could swamp the LLM context.

        Args:
            plan_data: A list of dictionaries containing the schedule. Expected keys for each dictionary include:
                'day': The specific day or date identifier for the task.
                'task': A clear description of the development task.
            output_path: The file path destination for the generated document. Defaults to 'outputs/project_plan.md'.

        Returns:
            A short string representing the file path to the successfully generated Markdown document.

        Example return value:
            'outputs/project_plan.md'
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        md_content = "# 📅 CA6123 AssignmentPilot Project Timeline\n\n"
        md_content += "## 📊 Visual Progress (Mermaid Gantt)\n"
        md_content += "```mermaid\ngantt\n    title Project Development Timeline\n    dateFormat  YYYY-MM-DD\n"
        
        for i, task in enumerate(plan_data):
            day_label = task.get("day", f"Day {i+1}")
            task_desc = task.get("task", "Unnamed Task")
            md_content += f"    {task_desc} :a{i}, 2026-05-0{i+5}, 1d\n"
        md_content += "```\n\n"
        
        md_content += "## 📋 Detailed Schedule\n"
        md_content += "| Phase | Core Task Description |\n|---|---|\n"
        for task in plan_data:
            md_content += f"| **{task.get('day', '')}** | {task.get('task', '')} |\n"
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        return output_path