# Need some methods that keep track:
# who is in a circuit
# what tags/stables are available in a circuit
# Which wrestlers have appeared on the card already
# random match builders need to be heel vs face
# may need a relational all_wrestlersbase for this.

import logging
import circuits
import wrestlers
import tag_teams
import stables


def circuit_assets():
    """Map over all the specifics to a circuit and add them to each circuit"""
    all_circuits = circuits.get_all_circuits()
    all_wrestlers = wrestlers.get_all_wrestlers()
    all_tags = tag_teams.get_all_tags()
    all_stables = stables.get_all_stables()
    map_injuries_to_circuits(all_circuits)
    map_circuit_to_wrestlers(all_circuits)
    map_tags_to_circuits(all_circuits, all_tags)
    map_stables_to_circuits(all_stables, all_circuits)


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


def map_stables_to_circuits(stables, all_circuits):
    """Maps over the stable list add adds them to wrestlers and circuits"""

    for circuit in all_circuits:
        for stable in stables:
            for id in stable["members"]:
                if id in circuit["wrestlers"]:
                    if stable["id"] not in circuit["stables"]:
                        circuit["stables"].append(stable["id"])
        circuits.patch_circuit(circuit["id"], "stables", circuit["stables"])
