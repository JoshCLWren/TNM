import pytest

import wrestlers
import psycopg2

con = psycopg2.connect("dbname=test user=postgres")
cursor = con.cursor()

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
    with con:
        cursor.execute("Select * from wrestlers;")

    wrestlers_in_db = cursor.fetchall()

    assert len(wrestlers_in_db) == 1
    assert wrestlers_in_db[0][1] == "Mr. X"


def test_updating_wrestler_circuits():
    """Tests modifiying a wrestlers circuit array column"""
    test_adding_to_an_empty_array = wrestlers.add_circuit(circuit_id=7, wrestler_id=1)

    assert test_adding_to_an_empty_array[8] == [7]


def test_duplicate_circuit():
    """Testing that you can't add duplicates to the circuit array column"""

    test_adding_duplicate_circuit = wrestlers.add_circuit(circuit_id=7, wrestler_id=1)

    assert test_adding_duplicate_circuit[8] == [7]


def test_adding_mulitple_circuits_to_one_wrestler():
    """Testing that a wrestler can have any amount of non duplicate circuit id"""

    circuit_ids = [*range(1, 1000, 1)]

    for circuit in circuit_ids:
        test = wrestlers.add_circuit(circuit_id=circuit, wrestler_id=1)

    wrestler = wrestlers.get_by_id(1)

    assert len(wrestler[8]) == 999
