"""
Configuration Management for FHL Bible MCP Server

Supports:
- JSON/YAML config files
- Environment variables (FHL_ prefix)
- Runtime configuration updates
- Type validation
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class ServerConfig:
    """Server configuration"""
    name: str = "fhl-bible-server"
    version: str = "1.0.0"
    

@dataclass
class APIConfig:
    """API configuration"""
    base_url: str = "https://bible.fhl.net/api/"  # Updated to /api/ endpoint (Phase 1)
    timeout: int = 30
    max_retries: int = 3


@dataclass
class DefaultsConfig:
    """Default values configuration"""
    bible_version: str = "unv"
    chinese_variant: str = "traditional"  # "traditional" or "simplified"
    search_limit: int = 50
    include_strong: bool = False


@dataclass
class CacheConfig:
    """Cache configuration"""
    enabled: bool = True
    directory: str = ".cache"
    cleanup_on_start: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    file: Optional[str] = None
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class Config:
    """
    Main configuration class for FHL Bible MCP Server.
    
    Supports loading from:
    1. Config file (JSON)
    2. Environment variables (FHL_ prefix)
    3. Runtime updates
    """
    
    server: ServerConfig = field(default_factory=ServerConfig)
    api: APIConfig = field(default_factory=APIConfig)
    defaults: DefaultsConfig = field(default_factory=DefaultsConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # 追蹤設定來源
    _sources: Dict[str, str] = field(default_factory=dict, repr=False)
    
    @classmethod
    def load(
        cls,
        config_file: Optional[str] = None,
        use_env: bool = True
    ) -> "Config":
        """
        Load configuration from file and environment.
        
        Args:
            config_file: Path to JSON config file (optional)
            use_env: Whether to load from environment variables
            
        Returns:
            Config instance
        """
        config = cls()
        
        # 1. Load from file
        if config_file:
            config._load_from_file(config_file)
        else:
            # Try default locations
            default_paths = [
                "config.json",
                ".config/fhl_bible.json",
                os.path.expanduser("~/.config/fhl_bible/config.json"),
            ]
            for path in default_paths:
                if os.path.exists(path):
                    config._load_from_file(path)
                    break
        
        # 2. Load from environment variables
        if use_env:
            config._load_from_env()
        
        logger.info(f"Configuration loaded: {len(config._sources)} settings from various sources")
        return config
    
    def _load_from_file(self, file_path: str) -> None:
        """Load configuration from JSON file"""
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"Config file not found: {file_path}")
                return
            
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Update each section
            if "server" in data:
                self._update_section(self.server, data["server"], "file", "server")
            if "api" in data:
                self._update_section(self.api, data["api"], "file", "api")
            if "defaults" in data:
                self._update_section(self.defaults, data["defaults"], "file", "defaults")
            if "cache" in data:
                self._update_section(self.cache, data["cache"], "file", "cache")
            if "logging" in data:
                self._update_section(self.logging, data["logging"], "file", "logging")
            
            logger.info(f"Loaded config from file: {file_path}")
            
        except Exception as e:
            logger.error(f"Error loading config file {file_path}: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables"""
        env_prefix = "FHL_"
        
        # Map environment variables to config paths
        env_mappings = {
            # Server
            f"{env_prefix}SERVER_NAME": ("server", "name"),
            f"{env_prefix}SERVER_VERSION": ("server", "version"),
            
            # API
            f"{env_prefix}API_BASE_URL": ("api", "base_url"),
            f"{env_prefix}API_TIMEOUT": ("api", "timeout", int),
            f"{env_prefix}API_MAX_RETRIES": ("api", "max_retries", int),
            
            # Defaults
            f"{env_prefix}DEFAULT_VERSION": ("defaults", "bible_version"),
            f"{env_prefix}DEFAULT_CHINESE": ("defaults", "chinese_variant"),
            f"{env_prefix}DEFAULT_SEARCH_LIMIT": ("defaults", "search_limit", int),
            f"{env_prefix}DEFAULT_INCLUDE_STRONG": ("defaults", "include_strong", bool),
            
            # Cache
            f"{env_prefix}CACHE_ENABLED": ("cache", "enabled", bool),
            f"{env_prefix}CACHE_DIR": ("cache", "directory"),
            f"{env_prefix}CACHE_CLEANUP_ON_START": ("cache", "cleanup_on_start", bool),
            
            # Logging
            f"{env_prefix}LOG_LEVEL": ("logging", "level"),
            f"{env_prefix}LOG_FILE": ("logging", "file"),
            f"{env_prefix}LOG_FORMAT": ("logging", "format"),
        }
        
        loaded_count = 0
        for env_var, mapping in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                section_name = mapping[0]
                field_name = mapping[1]
                converter = mapping[2] if len(mapping) > 2 else str
                
                # Get section object
                section = getattr(self, section_name)
                
                # Convert value
                try:
                    if converter == bool:
                        converted_value = value.lower() in ('true', '1', 'yes', 'on')
                    elif converter == int:
                        converted_value = int(value)
                    else:
                        converted_value = value
                    
                    # Set value
                    setattr(section, field_name, converted_value)
                    
                    # Track source
                    key = f"{section_name}.{field_name}"
                    self._sources[key] = f"env:{env_var}"
                    loaded_count += 1
                    
                    logger.debug(f"Loaded from env: {env_var} -> {key}")
                    
                except Exception as e:
                    logger.error(f"Error converting env var {env_var}={value}: {e}")
        
        if loaded_count > 0:
            logger.info(f"Loaded {loaded_count} settings from environment variables")
    
    def _update_section(
        self,
        section: Any,
        data: Dict[str, Any],
        source: str,
        section_name: str
    ) -> None:
        """Update a config section from dict"""
        for key, value in data.items():
            if hasattr(section, key):
                setattr(section, key, value)
                self._sources[f"{section_name}.{key}"] = source
    
    def update(
        self,
        section: str,
        key: str,
        value: Any,
        validate: bool = True
    ) -> bool:
        """
        Update configuration at runtime.
        
        Args:
            section: Section name (server, api, defaults, cache, logging)
            key: Setting key
            value: New value
            validate: Whether to validate the value type
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get section object
            if not hasattr(self, section):
                logger.error(f"Invalid section: {section}")
                return False
            
            section_obj = getattr(self, section)
            
            # Check if key exists
            if not hasattr(section_obj, key):
                logger.error(f"Invalid key: {section}.{key}")
                return False
            
            # Validate type if requested
            if validate:
                current_value = getattr(section_obj, key)
                if current_value is not None and not isinstance(value, type(current_value)):
                    logger.error(
                        f"Type mismatch for {section}.{key}: "
                        f"expected {type(current_value)}, got {type(value)}"
                    )
                    return False
            
            # Update value
            setattr(section_obj, key, value)
            self._sources[f"{section}.{key}"] = "runtime"
            
            logger.info(f"Updated config: {section}.{key} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating config {section}.{key}: {e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Section name
            key: Setting key
            default: Default value if not found
            
        Returns:
            Configuration value or default
        """
        try:
            if hasattr(self, section):
                section_obj = getattr(self, section)
                if hasattr(section_obj, key):
                    return getattr(section_obj, key)
            return default
        except Exception:
            return default
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "server": asdict(self.server),
            "api": asdict(self.api),
            "defaults": asdict(self.defaults),
            "cache": asdict(self.cache),
            "logging": asdict(self.logging),
        }
    
    def save(self, file_path: str) -> bool:
        """
        Save configuration to JSON file.
        
        Args:
            file_path: Path to save config file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved config to: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving config to {file_path}: {e}")
            return False
    
    def get_sources(self) -> Dict[str, str]:
        """Get the sources of all configuration values"""
        return self._sources.copy()
    
    def __str__(self) -> str:
        """String representation"""
        return (
            f"Config(\n"
            f"  server={self.server}\n"
            f"  api={self.api}\n"
            f"  defaults={self.defaults}\n"
            f"  cache={self.cache}\n"
            f"  logging={self.logging}\n"
            f")"
        )


# Global configuration instance
_global_config: Optional[Config] = None


def get_config(
    config_file: Optional[str] = None,
    use_env: bool = True,
    reload: bool = False
) -> Config:
    """
    Get global configuration instance.
    
    Args:
        config_file: Path to config file (optional)
        use_env: Whether to load from environment
        reload: Force reload configuration
        
    Returns:
        Config instance
    """
    global _global_config
    
    if _global_config is None or reload:
        _global_config = Config.load(config_file=config_file, use_env=use_env)
    
    return _global_config


def reset_config() -> None:
    """Reset global configuration (mainly for testing)"""
    global _global_config
    _global_config = None
