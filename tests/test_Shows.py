from test_circuits import mock_circuit

fake_circuit = mock_circuit()
fake_circuit["stables"] = [1, 2, 3]
fake_circuit["tag_teams"] = [4, 5, 6]
fake_circuit["wrestlers"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
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


def test_creating_Show():
    """Tests that the Show object is created and moves all wrestlers in the correct lists"""
