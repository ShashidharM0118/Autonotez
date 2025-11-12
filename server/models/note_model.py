"""
Data models for meeting notes using dataclasses.
Provides type-safe structures for notes and action items.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class ActionItem:
    """
    Represents a single action item from a meeting.
    
    Attributes:
        text: Description of the action to be taken
        owner: Person responsible for the action (optional)
        due_date: Expected completion date (optional)
    """
    text: str
    owner: Optional[str] = None
    due_date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action item to dictionary representation."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ActionItem":
        """Create ActionItem instance from dictionary."""
        return cls(
            text=data.get("text", ""),
            owner=data.get("owner"),
            due_date=data.get("due_date")
        )


@dataclass
class Note:
    """
    Represents structured meeting notes generated from a transcript.
    
    Attributes:
        summary: Concise overview of the meeting (2-3 sentences)
        action_items: List of tasks identified during the meeting
        decisions: List of key decisions made
        keywords: List of 5 relevant keywords
        created_at: Timestamp when the note was created
        note_id: MongoDB ObjectId (populated after saving)
    """
    summary: str
    action_items: List[ActionItem]
    decisions: List[str]
    keywords: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)
    note_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert note to dictionary representation suitable for JSON serialization.
        
        Returns:
            Dictionary with all note fields, action_items converted to dicts
        """
        return {
            "summary": self.summary,
            "action_items": [item.to_dict() for item in self.action_items],
            "decisions": self.decisions,
            "keywords": self.keywords,
            "created_at": self.created_at.isoformat(),
            "note_id": self.note_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Note":
        """
        Create Note instance from dictionary.
        
        Args:
            data: Dictionary containing note fields
            
        Returns:
            Note instance with populated fields
        """
        action_items = [
            ActionItem.from_dict(item) if isinstance(item, dict) else item
            for item in data.get("action_items", [])
        ]
        
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.utcnow()
            
        return cls(
            summary=data.get("summary", ""),
            action_items=action_items,
            decisions=data.get("decisions", []),
            keywords=data.get("keywords", []),
            created_at=created_at,
            note_id=data.get("note_id")
        )
