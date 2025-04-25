"""
Configuration module for ISO20022Gen.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Default configuration values
_DEFAULT_CONFIG = {
    "ROUTING_NUMBER": "021151080",
    "BUSINESS_SERVICE": "TEST",
    "MARKET_PRACTICE_REGY": (
        "www2.swift.com/mystandards/#/group/Federal_Reserve_Financial_Services/Fedwire_Funds_Service"
    ),
    "MARKET_PRACTICE_ID": "frb.fedwire.01",
    "XSD_PATH": "schemas/",
}

# Initialize with default values
_config: Dict[str, Any] = _DEFAULT_CONFIG.copy()


def load_from_env() -> None:
    """
    Load configuration from environment variables.
    """
    load_dotenv()  # will pick up .env in cwd

    for key in _DEFAULT_CONFIG:
        env_value = os.getenv(key)
        if env_value is not None:
            _config[key] = env_value


def configure(config_dict: Dict[str, Any] = None, env_file: str = None) -> None:
    """
    Configure the ISO20022Gen library.
    
    Args:
        config_dict: Dictionary with configuration values to override.
        env_file: Path to .env file to load.
    """
    # Load from env file if specified
    if env_file:
        load_dotenv(dotenv_path=env_file)

    # Load from environment variables
    load_from_env()

    # Override with provided config
    if config_dict:
        _config.update(config_dict)


def get_config(key: str) -> Any:
    """
    Get a configuration value.
    
    Args:
        key: Configuration key to get.
        
    Returns:
        Configuration value.
    """
    return _config.get(key, _DEFAULT_CONFIG.get(key))


# Load configuration from environment variables on import
load_from_env()

# Make config values accessible as module attributes
ROUTING_NUMBER = get_config("ROUTING_NUMBER")
BUSINESS_SERVICE = get_config("BUSINESS_SERVICE")
MARKET_PRACTICE_REGY = get_config("MARKET_PRACTICE_REGY")
MARKET_PRACTICE_ID = get_config("MARKET_PRACTICE_ID")
XSD_PATH = get_config("XSD_PATH")
