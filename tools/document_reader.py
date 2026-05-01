from pathlib import Path


class DocumentReaderTool:
    def read(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8")

        if not content.strip():
            raise ValueError(f"File is empty: {file_path}")

        return content