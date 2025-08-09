import pytest
from datetime import datetime
from src.utils.date_utils import parse_iso_date


class TestParseIsoDate:
    def test_parse_iso_date_with_z_suffix(self):
        iso_str = "2025-04-12T01:48:22.5386879Z"
        result = parse_iso_date(iso_str)
        assert result == datetime.fromisoformat("2025-04-12T01:48:22.5386879+00:00")

    def test_parse_iso_date_with_timezone_offset(self):
        iso_str = "2025-04-12T01:48:22.5386879-03:00"
        result = parse_iso_date(iso_str)
        assert result == datetime.fromisoformat(iso_str)

    def test_parse_iso_date_with_no_timezone(self):
        iso_str = "2025-04-12T01:48:22.538687"
        result = parse_iso_date(iso_str)
        assert result == datetime.fromisoformat(iso_str)

    def test_parse_iso_date_invalid(self):
        assert parse_iso_date("invalid-date") is None

    def test_parse_iso_date_none(self):
        assert parse_iso_date(None) is None
