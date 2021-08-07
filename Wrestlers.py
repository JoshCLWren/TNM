db = "WRESTLRS.DAT"
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
with open(db) as wrestlers:
    for index, line in enumerate(wrestlers):
        if index == 0:
            wrestler_total = line.strip()
        if index == wrestler_name:
            wrestler_list.append({"name": line.strip()})
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
            # wrestler_list[wrestle_count]["circuits"] = []
            # wrestler_list[wrestle_count]["tag_teams"] = []
            # wrestler_list[wrestle_count]["stables"] = []

    print(wrestler_list)
    print(wrestler_total)

circuits = ["AEW", "CMLL", "IMPACT", "MLW", "NJPW", "NXT", "ROH", "WWE"]
circuit_roster = []
circuit_wrestler_name_line_number = 1
circuit_counter = 0
contract_status = 4
circuit_roster_count = 0

folderpath = r"TNM/tnm7se_build_13/tnm7se/TNM7SE/"
filepaths = []

for circuit in circuits:
    with open(f"TNM/tnm7se_build_13/tnm7se/TNM7SE/{circuit}/CIRCDB.DAT") as circuit_db:
        circuit_roster.append({"circuit_name": circuit, "roster": []})
        for index, line in enumerate(circuit_db):
            if index == circuit_wrestler_name_line_number:
                circuit_roster[circuit_counter]["roster"].append(
                    [{"name": line.strip()}]
                )
                circuit_wrestler_name_line_number += 18
            if index == contract_status:
                if int(line.strip()) > 1 and int(line.strip()) < 53:
                    circuit_roster[circuit_counter]["roster"][
                        circuit_roster_count
                    ].append({"contract_length": int(line.strip())})
                else:
                    circuit_roster[circuit_counter]["roster"][
                        circuit_roster_count
                    ].append({"contract_length": "unsigned"})
                contract_status += 18
                circuit_roster_count += 1

    circuit_wrestler_name_line_number = 1
    contract_status = 4
    circuit_counter += 1
    circuit_roster_count = 0
# print(circuit_roster)
# bad_contract_values = [0, 100, 1, "1", "0"]

print(circuit_roster)
tag_team_name = 3
tag_team_count = 0
tag_teams = []
member_1 = 1
member_2 = 2

print("*" * 100)
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
            tag_team_name += 10
            tag_team_count += 1
print(tag_teams)
