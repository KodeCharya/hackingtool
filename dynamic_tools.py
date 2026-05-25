import json
from pathlib import Path

from core import HackingTool, HackingToolsCollection, console


class DynamicTool(HackingTool):
    def __init__(self, spec: dict):
        self.TITLE = spec.get("title", "Unnamed Tool")
        self.DESCRIPTION = spec.get("description", "")
        self.PROJECT_URL = spec.get("project_url", "")
        self.INSTALL_COMMANDS = list(spec.get("install_commands", []))
        self.RUN_COMMANDS = list(spec.get("run_commands", []))
        self.TAGS = list(spec.get("tags", []))
        self.SUPPORTED_OS = list(spec.get("supported_os", ["linux", "macos"]))
        self.ARCHIVED = bool(spec.get("archived", False))
        self.ARCHIVED_REASON = spec.get("archived_reason", "")
        super().__init__()


class DynamicCategory(HackingToolsCollection):
    def __init__(self, title: str, description: str, tools: list[HackingTool]):
        super().__init__()
        self.TITLE = title
        self.DESCRIPTION = description
        self.TOOLS = tools


def load_dynamic_categories(config_path: str | Path) -> list[DynamicCategory]:
    path = Path(config_path)
    if not path.exists():
        return []

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"[warning]Dynamic tools config is invalid: {exc}[/warning]")
        return []

    categories = []
    for category in raw.get("categories", []):
        tool_specs = category.get("tools", [])
        tools = [DynamicTool(spec) for spec in tool_specs]
        categories.append(
            DynamicCategory(
                title=category.get("title", "Custom Category"),
                description=category.get("description", ""),
                tools=tools,
            )
        )
    return categories
