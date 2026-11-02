# ai/parser.py
import json
from enum import Enum
from typing import Tuple, Optional

class ResponseType(Enum):
    COMMAND = 1
    TEXT = 2

class ResponseParser:
    def parse(self, raw_response: str) -> Tuple[ResponseType, dict]:
        cleaned = raw_response.strip()
        
        if cleaned.startswith("{") and cleaned.endswith("}"):
            try:
                data = json.loads(cleaned)
                if "intent" in data and "action" in data:
                    return ResponseType.COMMAND, data
            except json.JSONDecodeError:
                pass
                
        return ResponseType.TEXT, {"text": raw_response}