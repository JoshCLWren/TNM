import logging
import json
from roster import roster


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
            male_anti_heroes = []
            female_heels = []
            female_faces = []
            female_tweeners = []
            female_jobbers = []
            female_anti_heroes = []
            errors = []
            for wrestler in promotion["roster"]:
                personality = wrestler[2]["personality"]
                gender = wrestler[3]["gender"]
                name = wrestler[0]["name"]
                # anti-heroes are faces that employ heel tactics
                if gender == "male":
                    if personality == "face":
                        male_faces.append(name)
                    elif personality == "heel":
                        male_heels.append(name)
                    elif personality == "tweener":
                        male_tweeners.append(name)
                    elif personality == "anti-hero":
                        male_anti_heroes.append(name)
                    elif personality == "jobber":
                        male_jobbers.append(name)
                    else:
                        print("Wrestler has no personality")
                        print(wrestler)

                else:
                    if personality == "face":
                        female_faces.append(name)
                    elif personality == "heel":
                        female_heels.append(name)
                    elif personality == "tweener":
                        female_tweeners.append(name)
                    elif personality == "anti-hero":
                        female_anti_heroes.append(name)
                    elif personality == "jobber":
                        female_jobbers.append(name)
                    else:
                        print("Wrestler has no personality")
                        print(wrestler)
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
                "Male Ready Heels": male_heels,
                "Male Ready Faces": male_faces,
                "Male Ready Anti Heroes": male_anti_heroes,
                "Male Ready Tweeners": male_tweeners,
                "Male Ready Jobbers": male_jobbers,
                "Female Ready Heels": female_heels,
                "Female Ready Faces": female_faces,
                "Female Ready Anti Heroes": female_anti_heroes,
                "Female Ready Tweeners": female_tweeners,
                "Female Ready Jobbers": female_jobbers,
                "Tag Teams": promotion["tag teams"],
                "Hired Tag List": promotion["Hired Tag List"],
                "Stables": stables,
                "Stable List": stable_list,
                "Stable Tags": stable_tags,
                "Stable Tags List": stable_tags_list,
                "injured names": promotion["injury names"],
                "Eligible Roster": [],
                "Busy Wrestlers": busy_wrestlers,
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

    with open("roster.py", "w") as roster:
        roster.write(f"roster = {str(circuit_roster)}")


def roster_updater(busy_wrestlers=[]):
    for wrestler in busy_wrestlers:
        if wrestler not in roster["Busy Wrestlers"]:
            roster["Busy Wrestlers"].append(wrestler)

    with open("roster.py", "w") as new_roster:
        new_roster.write(f"roster = {str(roster)}")
