import pytest

import wrestlers
from database import cursor, con
import psycopg2

fake_wrestler = {
    "name": "Mr. X",
    "work_rate": 99,
    "push": 98,
    "charisma": 97,
    "weight": 98,
    "gender": "male",
    "tnm_index": 1,
    "circuits": None,
    "tag_teams": None,
    "stables": None,
}


def test_wrestler_serializer():
    """Tests Dropping and rebuilding table and adding one wrestler"""
    wrestlers.seed_wrestlers([fake_wrestler])

    wrestlers_in_db = wrestlers.get_all_wrestlers()

    assert len(wrestlers_in_db) == 1
    assert wrestlers_in_db[0]["name"] == "Mr. X"


def test_updating_wrestler_circuits():
    """Tests modifiying a wrestlers circuit array column"""
    test_adding_to_an_empty_array = wrestlers.patch_wrestler(
        wrestler_id=1, column="circuits", new_value=7
    )

    assert test_adding_to_an_empty_array["circuits"] == [7]


def test_duplicate_circuit():
    """Testing that you can't add duplicates to the circuit array column"""

    test_adding_duplicate_circuit = wrestlers.patch_wrestler(
        wrestler_id=1, column="circuits", new_value=7
    )

    assert test_adding_duplicate_circuit["circuits"] == [7]


def test_adding_mulitple_circuits_to_one_wrestler():
    """Testing that a wrestler can have any amount of non duplicate circuit id"""

    circuit_ids = [*range(0, 1000)]

    for circuit in circuit_ids:
        wrestlers.patch_wrestler(wrestler_id=1, column="circuits", new_value=circuit)

    wrestler = wrestlers.get_by_id(1)

    assert len(wrestler["circuits"]) == 1000


def test_patching_tag_teams():
    """Test that the patch_wrestler method can work with other list types"""

    # try adding a tag team to the empty list
    wrestler = wrestlers.patch_wrestler(1, "tag_teams", 4)

    assert wrestler["tag_teams"] == [4]

    # try adding another tag team the list
    wrestler = wrestlers.patch_wrestler(1, "tag_teams", 5)

    assert wrestler["tag_teams"] == [4, 5]

    # try adding a duplicate tag team to the list

    wrestler = wrestlers.patch_wrestler(1, "tag_teams", 5)

    assert wrestler["tag_teams"] == [4, 5]

    # ensure stables works the same way as tag teams

    wrestler = wrestlers.patch_wrestler(1, "stables", 4)

    assert wrestler["stables"] == [4]

    # try adding another tag team the list
    wrestler = wrestlers.patch_wrestler(1, "stables", 5)

    assert wrestler["stables"] == [4, 5]

    # try adding a duplicate tag team to the list

    wrestler = wrestlers.patch_wrestler(1, "stables", 5)

    assert wrestler["stables"] == [4, 5]

    # try patching a non list value

    wrestler = wrestlers.patch_wrestler(1, "name", "Lady X")

    assert wrestler["name"] == "Lady X"

    wrestler = wrestlers.patch_wrestler(1, "gender", "female")

    assert wrestler["gender"] == "female"

    # check sending the wrong type

    wrestler = wrestlers.patch_wrestler(1, "weight", "x")

    # check that it did not change the value to the wrong type and new value passed
    assert wrestler["weight"] != "x"

    # check that the column is unchanged
    assert wrestler["weight"] == fake_wrestler["weight"]

    # check sending a non integer into a array of integers column

    wrestler = wrestlers.patch_wrestler(1, "stables", "nwo")

    assert "nwo" not in wrestler["stables"]
    assert wrestler["stables"] == [4, 5]
