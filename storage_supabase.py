"""
Supabase-based storage for presentations with PostgreSQL + Storage backend

Architecture:
- Tier 1: Supabase PostgreSQL (metadata + primary storage)
- Tier 2: Supabase Storage (backup JSON files)
- Tier 3: Local cache (in-memory, optional)

This replaces the ephemeral filesystem storage with persistent Supabase storage.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from pathlib import Path

from supabase import create_client, Client
from config import get_settings
from logger import get_storage_logger

# Initialize logger
logger = get_storage_logger()


class SupabaseStorageError(Exception):
    """Custom exception for Supabase storage errors"""
    pass


class LocalCache:
    """
    Simple in-memory cache for presentations

    Reduces Supabase queries for frequently accessed presentations
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """
        Initialize cache

        Args:
            max_size: Maximum number of presentations to cache
            ttl_seconds: Time-to-live for cache entries
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.timestamps: Dict[str, datetime] = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        logger.info("Cache initialized", max_size=max_size, ttl_seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Get item from cache if not expired"""
        if key not in self.cache:
            logger.debug("Cache miss", key=key)
            return None

        # Check expiration
        if datetime.utcnow() - self.timestamps[key] > timedelta(seconds=self.ttl_seconds):
            self.invalidate(key)
            logger.debug("Cache expired", key=key)
            return None

        logger.debug("Cache hit", key=key)
        return self.cache[key]

    def set(self, key: str, value: Dict[str, Any]):
        """Set item in cache with LRU eviction if needed"""
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            self.invalidate(oldest_key)
            logger.debug("Cache eviction", evicted_key=oldest_key)

        self.cache[key] = value
        self.timestamps[key] = datetime.utcnow()
        logger.debug("Cache set", key=key)

    def invalidate(self, key: str):
        """Remove item from cache"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
        logger.debug("Cache invalidated", key=key)

    def clear(self):
        """Clear entire cache"""
        count = len(self.cache)
        self.cache.clear()
        self.timestamps.clear()
        logger.info("Cache cleared", cleared_count=count)


class SupabasePresentationStorage:
    """
    Supabase-based presentation storage with PostgreSQL + Storage + Cache

    Storage Architecture:
    1. PostgreSQL tables:
       - presentations: Current state with metadata
       - presentation_versions: Version history
    2. Storage bucket:
       - presentation-data/presentations/{id}.json: Backup files
       - presentation-data/versions/{id}/{version_id}.json: Version backups
    3. Local cache: In-memory for frequently accessed presentations
    """

    def __init__(self):
        """Initialize Supabase storage with PostgreSQL, Storage, and Cache"""
        settings = get_settings()

        # Validate Supabase configuration
        if not settings.is_supabase_configured():
            error_msg = "Supabase not configured. Set SUPABASE_URL and SUPABASE_SERVICE_KEY"
            logger.error("Initialization failed", reason=error_msg)
            raise SupabaseStorageError(error_msg)

        try:
            # Initialize Supabase client
            self.client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY
            )
            self.bucket = settings.SUPABASE_BUCKET

            logger.info(
                "Supabase client initialized",
                url=settings.SUPABASE_URL,
                bucket=self.bucket
            )

            # Initialize cache if enabled
            self.cache: Optional[LocalCache] = None
            if settings.ENABLE_LOCAL_CACHE:
                self.cache = LocalCache(
                    max_size=settings.MAX_CACHE_SIZE,
                    ttl_seconds=settings.CACHE_TTL_SECONDS
                )
                logger.info("Cache enabled",
                          max_size=settings.MAX_CACHE_SIZE,
                          ttl=settings.CACHE_TTL_SECONDS)

            # Verify Supabase connection
            self._verify_connection()

        except Exception as e:
            logger.error("Supabase initialization failed", error=str(e), exc_info=True)
            raise SupabaseStorageError(f"Failed to initialize Supabase: {e}")

    def _verify_connection(self):
        """Verify Supabase connection and table existence"""
        try:
            # Test PostgreSQL connection
            result = self.client.table("ls_presentations").select("id").limit(1).execute()
            logger.info("PostgreSQL connection verified", table="ls_presentations")

            # Test Storage bucket access
            self.client.storage.from_(self.bucket).list()
            logger.info("Storage bucket verified", bucket=self.bucket)

        except Exception as e:
            logger.error("Connection verification failed", error=str(e))
            raise SupabaseStorageError(f"Supabase connection failed: {e}")

    # ==================== Core Storage Methods ====================

    def generate_id(self) -> str:
        """Generate unique presentation ID"""
        return str(uuid.uuid4())

    async def save(self, presentation_data: Dict[str, Any]) -> str:
        """
        Save a new presentation to Supabase

        Args:
            presentation_data: Presentation data (title, slides, etc.)

        Returns:
            presentation_id: UUID of saved presentation

        Raises:
            SupabaseStorageError: If save fails
        """
        presentation_id = self.generate_id()

        try:
            # Add metadata
            presentation_data["id"] = presentation_id
            presentation_data["created_at"] = datetime.utcnow().isoformat()

            # 1. Save to PostgreSQL (primary storage)
            self.client.table("ls_presentations").insert({
                "id": presentation_id,
                "title": presentation_data.get("title", "Untitled"),
                "slides": presentation_data.get("slides", []),
                "created_at": presentation_data["created_at"],
                "metadata": {
                    "slide_count": len(presentation_data.get("slides", [])),
                    "source": "layout_builder"
                },
                "derivative_elements": presentation_data.get("derivative_elements"),
                "theme_config": presentation_data.get("theme_config")
            }).execute()

            logger.info("Presentation saved to PostgreSQL",
                       presentation_id=presentation_id,
                       slide_count=len(presentation_data.get("slides", [])))

            # 2. Backup to Storage bucket (async, non-blocking)
            try:
                self._save_to_storage(presentation_id, presentation_data)
            except Exception as storage_error:
                logger.warning("Storage backup failed (non-critical)",
                             presentation_id=presentation_id,
                             error=str(storage_error))

            # 3. Update cache
            if self.cache:
                self.cache.set(presentation_id, presentation_data)

            return presentation_id

        except Exception as e:
            logger.error("Save failed",
                        presentation_id=presentation_id,
                        error=str(e),
                        exc_info=True)
            raise SupabaseStorageError(f"Failed to save presentation: {e}")

    async def load(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a presentation by ID

        Tier hierarchy:
        1. Check local cache (if enabled)
        2. Query PostgreSQL
        3. Reconstruct from Storage backup (fallback)

        Args:
            presentation_id: Presentation UUID

        Returns:
            Presentation data or None if not found
        """
        try:
            # Tier 3: Check cache first
            if self.cache:
                cached = self.cache.get(presentation_id)
                if cached:
                    logger.info("Loaded from cache", presentation_id=presentation_id)
                    return cached

            # Tier 1: Load from PostgreSQL
            result = self.client.table("ls_presentations").select("*").eq("id", presentation_id).execute()

            if not result.data or len(result.data) == 0:
                logger.warning("Presentation not found", presentation_id=presentation_id)
                return None

            row = result.data[0]

            # Reconstruct presentation data
            presentation_data = {
                "id": row["id"],
                "title": row["title"],
                "slides": row["slides"],
                "created_at": row["created_at"],
                "updated_at": row.get("updated_at"),
                "updated_by": row.get("updated_by"),
                "restored_from": row.get("restored_from"),
                "metadata": row.get("metadata", {}),
                "derivative_elements": row.get("derivative_elements"),
                "theme_config": row.get("theme_config")
            }

            # Update cache
            if self.cache:
                self.cache.set(presentation_id, presentation_data)

            logger.info("Loaded from PostgreSQL", presentation_id=presentation_id)
            return presentation_data

        except Exception as e:
            logger.error("Load failed",
                        presentation_id=presentation_id,
                        error=str(e),
                        exc_info=True)

            # Tier 2 fallback: Try loading from Storage backup
            try:
                return self._load_from_storage(presentation_id)
            except Exception as storage_error:
                logger.error("Storage fallback failed",
                           presentation_id=presentation_id,
                           error=str(storage_error))
                return None

    async def delete(self, presentation_id: str) -> bool:
        """
        Delete a presentation and all its versions

        Args:
            presentation_id: Presentation UUID

        Returns:
            True if deleted, False if not found
        """
        try:
            # Delete from PostgreSQL (cascade deletes versions)
            result = self.client.table("ls_presentations").delete().eq("id", presentation_id).execute()

            if not result.data or len(result.data) == 0:
                logger.warning("Delete failed - not found", presentation_id=presentation_id)
                return False

            # Delete from Storage bucket
            try:
                self._delete_from_storage(presentation_id)
            except Exception as storage_error:
                logger.warning("Storage delete failed (non-critical)",
                             presentation_id=presentation_id,
                             error=str(storage_error))

            # Invalidate cache
            if self.cache:
                self.cache.invalidate(presentation_id)

            logger.info("Presentation deleted", presentation_id=presentation_id)
            return True

        except Exception as e:
            logger.error("Delete failed",
                        presentation_id=presentation_id,
                        error=str(e),
                        exc_info=True)
            return False

    async def list_all(self) -> List[str]:
        """
        List all presentation IDs

        Returns:
            List of presentation UUIDs
        """
        try:
            result = self.client.table("ls_presentations").select("id").execute()
            ids = [row["id"] for row in result.data]
            logger.info("Listed presentations", count=len(ids))
            return ids
        except Exception as e:
            logger.error("List failed", error=str(e), exc_info=True)
            return []

    # ==================== Version History Methods ====================

    def _generate_version_id(self) -> str:
        """Generate unique version ID with timestamp"""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"v_{timestamp}_{short_uuid}"

    async def save_version(
        self,
        presentation_id: str,
        presentation_data: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None
    ) -> str:
        """
        Save a version snapshot to version history

        Args:
            presentation_id: Presentation UUID
            presentation_data: Complete presentation data
            created_by: Who created this version
            change_summary: Brief description of changes

        Returns:
            version_id: Unique version identifier
        """
        version_id = self._generate_version_id()

        try:
            # Save to ls_presentation_versions table
            self.client.table("ls_presentation_versions").insert({
                "presentation_id": presentation_id,
                "version_id": version_id,
                "version_data": presentation_data,
                "created_by": created_by,
                "change_summary": change_summary or "No description provided"
            }).execute()

            logger.info("Version saved",
                       presentation_id=presentation_id,
                       version_id=version_id,
                       created_by=created_by)

            # Backup to Storage
            try:
                self._save_version_to_storage(presentation_id, version_id, presentation_data)
            except Exception as storage_error:
                logger.warning("Version storage backup failed",
                             version_id=version_id,
                             error=str(storage_error))

            return version_id

        except Exception as e:
            logger.error("Save version failed",
                        presentation_id=presentation_id,
                        error=str(e),
                        exc_info=True)
            raise SupabaseStorageError(f"Failed to save version: {e}")

    async def update(
        self,
        presentation_id: str,
        updates: Dict[str, Any],
        created_by: str = "user",
        change_summary: Optional[str] = None,
        create_version: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing presentation

        Args:
            presentation_id: Presentation UUID
            updates: Fields to update
            created_by: Who made the update
            change_summary: Description of changes
            create_version: Whether to create version backup first

        Returns:
            Updated presentation data or None if not found
        """
        try:
            # Load current state
            current = await self.load(presentation_id)
            if not current:
                logger.warning("Update failed - not found", presentation_id=presentation_id)
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

            # Update PostgreSQL
            self.client.table("ls_presentations").update({
                "title": current.get("title"),
                "slides": current.get("slides"),
                "updated_at": current["updated_at"],
                "updated_by": created_by,
                "metadata": current.get("metadata", {}),
                "derivative_elements": current.get("derivative_elements"),
                "theme_config": current.get("theme_config")
            }).eq("id", presentation_id).execute()

            # Update Storage backup
            try:
                self._save_to_storage(presentation_id, current)
            except Exception as storage_error:
                logger.warning("Update storage backup failed",
                             presentation_id=presentation_id,
                             error=str(storage_error))

            # Invalidate cache
            if self.cache:
                self.cache.invalidate(presentation_id)

            logger.info("Presentation updated",
                       presentation_id=presentation_id,
                       created_by=created_by)

            return current

        except Exception as e:
            logger.error("Update failed",
                        presentation_id=presentation_id,
                        error=str(e),
                        exc_info=True)
            return None

    async def get_version_history(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get version history metadata for a presentation

        Args:
            presentation_id: Presentation UUID

        Returns:
            Version history with metadata list
        """
        try:
            result = self.client.table("ls_presentation_versions").select(
                "version_id, created_at, created_by, change_summary"
            ).eq("presentation_id", presentation_id).order("created_at", desc=True).execute()

            if not result.data:
                return None

            history = {
                "presentation_id": presentation_id,
                "versions": result.data
            }

            logger.info("Retrieved version history",
                       presentation_id=presentation_id,
                       version_count=len(result.data))

            return history

        except Exception as e:
            logger.error("Get version history failed",
                        presentation_id=presentation_id,
                        error=str(e),
                        exc_info=True)
            return None

    async def load_version(self, presentation_id: str, version_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific version of a presentation

        Args:
            presentation_id: Presentation UUID
            version_id: Version ID to load

        Returns:
            Version data or None if not found
        """
        try:
            result = self.client.table("ls_presentation_versions").select("version_data").eq(
                "presentation_id", presentation_id
            ).eq("version_id", version_id).execute()

            if not result.data or len(result.data) == 0:
                logger.warning("Version not found",
                             presentation_id=presentation_id,
                             version_id=version_id)
                return None

            version_data = result.data[0]["version_data"]
            logger.info("Version loaded",
                       presentation_id=presentation_id,
                       version_id=version_id)

            return version_data

        except Exception as e:
            logger.error("Load version failed",
                        presentation_id=presentation_id,
                        version_id=version_id,
                        error=str(e),
                        exc_info=True)
            return None

    async def restore_version(
        self,
        presentation_id: str,
        version_id: str,
        create_backup: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Restore a presentation to a specific version

        Args:
            presentation_id: Presentation UUID
            version_id: Version ID to restore
            create_backup: Whether to backup current state first

        Returns:
            Restored presentation data or None if version not found
        """
        try:
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

            # Restore the version (clean up version metadata)
            restored = version_data.copy()
            restored.pop("version_id", None)
            restored.pop("versioned_at", None)
            restored["updated_at"] = datetime.utcnow().isoformat()
            restored["restored_from"] = version_id

            # Update PostgreSQL
            self.client.table("ls_presentations").update({
                "title": restored.get("title"),
                "slides": restored.get("slides"),
                "updated_at": restored["updated_at"],
                "restored_from": version_id,
                "metadata": restored.get("metadata", {})
            }).eq("id", presentation_id).execute()

            # Update Storage backup
            try:
                self._save_to_storage(presentation_id, restored)
            except Exception as storage_error:
                logger.warning("Restore storage backup failed",
                             presentation_id=presentation_id,
                             error=str(storage_error))

            # Invalidate cache
            if self.cache:
                self.cache.invalidate(presentation_id)

            logger.info("Version restored",
                       presentation_id=presentation_id,
                       version_id=version_id)

            return restored

        except Exception as e:
            logger.error("Restore version failed",
                        presentation_id=presentation_id,
                        version_id=version_id,
                        error=str(e),
                        exc_info=True)
            return None

    # ==================== Storage Bucket Helper Methods ====================

    def _save_to_storage(self, presentation_id: str, data: Dict[str, Any]):
        """Save presentation JSON to Storage bucket as backup"""
        try:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            file_path = f"presentations/{presentation_id}.json"

            self.client.storage.from_(self.bucket).upload(
                file_path,
                json_data.encode('utf-8'),
                {"content-type": "application/json", "upsert": "true"}
            )

            logger.debug("Saved to storage", presentation_id=presentation_id, path=file_path)
        except Exception as e:
            logger.warning("Storage save failed", presentation_id=presentation_id, error=str(e))
            raise

    def _load_from_storage(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """Load presentation JSON from Storage bucket (fallback)"""
        try:
            file_path = f"presentations/{presentation_id}.json"
            response = self.client.storage.from_(self.bucket).download(file_path)

            if response:
                data = json.loads(response.decode('utf-8'))
                logger.info("Loaded from storage fallback", presentation_id=presentation_id)
                return data
            return None
        except Exception as e:
            logger.warning("Storage load failed", presentation_id=presentation_id, error=str(e))
            return None

    def _delete_from_storage(self, presentation_id: str):
        """Delete presentation and versions from Storage bucket"""
        try:
            # Delete main presentation file
            self.client.storage.from_(self.bucket).remove([f"presentations/{presentation_id}.json"])

            # Delete all version files
            # Note: This lists and deletes all files in versions/{presentation_id}/
            try:
                version_files = self.client.storage.from_(self.bucket).list(f"versions/{presentation_id}")
                if version_files:
                    paths = [f"versions/{presentation_id}/{f['name']}" for f in version_files]
                    self.client.storage.from_(self.bucket).remove(paths)
            except:
                pass  # Versions folder might not exist

            logger.debug("Deleted from storage", presentation_id=presentation_id)
        except Exception as e:
            logger.warning("Storage delete failed", presentation_id=presentation_id, error=str(e))
            raise

    def _save_version_to_storage(self, presentation_id: str, version_id: str, data: Dict[str, Any]):
        """Save version JSON to Storage bucket"""
        try:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            file_path = f"versions/{presentation_id}/{version_id}.json"

            self.client.storage.from_(self.bucket).upload(
                file_path,
                json_data.encode('utf-8'),
                {"content-type": "application/json", "upsert": "true"}
            )

            logger.debug("Version saved to storage",
                        presentation_id=presentation_id,
                        version_id=version_id,
                        path=file_path)
        except Exception as e:
            logger.warning("Version storage save failed",
                         presentation_id=presentation_id,
                         version_id=version_id,
                         error=str(e))
            raise
