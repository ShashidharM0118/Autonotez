"""
Validation utilities for request data and LLM responses.
Ensures data integrity and provides clear error messages.
"""

from typing import Dict, Any, List


class ValidationError(Exception):
    """Custom exception for validation failures."""
    pass


def validate_transcript_request(request_data: Dict[str, Any]) -> str:
    """
    Validate incoming request contains a non-empty transcript.
    
    Args:
        request_data: Dictionary containing request body
        
    Returns:
        The validated transcript string
        
    Raises:
        ValidationError: If transcript is missing or empty
    """
    if not request_data:
        raise ValidationError("Request body is required")
    
    transcript = request_data.get("transcript")
    
    if transcript is None:
        raise ValidationError("Field 'transcript' is required")
    
    if not isinstance(transcript, str):
        raise ValidationError("Field 'transcript' must be a string")
    
    transcript = transcript.strip()
    
    if not transcript:
        raise ValidationError("Field 'transcript' cannot be empty")
    
    # Basic length validation (prevent abuse)
    if len(transcript) > 100000:  # 100k chars max
        raise ValidationError("Transcript exceeds maximum length of 100,000 characters")
    
    return transcript


def validate_llm_response(response_data: Dict[str, Any]) -> None:
    """
    Validate that LLM response contains all required fields.
    
    Args:
        response_data: Dictionary parsed from LLM JSON response
        
    Raises:
        ValidationError: If required fields are missing or invalid
    """
    required_fields = ["summary", "action_items", "decisions", "keywords"]
    
    for field in required_fields:
        if field not in response_data:
            raise ValidationError(f"LLM response missing required field: '{field}'")
    
    # Validate field types
    if not isinstance(response_data["summary"], str):
        raise ValidationError("Field 'summary' must be a string")
    
    if not isinstance(response_data["action_items"], list):
        raise ValidationError("Field 'action_items' must be a list")
    
    if not isinstance(response_data["decisions"], list):
        raise ValidationError("Field 'decisions' must be a list")
    
    if not isinstance(response_data["keywords"], list):
        raise ValidationError("Field 'keywords' must be a list")
    
    # Validate action items structure
    for idx, action_item in enumerate(response_data["action_items"]):
        if not isinstance(action_item, dict):
            raise ValidationError(f"Action item at index {idx} must be an object")
        
        if "text" not in action_item:
            raise ValidationError(f"Action item at index {idx} missing 'text' field")
        
        if not isinstance(action_item["text"], str):
            raise ValidationError(f"Action item at index {idx} 'text' must be a string")
    
    # Validate decisions are strings
    for idx, decision in enumerate(response_data["decisions"]):
        if not isinstance(decision, str):
            raise ValidationError(f"Decision at index {idx} must be a string")
    
    # Validate keywords are strings
    for idx, keyword in enumerate(response_data["keywords"]):
        if not isinstance(keyword, str):
            raise ValidationError(f"Keyword at index {idx} must be a string")
    
    # Validate non-empty summary
    if not response_data["summary"].strip():
        raise ValidationError("Field 'summary' cannot be empty")


def sanitize_note_data(note_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitize and normalize note data before storage.
    
    Args:
        note_data: Raw note data from LLM
        
    Returns:
        Sanitized note data
    """
    return {
        "summary": note_data["summary"].strip(),
        "action_items": [
            {
                "text": item["text"].strip(),
                "owner": item.get("owner", "").strip() or None,
                "due_date": item.get("due_date", "").strip() or None
            }
            for item in note_data["action_items"]
        ],
        "decisions": [decision.strip() for decision in note_data["decisions"]],
        "keywords": [keyword.strip().lower() for keyword in note_data["keywords"]]
    }
