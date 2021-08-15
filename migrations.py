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
import tag_teams
import database


def db_builder():

    database.wrestler_table()
    wrestler_list = wrestlers.wrestler_serializer()
    wrestlers.seed_wrestlers(wrestler_list)

    database.circuit_table()
    circuit_rosters = circuits.circuit_serializer()
    circuits.seed_circuits(circuit_rosters)

    database.tag_teams_table()
    tags = tag_teams.tag_team_serializer()
    tag_teams.seed_tags(tags)

    database.stables_table()

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

    # logging.warning("Creating circuit_roster_db.json")
    # with open("circuit_roster_db.json", "w") as fp:
    #     json.dump({"Circuits": circuit_rosters}, fp, indent=2)

    # logging.warning("Creating tag_team_roster.json")
    # with open("tag_team_roster.json", "w") as fp:
    #     json.dump({"tag_teams": tag_teams}, fp, indent=2)

    # logging.warning("Creating stables.json")
    # with open("stables.json", "w") as fp:
    #     json.dump({"stables": stable_list}, fp, indent=2)
