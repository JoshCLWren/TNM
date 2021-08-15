import json
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename="migration.log",
    filemode="w",
    format="%(message)s",
)
logging.warning("migrations.py")
import psycopg2
import wrestlers
import circuits

con = psycopg2.connect("dbname=test user=postgres")
cursor = con.cursor()


def db_builder():
    wrestler_list = wrestlers.wrestler_serializer()

    circuit_rosters = circuits.circuit_serializer()

    tag_team_name = 3
    tag_team_count = 0
    tag_teams = []
    member_1 = 1
    member_2 = 2

    # logging.warning("Processing TEAMS.DAT")
    # with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/TEAMS.DAT") as tags:
    #     for index, line in enumerate(tags):
    #         if index == member_1:
    #             tag_teams.append({"Member 1": line.strip()})
    #             member_1 += 10
    #         if index == member_2:
    #             tag_teams[tag_team_count]["Member 2"] = line.strip()
    #             member_2 += 10
    #         if index == tag_team_name:
    #             tag_teams[tag_team_count]["Tag Team Name"] = line.strip()
    #             logging.warning(f"Adding {line.strip()}")
    #             tag_team_name += 10
    #             tag_team_count += 1

    logging.warning(f"Adding tag teams to circuit")
    # for wrestler in wrestler_list:
    #     for circuit in circuit_roster:
    #         for wrassler in circuit["roster"]:
    #             if wrassler[0]["name"] == wrestler["name"]:
    #                 wrestler["circuits"].append(circuit["circuit_name"])
    #     for tag in tag_teams:
    #         if tag["Member 1"] == wrestler["name"]:
    #             if tag["Tag Team Name"] == "":
    #                 tag["Tag Team Name"] = f'{tag["Member 1"]}/{tag["Member 2"]}'

    #             wrestler["tag teams"].append(
    #                 {
    #                     "Tag Team Name": tag["Tag Team Name"],
    #                     "Partner": tag["Member 2"],
    #                 }
    #             )
    #         if tag["Member 2"] == wrestler["name"]:
    #             wrestler["tag teams"].append(
    #                 {
    #                     "Tag Team Name": tag["Tag Team Name"],
    #                     "Partner": tag["Member 1"],
    #                 }
    #             )
    #     for circuit in circuit_roster:
    #         if circuit["circuit_name"] in wrestler["circuits"]:
    #             for team in wrestler["tag teams"]:
    #                 for partner in circuit["roster"]:
    #                     if team["Partner"] == partner[0]["name"]:
    #                         names = [team["Partner"], wrestler["name"]]
    #                         names = sorted(names)
    #                         circuit["tag teams"].append(
    #                             {
    #                                 "Tag Team": team["Tag Team Name"],
    #                                 "Members": f"{names[0]}/{names[1]}",
    #                             },
    #                         )

    # # remove duplicate tag teams from circuits
    # logging.warning("Removing Tag Duplicates")
    # for circuit in circuit_roster:
    #     new_tags = []
    #     for tag in circuit["tag teams"]:
    #         if tag not in new_tags:
    #             new_tags.append(tag)
    #     circuit["tag teams"] = new_tags

    # # adding wrestler index to wrestler object
    # logging.warning("Adding TNM index values to each wrestler")

    # x = cursor.execute("Select * from Wrestlers;")
    # x = cursor.fetchall()
    # x = len(x)
    # import pdb

    # pdb.set_trace()

    # stable_count = -1
    # stable_list = []
    # stable_total = 0

    # logging.warning(f"Adding Stables to {circuit['circuit_name']}")
    # with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/STABLES.DAT") as stables:
    #     for index, line in enumerate(stables):
    #         if index == 0:
    #             stable_total = line.strip()
    #         if (
    #             line.strip().isalpha() == True
    #             or " " in line.strip()
    #             or "-" in line.strip()
    #         ):
    #             stable_count += 1
    #             stable_list.append({"Stable Name": line.strip()})
    #             logging.warning(f"adding {line.strip()}")
    #             stable_list[stable_count]["ids"] = []
    #         if (
    #             line.strip().isdigit() == True
    #             and line.strip() != stable_total
    #             and line.strip() != "0"
    #         ):
    #             stable_list[stable_count]["ids"].append(line.strip())

    # for stable in stable_list:
    #     if len(stable["ids"]) > 1:
    #         member_count = stable["ids"][0]
    #         stable["member count"] = member_count
    #     else:
    #         stable["member count"] = 0

    # # adding stables to wrestlers
    # logging.warning("Adding Wrestlers to Stables")
    # for stable in stable_list:
    #     stable_member_ids = []
    #     for index, member in enumerate(stable["ids"]):
    #         # first index is the member count and we skip it
    #         if index == 0:
    #             pass
    #         else:
    #             stable_member_ids.append(int(member))
    #     stable_members = []
    #     for wrestler in wrestler_list:
    #         if wrestler["id"] in stable_member_ids:
    #             stable_members.append(wrestler["name"])
    #             wrestler["stables"].append(
    #                 {
    #                     "Stable Name": stable["Stable Name"],
    #                     "Member Ids": stable_member_ids,
    #                 }
    #             )

    # class json_convert(dict):
    #     def __str__(self):
    #         return json.dumps(self)
    wrestlers.seed_wrestlers(wrestler_list)
    circuits.seed_circuits(circuit_rosters)

    logging.warning("Creating circuit_roster_db.json")
    with open("circuit_roster_db.json", "w") as fp:
        json.dump({"Circuits": circuit_rosters}, fp, indent=2)

    logging.warning("Creating tag_team_roster.json")
    with open("tag_team_roster.json", "w") as fp:
        json.dump({"tag_teams": tag_teams}, fp, indent=2)

    # logging.warning("Creating stables.json")
    # with open("stables.json", "w") as fp:
    #     json.dump({"stables": stable_list}, fp, indent=2)
