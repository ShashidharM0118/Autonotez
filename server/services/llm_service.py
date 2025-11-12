"""
LLM service for generating structured meeting notes using Google Gemini API.
Handles API communication, prompt engineering, and response parsing.
"""

import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv

from utils.validators import validate_llm_response, ValidationError

# Load environment variables
load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# System prompt for structured note generation
SYSTEM_PROMPT = """
You are a concise meeting assistant.
Given a meeting transcript, return valid JSON with:
  summary: 2-3 sentence overview
  action_items: list of {text, owner (optional), due_date (optional)}
  decisions: list of decisions made
  keywords: list of 5 keywords
Respond ONLY with JSON.
"""


class LLMServiceError(Exception):
    """Custom exception for LLM service failures."""
    pass


def generate_notes(transcript: str) -> Dict[str, Any]:
    """
    Generate structured meeting notes from a transcript using Gemini API.
    
    Args:
        transcript: Raw meeting transcript text
        
    Returns:
        Dictionary containing parsed meeting notes with keys:
        - summary: str
        - action_items: List[Dict]
        - decisions: List[str]
        - keywords: List[str]
        
    Raises:
        LLMServiceError: If API call fails or response is invalid
        ValidationError: If response JSON doesn't match expected schema
    """
    if not GEMINI_API_KEY:
        raise LLMServiceError(
            "GEMINI_API_KEY not configured. Please set it in your .env file."
        )
    
    # Construct the prompt with system instructions and user transcript
    full_prompt = f"{SYSTEM_PROMPT}\n\nTranscript:\n{transcript}"
    
    # Prepare request payload for Gemini API
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,  # Lower temperature for more consistent JSON output
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add API key as query parameter (Gemini's preferred method)
    url = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
    
    try:
        # Make API request with timeout
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        
    except requests.exceptions.Timeout:
        raise LLMServiceError("Gemini API request timed out after 30 seconds")
    
    except requests.exceptions.ConnectionError:
        raise LLMServiceError("Failed to connect to Gemini API. Check your internet connection.")
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_msg = f"Gemini API returned error {status_code}"
        
        try:
            error_detail = e.response.json()
            if "error" in error_detail:
                error_msg += f": {error_detail['error'].get('message', 'Unknown error')}"
        except:
            pass
        
        raise LLMServiceError(error_msg)
    
    except requests.exceptions.RequestException as e:
        # Catch base requests exceptions and wrap
        raise LLMServiceError(f"Request to Gemini API failed: {str(e)}")

    except Exception as e:
        # Catch any unexpected exceptions (including those raised by mocks in tests)
        raise LLMServiceError(f"Request to Gemini API failed: {str(e)}")
    
    # Parse response
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        raise LLMServiceError("Gemini API returned invalid JSON response")
    
    # Extract generated text from Gemini's response structure
    try:
        candidates = response_json.get("candidates", [])
        if not candidates:
            raise LLMServiceError("Gemini API returned no candidates in response")
        
        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        
        if not parts:
            raise LLMServiceError("Gemini API returned no content parts")
        
        generated_text = parts[0].get("text", "")
        
        if not generated_text:
            raise LLMServiceError("Gemini API returned empty response text")
            
    except (KeyError, IndexError) as e:
        raise LLMServiceError(f"Unexpected Gemini API response structure: {str(e)}")
    
    # Parse the generated text as JSON
    try:
        # Clean potential markdown code blocks from response
        generated_text = generated_text.strip()
        if generated_text.startswith("```json"):
            generated_text = generated_text[7:]
        if generated_text.startswith("```"):
            generated_text = generated_text[3:]
        if generated_text.endswith("```"):
            generated_text = generated_text[:-3]
        
        generated_text = generated_text.strip()
        
        notes_data = json.loads(generated_text)
        
    except json.JSONDecodeError as e:
        raise LLMServiceError(
            f"Failed to parse LLM response as JSON. Error: {str(e)}. "
            f"Response text: {generated_text[:200]}"
        )
    
    # Validate the parsed JSON structure
    validate_llm_response(notes_data)
    
    return notes_data


def health_check() -> bool:
    """
    Check if Gemini API is accessible and API key is valid.
    
    Returns:
        True if service is healthy, False otherwise
    """
    if not GEMINI_API_KEY:
        return False
    
    try:
        # Make a minimal test request
        test_response = generate_notes("Test meeting: discussed project timeline.")
        return "summary" in test_response
    except:
        return False
