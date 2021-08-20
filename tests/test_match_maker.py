# from test_wrestlers import fake_wrestler
# import pytest
# import circuits
# import wrestlers
# import stables
# import database
# import Match_Maker
# import utilities


# eligible_wrestlers = {
#     "male": [1, 3, 5, 7],
#     "female": [2, 4, 6, 8],
#     "heels": [1, 2, 3, 4],
#     "faces": [5, 6, 7, 8],
#     "tweeners": [],
#     "jobbers": [],
#     "anti_heroes": [],
# }


# def test_gendered_person_set():
#     """Tests the gendered persona returns the correct list"""

#     male_heels = Match_Maker.gendered_persona(
#         eligible_wrestlers, persona="heels", gender="male"
#     )

#     assert male_heels == [1, 3]

#     female_faces = Match_Maker.gendered_persona(
#         eligible_wrestlers, persona="faces", gender="female"
#     )

#     assert female_faces == [8, 6]


# def stable_member_mapper_returns_a_stable():
#     """Tests that the stable_member_mapper returns all hired stable members in a circuit"""

#     stable = stables.fake_stable()

#     fake_roster = [1, 2, 3, 4]

#     hired_members = Match_Maker.stable_member_mapper(fake_roster, stable["id"])

#     assert hired_members == stable["members"]


# def stable_member_mapper_returns_empty_list_when_no_stable_found():
#     """Tests that the stable member mapper returns an empty list if it doesn't find a stable"""

#     employees = Match_Maker.stable_member_mapper(roster=[1], stable_id=99)

#     assert employees == []


# def test_multi_man_match():
#     """Tests that the mutli man match method returns a valid match"""

#     wwe = {
#         "name": "WWE",
#         "stables": [1, 2],
#         "tag_teams": [],
#         "wrestlers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#         "injuries": [],
#         "heels": [1, 2, 3],
#         "faces": [4, 5, 6],
#         "anti_heroes": [],
#         "tweeners": [],
#         "jobbers": [],
#         "championships": [],
#     }

#     # nwo = stables.patch_stable(1, "members", [1, 2, 3])
#     # wolfpack = stables.post_stable({"name": "wolfpack", "members": [4, 5, 6]})

#     # circuit = circuits.post_circuit(**wwe)

#     # for number in range(1, 6):
#     #     if number % 2 == 0:
#     #         dude = fake_wrestler(circuits=[circuit["id"]], stables=[2], gender="male")
#     #         wrestlers.post_wrestler(**dude)
#     #     else:
#     #         dude = fake_wrestler(circuits=[circuit["id"]], stables=[1], gender="male")
#     #         wrestlers.post_wrestler(**dude)

#     # x_man_match = {
#     #     "team_size": 6,
#     #     "team1": {"name": "nwo", "members": [1, 3, 5, 7, 9], "id": 1},
#     #     "team2": {"name": "wolfpack", "members": [2, 4, 6, 8, 10], "id": 2},
#     # }
#     # # roster_mutation = Match_Maker.roster_selector(
#     # #     tv_show="RAW",
#     # #     roster=eligible_wrestlers,
#     # #     people=x_man_match["team_size"],
#     # #     gender="male",
#     # #     _stables=True,
#     # #     team1="nwo",
#     # #     team2="wolfpack",
#     # # )
#     # match = 1

#     # six_man_match = Match_Maker.multi_persons_match(x_man_match, match, roster_mutation)

#     # assert six_man_match == "Mr. X Mr. X Lady X  vs Mr. X Mr. X Mr. X "
