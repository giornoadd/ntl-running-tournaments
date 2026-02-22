import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from recalculate_csv import parse_runners_string

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
