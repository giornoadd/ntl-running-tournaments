import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.files import get_nickname

def test_get_nickname_with_parens_english():
    assert get_nickname("Manda-1_โจ (GIO)") == "gio"
    assert get_nickname("ITSystem-2_เกมส์ (Game)") == "game"

def test_get_nickname_no_parens_english():
    assert get_nickname("ITSystem-8_Boy (บอย)") == "boy"
    assert get_nickname("Manda-2_Boat (โบ๊ท)") == "boat"

def test_get_nickname_invalid():
    assert get_nickname("Manda-3_ภาษาไทย") is None
    assert get_nickname("InvalidFormatFolder") is None

def test_get_nickname_spacing():
    assert get_nickname("ITSystem-4_ Palm (ปาล์ม) ") == "palm"
