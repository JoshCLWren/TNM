from test_wrestlers import fake_wrestler
import pytest
import circuits
import wrestlers
import stables
import database
import Match_Maker
import utilities
import seed_db
import Shows


def test_mutli_man_match():
    """Test that match maker can create a multi man match"""
    seed_db.seed_database()

    raw = Shows.create_show("wwf", 1)

    Match_Maker.matches(raw, roll_override=55)

    assert "will be a 6 tag match" in raw["card"][0]


def test_24_7_match():
    """Test that 24/7 matches can be made and are valid"""
    seed_db.seed_database()

    raw = Shows.create_show("wwf", 1)

    Match_Maker.matches(raw, roll_override=1)

    assert "24/7 Title Defense" in raw["card"][0]
