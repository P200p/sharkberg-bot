"""Configuration settings for the Discord bot."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
    ADMIN_USER_IDS: list = field(default_factory=lambda: [int(x) for x in os.getenv("ADMIN_USER_IDS", "").split(",") if x])
    MAIN_CHANNEL_ID: int = int(os.getenv("MAIN_CHANNEL_ID", "0"))
    TOGETHER_API_KEY: str = os.getenv("TOGETHER_API_KEY", "")
    TOGETHER_MODEL: str = os.getenv(
        "TOGETHER_MODEL",
        "mistralai/Mistral-7B-Instruct-v0.2"
    )
    LAST_MSG_FILE: str = os.getenv("LAST_MSG_FILE", "data/last_msg.json")

    """Bot configuration settings.

    This class holds all configuration parameters required by the bot,
    loaded from environment variables with sensible defaults where applicable.
    """

    def validate(self):
        """Validate configuration settings.

        Raises:
            ValueError: If any required configuration is missing or invalid.
        """
        if not self.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required in .env")
        if not self.TOGETHER_API_KEY:
            raise ValueError("TOGETHER_API_KEY is required in .env")


# Create a global config instance that will be imported by other modules
config = Config()

# Validate configuration on import
try:
    config.validate()
except ValueError as e:
    print(f"❌ Configuration error: {e}")
    raise
