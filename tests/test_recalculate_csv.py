import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from recalculate_csv import parse_runners_string, is_walk_activity
from utils.config import RUN_MIN_DISTANCE, WALK_MIN_DISTANCE

def test_parse_runners_string_empty():
    assert parse_runners_string("") == []
    assert parse_runners_string(None) == []

def test_parse_runners_string_single():
    res = parse_runners_string("GIO: 4.53km")
    assert len(res) == 1
    assert res[0]['name'] == 'GIO'
    assert res[0]['dist'] == 4.53
    assert res[0]['original'] == 'GIO: 4.53km'

def test_parse_runners_string_multiple():
    res = parse_runners_string("GIO: 3.51km, Sand: 2.95km")
    assert len(res) == 2
    
    assert res[0]['name'] == 'GIO'
    assert res[0]['dist'] == 3.51
    
    assert res[1]['name'] == 'Sand'
    assert res[1]['dist'] == 2.95

def test_parse_runners_string_with_noise():
    # Ensuring it correctly ignores additional parens or spaces that might get caught
    res = parse_runners_string("GIO: 5.44km, Mos: 3.13km (น้อยกว่า 1km)")
    assert len(res) == 2
    assert res[1]['name'] == 'Mos'
    assert res[1]['dist'] == 3.13


# --- Walk Activity Detection ---

class TestIsWalkActivity:
    def test_sand_is_walker(self):
        assert is_walk_activity('Sand') is True

    def test_jojo_default_is_walker(self):
        assert is_walk_activity('Jojo') is True

    def test_gio_is_not_walker(self):
        assert is_walk_activity('GIO') is False

    def test_boy_is_not_walker(self):
        assert is_walk_activity('Boy') is False

    def test_jojo_override_to_run(self):
        # Jojo was running on 2026-02-02
        assert is_walk_activity('Jojo', '2026-02-02') is False

    def test_oum_default_is_runner(self):
        assert is_walk_activity('Oum') is False

    def test_oum_override_to_walk(self):
        # Oum was walking on 2026-01-14
        assert is_walk_activity('Oum', '2026-01-14') is True

    def test_unknown_player(self):
        assert is_walk_activity('Superman') is False

    def test_fuse_is_walker(self):
        assert is_walk_activity('fuse') is True

    def test_chan_default_is_walker(self):
        assert is_walk_activity('Chan') is True

    def test_chan_override_to_run(self):
        assert is_walk_activity('Chan', '2026-02-17') is False


# --- Distance Constants ---

class TestDistanceConstants:
    def test_run_minimum(self):
        assert RUN_MIN_DISTANCE == 1.0

    def test_walk_minimum(self):
        assert WALK_MIN_DISTANCE == 2.0

    def test_walk_higher_than_run(self):
        assert WALK_MIN_DISTANCE > RUN_MIN_DISTANCE

