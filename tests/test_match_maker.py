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


# def test_stable_member_mapper_returns_a_stable():
#     """Tests that the stable_member_mapper returns all hired stable members in a circuit"""

#     stable = stables.get_by_id(1)

#     hired_members = Match_Maker.stable_member_mapper(circuit, stable["id"])

#     assert hired_members == stable["members"]


# def test_stable_member_mapper_returns_empty_list_when_no_stable_found():
#     """Tests that the stable member mapper returns an empty list if it doesn't find a stable"""

#     employees = Match_Maker.stable_member_mapper(roster=[1], stable_id=99)

#     assert employees == []


def test_mutli_man_match():
    """Test that match maker can create a multi man match"""
    seed_db.seed_database()

    raw = Shows.create_show("wwf", 1)

    Match_Maker.matches(raw, roll_override=55)

    assert "will be a 6 tag match" in raw["card"][0]
