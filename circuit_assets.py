# Need some methods that keep track:
# who is in a circuit
# what tags/stables are available in a circuit
# Which wrestlers have appeared on the card already
# random match builders need to be heel vs face
# may need a relational all_wrestlersbase for this.

import json
import logging
import circuits
import wrestlers
import tag_teams

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename="asset.log",
    filemode="w",
    format="%(message)s",
)
logging.warning("circuit_assets.py")


def circuit_assets():
    """Map over all the specifics to a circuit and add them to each circuit"""
    all_circuits = circuits.get_all_circuits()
    all_wrestlers = wrestlers.get_all_wrestlers()
    all_tags = tag_teams.get_all_tags()
    map_injuries_to_circuits(all_circuits)
    map_circuit_to_wrestlers(all_circuits)
    map_tags_to_circuits(all_circuits, all_tags)

    # hired_stable_names = []
    # hired_stables = []
    # stables = open("stables.json")
    # stables = json.load(stables)
    # logging.warning(
    #     f"Mapping stables to hired wrestlers in {circuit['circuit_name']}"
    # )
    # for stable in stables["stables"]:
    #     for index, id in enumerate(stable["ids"]):
    #         if index == 0:
    #             pass
    #         else:
    #             if int(id) in hired_wrestler_ids:
    #                 if stable not in hired_stables:
    #                     id = int(id) - 1
    #                     hired_stable_names.append(stable["Stable Name"])
    #                     hired_stables.append(stable)
    #                     logging.warning(f"Adding {stable['Stable Name']}")
    # hired_stable_copy = []
    # # remove unusable first index of stable ids
    # for index, stable in enumerate(hired_stables):
    #     id_list = []
    #     for dex, id in enumerate(stable["ids"]):
    #         if dex == 0:
    #             pass
    #         else:
    #             id_list.append(id)
    #     hired_stable_copy.append(
    #         {
    #             "Stable Name": stable["Stable Name"],
    #             "Global Member Count": stable["member count"],
    #             "Member Ids": id_list,
    #         }
    #     )
    #     logging.warning(f"Removing duplicate {stable['Stable Name']}")

    # hired_stables = hired_stable_copy

    # for stable in hired_stables:
    #     logging.warning(f"Mapping {stable['Stable Name']} to hired wrstlers")
    #     member_names = []
    #     for id in stable["Member Ids"]:
    #         # The id corresponds to normal list indexing but is one greater
    #         wrestler_id = int(id) - 1
    #         if all_wrestlers["wrestlers"][wrestler_id]["name"] in hired_wrestlers_names:
    #             member_names.append(all_wrestlers["wrestlers"][wrestler_id]["name"])
    #             logging.warning(
    #                 f"Adding {all_wrestlers['wrestlers'][wrestler_id]['name']} to {stable['Stable Name']}"
    #             )
    #     stable["Members"] = member_names
    #     stable["Hired Members"] = len(stable["Members"])

    # circuit["Stables"] = hired_stables
    # circuit["Stable List"] = hired_stable_names

    # circuit_roster = all_circuits["Circuits"]


def map_injuries_to_circuits(all_circuits):
    """Maps over the CARD.INJ of each circuit and updates the injury list"""

    filepath = "TNM/tnm7se_build_13/tnm7se/TNM7SE/"
    for circuit in all_circuits:

        circuit["injuries"] = []
        injured_wrestler_count = 0
        logging.warning("Finding Injured Wrestlers")

        try:
            with open(f"{filepath}{circuit['name']}/CARD.INJ") as injuries:
                logging.warning(f" Processing {filepath}{circuit['name']}/CARD.INJ")
                for index, line in enumerate(injuries):
                    if index % 2 == 0:
                        wrestler_id = line.strip()
                        try:
                            wrestler_id = int(wrestler_id)
                            wrestler_id = wrestler_id - 1
                        except ValueError:
                            wrestler = wrestlers.get_by_name(wrestler_id)
                            wrestler_id = wrestler["id"]
                        circuit["injuries"].append(wrestler_id)

                    else:
                        injured_wrestler_count += 1
        except FileNotFoundError:
            pass

        circuits.update_circuit(**circuit)


def map_circuit_to_wrestlers(all_circuits):
    """maps each id in each circit wrestler to each wrestler"""

    for circuit in all_circuits:
        for wrestler in circuit["wrestlers"]:
            wrestlers.patch_wrestler(wrestler, "circuits", circuit["id"])


def map_tags_to_circuits(all_circuits, all_tags):
    """maps each id in tag to each circuit"""

    for circuit in all_circuits:
        for tag in all_tags:
            tag_members = []
            for member in tag["tag_team_members"]:

                if member in circuit["wrestlers"]:
                    tag_members.append(member)
                else:
                    continue
            if len(tag_members) == 2:
                circuit["tag_teams"].append(tag["id"])
        circuits.patch_circuit(circuit["id"], "tag_teams", circuit["tag_teams"])


def map_stables_to_wrestlers_and_circuits(stable_list):
    """Maps over the stable list add adds them to wrestlers and circuits"""
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
