import pytest
import circuits
import wrestlers
import stables
import database
import Match_Maker


eligible_wrestlers = {
    "male": [1, 3, 5, 7],
    "female": [2, 4, 6, 8],
    "heels": [1, 2, 3, 4],
    "faces": [5, 6, 7, 8],
    "tweeners": [],
    "jobbers": [],
    "anti_heroes": [],
}


def test_gendered_person_set():
    """Tests the gendered persona returns the correct list"""

    male_heels = Match_Maker.gendered_persona(
        eligible_wrestlers, persona="heels", gender="male"
    )

    assert male_heels == [1, 3]

    female_faces = Match_Maker.gendered_persona(
        eligible_wrestlers, persona="faces", gender="female"
    )

    assert female_faces == [8, 6]


def test_opponents_dict():
    """Test that a dictionary of eligible and logical opponents is returned"""

    opponents = Match_Maker.opponent_dict(eligible_wrestlers, gender="male")

    # should only return the males which are odd numbered 1-7
    print(opponents)
    assert opponents == {
        "heels": [1, 3],
        "faces": [5, 7],
        "tweeners": [],
        "jobbers": [],
        "anti_heroes": [],
    }
