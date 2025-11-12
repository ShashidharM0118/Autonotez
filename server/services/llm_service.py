"""
LLM service for generating structured meeting notes using Groq API.
Handles API communication, prompt engineering, and response parsing.
"""

import os
import json
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

from utils.validators import validate_llm_response, ValidationError

# Load environment variables
load_dotenv()

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"  # Latest Llama 3.3 70B model (best quality)

# System prompt for structured note generation
SYSTEM_PROMPT = """You are a concise meeting assistant.
Given a meeting transcript, return valid JSON with:
  summary: 2-3 sentence overview
  action_items: list of {text, owner (optional), due_date (optional)}
  decisions: list of decisions made
  keywords: list of 5 keywords
Respond ONLY with JSON, no markdown formatting or code blocks."""


class LLMServiceError(Exception):
    """Custom exception for LLM service failures."""
    pass


def generate_notes(transcript: str) -> Dict[str, Any]:
    """
    Generate structured meeting notes from a transcript using Groq API.
    
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
    if not GROQ_API_KEY:
        raise LLMServiceError(
            "GROQ_API_KEY not configured. Please set it in your .env file."
        )
    
    # Prepare request payload for Groq API (OpenAI-compatible format)
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"Transcript:\n{transcript}"
            }
        ],
        "temperature": 0.3,  # Lower temperature for consistent JSON output
        "max_tokens": 2048,
        "response_format": {"type": "json_object"}  # Force JSON response
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    try:
        # Make API request with timeout
        response = requests.post(
            GROQ_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check for HTTP errors
        response.raise_for_status()
        
    except requests.exceptions.Timeout:
        raise LLMServiceError("Groq API request timed out after 30 seconds")
    
    except requests.exceptions.ConnectionError:
        raise LLMServiceError("Failed to connect to Groq API. Check your internet connection.")
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_msg = f"Groq API returned error {status_code}"
        
        try:
            error_detail = e.response.json()
            if "error" in error_detail:
                error_msg += f": {error_detail['error'].get('message', 'Unknown error')}"
        except:
            pass
        
        raise LLMServiceError(error_msg)
    
    except requests.exceptions.RequestException as e:
        # Catch base requests exceptions and wrap
        raise LLMServiceError(f"Request to Groq API failed: {str(e)}")

    except Exception as e:
        # Catch any unexpected exceptions
        raise LLMServiceError(f"Request to Groq API failed: {str(e)}")
    
    # Parse response
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        raise LLMServiceError("Groq API returned invalid JSON response")
    
    # Extract generated text from Groq's OpenAI-compatible response structure
    try:
        choices = response_json.get("choices", [])
        if not choices:
            raise LLMServiceError("Groq API returned no choices in response")
        
        message = choices[0].get("message", {})
        generated_text = message.get("content", "")
        
        if not generated_text:
            raise LLMServiceError("Groq API returned empty response text")
            
    except (KeyError, IndexError) as e:
        raise LLMServiceError(f"Unexpected Groq API response structure: {str(e)}")
    
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
    Check if Groq API is accessible and API key is valid.
    
    Returns:
        True if service is healthy, False otherwise
    """
    if not GROQ_API_KEY:
        return False
    
    try:
        # Make a minimal test request
        test_response = generate_notes("Test meeting: discussed project timeline.")
        return "summary" in test_response
    except:
        return False


def list_available_models() -> Dict[str, Any]:
    """
    List available Groq models and their capabilities.
    
    Returns:
        Dictionary containing list of available Groq models with capabilities
        
    Note:
        Returns static list of popular Groq models as Groq doesn't provide
        a models list API endpoint yet.
    """
    if not GROQ_API_KEY:
        raise LLMServiceError(
            "GROQ_API_KEY not configured. Please set it in your .env file."
        )
    
    # Groq models (open-source models with fast inference)
    groq_models = [
        {
            "name": "llama-3.3-70b-versatile",
            "display_name": "Llama 3.3 70B Versatile",
            "description": "Meta's latest Llama 3.3 70B - Best quality, 128K context, 32K output",
            "input_token_limit": 128000,
            "output_token_limit": 32768,
            "requests_per_minute": 30,
            "current": GROQ_MODEL == "llama-3.3-70b-versatile"
        },
        {
            "name": "llama-3.1-70b-versatile",
            "display_name": "Llama 3.1 70B Versatile",
            "description": "Meta's Llama 3.1 70B - High quality, 128K context, 32K output",
            "input_token_limit": 128000,
            "output_token_limit": 32768,
            "requests_per_minute": 30,
            "current": GROQ_MODEL == "llama-3.1-70b-versatile"
        },
        {
            "name": "mixtral-8x7b-32768",
            "display_name": "Mixtral 8x7B",
            "description": "Mistral's MoE model - Fast inference, 32K context",
            "input_token_limit": 32768,
            "output_token_limit": 32768,
            "requests_per_minute": 30,
            "current": GROQ_MODEL == "mixtral-8x7b-32768"
        },
        {
            "name": "gemma2-9b-it",
            "display_name": "Gemma 2 9B IT",
            "description": "Google's Gemma 2 9B instruction-tuned - Lightweight, 8K context",
            "input_token_limit": 8192,
            "output_token_limit": 8192,
            "requests_per_minute": 30,
            "current": GROQ_MODEL == "gemma2-9b-it"
        }
    ]
    
    return {
        "total_models": len(groq_models),
        "models": groq_models,
        "current_model": GROQ_MODEL,
        "rate_limits": {
            "free_tier_rpm": 30,
            "free_tier_rpd": 14400,
            "free_tier_tpm": 100000
        }
    }


def test_model(test_prompt: str = "Hello, can you confirm you're working?") -> Dict[str, Any]:
    """
    Test the current Groq model with a simple prompt.
    
    Args:
        test_prompt: Simple test prompt to send to the model
        
    Returns:
        Dictionary with test results and model response
        
    Raises:
        LLMServiceError: If test fails
    """
    if not GROQ_API_KEY:
        raise LLMServiceError(
            "GROQ_API_KEY not configured. Please set it in your .env file."
        )
    
    payload = {
        "model": GROQ_MODEL,
        "max_tokens": 256,
        "messages": [
            {
                "role": "user",
                "content": test_prompt
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    try:
        response = requests.post(
            GROQ_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        
        response_json = response.json()
        
        # Extract response from Groq API (OpenAI-compatible format)
        choices = response_json.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            response_text = message.get("content", "")
            
            return {
                "status": "success",
                "model": GROQ_MODEL,
                "test_prompt": test_prompt,
                "response": response_text,
                "usage": response_json.get("usage", {})
            }
        
        return {
            "status": "error",
            "message": "No response from model",
            "full_response": response_json
        }
        
    except requests.exceptions.RequestException as e:
        raise LLMServiceError(f"Model test failed: {str(e)}")
    except Exception as e:
        raise LLMServiceError(f"Unexpected error testing model: {str(e)}")

