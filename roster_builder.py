import logging
import json


def roster_builder(tv_show):
    logging.warning("Building Roster")
    wwe_products = ["Raw", "Smackdown", "205"]

    if tv_show == "ROH":
        tv_show = "CMLL"
    if tv_show in wwe_products:
        circuit = "WWE"
    else:
        circuit = tv_show.upper()
    logging.warning("Opening circuit_roster_db.json")
    circuit_json = open("circuit_roster_db.json")
    circuit_json = json.load(circuit_json)

    # todo: add filter to only add stables with more than one member

    # todo: add injured wrestlers and eligible wrestlers. stored in card.inj of each circuit

    for promotion in circuit_json["Circuits"]:
        logging.warning(f'processing {promotion["circuit_name"]}')
        if promotion["circuit_name"] == circuit:
            circuit_roster = {
                "Hired Wrestlers": promotion["Wrestler List"],
                "Tag Teams": promotion["tag teams"],
                "Hired Tag List": promotion["Hired Tag List"],
                "Stables": promotion["Stables"],
                "Stable List": promotion["Stable List"],
                "injured names": promotion["injury names"],
                "Eligible Roster": [],
                "Busy Wrestlers": [],
            }
            for wrestler in promotion["Wrestler List"]:
                if wrestler not in promotion["injury names"]:
                    circuit_roster["Eligible Roster"].append(wrestler)
            # the idea is to make matches heel vs face matches that
            # only have wrestlers that aren't in Busy Wrestlers
            # So that nobody wresters more than once
            # except for 24/7 or other exceptions I can't think of
            # the circuit_roster dictionary will need to be mutated with each match
            # Injured non/title holders can't wrestler

    return circuit_roster
