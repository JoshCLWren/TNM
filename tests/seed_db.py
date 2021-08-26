"""Seed the database with Circuit, Wrestlers, Show, Stables, and Tag Teams"""
import faker

from faker import Faker
import wrestlers
import circuits
import Shows
import stables
import tag_teams
import database

fake = Faker("en_US")


def fake_wrestler(
    name="Mr. X",
    work_rate=99,
    push=98,
    charisma=97,
    weight=98,
    gender="male",
    tnm_index=1,
    circuits=[],
    tag_teams=[],
    stables=[],
):
    fake_wrestler = {
        "name": name,
        "work_rate": work_rate,
        "push": push,
        "charisma": charisma,
        "weight": weight,
        "gender": gender,
        "tnm_index": tnm_index,
        "circuits": circuits,
        "tag_teams": tag_teams,
        "stables": stables,
    }
    return fake_wrestler


def create_wrestlers(amount, gender, reset=True):
    """Seed the DB with five male(or female) wrestlers"""
    if reset == True:
        database.reset_and_delete("wrestlers")
    count = 0

    while count != amount:
        count += 1
        if gender == "even":
            if count % 2 == 0:
                dude = fake_wrestler(name=fake.name(), gender="male")
            else:
                dude = fake_wrestler(name=fake.name(), gender="female")
        else:
            dude = fake_wrestler(name=fake.name(), gender=gender)
        wrestlers.post_wrestler(**dude)


def create_circuit(
    name="WWF",
    stables=[],
    tag_teams=[],
    _wrestlers=[],
    injuries=[],
    heels=[],
    faces=[],
    anti_heroes=[],
    jobbers=[],
    championships=[],
    tweeners=[],
):
    return {
        "name": name,
        "stables": stables,
        "tag_teams": tag_teams,
        "wrestlers": _wrestlers,
        "injuries": injuries,
        "heels": heels,
        "faces": faces,
        "anti_heroes": anti_heroes,
        "tweeners": tweeners,
        "jobbers": jobbers,
        "championships": championships,
    }


def fake_stable(name="nwo", ids=[1, 2, 3]):
    return {"name": name, "members": ids}


def create_stable(factions):
    database.reset_and_delete("stables")
    for faction in factions:
        stable = fake_stable(faction, factions[faction])
        stables.post_stable(stable)


def fake_tag(members=[1, 2]):
    return {"name": fake.slug(), "members": members}


def create_tag(amount, members=[1, 2]):
    count = 0
    while count != amount:
        count += 1
        tag = {"name": fake.slug(), "members": members}
        tag_teams.post_tag_team(**tag)


def seed_database(name="wwf"):

    circuits.seed_circuits([create_circuit(name)])

    wwf = circuits.get_by_id(1)

    create_wrestlers(40, gender="even", reset=True)

    grapplers = wrestlers.get_all_wrestlers()

    factions = {
        "heels": [],
        "faces": [],
        "tweeners": [],
        "jobbers": [],
        "anti_heroes": [],
    }
    counter = 0

    for faction in factions:
        while len(factions[faction]) != 8:
            factions[faction].append(grapplers[counter]["id"])
            wwf[faction].append(grapplers[counter]["id"])
            counter += 1

    create_stable(factions)
    for faction in factions:
        circuits.patch_circuit(1, faction, factions[faction])
    circuits.patch_circuit(1, "stables", [1, 2, 3, 4, 5])
    circuits.patch_circuit(1, "wrestlers", [*range(1, 41)])
