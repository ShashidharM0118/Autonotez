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
        
        # Retrieve the saved note (this properly converts ObjectId to string)
        saved_note = get_note_by_id(note_id)
        
        if not saved_note:
            raise StorageServiceError("Failed to retrieve saved note")
        
        return jsonify(saved_note), 200
        
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


@notes_bp.route('/models', methods=['GET'])
def list_models():
    """
    List all available Gemini models that support content generation.
    
    Response (200):
        {
            "total_models": number,
            "current_model": "string - currently configured model",
            "models": [
                {
                    "name": "string - full model path",
                    "display_name": "string - human readable name",
                    "description": "string - model description",
                    "supported_methods": ["array of supported methods"],
                    "input_token_limit": number,
                    "output_token_limit": number
                }
            ]
        }
    
    Error Responses:
        500: Failed to fetch models
    """
    try:
        from services.llm_service import list_available_models
        
        models_data = list_available_models()
        return jsonify(models_data), 200
        
    except LLMServiceError as e:
        return jsonify({
            "error": "LLM service error",
            "message": str(e)
        }), 500
    
    except Exception as e:
        print(f"Unexpected error in list_models: {str(e)}")
        
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to list available models"
        }), 500


@notes_bp.route('/test', methods=['GET', 'POST'])
def test_model():
    """
    Test the current Gemini model with a simple prompt.
    
    Query Parameters (GET):
        prompt: Optional test prompt (default: "Hello, can you confirm you're working?")
    
    Request Body (POST):
        {
            "prompt": "string - test prompt"
        }
    
    Response (200):
        {
            "status": "success",
            "model": "string - model name",
            "test_prompt": "string - prompt sent",
            "response": "string - model response"
        }
    
    Error Responses:
        500: Model test failed
    """
    try:
        from services.llm_service import test_model as test_llm_model
        
        # Get prompt from query param or request body
        if request.method == 'POST':
            data = request.get_json() or {}
            prompt = data.get('prompt', 'Hello, can you confirm you\'re working?')
        else:
            prompt = request.args.get('prompt', 'Hello, can you confirm you\'re working?')
        
        test_result = test_llm_model(prompt)
        return jsonify(test_result), 200
        
    except LLMServiceError as e:
        return jsonify({
            "error": "LLM service error",
            "message": str(e)
        }), 500
    
    except Exception as e:
        print(f"Unexpected error in test_model: {str(e)}")
        
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to test model"
        }), 500
