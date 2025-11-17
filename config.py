"""
Configuration management for v7.5-main Layout Builder

Handles environment variables and settings for:
- Server configuration (port, CORS)
- Supabase integration (database, storage)
- Caching configuration
- Feature flags

Usage:
    from config import get_settings

    settings = get_settings()
    print(settings.SUPABASE_URL)
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # ==================== Server Configuration ====================

    PORT: int = 8504
    """Server port (Railway sets this automatically)"""

    ALLOWED_ORIGINS: str = "*"
    """
    CORS allowed origins (comma-separated)
    Examples:
        - "*" (allow all - development only)
        - "https://deckster.xyz,https://www.deckster.xyz"
    """

    # ==================== Supabase Configuration ====================

    SUPABASE_URL: Optional[str] = None
    """
    Supabase project URL
    Format: https://{project-id}.supabase.co
    Example: https://eshvntffcestlfuofwhv.supabase.co
    """

    SUPABASE_ANON_KEY: Optional[str] = None
    """
    Supabase anon (public) key
    Note: Used for client-side operations (not currently needed for server-only)
    """

    SUPABASE_SERVICE_KEY: Optional[str] = None
    """
    Supabase service_role (secret) key
    ⚠️ IMPORTANT: Keep secret, never expose in client code
    Used for: Server-side operations, bypasses RLS
    """

    SUPABASE_BUCKET: str = "ls-presentation-data"
    """
    Supabase Storage bucket name for Layout Service presentations
    Must match bucket created in Supabase dashboard
    Prefix: ls- (Layout Service) for multi-service Supabase projects
    """

    # ==================== Feature Flags ====================

    ENABLE_SUPABASE: bool = True
    """
    Enable Supabase storage backend
    - True: Use Supabase (production)
    - False: Use filesystem storage (development/fallback)
    """

    ENABLE_LOCAL_CACHE: bool = True
    """
    Enable local caching layer (Tier 2)
    - True: Cache presentations in memory (faster reads)
    - False: Always query Supabase (slower but always fresh)
    """

    # ==================== Cache Configuration ====================

    CACHE_TTL_SECONDS: int = 3600
    """
    Cache time-to-live in seconds
    Default: 3600 (1 hour)
    Examples:
        - 300 (5 minutes) - more cache refreshes
        - 7200 (2 hours) - fewer queries
        - 86400 (24 hours) - very long cache
    """

    MAX_CACHE_SIZE: int = 1000
    """
    Maximum number of presentations to cache in memory
    Default: 1000 presentations (~10-50MB depending on size)
    """

    # ==================== Storage Configuration ====================

    STORAGE_DIR: str = "storage/presentations"
    """
    Filesystem storage directory (fallback/development)
    Used when ENABLE_SUPABASE=false
    """

    # ==================== Model Configuration ====================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra environment variables
    )

    # ==================== Validation Methods ====================

    def is_supabase_configured(self) -> bool:
        """
        Check if Supabase is properly configured

        Returns:
            True if all required Supabase variables are set
        """
        return all([
            self.ENABLE_SUPABASE,
            self.SUPABASE_URL is not None,
            self.SUPABASE_SERVICE_KEY is not None,
        ])

    def get_storage_backend(self) -> str:
        """
        Determine which storage backend to use

        Returns:
            "supabase" or "filesystem"
        """
        if self.is_supabase_configured():
            return "supabase"
        return "filesystem"

    def validate_supabase_config(self) -> dict[str, str]:
        """
        Validate Supabase configuration and return status

        Returns:
            dict with validation results
        """
        validation = {
            "backend": self.get_storage_backend(),
            "supabase_enabled": self.ENABLE_SUPABASE,
            "supabase_url_set": self.SUPABASE_URL is not None,
            "service_key_set": self.SUPABASE_SERVICE_KEY is not None,
            "bucket_name": self.SUPABASE_BUCKET,
            "cache_enabled": self.ENABLE_LOCAL_CACHE,
            "cache_ttl": self.CACHE_TTL_SECONDS,
        }
        return validation


# ==================== Global Settings Instance ====================

_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get global settings instance (singleton pattern)

    Returns:
        Settings instance with all configuration loaded

    Example:
        settings = get_settings()
        if settings.is_supabase_configured():
            print("✅ Supabase ready")
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment (useful for testing)

    Returns:
        Fresh Settings instance

    Example:
        # Change environment variable
        os.environ['ENABLE_SUPABASE'] = 'false'
        # Reload to pick up changes
        settings = reload_settings()
    """
    global _settings
    _settings = Settings()
    return _settings


# ==================== Utility Functions ====================

def print_config_summary():
    """
    Print configuration summary (for debugging)

    Useful for:
        - Server startup logging
        - Deployment verification
        - Troubleshooting configuration issues
    """
    settings = get_settings()
    validation = settings.validate_supabase_config()

    print("=" * 60)
    print("v7.5-main Layout Builder Configuration")
    print("=" * 60)
    print(f"Storage Backend:     {validation['backend']}")
    print(f"Supabase Enabled:    {validation['supabase_enabled']}")
    print(f"Supabase URL Set:    {validation['supabase_url_set']}")
    print(f"Service Key Set:     {validation['service_key_set']}")
    print(f"Storage Bucket:      {validation['bucket_name']}")
    print(f"Cache Enabled:       {validation['cache_enabled']}")
    print(f"Cache TTL:           {validation['cache_ttl']}s")
    print(f"Port:                {settings.PORT}")
    print(f"CORS Origins:        {settings.ALLOWED_ORIGINS}")
    print("=" * 60)

    # Warnings
    if not settings.is_supabase_configured() and settings.ENABLE_SUPABASE:
        print("⚠️  WARNING: ENABLE_SUPABASE=true but configuration incomplete!")
        print("    Falling back to filesystem storage (ephemeral)")
        print("    Set SUPABASE_URL and SUPABASE_SERVICE_KEY to enable Supabase")
        print("=" * 60)


# ==================== Main (for testing) ====================

if __name__ == "__main__":
    """Test configuration loading"""
    print_config_summary()

    # Example: Check if Supabase configured
    settings = get_settings()
    if settings.is_supabase_configured():
        print("\n✅ Supabase is properly configured")
    else:
        print("\n❌ Supabase configuration incomplete")
        print("   Using filesystem storage (presentations will be lost on restart)")
