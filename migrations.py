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


def db_builder():
    db = "TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/WRESTLRS.DAT"
    wrestler_list = []
    wrestler_name = 1
    work_rate = 57
    push = 58
    charisma = 59
    weight = 67
    gender = 79
    # gender is 1 for female and blank for male
    wrestle_count = 0
    wrestler = {}
    idcount = 1
    logging.warning("Opening {db}")
    with open(db) as wrestlers:
        for index, line in enumerate(wrestlers):
            if index == 0:
                wrestler_total = line.strip()
            if index == wrestler_name:
                wrestler_list.append({"name": line.strip()})
                logging.warning(f"adding {line.strip()}")
                wrestler_list[wrestle_count]["circuits"] = []
                wrestler_list[wrestle_count]["tag teams"] = []
                wrestler_list[wrestle_count]["stables"] = []
                wrestler_list[wrestle_count]["id"] = idcount
                idcount += 1
                wrestler_name += 120
            if index == work_rate:
                wrestler_list[wrestle_count]["work_rate"] = line.strip()
                work_rate += 120
            if index == push:
                wrestler_list[wrestle_count]["push"] = line.strip()
                push += 120
            if index == charisma:
                wrestler_list[wrestle_count]["charimsa"] = line.strip()
                charisma += 120
            if index == weight:
                wrestler_list[wrestle_count]["weight"] = line.strip()
                weight += 120
            if index == gender:
                if line.strip() == "1":
                    sex = "female"
                else:
                    sex = "male"
                wrestler_list[wrestle_count]["gender"] = sex
                gender += 120

                wrestle_count += 1

    circuits = ["AEW", "CMLL", "IMPACT", "MLW", "NJPW", "NXT", "ROH", "WWE"]
    circuit_roster = []
    circuit_counter = 0

    logging.warning("Building Circuit Databases")
    for circuit in circuits:
        with open(
            f"TNM/tnm7se_build_13/tnm7se/TNM7SE/{circuit}/CIRCDB.DAT"
        ) as circuit_db:
            logging.warning(f"parsing {circuit}")
            circuit_roster.append(
                {"circuit_name": circuit, "roster": [], "tag teams": []}
            )
            for index, line in enumerate(circuit_db):
                if index == 0:
                    circuit_wrestler_name_line_number = 1
                    contract_status = 3
                    personality = 4
                    circuit_roster_count = 0
                if index == circuit_wrestler_name_line_number:
                    circuit_roster[circuit_counter]["roster"].append(
                        [{"name": line.strip()}]
                    )
                    logging.warning(f"adding {line.strip()} to {circuit}")
                    circuit_wrestler_name_line_number += 18
                if index == contract_status:
                    logging.warning("Adding Contract Status")
                    if int(line.strip()) > 0 and int(line.strip()) < 53:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"contract_length": int(line.strip())})
                    else:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"contract_length": 0})
                    contract_status += 18
                if index == personality:
                    logging.warning("Adding Personality")
                    line = int(line.strip())
                    if line == 0:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"personality": "face"})
                    elif line == 1:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"personality": "heel"})
                    elif line == 2:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"personality": "tweener"})
                    elif line == 3:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"personality": "jobber"})
                        logging.warning("Jobber Detected")
                    else:
                        circuit_roster[circuit_counter]["roster"][
                            circuit_roster_count
                        ].append({"personality": "anti-hero"})
                    personality += 18
                    circuit_roster_count += 1
        circuit_counter += 1
    for lst in circuit_roster:
        lst["roster"] = [x for x in lst["roster"] if x[1]["contract_length"] != 0]
    # add genders to circuit wresterl dbs
    for circuit in circuit_roster:
        for performer in circuit["roster"]:
            for wrestler in wrestler_list:
                if performer[0]["name"] == wrestler["name"]:
                    performer.append({"gender": wrestler["gender"]})
    tag_team_name = 3
    tag_team_count = 0
    tag_teams = []
    member_1 = 1
    member_2 = 2

    logging.warning("Processing TEAMS.DAT")
    with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/TEAMS.DAT") as tags:
        for index, line in enumerate(tags):
            if index == member_1:
                tag_teams.append({"Member 1": line.strip()})
                member_1 += 10
            if index == member_2:
                tag_teams[tag_team_count]["Member 2"] = line.strip()
                member_2 += 10
            if index == tag_team_name:
                tag_teams[tag_team_count]["Tag Team Name"] = line.strip()
                logging.warning(f"Adding {line.strip()}")
                tag_team_name += 10
                tag_team_count += 1

    logging.warning(f"Adding tag teams to circuit")
    for wrestler in wrestler_list:
        for circuit in circuit_roster:
            for wrassler in circuit["roster"]:
                if wrassler[0]["name"] == wrestler["name"]:
                    wrestler["circuits"].append(circuit["circuit_name"])
        for tag in tag_teams:
            if tag["Member 1"] == wrestler["name"]:
                if tag["Tag Team Name"] == "":
                    tag["Tag Team Name"] = f'{tag["Member 1"]}/{tag["Member 2"]}'

                wrestler["tag teams"].append(
                    {
                        "Tag Team Name": tag["Tag Team Name"],
                        "Partner": tag["Member 2"],
                    }
                )
            if tag["Member 2"] == wrestler["name"]:
                wrestler["tag teams"].append(
                    {
                        "Tag Team Name": tag["Tag Team Name"],
                        "Partner": tag["Member 1"],
                    }
                )
        for circuit in circuit_roster:
            if circuit["circuit_name"] in wrestler["circuits"]:
                for team in wrestler["tag teams"]:
                    for partner in circuit["roster"]:
                        if team["Partner"] == partner[0]["name"]:
                            names = [team["Partner"], wrestler["name"]]
                            names = sorted(names)
                            circuit["tag teams"].append(
                                {
                                    "Tag Team": team["Tag Team Name"],
                                    "Members": f"{names[0]}/{names[1]}",
                                },
                            )

    # remove duplicate tag teams from circuits
    logging.warning("Removing Tag Duplicates")
    for circuit in circuit_roster:
        new_tags = []
        for tag in circuit["tag teams"]:
            if tag not in new_tags:
                new_tags.append(tag)
        circuit["tag teams"] = new_tags

    # adding wrestler index to wrestler object
    logging.warning("Adding TNM index values to each wrestler")
    with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/WRESTLRS.IDX") as wrestler_index:
        index_list = []
        for line in wrestler_index:
            index_list.append({"index": line.strip()})
    for id, wrestler in zip(index_list, wrestler_list):
        wrestler["index"] = id["index"]

    stable_count = -1
    stable_list = []
    stable_total = 0

    logging.warning(f"Adding Stables to {circuit['circuit_name']}")
    with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/STABLES.DAT") as stables:
        for index, line in enumerate(stables):
            if index == 0:
                stable_total = line.strip()
            if (
                line.strip().isalpha() == True
                or " " in line.strip()
                or "-" in line.strip()
            ):
                stable_count += 1
                stable_list.append({"Stable Name": line.strip()})
                logging.warning(f"adding {line.strip()}")
                stable_list[stable_count]["ids"] = []
            if (
                line.strip().isdigit() == True
                and line.strip() != stable_total
                and line.strip() != "0"
            ):
                stable_list[stable_count]["ids"].append(line.strip())

    for stable in stable_list:
        if len(stable["ids"]) > 1:
            member_count = stable["ids"][0]
            stable["member count"] = member_count
        else:
            stable["member count"] = 0

    # adding stables to wrestlers
    logging.warning("Adding Wrestlers to Stables")
    for stable in stable_list:
        stable_member_ids = []
        for index, member in enumerate(stable["ids"]):
            # first index is the member count and we skip it
            if index == 0:
                pass
            else:
                stable_member_ids.append(int(member))
        stable_members = []
        for wrestler in wrestler_list:
            if wrestler["id"] in stable_member_ids:
                stable_members.append(wrestler["name"])
                wrestler["stables"].append(
                    {
                        "Stable Name": stable["Stable Name"],
                        "Member Ids": stable_member_ids,
                    }
                )

    class json_convert(dict):
        def __str__(self):
            return json.dumps(self)

    logging.warning("Creating wrestler_db.json")
    with open("wrestler_db.json", "w") as fp:
        json.dump({"wrestlers": wrestler_list}, fp, indent=2)

    logging.warning("Creating circuit_roster_db.json")
    with open("circuit_roster_db.json", "w") as fp:
        json.dump({"Circuits": circuit_roster}, fp, indent=2)

    logging.warning("Creating tag_team_roster.json")
    with open("tag_team_roster.json", "w") as fp:
        json.dump({"tag_teams": tag_teams}, fp, indent=2)

    logging.warning("Creating stables.json")
    with open("stables.json", "w") as fp:
        json.dump({"stables": stable_list}, fp, indent=2)
