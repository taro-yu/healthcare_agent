from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class Message:
    role: str
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None

@dataclass
class ToolCall:
    id: str
    type: str
    function_name: str
    arguments: Dict[str, Any]

@dataclass
class ToolResult:
    tool_call_id: str
    content: str