"""
Simple file-based storage for presentations.
Stores each presentation as a JSON file with UUID filename.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class PresentationStorage:
    """Handle storage and retrieval of presentations"""

    def __init__(self, storage_dir: str = "storage/presentations"):
        """Initialize storage with directory path"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def generate_id(self) -> str:
        """Generate unique presentation ID"""
        return str(uuid.uuid4())

    def _get_file_path(self, presentation_id: str) -> Path:
        """Get file path for a presentation ID"""
        return self.storage_dir / f"{presentation_id}.json"

    def save(self, presentation_data: Dict[str, Any]) -> str:
        """
        Save a presentation and return its ID

        Args:
            presentation_data: Dictionary containing presentation data

        Returns:
            presentation_id: Unique ID for the saved presentation
        """
        # Generate unique ID
        presentation_id = self.generate_id()

        # Add metadata
        presentation_data["id"] = presentation_id
        presentation_data["created_at"] = datetime.utcnow().isoformat()

        # Save to file
        file_path = self._get_file_path(presentation_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(presentation_data, f, indent=2, ensure_ascii=False)

        return presentation_id

    def load(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a presentation by ID

        Args:
            presentation_id: Unique presentation ID

        Returns:
            presentation_data: Dictionary containing presentation data, or None if not found
        """
        file_path = self._get_file_path(presentation_id)

        if not file_path.exists():
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading presentation {presentation_id}: {e}")
            return None

    def delete(self, presentation_id: str) -> bool:
        """
        Delete a presentation by ID

        Args:
            presentation_id: Unique presentation ID

        Returns:
            success: True if deleted, False if not found
        """
        file_path = self._get_file_path(presentation_id)

        if not file_path.exists():
            return False

        try:
            file_path.unlink()
            return True
        except IOError as e:
            print(f"Error deleting presentation {presentation_id}: {e}")
            return False

    def list_all(self) -> list[str]:
        """
        List all presentation IDs

        Returns:
            ids: List of all presentation IDs
        """
        return [f.stem for f in self.storage_dir.glob("*.json")]


# Global storage instance
storage = PresentationStorage()
