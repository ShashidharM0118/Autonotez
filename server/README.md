# AutoNotes Backend

Full-stack meeting notes generator using Flask, MongoDB, and Google Gemini AI.

## 📁 Project Structure

```
server/
├── app.py                          # Flask application entry point
├── routes/
│   └── notes_routes.py            # API endpoints for notes
├── services/
│   ├── llm_service.py             # Gemini API integration
│   └── storage_service.py         # MongoDB CRUD operations
├── models/
│   └── note_model.py              # Data models (Note, ActionItem)
├── utils/
│   └── validators.py              # Request and response validators
├── tests/
│   └── test_llm_service.py        # Unit tests
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB instance (local or MongoDB Atlas)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Navigate to server directory:**
   ```powershell
   cd "e:\projects\web_projects\code_sample mlh\server"
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   
   If you encounter execution policy errors, use:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install dependencies:**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```powershell
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/autonotes
   ```

5. **Run the application:**
   ```powershell
   python app.py
   ```
   
   Server will start on `http://localhost:5000`

## 📡 API Endpoints

### 1. Generate Meeting Notes

**Endpoint:** `POST /api/notes`

**Request Body:**
```json
{
  "transcript": "Team meeting discussing Q4 goals. John will create roadmap by Friday. Sarah approved budget increase. Decided to launch on December 1st."
}
```

**Response (200):**
```json
{
  "note_id": "673d9e8f1a2b3c4d5e6f7g8h",
  "summary": "Team discussed Q4 goals and project timeline. Key milestones were identified for the upcoming sprint. Budget approval secured for additional resources.",
  "action_items": [
    {
      "text": "Create detailed project roadmap",
      "owner": "John",
      "due_date": "Friday"
    },
    {
      "text": "Finalize budget allocation",
      "owner": "Sarah",
      "due_date": null
    }
  ],
  "decisions": [
    "Launch date set for December 1st",
    "Budget increase approved"
  ],
  "keywords": ["Q4", "goals", "timeline", "budget", "launch"],
  "created_at": "2025-11-12T10:30:00.000Z"
}
```

**Error Responses:**
- `400`: Missing or empty transcript
- `500`: LLM service or storage error

### 2. Get Note by ID

**Endpoint:** `GET /api/notes/<note_id>`

**Response (200):** Same structure as POST response

**Error Responses:**
- `404`: Note not found
- `500`: Storage error

### 3. List All Notes

**Endpoint:** `GET /api/notes?limit=50&skip=0`

**Query Parameters:**
- `limit` (optional): Maximum notes to return (default: 50, max: 100)
- `skip` (optional): Number of notes to skip (default: 0)

**Response (200):**
```json
{
  "notes": [ /* array of note objects */ ],
  "count": 50,
  "limit": 50,
  "skip": 0
}
```

### 4. Health Check

**Endpoint:** `GET /api/notes/health`

**Response (200):**
```json
{
  "status": "healthy",
  "services": {
    "llm": true,
    "storage": true
  }
}
```

### 5. Root Endpoint

**Endpoint:** `GET /`

**Response (200):** API information and available endpoints

## 🧪 Testing

Run unit tests with pytest:

```powershell
pytest tests/ -v
```

Run specific test file:

```powershell
pytest tests/test_llm_service.py -v
```

## 🏗️ Architecture

### Modular Design

- **Flask Blueprints**: Routes organized by resource (`notes_routes.py`)
- **Service Layer**: Business logic separated (`llm_service.py`, `storage_service.py`)
- **Data Models**: Type-safe dataclasses with validation (`note_model.py`)
- **Validators**: Centralized validation logic (`validators.py`)

### Key Features

- ✅ **Type hints** throughout codebase
- ✅ **Comprehensive error handling** with custom exceptions
- ✅ **MongoDB connection pooling** for performance
- ✅ **CORS enabled** for cross-origin requests
- ✅ **Request validation** with descriptive error messages
- ✅ **Unit tests** with mocked external dependencies
- ✅ **PEP8 compliant** code style
- ✅ **Detailed docstrings** for all functions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIzaSyD...` |
| `MONGO_URI` | MongoDB connection string | `mongodb+srv://...` |

### MongoDB Setup

**Option 1: MongoDB Atlas (Cloud)**
1. Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create cluster and get connection string
3. Replace `<username>`, `<password>`, and `<cluster>` in URI

**Option 2: Local MongoDB**
```powershell
# Install MongoDB Community Server
# Then use:
MONGO_URI=mongodb://localhost:27017/autonotes
```

### Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create new API key
3. Copy key to `.env` file

## 🐛 Troubleshooting

### Import Errors

If you see import errors after creating files, install dependencies:
```powershell
pip install -r requirements.txt
```

### MongoDB Connection Issues

- Verify `MONGO_URI` is correct
- Check IP whitelist in MongoDB Atlas (add `0.0.0.0/0` for testing)
- Ensure network allows outbound connections on port 27017

### Gemini API Errors

- Verify API key is valid and not expired
- Check you haven't exceeded rate limits
- Ensure you have enabled the Gemini API in Google Cloud Console

### CORS Issues

If frontend can't connect, verify CORS is enabled in `app.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

## 📝 Code Style Guidelines

- **Indentation**: 4 spaces (no tabs)
- **Type hints**: Required for all function parameters and returns
- **Docstrings**: Google-style docstrings for all functions
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes
- **Line length**: Maximum 100 characters (recommended)
- **Comments**: Only when clarifying complex logic

## 🚀 Production Deployment

For production environments:

1. **Use a production WSGI server:**
   ```powershell
   pip install gunicorn  # Linux/Mac
   pip install waitress  # Windows
   ```
   
   ```powershell
   # Windows
   waitress-serve --host=0.0.0.0 --port=5000 app:app
   
   # Linux/Mac
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Disable debug mode** in `app.py`:
   ```python
   app.run(host='0.0.0.0', port=5000, debug=False)
   ```

3. **Set up proper logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

4. **Configure CORS** to only allow specific origins:
   ```python
   CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
   ```

5. **Use environment-specific configs:**
   - Separate `.env.production` file
   - Use secrets manager for sensitive data

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Google Gemini API](https://ai.google.dev/docs)
- [pytest Documentation](https://docs.pytest.org/)

## 📄 License

MIT License - feel free to use this project for learning or production.

---

**Built with ❤️ using Flask, MongoDB, and Google Gemini AI**
