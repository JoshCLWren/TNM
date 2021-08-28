from database import cursor, con, wrestler_table
import utilities
import stables
import tag_teams


def wrestler_serializer():
    """This Maps over the WRESTLER.DAT file from tnm and builds a list of wrestlers and attributes"""
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
    with open(db) as wrestlers:
        for index, line in enumerate(wrestlers):
            if index == 0:
                wrestler_total = line.strip()
            if index == wrestler_name:
                wrestler_list.append({"name": line.strip()})
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
                wrestler_list[wrestle_count]["charisma"] = line.strip()
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
        with open(
            "TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/WRESTLRS.IDX"
        ) as wrestler_index:
            index_list = []
            for line in wrestler_index:
                index_list.append({"index": line.strip()})
            for id, wrestler in zip(index_list, wrestler_list):
                wrestler["tnm_index"] = id["index"]
    return wrestler_list


def seed_wrestlers(wrestler_list, drop=True, create_table=True):
    """Maps over a list of wrestlers and adds them to the wrestlers pg table"""
    if drop == True:
        cursor.execute("DROP TABLE wrestlers;")

    if create_table == True:
        wrestler_table()

    for wrestler in wrestler_list:
        query = """
                INSERT INTO WRESTLERS (name, work_rate, push, charisma, weight, gender, tnm_index)
                VALUES (%(name)s, %(work_rate)s, %(push)s, %(charisma)s, %(weight)s, %(gender)s, %(tnm_index)s);
                """
        with con:
            cursor.execute(query, wrestler)


def patch_wrestler(wrestler_id, column, new_value):
    """Changes the value of a given column to include the new_value if it's not a duplicate"""
    wrestler = get_by_id(wrestler_id)

    column_type = type(wrestler[column])

    new_value_type = type(new_value)

    mistypes = []

    if isinstance(wrestler[column], list):
        if new_value_type == int:
            utilities.check_dupes(wrestler[column], new_value)
        else:
            for number in new_value:
                if isinstance(number, int):
                    utilities.check_dupes(wrestler[column], number)
                else:
                    mistypes.append(number)
    else:
        if new_value_type == column_type:
            wrestler[column] = new_value
        else:
            return wrestler

    kwargs = {"id": wrestler_id, column: wrestler[column]}

    query = utilities.prepare_columns(table="wrestlers", **kwargs)

    cursor.execute(query, kwargs)

    wrestler = cursor.fetchone()

    return wrestler


def get_by_id(id):
    """Returns a wrestler with the matching id"""
    ids = []
    if isinstance(id, int):
        with con:
            cursor.execute("Select * from wrestlers where id = %(id)s;", {"id": id})

        return cursor.fetchone()
    if isinstance(id, list):
        for _id in id:
            with con:
                cursor.execute(
                    "Select * from wrestlers where id = %(id)s;", {"id": _id}
                )

                ids.append(cursor.fetchone())
        return ids


def get_all_wrestlers():
    """Returns all the wrestlers in the table"""
    with con:
        cursor.execute("Select * from wrestlers;")

    return cursor.fetchall()


def get_by_name(wrestler_name):
    """queries the wrestler table by the name value passed"""
    with con:
        cursor.execute(
            "Select * from wrestlers where name = %(wrestler_name)s;",
            {"wrestler_name": wrestler_name},
        )

    return cursor.fetchone()


def map_stables_to_wrestlers():
    """Maps the stable ids to each wrestler"""

    stables_list = stables.get_all_stables()

    for stable in stables_list:
        for member in stable["members"]:
            wrestler = get_by_id(member)
            wrestler["stables"].append(stable["id"])

            patch_wrestler(wrestler["id"], "stables", wrestler["stables"])


def map_tags_to_wrestlers():
    """Maps the tag ids to each wrestler"""

    tags_list = tag_teams.get_all_tags()

    for tag in tags_list:
        for member in tag["tag_team_members"]:
            wrestler = get_by_id(member)
            wrestler["tag_teams"].append(tag["id"])

            patch_wrestler(wrestler["id"], "tag_teams", wrestler["tag_teams"])


def post_wrestler(**wrestler):
    """Adds a wrestler row to the table"""

    query = """
                INSERT INTO WRESTLERS (name, work_rate, push, charisma, weight, gender, tnm_index)
                VALUES (%(name)s, %(work_rate)s, %(push)s, %(charisma)s, %(weight)s, %(gender)s, %(tnm_index)s)
                returning *;
                """
    with con:
        cursor.execute(query, wrestler)

    return cursor.fetchone()
