from database import cursor, con, stables_table
import utilities


def stable_serializer():
    """this maps over the STABLES.DAT file from TNM and builds a python list out of it"""
    stable_count = -1
    stable_list = []
    stable_total = 0

    with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/STABLES.DAT") as stables:
        for index, line in enumerate(stables):
            if index == 0:
                stable_total = line.strip()
            if (
                line.strip().isalpha() == True
                or " " in line.strip()
                or "-" in line.strip()
            ):
                stable_count += 1
                stable_list.append({"Stable Name": line.strip()})
                stable_list[stable_count]["ids"] = []
            if (
                line.strip().isdigit() == True
                and line.strip() != stable_total
                and line.strip() != "0"
            ):
                stable_list[stable_count]["ids"].append(int(line.strip()))

    return stable_list


def seed_stables(stable_list, drop=True, create_table=True):
    """Maps over a list of stables and add them to the stable table"""
    if drop == True:
        cursor.execute("DROP TABLE stables;")

    if create_table == True:
        stables_table()

    for stable in stable_list:

        stable_copy = {}
        stable_copy["name"] = stable["Stable Name"]
        stable_copy["members"] = stable["ids"][1:]

        query = """
                INSERT INTO STABLES (name, members)
                VALUES (%(name)s, %(members)s);
                """
        with con:
            cursor.execute(query, stable_copy)


def get_all_stables():
    """Returns all stables in the db"""

    with con:
        cursor.execute("Select * from stables;")

    return cursor.fetchall()


def get_by_id(id):
    """Returns the stable specified, if a stable name is passed searches by that instead"""

    if isinstance(id, str):
        with con:
            cursor.execute("select * from stables where name = %(name)s;", {"name": id})

    if id == []:
        return None

    if isinstance(id, int):
        with con:
            cursor.execute("select * from stables where id = %(id)s;", {"id": id})

    stable = cursor.fetchone()

    if stable == None:
        return None
    return stable


def patch_stable(id, column, new_value):
    """Change the name or members of a stable"""

    stable = get_by_id(id)

    column_type = type(stable[column])

    new_value_type = type(new_value)

    mistypes = []

    if isinstance(stable[column], list):
        if new_value_type == int:
            utilities.check_dupes(stable[column], new_value)
        else:
            for number in new_value:
                if isinstance(number, int):
                    utilities.check_dupes(stable[column], number)
                else:
                    mistypes.append(number)
    else:
        if new_value_type == column_type:
            stable[column] = new_value
        else:
            return stable

    kwargs = {"id": id, column: stable[column]}

    query = utilities.prepare_columns(table="stables", **kwargs)

    cursor.execute(query, kwargs)

    stable = cursor.fetchone()

    return stable


def post_stable(stable):
    """Adds a stable row to the table"""

    query = """
                INSERT INTO stables (name, members)
                VALUES (%(name)s, %(members)s)
                returning *;
                """
    with con:
        cursor.execute(query, stable)

    return cursor.fetchone()
