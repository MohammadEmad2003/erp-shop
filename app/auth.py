"""Staff-only endpoints require the shop's API key in the X-API-Key header."""

import os
import secrets

from fastapi import Header, HTTPException


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.environ.get("ERP_API_KEY", "dev-key")
    if x_api_key is None or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
