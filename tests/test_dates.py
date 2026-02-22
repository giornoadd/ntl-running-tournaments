import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils.dates import parse_date_from_filename, parse_date_generic, adjust_year
from datetime import datetime


class TestAdjustYear:
    def test_buddhist_era_year(self):
        dt = datetime(2569, 1, 15)
        result = adjust_year(dt)
        assert result.year == 2026

    def test_ad_year_unchanged(self):
        dt = datetime(2026, 1, 15)
        result = adjust_year(dt)
        assert result.year == 2026

    def test_old_ad_year_unchanged(self):
        dt = datetime(2000, 6, 1)
        result = adjust_year(dt)
        assert result.year == 2000


class TestParseDateFromFilename:
    def test_standard_format(self):
        dt = parse_date_from_filename("gio-2026-jan-05.jpg")
        assert dt is not None
        assert dt.year == 2026
        assert dt.month == 1
        assert dt.day == 5

    def test_with_suffix(self):
        dt = parse_date_from_filename("gio-2026-feb-07_1.jpg")
        assert dt is not None
        assert dt.year == 2026
        assert dt.month == 2
        assert dt.day == 7

    def test_2025_date(self):
        dt = parse_date_from_filename("sand-2025-dec-23.jpg")
        assert dt is not None
        assert dt.year == 2025
        assert dt.month == 12
        assert dt.day == 23

    def test_runna_format(self):
        dt = parse_date_from_filename("Runna 5km Easy Run on Feb 9, 2026 - 04.59.17.JPEG")
        assert dt is not None
        assert dt.year == 2026
        assert dt.month == 2
        assert dt.day == 9

    def test_invalid_format(self):
        assert parse_date_from_filename("IMG_8764.JPG") is None
        assert parse_date_from_filename("random_file.jpg") is None


class TestParseDateGeneric:
    def test_dd_mon_yyyy(self):
        dt = parse_date_generic("29 Jan 2026")
        assert dt is not None
        assert dt.day == 29
        assert dt.month == 1
        assert dt.year == 2026

    def test_month_dd_yyyy(self):
        dt = parse_date_generic("January 15, 2026")
        assert dt is not None
        assert dt.day == 15
        assert dt.month == 1
        assert dt.year == 2026

    def test_buddhist_era(self):
        dt = parse_date_generic("15 Jan 2569")
        assert dt is not None
        assert dt.year == 2026

    def test_empty_string(self):
        assert parse_date_generic("") is None

    def test_no_date(self):
        assert parse_date_generic("some random text without dates") is None
