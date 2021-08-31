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
    seed_db.seed_database(name="wwf")

    raw = Shows.create_show("wwf", 2)

    Match_Maker.matches(raw, roll_override=55)

    raw = Shows.get_by_id(raw["id"])

    assert "will be a 6 tag match" in raw["card"][0]


def test_24_7_match():
    """Test that 24/7 matches can be made and are valid"""
    seed_db.seed_database(name="wwf")

    raw = Shows.create_show("wwf", 2)

    Match_Maker.matches(raw, roll_override=1)

    raw = Shows.get_by_id(raw["id"])

    assert "24/7 Title Defense" in raw["card"][0]


def test_trio_match():
    """Test that trio matches can be made and are valid"""

    seed_db.seed_database(name="cmll")

    lucha_show = Shows.create_show("cmll", 2)

    Match_Maker.matches(lucha_show, roll_override=1)

    lucha_show = Shows.get_by_id(lucha_show["id"])

    assert "will be a 6 tag match" in lucha_show["card"][0]


def test_singles_match():
    """Test that match maker can create a singles match"""
    seed_db.seed_database(name="wwf")

    raw = Shows.create_show("wwf", 2)

    Match_Maker.matches(raw, roll_override=49)

    raw = Shows.get_by_id(raw["id"])

    assert "one on one singles match" in raw["card"][0]


def test_tag_match():
    """Test that match maker can create a tag match"""

    seed_db.seed_database(name="wwf")

    raw = Shows.create_show("wwf", 2)

    Match_Maker.matches(raw, roll_override=89)

    raw = Shows.get_by_id(raw["id"])

    assert "tag team match" in raw["card"][0]


def test_undercard_match_presentation():
    """Test that the undercard matches for a show are stored and displayed correctly"""

    seed_db.seed_database(name="wccw")

    wccw = Shows.create_show("wccw", match_total=3)

    Match_Maker.matches(wccw)

    wccw = Shows.get_by_id(wccw["id"])

    assert "Match 1" in wccw["card"][0]

    assert "Match 2" in wccw["card"][1]


def test_main_event():
    """Test that main events are stored and displayed correctly"""

    seed_db.seed_database(name="wccw")

    wccw = Shows.create_show("wccw", 3)

    Match_Maker.matches(wccw)

    wccw = Shows.get_by_id(wccw["id"])

    assert wccw["card"][1]


def test_battle_royale_main_event():
    """Test that battle royale main event displays correctly"""

    seed_db.seed_database(name="wccw")

    wccw = Shows.create_show("wccw", 3)

    Match_Maker.matches(wccw, main_event_roll_override=100)

    wccw = Shows.get_by_id(wccw["id"])

    assert "Battle Royal" in wccw["card"][2]


def test_small_battle_royale_main_event():
    """Test that small battle royale main events displays correctly"""
    seed_db.seed_database(name="wccw", wrestler_override=10)

    wccw = Shows.create_show("wccw", 2)

    Match_Maker.matches(wccw, roll_override=54, main_event_roll_override=100)

    wccw = Shows.get_by_id(wccw["id"])

    # num = 5 - len(wccw["males"])

    assert "Man Battle Royal" in wccw["card"][1]


def test_tag_match():
    """Test that match maker can create tag matches without duplicates"""

    seed_db.seed_database(name="wwf", wrestler_override=10)

    raw = Shows.create_show("wwf", 5)

    Match_Maker.matches(raw, roll_override=89)

    raw = Shows.get_by_id(raw["id"])

    assert len(raw["busy_wrestlers"]) > 9
