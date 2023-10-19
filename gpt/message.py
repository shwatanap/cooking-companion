from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from gpt.constants import Role

#メッセージらを生成する
@dataclass
class Message:
    role: Role
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role.value, "content": self.content}

    @classmethod
    def from_dict(cls, message: Dict[str, str]) -> Message:
        return cls(role=Role(message["role"]), content=message["content"])
