"""Optional Telegram delivery for newly discovered job digests."""

from __future__ import annotations

import os
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class TelegramConfig:
    bot_token: str
    chat_id: str

    @classmethod
    def from_env(cls) -> "TelegramConfig | None":
        token = os.getenv("JOBMAXXER_TELEGRAM_BOT_TOKEN", "").strip()
        chat_id = os.getenv("JOBMAXXER_TELEGRAM_CHAT_ID", "").strip()
        if not token or not chat_id:
            return None
        return cls(token, chat_id)


def send_message(text: str, config: TelegramConfig, timeout: float = 10.0) -> None:
    """Send one message; raise requests errors so callers can handle failures."""
    if not text.strip():
        return
    response = requests.post(
        f"https://api.telegram.org/bot{config.bot_token}/sendMessage",
        json={"chat_id": config.chat_id, "text": text},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("ok") is not True:
        raise RuntimeError("Telegram rejected the message")
