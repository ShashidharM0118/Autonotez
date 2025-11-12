"""
Storage service for persisting meeting notes in MongoDB.
Provides CRUD operations with connection pooling and error handling.
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure, 
    ServerSelectionTimeoutError,
    DuplicateKeyError,
    PyMongoError
)
from bson import ObjectId
from dotenv import load_dotenv

from models.note_model import Note, ActionItem

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = "autonotes"
COLLECTION_NAME = "notes"

# Global client instance (connection pooling)
_mongo_client: Optional[MongoClient] = None


class StorageServiceError(Exception):
    """Custom exception for storage service failures."""
    pass


def get_mongo_client() -> MongoClient:
    """
    Get or create MongoDB client with connection pooling.
    
    Returns:
        MongoClient instance
        
    Raises:
        StorageServiceError: If connection cannot be established
    """
    global _mongo_client
    
    if _mongo_client is None:
        if not MONGO_URI:
            raise StorageServiceError(
                "MONGO_URI not configured. Please set it in your .env file."
            )
        
        try:
            # Create client with connection pooling and timeout settings
            _mongo_client = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,  # 10 second connection timeout
                maxPoolSize=50,  # Connection pool size
                retryWrites=True
            )
            
            # Verify connection by pinging the server
            _mongo_client.admin.command('ping')
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            raise StorageServiceError(
                f"Failed to connect to MongoDB: {str(e)}"
            )
        except Exception as e:
            raise StorageServiceError(
                f"Unexpected error connecting to MongoDB: {str(e)}"
            )
    
    return _mongo_client


def get_collection():
    """
    Get the notes collection from MongoDB.
    
    Returns:
        pymongo.collection.Collection instance
    """
    client = get_mongo_client()
    database = client[DATABASE_NAME]
    return database[COLLECTION_NAME]


def save_note(note_data: Dict[str, Any]) -> str:
    """
    Save a meeting note to MongoDB.
    
    Args:
        note_data: Dictionary containing note fields (summary, action_items, etc.)
        
    Returns:
        String representation of the inserted document's ObjectId
        
    Raises:
        StorageServiceError: If save operation fails
    """
    try:
        collection = get_collection()
        
        # Add timestamp if not present
        if "created_at" not in note_data:
            note_data["created_at"] = datetime.utcnow()
        
        # Insert document
        result = collection.insert_one(note_data)
        
        if not result.inserted_id:
            raise StorageServiceError("Failed to insert note: no ID returned")
        
        return str(result.inserted_id)
        
    except DuplicateKeyError:
        raise StorageServiceError("Duplicate note entry detected")
    
    except PyMongoError as e:
        raise StorageServiceError(f"Database error while saving note: {str(e)}")
    
    except Exception as e:
        raise StorageServiceError(f"Unexpected error saving note: {str(e)}")


def get_note_by_id(note_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a meeting note by its ID.
    
    Args:
        note_id: String representation of the note's ObjectId
        
    Returns:
        Dictionary containing note data, or None if not found
        
    Raises:
        StorageServiceError: If retrieval operation fails
    """
    try:
        # Validate ObjectId format
        try:
            object_id = ObjectId(note_id)
        except Exception:
            raise StorageServiceError(f"Invalid note ID format: {note_id}")
        
        collection = get_collection()
        
        # Find document by ID
        note_doc = collection.find_one({"_id": object_id})
        
        if not note_doc:
            return None
        
        # Convert ObjectId to string for JSON serialization
        note_doc["note_id"] = str(note_doc.pop("_id"))
        
        return note_doc
        
    except StorageServiceError:
        raise
    
    except PyMongoError as e:
        raise StorageServiceError(f"Database error while retrieving note: {str(e)}")
    
    except Exception as e:
        raise StorageServiceError(f"Unexpected error retrieving note: {str(e)}")


def get_all_notes(limit: int = 50, skip: int = 0) -> list[Dict[str, Any]]:
    """
    Retrieve multiple notes with pagination.
    
    Args:
        limit: Maximum number of notes to return (default 50)
        skip: Number of notes to skip for pagination (default 0)
        
    Returns:
        List of note dictionaries, sorted by creation date (newest first)
        
    Raises:
        StorageServiceError: If retrieval operation fails
    """
    try:
        collection = get_collection()
        
        # Query with pagination and sorting
        cursor = collection.find().sort("created_at", -1).skip(skip).limit(limit)
        
        notes = []
        for note_doc in cursor:
            # Convert ObjectId to string
            note_doc["note_id"] = str(note_doc.pop("_id"))
            notes.append(note_doc)
        
        return notes
        
    except PyMongoError as e:
        raise StorageServiceError(f"Database error while retrieving notes: {str(e)}")
    
    except Exception as e:
        raise StorageServiceError(f"Unexpected error retrieving notes: {str(e)}")


def delete_note_by_id(note_id: str) -> bool:
    """
    Delete a meeting note by its ID.
    
    Args:
        note_id: String representation of the note's ObjectId
        
    Returns:
        True if note was deleted, False if not found
        
    Raises:
        StorageServiceError: If delete operation fails
    """
    try:
        # Validate ObjectId format
        try:
            object_id = ObjectId(note_id)
        except Exception:
            raise StorageServiceError(f"Invalid note ID format: {note_id}")
        
        collection = get_collection()
        
        # Delete document
        result = collection.delete_one({"_id": object_id})
        
        return result.deleted_count > 0
        
    except PyMongoError as e:
        raise StorageServiceError(f"Database error while deleting note: {str(e)}")
    
    except Exception as e:
        raise StorageServiceError(f"Unexpected error deleting note: {str(e)}")


def close_connection() -> None:
    """
    Close MongoDB connection. Should be called on application shutdown.
    """
    global _mongo_client
    
    if _mongo_client is not None:
        _mongo_client.close()
        _mongo_client = None


def health_check() -> bool:
    """
    Check if MongoDB connection is healthy.
    
    Returns:
        True if connection is working, False otherwise
    """
    try:
        client = get_mongo_client()
        client.admin.command('ping')
        return True
    except:
        return False
