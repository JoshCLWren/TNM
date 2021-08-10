# Need some methods that keep track:
# who is in a circuit
# what tags/stables are available in a circuit
# Which wrestlers have appeared on the card already
# random match builders need to be heel vs face
# may need a relational database for this.

import json

data = open("wrestler_db.json")

data = json.load(data)


def circuit_assets():
    circuit_json = open("circuit_roster_db.json")
    circuit_json = json.load(circuit_json)
    data = open("wrestler_db.json")
    data = json.load(data)

    for circuit in circuit_json["Circuits"]:
        hired_wrestler_ids = []
        hired_wrestlers = []
        hired_wrestlers_names = []
        for wrestler in data["wrestlers"]:
            if circuit["circuit_name"] in wrestler["circuits"]:
                hired_wrestlers.append(wrestler)
                hired_wrestlers_names.append(wrestler["name"])
                hired_wrestler_ids.append(wrestler["id"])

        circuit["Wrestler List"] = hired_wrestlers_names

        hired_tags_names = []
        hired_tag_teams = []
        for wrestler in hired_wrestlers:
            for tag in wrestler["tag teams"]:
                if (
                    tag["Partner"] in hired_wrestlers_names
                    and tag["Tag Team Name"] not in hired_tags_names
                ):
                    hired_tags_names.append(tag["Tag Team Name"])
                    hired_tag_teams.append(
                        {
                            "Tag Team Name": tag["Tag Team Name"],
                            "Member 1": wrestler["name"],
                            "Member 2": tag["Partner"],
                        }
                    )

        circuit["Hired Tag List"] = hired_tags_names

        hired_stable_names = []
        hired_stables = []
        stables = open("stables.json")
        stables = json.load(stables)
        for stable in stables["stables"]:
            for index, id in enumerate(stable["ids"]):
                if index == 0:
                    pass
                else:
                    if int(id) in hired_wrestler_ids:
                        if stable not in hired_stables:
                            id = int(id) - 1
                            hired_stable_names.append(stable["Stable Name"])
                            hired_stables.append(stable)
        hired_stable_copy = []
        # remove unusable first index of stable ids
        for index, stable in enumerate(hired_stables):
            id_list = []
            for dex, id in enumerate(stable["ids"]):
                if dex == 0:
                    pass
                else:
                    id_list.append(id)
            hired_stable_copy.append(
                {
                    "Stable Name": stable["Stable Name"],
                    "Global Member Count": stable["member count"],
                    "Member Ids": id_list,
                }
            )
        hired_stables = hired_stable_copy

        for stable in hired_stables:
            member_names = []
            for id in stable["Member Ids"]:
                # The id corresponds to normal list indexing but is one greater
                wrestler_id = int(id) - 1
                if data["wrestlers"][wrestler_id]["name"] in hired_wrestlers_names:
                    member_names.append(data["wrestlers"][wrestler_id]["name"])
            stable["Members"] = member_names
            stable["Hired Members"] = len(stable["Members"])

        circuit["Stables"] = hired_stables
        circuit["Stable List"] = hired_stable_names

    circuit_roster = circuit_json["Circuits"]

    class json_convert(dict):
        def __str__(self):
            return json.dumps(self)

    with open("circuit_roster_db.json", "w") as file:
        file.write('{"Circuits": [')
        for index, circuit in enumerate(circuit_roster):
            circuit = json_convert(circuit)
            last_spot = len(circuit_roster) - 1
            if index == last_spot:
                file.write(f"{circuit}\n")
            else:
                file.write(f"{circuit}\n,")
        file.write("]}")
