"""
AutoNotes Backend - Flask application entry point.
Provides API endpoints for generating structured meeting notes from transcripts.
"""

from flask import Flask, jsonify
from flask_cors import CORS

from routes.notes_routes import notes_bp

# Initialize Flask application
app = Flask(__name__)

# Configure CORS to allow all origins (adjust for production)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})


@app.route('/')
def index():
    """
    Root endpoint - API status and information.
    
    Returns:
        JSON response with API information
    """
    return jsonify({
        "service": "AutoNotes API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /api/notes": "Generate structured notes from transcript",
            "GET /api/notes/<id>": "Retrieve a specific note by ID",
            "GET /api/notes": "List all notes (paginated)",
            "GET /api/notes/health": "Check service health"
        }
    }), 200


@app.route('/health')
def health():
    """
    Application health check endpoint.
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        "status": "healthy",
        "service": "AutoNotes API"
    }), 200


# Register blueprints
app.register_blueprint(notes_bp)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response."""
    return jsonify({
        "error": "Not found",
        "message": "The requested resource was not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with JSON response."""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    # Start Flask development server
    # In production, use a WSGI server like Gunicorn or Waitress
    app.run(
        host='0.0.0.0',  # Listen on all network interfaces
        port=5000,
        debug=True  # Enable debug mode for development
    )
