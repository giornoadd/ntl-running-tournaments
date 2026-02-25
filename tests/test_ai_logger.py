import sys
import os
import pytest
from datetime import datetime, timezone, timedelta

# Add src/ to sys.path so we can import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.ai_logger import log_ai_interaction, _get_log_path, _build_header, _build_entry, _BKK_TZ


# Fixed time for deterministic tests
FIXED_TIME = datetime(2026, 2, 25, 13, 30, 0, tzinfo=_BKK_TZ)


class TestGetLogPath:
    def test_ollama_path(self):
        path = _get_log_path("ollama", "running-coach", FIXED_TIME)
        assert path.endswith(os.path.join("ollama-log", "running-coach", "2026-02-25.md"))

    def test_notebooklm_path(self):
        path = _get_log_path("notebooklm", "tournament-reporter", FIXED_TIME)
        assert path.endswith(os.path.join("notebooklm-log", "tournament-reporter", "2026-02-25.md"))

    def test_different_date(self):
        t = datetime(2026, 12, 31, 23, 59, tzinfo=_BKK_TZ)
        path = _get_log_path("ollama", "general", t)
        assert "2026-12-31.md" in path


class TestBuildHeader:
    def test_ollama_header(self):
        header = _build_header("ollama", "sports-analyst", FIXED_TIME)
        assert "Ollama" in header
        assert "Sports Analyst" in header
        assert "2026-02-25" in header

    def test_notebooklm_header(self):
        header = _build_header("notebooklm", "process-image", FIXED_TIME)
        assert "NotebookLM" in header
        assert "Process Image" in header


class TestBuildEntry:
    def test_entry_contains_prompt_and_response(self):
        entry = _build_entry(FIXED_TIME, "Hello?", "Hi there!", {"model": "qwen3:8b"})
        assert "[13:30]" in entry
        assert "Hello?" in entry
        assert "Hi there!" in entry
        assert "qwen3:8b" in entry

    def test_long_response_truncated(self):
        long_resp = "x" * 2000
        entry = _build_entry(FIXED_TIME, "prompt", long_resp)
        assert "truncated" in entry
        assert len(long_resp) > 1000  # original is long
        # The entry itself should contain at most 1000 chars of response + truncation note


class TestLogAiInteraction:
    def test_creates_file_and_writes_header(self, tmp_path, monkeypatch):
        monkeypatch.setattr("utils.ai_logger._get_log_dir",
                            lambda service, agent: str(tmp_path / f"{service}-log" / agent))

        path = log_ai_interaction(
            service="ollama", agent="running-coach",
            prompt="Analyze pace", response="Your pace is good.",
            metadata={"model": "qwen3:8b"}, now=FIXED_TIME,
        )
        assert os.path.exists(path)
        content = open(path, encoding="utf-8").read()
        assert "Ollama" in content
        assert "Running Coach" in content
        assert "Analyze pace" in content
        assert "Your pace is good." in content

    def test_appends_to_existing_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("utils.ai_logger._get_log_dir",
                            lambda service, agent: str(tmp_path / f"{service}-log" / agent))

        # First entry
        log_ai_interaction(
            service="ollama", agent="general",
            prompt="First", response="Reply 1", now=FIXED_TIME,
        )
        # Second entry
        t2 = FIXED_TIME.replace(minute=45)
        log_ai_interaction(
            service="ollama", agent="general",
            prompt="Second", response="Reply 2", now=t2,
        )
        path = _get_log_path("ollama", "general", FIXED_TIME)
        # Monkeypatched, so build the expected path manually
        expected = tmp_path / "ollama-log" / "general" / "2026-02-25.md"
        content = open(expected, encoding="utf-8").read()

        # Header should appear only once
        assert content.count("📝 Ollama Log") == 1
        # Both entries present
        assert "First" in content
        assert "Second" in content
        assert "[13:30]" in content
        assert "[13:45]" in content

    def test_notebooklm_logging(self, tmp_path, monkeypatch):
        monkeypatch.setattr("utils.ai_logger._get_log_dir",
                            lambda service, agent: str(tmp_path / f"{service}-log" / agent))

        log_ai_interaction(
            service="notebooklm", agent="tournament-reporter",
            prompt="Competition rules?", response="Run >= 1km...",
            metadata={"tool": "notebook_query"}, now=FIXED_TIME,
        )
        expected = tmp_path / "notebooklm-log" / "tournament-reporter" / "2026-02-25.md"
        assert expected.exists()
        content = expected.read_text(encoding="utf-8")
        assert "NotebookLM" in content
        assert "Tournament Reporter" in content
        assert "notebook_query" in content

    def test_creates_directories(self, tmp_path, monkeypatch):
        deep = tmp_path / "a" / "b" / "c"
        monkeypatch.setattr("utils.ai_logger._get_log_dir",
                            lambda service, agent: str(deep / f"{service}-log" / agent))

        log_ai_interaction(
            service="ollama", agent="new-agent",
            prompt="test", response="ok", now=FIXED_TIME,
        )
        assert (deep / "ollama-log" / "new-agent" / "2026-02-25.md").exists()
