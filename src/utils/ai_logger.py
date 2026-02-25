"""
AI Interaction Logger — logs Ollama and NotebookLM requests/responses.

Logs are stored as append-only markdown files under:
    resources/{service}-log/{agent}/{yyyy-mm-dd}.md

Each entry includes a timestamp, the prompt/query, response summary,
and optional metadata (model, preset, tool name, etc.).
"""

import os
from datetime import datetime, timezone, timedelta

# Bangkok timezone (UTC+7)
_BKK_TZ = timezone(timedelta(hours=7))


def _get_log_dir(service: str, agent: str) -> str:
    """Return the absolute log directory path for a given service and agent."""
    from src.utils.config import RESOURCES_DIR
    return os.path.join(RESOURCES_DIR, f"{service}-log", agent)


def _get_log_path(service: str, agent: str, now: datetime = None) -> str:
    """Return the absolute log file path for a given service, agent, and date."""
    if now is None:
        now = datetime.now(_BKK_TZ)
    date_str = now.strftime("%Y-%m-%d")
    return os.path.join(_get_log_dir(service, agent), f"{date_str}.md")


def _build_header(service: str, agent: str, now: datetime) -> str:
    """Build the markdown header for a new log file."""
    service_label = "Ollama" if service == "ollama" else "NotebookLM"
    agent_label = agent.replace("-", " ").title()
    date_str = now.strftime("%Y-%m-%d")
    return (
        f"# 📝 {service_label} Log — {agent_label}\n"
        f"📅 Date: {date_str}\n"
    )


def _build_entry(
    now: datetime,
    prompt: str,
    response: str,
    metadata: dict = None,
) -> str:
    """Build a single markdown log entry."""
    time_str = now.strftime("%H:%M")
    meta = metadata or {}

    lines = [
        f"\n---\n",
        f"## [{time_str}] Request\n",
    ]

    # Metadata fields (model, preset, tool, etc.)
    for key, value in meta.items():
        label = key.replace("_", " ").title()
        lines.append(f"**{label}:** {value}\n")

    lines.append(f"**Prompt:**\n```\n{prompt}\n```\n")

    # Truncate very long responses to keep logs readable
    max_len = 1000
    resp_display = response if len(response) <= max_len else response[:max_len] + "\n... (truncated)"
    lines.append(f"**Response:**\n```\n{resp_display}\n```\n")

    return "\n".join(lines)


def log_ai_interaction(
    service: str,
    agent: str,
    prompt: str,
    response: str,
    metadata: dict = None,
    now: datetime = None,
) -> str:
    """
    Append a request/response entry to the AI interaction log.

    Args:
        service:  'ollama' or 'notebooklm'.
        agent:    Agent name slug, e.g. 'process-image', 'running-coach',
                  'sports-analyst', 'tournament-reporter', or 'general'.
        prompt:   The prompt or query sent.
        response: The response text received.
        metadata: Optional dict of extra fields to log
                  (e.g. model, preset, tool, temperature).
        now:      Override current time (for testing).

    Returns:
        The absolute path of the log file written to.
    """
    if now is None:
        now = datetime.now(_BKK_TZ)

    log_path = _get_log_path(service, agent, now)

    # Ensure directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # If file doesn't exist, write the header first
    is_new = not os.path.exists(log_path)

    with open(log_path, "a", encoding="utf-8") as f:
        if is_new:
            f.write(_build_header(service, agent, now))
        f.write(_build_entry(now, prompt, response, metadata))

    return log_path
