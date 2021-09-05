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
import Championships


def before():
    seed_db.seed_database(wrestler_override=1, gender="male")

    fake_belt = seed_db.fake_championship()

    Championships.seed_championships([fake_belt])


def test_championship_serializer():
    """Tests Dropping and rebuilding championships table"""
    before()

    belt_in_db = Championships.get_some(columns=None, many=True)

    assert len(belt_in_db) == 1


def test_custom_query():
    """Tests Championship custom query"""
    before()
    champ = wrestlers.get_by_id(1)["name"]
    test = {"title_holder": champ}

    championship = Championships.get_some(columns=test)

    assert championship["title_holder"] == champ
