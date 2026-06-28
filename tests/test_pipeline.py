import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'pipeline'))

from config import FILTERS, SMARD_BASE_URL, REGION, RESOLUTION

def test_filters_count():
    assert len(FILTERS) == 10

def test_filters_have_required_fields():
    for f in FILTERS:
        assert "id" in f
        assert "name" in f
        assert "unit" in f
        assert "category" in f

def test_filter_categories():
    valid_categories = {"price", "generation", "consumption", "forecast"}
    for f in FILTERS:
        assert f["category"] in valid_categories

def test_filter_units():
    valid_units = {"EUR/MWh", "MWh"}
    for f in FILTERS:
        assert f["unit"] in valid_units

def test_smard_base_url():
    assert "smard.de" in SMARD_BASE_URL

def test_region():
    assert REGION == "DE"

def test_resolution():
    assert RESOLUTION == "hour"
