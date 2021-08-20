import pytest

import circuits
import wrestlers
from test_wrestlers import fake_wrestler
from database import cursor, con


def mock_circuit():
    return {
        "name": "WWF",
        "stables": [],
        "tag_teams": [],
        "wrestlers": [],
        "injuries": [],
        "heels": [],
        "faces": [],
        "anti_heroes": [],
        "tweeners": [],
        "jobbers": [],
        "championships": [],
    }


def test_circuit_serializer():
    """Tests Dropping and Rebuilding table and adding one circuit"""

    circuits.seed_circuits([mock_circuit()])

    circuits_in_db = circuits.get_all_circuits()

    assert len(circuits_in_db) == 1


def test_updating_a_circuit():
    """Tests updating columns of a circuit row by overiding the value"""
    fake_circuit = mock_circuit()
    fake_circuit["id"] = 1
    fake_circuit["name"] = "WWE"
    fake_circuit["stables"] = [1, 2, 3]
    fake_circuit["tag_teams"] = [4, 5, 6]
    fake_circuit["wrestlers"] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    fake_circuit["injuries"] = [1]
    fake_circuit["heels"] = [1, 2, 3, 4]
    fake_circuit["faces"] = [5, 6, 7, 8, 9]
    fake_circuit["anti_heroes"] = [1]
    fake_circuit["tweeners"] = [1321]
    fake_circuit["jobbers"] = [
        9,
        1,
        4,
        2,
        6,
    ]

    circuit = circuits.update_circuit(**fake_circuit)
    assert circuit["id"] == 1
    assert circuit["name"] == "WWE"
    assert circuit["stables"] == [1, 2, 3]
    assert circuit["tag_teams"] == [4, 5, 6]
    assert circuit["wrestlers"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert circuit["injuries"] == [1]
    assert circuit["heels"] == [1, 2, 3, 4]
    assert circuit["faces"] == [5, 6, 7, 8, 9]
    assert circuit["anti_heroes"] == [1]
    assert circuit["tweeners"] == [1321]
    assert circuit["jobbers"] == [
        9,
        1,
        4,
        2,
        6,
    ]


def test_adding_a_wrestler_to_a_circuit():
    """Ensure that we can add a wrestler to a circuit"""
    circuit = circuits.get_by_id(1)

    circuits.patch_circuit(circuit["id"], "wrestlers", 600)
    assert circuit


def test_passing_a_list_to_patch():
    """Ensure that if a list is passed the patch method checks the types of the list and updates"""
    circuit = circuits.get_by_id(1)

    circuit_with_more_injuries = circuits.patch_circuit(
        circuit["id"], "injuries", [1, 2, 3, 4]
    )

    assert circuit != circuit_with_more_injuries
