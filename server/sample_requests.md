# Sample API Requests for AutoNotes

## 1. Generate Meeting Notes (POST /api/notes)

### cURL (PowerShell)
```powershell
curl -X POST http://localhost:5000/api/notes `
  -H "Content-Type: application/json" `
  -d '{\"transcript\":\"Team standup meeting on Nov 12. John mentioned he will finish the user authentication module by Friday. Sarah reported that the database migration is complete and tested. We decided to move the launch date to December 1st to allow more time for testing. Mike raised concerns about the API rate limits. Action item: Sarah will research alternative API providers by next Monday. Decision made: We will use Groq instead of Claude for AI features.\"}'
```

### cURL (Bash/Linux/Mac)
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Team standup meeting on Nov 12. John mentioned he will finish the user authentication module by Friday. Sarah reported that the database migration is complete and tested. We decided to move the launch date to December 1st to allow more time for testing. Mike raised concerns about the API rate limits. Action item: Sarah will research alternative API providers by next Monday. Decision made: We will use Groq instead of Claude for AI features."
  }'
```

### Python
```python
import requests
import json

url = "http://localhost:5000/api/notes"
headers = {"Content-Type": "application/json"}

data = {
    "transcript": "Team standup meeting on Nov 12. John mentioned he will finish the user authentication module by Friday. Sarah reported that the database migration is complete and tested. We decided to move the launch date to December 1st to allow more time for testing. Mike raised concerns about the API rate limits. Action item: Sarah will research alternative API providers by next Monday. Decision made: We will use Groq instead of Claude for AI features."
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(json.dumps(response.json(), indent=2))
```

### JavaScript (fetch)
```javascript
fetch('http://localhost:5000/api/notes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    transcript: "Team standup meeting on Nov 12. John mentioned he will finish the user authentication module by Friday. Sarah reported that the database migration is complete and tested. We decided to move the launch date to December 1st to allow more time for testing. Mike raised concerns about the API rate limits. Action item: Sarah will research alternative API providers by next Monday. Decision made: We will use Groq instead of Claude for AI features."
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Request Body (JSON)
```json
{
  "transcript": "Team standup meeting on Nov 12. John mentioned he will finish the user authentication module by Friday. Sarah reported that the database migration is complete and tested. We decided to move the launch date to December 1st to allow more time for testing. Mike raised concerns about the API rate limits. Action item: Sarah will research alternative API providers by next Monday. Decision made: We will use Groq instead of Claude for AI features."
}
```

### Expected Response (200 OK)
```json
{
  "note_id": "673d9e8f1a2b3c4d5e6f7g8h",
  "summary": "Team standup on Nov 12 discussed project progress. User authentication module is on track for Friday completion. Database migration completed successfully. Launch date postponed to December 1st for additional testing time.",
  "action_items": [
    {
      "text": "Finish the user authentication module",
      "owner": "John",
      "due_date": "Friday"
    },
    {
      "text": "Research alternative API providers",
      "owner": "Sarah",
      "due_date": "next Monday"
    }
  ],
  "decisions": [
    "Move launch date to December 1st",
    "Use Groq instead of Claude for AI features"
  ],
  "keywords": [
    "standup",
    "authentication",
    "database migration",
    "launch date",
    "API rate limits",
    "Groq"
  ],
  "created_at": "2025-11-12T10:30:00.000Z"
}
```

---

## 2. Get Note by ID (GET /api/notes/<note_id>)

### cURL
```powershell
curl http://localhost:5000/api/notes/673d9e8f1a2b3c4d5e6f7g8h
```

### Expected Response (200 OK)
Same structure as POST response above.

### Error Response (404 Not Found)
```json
{
  "error": "Note not found",
  "message": "No note exists with ID: 673d9e8f1a2b3c4d5e6f7g8h"
}
```

---

## 3. List All Notes (GET /api/notes)

### cURL (with pagination)
```powershell
# Get first 10 notes
curl "http://localhost:5000/api/notes?limit=10&skip=0"

# Get next 10 notes (page 2)
curl "http://localhost:5000/api/notes?limit=10&skip=10"
```

### Expected Response (200 OK)
```json
{
  "notes": [
    {
      "note_id": "673d9e8f1a2b3c4d5e6f7g8h",
      "summary": "...",
      "action_items": [...],
      "decisions": [...],
      "keywords": [...],
      "created_at": "2025-11-12T10:30:00.000Z"
    }
  ],
  "count": 1,
  "limit": 10,
  "skip": 0
}
```

---

## 4. Health Check (GET /api/notes/health)

### cURL
```powershell
curl http://localhost:5000/api/notes/health
```

### Expected Response (200 OK)
```json
{
  "status": "healthy",
  "services": {
    "llm": true,
    "storage": true
  }
}
```

---

## 5. List Available Models (GET /api/notes/models)

### cURL
```powershell
curl http://localhost:5000/api/notes/models
```

### Expected Response (200 OK)
```json
{
  "total_models": 4,
  "models": [
    {
      "name": "llama-3.3-70b-versatile",
      "display_name": "Llama 3.3 70B Versatile",
      "description": "Meta's latest Llama 3.3 70B - Best quality, 128K context, 32K output",
      "input_token_limit": 128000,
      "output_token_limit": 32768,
      "requests_per_minute": 30,
      "current": true
    }
  ],
  "current_model": "llama-3.3-70b-versatile",
  "rate_limits": {
    "free_tier_rpm": 30,
    "free_tier_rpd": 14400,
    "free_tier_tpm": 100000
  }
}
```

---

## 6. Test Model (GET or POST /api/notes/test)

### GET Request
```powershell
curl http://localhost:5000/api/notes/test
```

### POST Request (custom prompt)
```powershell
curl -X POST http://localhost:5000/api/notes/test `
  -H "Content-Type: application/json" `
  -d '{\"prompt\":\"What is 2+2?\"}'
```

### Expected Response (200 OK)
```json
{
  "status": "success",
  "model": "llama-3.3-70b-versatile",
  "test_prompt": "Hello, can you confirm you're working?",
  "response": "Yes, I'm working perfectly! How can I assist you today?",
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 15,
    "total_tokens": 27
  }
}
```

---

## Sample Transcripts for Testing

### Short Meeting
```json
{
  "transcript": "Quick sync with the design team. Alice will update the mockups by tomorrow. We approved the new color scheme."
}
```

### Medium Meeting
```json
{
  "transcript": "Product roadmap review meeting. Discussed Q4 priorities: 1) Complete user dashboard redesign, 2) Implement real-time notifications, 3) Add export functionality. Tom will lead the dashboard project starting next week. Lisa raised concerns about the notification system's performance impact. Decision: We'll use WebSockets instead of polling. Budget approved for additional cloud resources. Next review scheduled for November 20th."
}
```

### Long Meeting
```json
{
  "transcript": "Quarterly all-hands meeting. CEO presented company growth metrics: 150% revenue increase, 50 new clients onboarded. Engineering team highlighted the successful migration to microservices architecture. Sarah mentioned that customer satisfaction scores improved to 4.8/5. Marketing team discussed the upcoming product launch campaign scheduled for January. Action items: John will prepare detailed technical documentation by end of month. Emma will coordinate with external PR agency by Friday. Finance team will review budget allocation for Q1 2026. HR announced new benefits package starting December 1st. Decision made to expand the engineering team by 5 positions. Key challenges discussed: scaling infrastructure, maintaining code quality during rapid growth, improving cross-team communication. Upcoming milestones: Beta launch on December 15th, Full launch on January 15th, Post-launch review on February 1st."
}
```

---

## Testing Script (PowerShell)

Save this as `test_api.ps1`:

```powershell
# AutoNotes API Test Script

$baseUrl = "http://localhost:5000"

Write-Host "Testing AutoNotes API..." -ForegroundColor Green

# 1. Health Check
Write-Host "`n1. Health Check" -ForegroundColor Yellow
curl "$baseUrl/api/notes/health"

# 2. List Models
Write-Host "`n`n2. List Available Models" -ForegroundColor Yellow
curl "$baseUrl/api/notes/models"

# 3. Test Model
Write-Host "`n`n3. Test Model" -ForegroundColor Yellow
curl "$baseUrl/api/notes/test"

# 4. Generate Notes
Write-Host "`n`n4. Generate Notes" -ForegroundColor Yellow
$transcript = @{
    transcript = "Team meeting. John will finish report by Friday. Sarah approved budget. Launch date set for Dec 1st."
} | ConvertTo-Json

curl -X POST "$baseUrl/api/notes" `
  -H "Content-Type: application/json" `
  -d $transcript

# 5. List All Notes
Write-Host "`n`n5. List All Notes" -ForegroundColor Yellow
curl "$baseUrl/api/notes?limit=5"

Write-Host "`n`nAll tests completed!" -ForegroundColor Green
```

Run with: `.\test_api.ps1`
