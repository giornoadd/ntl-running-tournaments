import sys
import os
import pytest

# Add src/ to sys.path so we can import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.config import determine_team, TEAMS, RENAMED_PATTERN

def test_determine_team_mandalorian():
    assert determine_team('GIO') == 'Mandalorian'
    assert determine_team('Boat') == 'Mandalorian'
    assert determine_team('sand') == 'Mandalorian'
    assert determine_team('fuse') == 'Mandalorian'

def test_determine_team_itsystem():
    assert determine_team('Oat') == 'IT System'
    assert determine_team('Boy') == 'IT System'
    assert determine_team('PAN') == 'IT System'
    assert determine_team('jojo') == 'IT System'

def test_determine_team_unknown():
    assert determine_team('InvalidPlayer') == 'Unknown'
    assert determine_team('Superman') == 'Unknown'

def test_renamed_pattern_valid():
    # Valid formats
    assert RENAMED_PATTERN.match('gio-2026-jan-05.jpg')
    assert RENAMED_PATTERN.match('boat-2026-feb-11.jpg')
    assert RENAMED_PATTERN.match('sand-2026-mar-01_1.png')

def test_renamed_pattern_invalid():
    # Invalid formats
    assert not RENAMED_PATTERN.match('gio-2026-01-05.jpg') # Missing string month
    assert not RENAMED_PATTERN.match('boat-feb-11.jpg')    # Missing year
    assert not RENAMED_PATTERN.match('sand-2026-jan-5.jpg') # Single digit day
