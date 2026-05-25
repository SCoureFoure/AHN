"""Task model."""
from dataclasses import dataclass, field
import uuid


@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
