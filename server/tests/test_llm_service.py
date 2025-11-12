"""
Unit tests for LLM service.
Tests the Gemini API integration with mocked responses.
"""

import json
import pytest
from unittest.mock import patch, Mock

from services.llm_service import generate_notes, LLMServiceError
from utils.validators import ValidationError


class TestGenerateNotes:
    """Test suite for the generate_notes function."""
    
    def test_generate_notes_success(self):
        """Test successful note generation with valid API response."""
        # Mock successful Gemini API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "summary": "Team discussed Q4 goals and project timeline. Key milestones were identified for the upcoming sprint.",
                                    "action_items": [
                                        {
                                            "text": "Create detailed project roadmap",
                                            "owner": "John",
                                            "due_date": "2025-11-20"
                                        },
                                        {
                                            "text": "Schedule follow-up meeting",
                                            "owner": "Sarah"
                                        }
                                    ],
                                    "decisions": [
                                        "Launch date set for December 1st",
                                        "Budget approved for additional resources"
                                    ],
                                    "keywords": ["Q4", "goals", "timeline", "sprint", "milestones"]
                                })
                            }
                        ]
                    }
                }
            ]
        }
        
        with patch('services.llm_service.requests.post', return_value=mock_response):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                result = generate_notes("Mock meeting transcript about Q4 planning")
                
                # Assertions
                assert "summary" in result
                assert isinstance(result["summary"], str)
                assert len(result["summary"]) > 0
                
                assert "action_items" in result
                assert isinstance(result["action_items"], list)
                assert len(result["action_items"]) == 2
                
                assert "decisions" in result
                assert isinstance(result["decisions"], list)
                assert len(result["decisions"]) == 2
                
                assert "keywords" in result
                assert isinstance(result["keywords"], list)
                assert len(result["keywords"]) == 5
    
    def test_generate_notes_with_markdown_code_blocks(self):
        """Test parsing when LLM wraps JSON in markdown code blocks."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "```json\n" + json.dumps({
                                    "summary": "Brief meeting summary",
                                    "action_items": [{"text": "Follow up on tasks"}],
                                    "decisions": ["Approved proposal"],
                                    "keywords": ["meeting", "tasks", "proposal", "team", "project"]
                                }) + "\n```"
                            }
                        ]
                    }
                }
            ]
        }
        
        with patch('services.llm_service.requests.post', return_value=mock_response):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                result = generate_notes("Test transcript")
                
                assert "summary" in result
                assert result["summary"] == "Brief meeting summary"
    
    def test_generate_notes_missing_api_key(self):
        """Test error handling when API key is not configured."""
        with patch('services.llm_service.GEMINI_API_KEY', None):
            with pytest.raises(LLMServiceError) as exc_info:
                generate_notes("Test transcript")
            
            assert "GEMINI_API_KEY not configured" in str(exc_info.value)
    
    def test_generate_notes_api_timeout(self):
        """Test error handling for API timeout."""
        with patch('services.llm_service.requests.post', side_effect=Exception("Timeout")):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                with pytest.raises(LLMServiceError):
                    generate_notes("Test transcript")
    
    def test_generate_notes_invalid_json_response(self):
        """Test error handling when LLM returns invalid JSON."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "This is not valid JSON"
                            }
                        ]
                    }
                }
            ]
        }
        
        with patch('services.llm_service.requests.post', return_value=mock_response):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                with pytest.raises(LLMServiceError) as exc_info:
                    generate_notes("Test transcript")
                
                assert "Failed to parse LLM response as JSON" in str(exc_info.value)
    
    def test_generate_notes_missing_required_fields(self):
        """Test error handling when LLM response is missing required fields."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": json.dumps({
                                    "summary": "Only has summary field"
                                    # Missing action_items, decisions, keywords
                                })
                            }
                        ]
                    }
                }
            ]
        }
        
        with patch('services.llm_service.requests.post', return_value=mock_response):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                with pytest.raises(ValidationError) as exc_info:
                    generate_notes("Test transcript")
                
                assert "missing required field" in str(exc_info.value)
    
    def test_generate_notes_http_error(self):
        """Test error handling for HTTP errors from API."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {
                "message": "Invalid API key"
            }
        }
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        
        with patch('services.llm_service.requests.post', return_value=mock_response):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                with pytest.raises(LLMServiceError):
                    generate_notes("Test transcript")
    
    def test_generate_notes_empty_response(self):
        """Test error handling when API returns empty response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": []
        }
        
        with patch('services.llm_service.requests.post', return_value=mock_response):
            with patch('services.llm_service.GEMINI_API_KEY', 'test-api-key'):
                with pytest.raises(LLMServiceError) as exc_info:
                    generate_notes("Test transcript")
                
                assert "no candidates" in str(exc_info.value).lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
