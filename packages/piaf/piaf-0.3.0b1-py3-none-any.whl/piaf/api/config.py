# coding: utf-8
"""Configuration module."""
from __future__ import annotations

import os
from typing import Tuple

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # CORS configuration
    cors_origins: Tuple[str] = ("*",)
    cors_methods: Tuple[str] = ("*",)
    cors_headers: Tuple[str] = ("*",)
    cors_credentials: bool = True

    class Config:
        """Extra configuration."""

        env_prefix = "PIAF_API_"
        env_file = os.getenv("PIAF_API_ENV_FILE", ".env")
