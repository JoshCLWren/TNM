"""Seed the database with Circuit, Wrestlers, Show, Stables, and Tag Teams"""
import faker

from faker import Faker
import wrestlers
import circuits
import Shows
import stables
import tag_teams

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


def create_wrestlers(amount, gender):
    """Seed the DB with five male wrestlers"""
    count = 0
    while count != amount:

        count += 1
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


def fake_stable(ids=[1, 2, 3]):
    return {"Stable Name": fake.slug(), "ids": ids}


def create_stable(amount, ids=[1, 2, 3]):
    count = 0
    while count != amount:
        count += 1
        stables.post_stable(fake_stable(ids=ids))


def fake_tag(members=[1, 2]):
    return {"name": fake.slug(), "members": members}


def create_tag(amount, members=[1, 2]):
    count = 0
    while count != amount:
        count += 1
        tag = {"name": fake.slug(), "members": members}
        tag_teams.post_tag_team(**tag)


def seed_database():
    circuits.seed_circuits([create_circuit()])

    wwf = circuits.get_by_id(1)

    import pdb

    pdb.set_trace()


seed_database()
