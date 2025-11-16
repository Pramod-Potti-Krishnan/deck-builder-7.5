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
    """Handle storage and retrieval of presentations with version history"""

    def __init__(self, storage_dir: str = "storage/presentations"):
        """Initialize storage with directory path"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Create version history directory
        self.versions_dir = Path("storage/versions")
        self.versions_dir.mkdir(parents=True, exist_ok=True)

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

    def _generate_version_id(self) -> str:
        """Generate unique version ID with timestamp"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"v_{timestamp}_{short_uuid}"

    def _get_version_dir(self, presentation_id: str) -> Path:
        """Get version directory for a presentation"""
        version_dir = self.versions_dir / presentation_id
        version_dir.mkdir(parents=True, exist_ok=True)
        return version_dir

    def _get_version_index_path(self, presentation_id: str) -> Path:
        """Get path to version index file"""
        return self._get_version_dir(presentation_id) / "index.json"

    def _update_version_index(
        self,
        presentation_id: str,
        version_id: str,
        created_by: str,
        change_summary: Optional[str]
    ):
        """Update version index with new version metadata"""
        index_path = self._get_version_index_path(presentation_id)

        # Load existing index or create new one
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {
                "presentation_id": presentation_id,
                "versions": []
            }

        # Add new version metadata
        version_metadata = {
            "version_id": version_id,
            "created_at": datetime.utcnow().isoformat(),
            "created_by": created_by,
            "change_summary": change_summary or "No description provided"
        }
        index["versions"].append(version_metadata)

        # Save updated index
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

    def save_version(
        self,
        presentation_id: str,
        presentation_data: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None
    ) -> str:
        """
        Save a version of the presentation to version history

        Args:
            presentation_id: Presentation ID
            presentation_data: Complete presentation data
            created_by: Who created this version
            change_summary: Brief description of changes

        Returns:
            version_id: Unique version identifier
        """
        version_id = self._generate_version_id()
        version_dir = self._get_version_dir(presentation_id)

        # Add version metadata to data
        versioned_data = presentation_data.copy()
        versioned_data["version_id"] = version_id
        versioned_data["versioned_at"] = datetime.utcnow().isoformat()

        # Save version file
        version_file = version_dir / f"{version_id}.json"
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(versioned_data, f, indent=2, ensure_ascii=False)

        # Update version index
        self._update_version_index(presentation_id, version_id, created_by, change_summary)

        return version_id

    def update(
        self,
        presentation_id: str,
        updates: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None,
        create_version: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing presentation with optional version tracking

        Args:
            presentation_id: Presentation ID to update
            updates: Dictionary of fields to update
            created_by: Who made the update
            change_summary: Description of changes
            create_version: Whether to create a version backup before updating

        Returns:
            updated_presentation: Updated presentation data, or None if not found
        """
        # Load current presentation
        current = self.load(presentation_id)
        if not current:
            return None

        # Create version backup if requested
        if create_version:
            self.save_version(
                presentation_id,
                current,
                created_by,
                change_summary or "Pre-update backup"
            )

        # Apply updates
        current.update(updates)
        current["updated_at"] = datetime.utcnow().isoformat()
        current["updated_by"] = created_by

        # Save updated presentation
        file_path = self._get_file_path(presentation_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(current, f, indent=2, ensure_ascii=False)

        return current

    def get_version_history(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get version history for a presentation

        Args:
            presentation_id: Presentation ID

        Returns:
            version_history: Dictionary with version metadata list, or None if no history
        """
        index_path = self._get_version_index_path(presentation_id)

        if not index_path.exists():
            return None

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading version history for {presentation_id}: {e}")
            return None

    def load_version(self, presentation_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific version of a presentation

        Args:
            presentation_id: Presentation ID
            version_id: Version ID to load

        Returns:
            version_data: Version data, or None if not found
        """
        version_dir = self._get_version_dir(presentation_id)
        version_file = version_dir / f"{version_id}.json"

        if not version_file.exists():
            return None

        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading version {version_id} for {presentation_id}: {e}")
            return None

    def restore_version(
        self,
        presentation_id: str,
        version_id: str,
        create_backup: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Restore a presentation to a specific version

        Args:
            presentation_id: Presentation ID
            version_id: Version ID to restore
            create_backup: Whether to backup current state before restoring

        Returns:
            restored_presentation: Restored presentation data, or None if version not found
        """
        # Load the version to restore
        version_data = self.load_version(presentation_id, version_id)
        if not version_data:
            return None

        # Create backup of current state if requested
        if create_backup:
            current = self.load(presentation_id)
            if current:
                self.save_version(
                    presentation_id,
                    current,
                    "system",
                    f"Pre-restore backup before reverting to {version_id}"
                )

        # Restore the version (remove version metadata fields)
        restored = version_data.copy()
        restored.pop("version_id", None)
        restored.pop("versioned_at", None)
        restored["updated_at"] = datetime.utcnow().isoformat()
        restored["restored_from"] = version_id

        # Save as current presentation
        file_path = self._get_file_path(presentation_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(restored, f, indent=2, ensure_ascii=False)

        return restored


# Global storage instance
storage = PresentationStorage()
