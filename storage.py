"""
Hybrid storage for presentations with Supabase + Filesystem fallback

Architecture:
- Primary: Supabase (PostgreSQL + Storage) - persistent across restarts
- Fallback: Filesystem - ephemeral but always available

This provides graceful degradation: if Supabase is unavailable or misconfigured,
the system automatically falls back to filesystem storage.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from config import get_settings
from logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# ==================== Filesystem Storage (Fallback) ====================

class FilesystemPresentationStorage:
    """
    File-based storage for presentations (fallback/development)

    Stores presentations as JSON files in local filesystem.
    ⚠️ WARNING: Ephemeral on Railway - data lost on restart!
    """

    def __init__(self, storage_dir: str = "storage/presentations"):
        """Initialize filesystem storage"""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Create version history directory
        self.versions_dir = Path("storage/versions")
        self.versions_dir.mkdir(parents=True, exist_ok=True)

        logger.info("Filesystem storage initialized",
                   storage_dir=str(self.storage_dir),
                   versions_dir=str(self.versions_dir))

    def generate_id(self) -> str:
        """Generate unique presentation ID"""
        return str(uuid.uuid4())

    def _get_file_path(self, presentation_id: str) -> Path:
        """Get file path for a presentation ID"""
        return self.storage_dir / f"{presentation_id}.json"

    async def save(self, presentation_data: Dict[str, Any]) -> str:
        """Save a presentation and return its ID"""
        presentation_id = self.generate_id()

        # Add metadata
        presentation_data["id"] = presentation_id
        presentation_data["created_at"] = datetime.utcnow().isoformat()

        # Save to file
        file_path = self._get_file_path(presentation_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(presentation_data, f, indent=2, ensure_ascii=False)

        logger.info("Saved to filesystem",
                   presentation_id=presentation_id,
                   path=str(file_path))

        return presentation_id

    async def load(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """Load a presentation by ID"""
        file_path = self._get_file_path(presentation_id)

        if not file_path.exists():
            logger.warning("Presentation not found in filesystem",
                         presentation_id=presentation_id)
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info("Loaded from filesystem", presentation_id=presentation_id)
            return data
        except (json.JSONDecodeError, IOError) as e:
            logger.error("Failed to load from filesystem",
                        presentation_id=presentation_id,
                        error=str(e))
            return None

    async def delete(self, presentation_id: str) -> bool:
        """Delete a presentation by ID"""
        file_path = self._get_file_path(presentation_id)

        if not file_path.exists():
            return False

        try:
            file_path.unlink()
            logger.info("Deleted from filesystem", presentation_id=presentation_id)
            return True
        except IOError as e:
            logger.error("Failed to delete from filesystem",
                        presentation_id=presentation_id,
                        error=str(e))
            return False

    async def list_all(self) -> List[str]:
        """List all presentation IDs"""
        ids = [f.stem for f in self.storage_dir.glob("*.json")]
        logger.info("Listed filesystem presentations", count=len(ids))
        return ids

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

    async def save_version(
        self,
        presentation_id: str,
        presentation_data: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None
    ) -> str:
        """Save a version of the presentation to version history"""
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

        logger.info("Version saved to filesystem",
                   presentation_id=presentation_id,
                   version_id=version_id)

        return version_id

    async def update(
        self,
        presentation_id: str,
        updates: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None,
        create_version: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Update an existing presentation with optional version tracking"""
        # Load current presentation
        current = await self.load(presentation_id)
        if not current:
            return None

        # Create version backup if requested
        if create_version:
            await self.save_version(
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

        logger.info("Updated in filesystem",
                   presentation_id=presentation_id,
                   created_by=created_by)

        return current

    async def get_version_history(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """Get version history for a presentation"""
        index_path = self._get_version_index_path(presentation_id)

        if not index_path.exists():
            return None

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error("Failed to load version history",
                        presentation_id=presentation_id,
                        error=str(e))
            return None

    async def load_version(self, presentation_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """Load a specific version of a presentation"""
        version_dir = self._get_version_dir(presentation_id)
        version_file = version_dir / f"{version_id}.json"

        if not version_file.exists():
            return None

        try:
            with open(version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error("Failed to load version",
                        presentation_id=presentation_id,
                        version_id=version_id,
                        error=str(e))
            return None

    async def restore_version(
        self,
        presentation_id: str,
        version_id: str,
        create_backup: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Restore a presentation to a specific version"""
        # Load the version to restore
        version_data = await self.load_version(presentation_id, version_id)
        if not version_data:
            return None

        # Create backup of current state if requested
        if create_backup:
            current = await self.load(presentation_id)
            if current:
                await self.save_version(
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

        logger.info("Version restored in filesystem",
                   presentation_id=presentation_id,
                   version_id=version_id)

        return restored


# ==================== Hybrid Storage Wrapper ====================

class HybridPresentationStorage:
    """
    Hybrid storage wrapper with Supabase primary + Filesystem fallback

    Behavior:
    1. If Supabase configured: Use Supabase for all operations
    2. If Supabase fails: Automatically fall back to filesystem
    3. If Supabase not configured: Use filesystem only

    This ensures the service is always available, even if Supabase is down.
    """

    def __init__(self):
        """Initialize hybrid storage with automatic backend selection"""
        settings = get_settings()

        # Determine storage backend
        self.backend_type = settings.get_storage_backend()

        logger.info("Initializing hybrid storage", backend=self.backend_type)

        # Initialize filesystem storage (always available as fallback)
        self.filesystem = FilesystemPresentationStorage(settings.STORAGE_DIR)

        # Initialize Supabase storage (if configured)
        self.supabase = None
        if self.backend_type == "supabase":
            try:
                from storage_supabase import SupabasePresentationStorage
                self.supabase = SupabasePresentationStorage()
                logger.info("Supabase storage initialized successfully")
            except Exception as e:
                logger.warning(
                    "Supabase initialization failed, falling back to filesystem",
                    error=str(e)
                )
                self.backend_type = "filesystem"

        # Log final configuration
        logger.info(
            "Hybrid storage ready",
            primary_backend=self.backend_type,
            fallback="filesystem" if self.supabase else "none"
        )

    def _get_backend(self):
        """Get current storage backend (Supabase or filesystem)"""
        return self.supabase if self.supabase else self.filesystem

    def _with_fallback(self, operation_name: str):
        """
        Decorator-like pattern for operations with Supabase -> filesystem fallback

        If Supabase operation fails, automatically retry with filesystem
        """
        async def wrapper(*args, **kwargs):
            backend = self._get_backend()
            method = getattr(backend, operation_name)

            try:
                result = await method(*args, **kwargs)
                return result
            except Exception as e:
                # If we were using Supabase and it failed, fall back to filesystem
                if self.supabase and backend == self.supabase:
                    logger.warning(
                        f"Supabase {operation_name} failed, falling back to filesystem",
                        error=str(e)
                    )
                    filesystem_method = getattr(self.filesystem, operation_name)
                    return await filesystem_method(*args, **kwargs)
                else:
                    # Already using filesystem or filesystem also failed
                    raise

        return wrapper

    # ==================== Public API (delegates to backend with fallback) ====================

    def generate_id(self) -> str:
        """Generate unique presentation ID"""
        return self._get_backend().generate_id()

    async def save(self, presentation_data: Dict[str, Any]) -> str:
        """Save presentation (Supabase with filesystem fallback)"""
        return await self._with_fallback("save")(presentation_data)

    async def load(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """Load presentation (Supabase with filesystem fallback)"""
        return await self._with_fallback("load")(presentation_id)

    async def delete(self, presentation_id: str) -> bool:
        """Delete presentation (Supabase with filesystem fallback)"""
        return await self._with_fallback("delete")(presentation_id)

    async def list_all(self) -> List[str]:
        """List all presentations (Supabase with filesystem fallback)"""
        return await self._with_fallback("list_all")()

    async def save_version(
        self,
        presentation_id: str,
        presentation_data: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None
    ) -> str:
        """Save version (Supabase with filesystem fallback)"""
        return await self._with_fallback("save_version")(
            presentation_id, presentation_data, created_by, change_summary
        )

    async def update(
        self,
        presentation_id: str,
        updates: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None,
        create_version: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Update presentation (Supabase with filesystem fallback)"""
        return await self._with_fallback("update")(
            presentation_id, updates, created_by, change_summary, create_version
        )

    async def get_version_history(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """Get version history (Supabase with filesystem fallback)"""
        return await self._with_fallback("get_version_history")(presentation_id)

    async def load_version(self, presentation_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """Load specific version (Supabase with filesystem fallback)"""
        return await self._with_fallback("load_version")(presentation_id, version_id)

    async def restore_version(
        self,
        presentation_id: str,
        version_id: str,
        create_backup: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Restore version (Supabase with filesystem fallback)"""
        return await self._with_fallback("restore_version")(
            presentation_id, version_id, create_backup
        )


# ==================== Global Storage Instance ====================

# Create global hybrid storage instance (used by server.py)
storage = HybridPresentationStorage()


# ==================== Compatibility Alias ====================

# For backward compatibility with existing code
PresentationStorage = HybridPresentationStorage
