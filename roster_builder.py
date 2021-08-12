import logging
import json


def roster_builder(tv_show, busy_wrestlers=[]):
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

    for promotion in circuit_json["Circuits"]:
        logging.warning(f'processing {promotion["circuit_name"]}')
        if promotion["circuit_name"] == circuit:
            male_heels = []
            male_faces = []
            male_tweeners = []
            male_jobbers = []
            female_heels = []
            female_faces = []
            female_tweeners = []
            female_jobbers = []
            # for wrestler in promotion["roster"]:
            #     import pdb

            #     pdb.set_trace()
            stables = []
            stable_list = []
            # Stable Tags are Stables that only have 2 members hired
            # that are a virtual tag team
            stable_tags = []
            stable_tags_list = []
            for stable in promotion["Stables"]:
                if stable["Hired Members"] > 2:
                    stables.append(stable)
                    stable_list.append(stable["Stable Name"])
                if stable["Hired Members"] == 2:
                    stable_tags.append(stable)
                    stable_tags_list.append(stable["Stable Name"])
            circuit_roster = {
                "Hired Wrestlers": promotion["Wrestler List"],
                "Ready Heels": [],
                "Ready Faces": [],
                "Tag Teams": promotion["tag teams"],
                "Hired Tag List": promotion["Hired Tag List"],
                "Stables": stables,
                "Stable List": stable_list,
                "Stable Tags": stable_tags,
                "Stable Tags List": stable_tags_list,
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
