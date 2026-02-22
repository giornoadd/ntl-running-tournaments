import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from generate_member_readmes import parse_runners, get_activity_info


class TestParseRunners:
    def test_single_runner(self):
        result = parse_runners("GIO: 4.53km")
        assert len(result) == 1
        assert result[0] == ("GIO", 4.53)

    def test_multiple_runners(self):
        result = parse_runners("GIO: 3.51km, Sand: 2.95km, Oum: 5.21km")
        assert len(result) == 3
        assert result[0] == ("GIO", 3.51)
        assert result[1] == ("Sand", 2.95)
        assert result[2] == ("Oum", 5.21)

    def test_empty_string(self):
        result = parse_runners("")
        assert result == []

    def test_none_input(self):
        result = parse_runners(None)
        assert result == []


class TestGetActivityInfo:
    def test_known_runner(self):
        label, activity = get_activity_info("gio")
        assert label is not None
        assert "run" in activity.lower()

    def test_walker_default(self):
        label, activity = get_activity_info("sand")
        assert label is not None
        assert "walk" in activity.lower()

    def test_walker_with_date_override(self):
        # Jojo defaults to Indoor Walk but has run override on 2026-02-02
        label, activity = get_activity_info("jojo", "2026-02-02")
        assert label is not None
        assert "run" in activity.lower()

    def test_unknown_runner(self):
        label, activity = get_activity_info("unknown_player")
        assert label is not None  # Should return a default
