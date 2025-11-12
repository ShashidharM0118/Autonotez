"""
Flask Blueprint for meeting notes API endpoints.
Handles HTTP requests for note generation and retrieval.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any

from services.llm_service import generate_notes, LLMServiceError
from services.storage_service import (
    save_note, 
    get_note_by_id, 
    get_all_notes,
    StorageServiceError
)
from utils.validators import (
    validate_transcript_request,
    validate_llm_response,
    sanitize_note_data,
    ValidationError
)
from models.note_model import Note, ActionItem

# Create Blueprint
notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')


@notes_bp.route('', methods=['POST'])
def create_note():
    """
    Generate structured meeting notes from a transcript.
    
    Request Body:
        {
            "transcript": "string - meeting transcript text"
        }
    
    Response (200):
        {
            "note_id": "string - MongoDB ObjectId",
            "summary": "string - 2-3 sentence overview",
            "action_items": [
                {
                    "text": "string - action description",
                    "owner": "string|null - person responsible",
                    "due_date": "string|null - expected completion date"
                }
            ],
            "decisions": ["string - decision made"],
            "keywords": ["string - relevant keyword"],
            "created_at": "string - ISO 8601 timestamp"
        }
    
    Error Responses:
        400: Invalid request (missing/empty transcript)
        500: Internal server error (LLM or storage failure)
    """
    try:
        # Get and validate request data
        request_data = request.get_json()
        transcript = validate_transcript_request(request_data)
        
        # Generate notes using LLM
        notes_data = generate_notes(transcript)
        
        # Sanitize and normalize the data
        sanitized_data = sanitize_note_data(notes_data)
        
        # Create Note model instance
        note = Note.from_dict(sanitized_data)
        
        # Save to database
        note_dict = note.to_dict()
        note_id = save_note(note_dict)
        
        # Add note_id to response
        note_dict["note_id"] = note_id
        
        return jsonify(note_dict), 200
        
    except ValidationError as e:
        return jsonify({
            "error": "Validation error",
            "message": str(e)
        }), 400
    
    except LLMServiceError as e:
        return jsonify({
            "error": "LLM service error",
            "message": str(e)
        }), 500
    
    except StorageServiceError as e:
        return jsonify({
            "error": "Storage error",
            "message": str(e)
        }), 500
    
    except Exception as e:
        # Log unexpected errors (in production, use proper logging)
        print(f"Unexpected error in create_note: {str(e)}")
        
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }), 500


@notes_bp.route('/<note_id>', methods=['GET'])
def get_note(note_id: str):
    """
    Retrieve a specific meeting note by ID.
    
    Path Parameters:
        note_id: MongoDB ObjectId string
    
    Response (200):
        Note object (same structure as create_note response)
    
    Error Responses:
        404: Note not found
        500: Internal server error
    """
    try:
        note_data = get_note_by_id(note_id)
        
        if note_data is None:
            return jsonify({
                "error": "Not found",
                "message": f"Note with ID '{note_id}' not found"
            }), 404
        
        return jsonify(note_data), 200
        
    except StorageServiceError as e:
        return jsonify({
            "error": "Storage error",
            "message": str(e)
        }), 500
    
    except Exception as e:
        print(f"Unexpected error in get_note: {str(e)}")
        
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred while retrieving the note"
        }), 500


@notes_bp.route('', methods=['GET'])
def list_notes():
    """
    Retrieve a paginated list of meeting notes.
    
    Query Parameters:
        limit: Maximum number of notes to return (default 50, max 100)
        skip: Number of notes to skip for pagination (default 0)
    
    Response (200):
        {
            "notes": [array of note objects],
            "count": number of notes returned,
            "limit": limit used,
            "skip": skip value used
        }
    
    Error Responses:
        500: Internal server error
    """
    try:
        # Parse query parameters
        limit = request.args.get('limit', default=50, type=int)
        skip = request.args.get('skip', default=0, type=int)
        
        # Enforce limits
        limit = min(max(1, limit), 100)  # Between 1 and 100
        skip = max(0, skip)  # Non-negative
        
        # Retrieve notes
        notes = get_all_notes(limit=limit, skip=skip)
        
        return jsonify({
            "notes": notes,
            "count": len(notes),
            "limit": limit,
            "skip": skip
        }), 200
        
    except StorageServiceError as e:
        return jsonify({
            "error": "Storage error",
            "message": str(e)
        }), 500
    
    except Exception as e:
        print(f"Unexpected error in list_notes: {str(e)}")
        
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred while retrieving notes"
        }), 500


@notes_bp.route('/health', methods=['GET'])
def health_check():
    """
    Check the health status of the notes service.
    
    Response (200):
        {
            "status": "healthy",
            "services": {
                "llm": boolean,
                "storage": boolean
            }
        }
    """
    from services.llm_service import health_check as llm_health
    from services.storage_service import health_check as storage_health
    
    llm_status = llm_health()
    storage_status = storage_health()
    
    overall_status = "healthy" if (llm_status and storage_status) else "degraded"
    
    return jsonify({
        "status": overall_status,
        "services": {
            "llm": llm_status,
            "storage": storage_status
        }
    }), 200
