# AutoNotes API Test Script for PowerShell
# Make sure the Flask server is running before executing this script

Write-Host "=== AutoNotes API Test ===" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:5000"

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/api/notes/health" -Method Get
    Write-Host "✓ Health Check Passed" -ForegroundColor Green
    $health | ConvertTo-Json -Depth 10
} catch {
    Write-Host "✗ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 2: List Models
Write-Host "2. Testing List Models..." -ForegroundColor Yellow
try {
    $models = Invoke-RestMethod -Uri "$baseUrl/api/notes/models" -Method Get
    Write-Host "✓ Models Retrieved" -ForegroundColor Green
    $models | ConvertTo-Json -Depth 10
} catch {
    Write-Host "✗ List Models Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 3: Test Model
Write-Host "3. Testing Model..." -ForegroundColor Yellow
try {
    $testResult = Invoke-RestMethod -Uri "$baseUrl/api/notes/test" -Method Get
    Write-Host "✓ Model Test Passed" -ForegroundColor Green
    $testResult | ConvertTo-Json -Depth 10
} catch {
    Write-Host "✗ Model Test Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n---`n"

# Test 4: Generate Notes
Write-Host "4. Testing Note Generation..." -ForegroundColor Yellow
try {
    $transcript = @{
        transcript = "Team standup meeting on Nov 12. John will finish the authentication module by Friday. Sarah completed the database migration and testing. We decided to move the launch date to December 1st for additional testing. Mike raised concerns about API rate limits. Action: Sarah will research alternative API providers by Monday. Decision: Use Groq instead of Claude for AI features."
    } | ConvertTo-Json
    
    $note = Invoke-RestMethod -Uri "$baseUrl/api/notes" -Method Post -Body $transcript -ContentType "application/json"
    Write-Host "✓ Note Generated Successfully" -ForegroundColor Green
    Write-Host "Note ID: $($note.note_id)" -ForegroundColor Cyan
    $note | ConvertTo-Json -Depth 10
    
    # Save note ID for next test
    $global:lastNoteId = $note.note_id
} catch {
    Write-Host "✗ Note Generation Failed: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}

Write-Host "`n---`n"

# Test 5: Get Note by ID
if ($global:lastNoteId) {
    Write-Host "5. Testing Get Note by ID..." -ForegroundColor Yellow
    try {
        $retrievedNote = Invoke-RestMethod -Uri "$baseUrl/api/notes/$($global:lastNoteId)" -Method Get
        Write-Host "✓ Note Retrieved Successfully" -ForegroundColor Green
        $retrievedNote | ConvertTo-Json -Depth 10
    } catch {
        Write-Host "✗ Get Note Failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host "`n---`n"
}

# Test 6: List All Notes
Write-Host "6. Testing List All Notes..." -ForegroundColor Yellow
try {
    $allNotes = Invoke-RestMethod -Uri "$baseUrl/api/notes?limit=5" -Method Get
    Write-Host "✓ Notes List Retrieved" -ForegroundColor Green
    Write-Host "Total Notes: $($allNotes.count)" -ForegroundColor Cyan
    $allNotes | ConvertTo-Json -Depth 10
} catch {
    Write-Host "✗ List Notes Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== All Tests Completed ===" -ForegroundColor Cyan
