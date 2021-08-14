import psycopg2.extras

con = psycopg2.connect("dbname=test user=postgres")
cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


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
        with con:
            cursor.execute(
                """
              CREATE TABLE IF NOT EXISTS WRESTLERS(
              id bigserial PRIMARY KEY,
              name VARCHAR,
              work_rate INTEGER,
              push INTEGER,
              charisma INTEGER,
              weight INTEGER,
              gender VARCHAR,
              tnm_index INTEGER,
              circuits INTEGER[] DEFAULT '{}',
              tag_teams INTEGER[] DEFAULT '{}',
              stables INTEGER[] DEFAULT '{}'
              );
                """
            )

    for wrestler in wrestler_list:
        query = """
                INSERT INTO WRESTLERS (name, work_rate, push, charisma, weight, gender, tnm_index)
                VALUES (%(name)s, %(work_rate)s, %(push)s, %(charisma)s, %(weight)s, %(gender)s, %(tnm_index)s);
                """
        with con:
            cursor.execute(query, wrestler)


def add_circuit(wrestler_id, circuit_id):
    """Adds a circuit to a wrestlers circuit array column"""
    wrestler = get_by_id(wrestler_id)

    if circuit_id not in wrestler["circuits"]:
        wrestler["circuits"].append(circuit_id)
    else:
        return wrestler

    query = """
            UPDATE WRESTLERS
            SET circuits = %(circuits)s WHERE id = %(id)s
            RETURNING *;
            """

    cursor.execute(query, {"id": wrestler_id, "circuits": wrestler["circuits"]})

    wrestler = cursor.fetchone()

    return wrestler


def get_by_id(id):
    """Returns a wrestler with the matching id"""

    cursor.execute("Select * from wrestlers where id = %(id)s;", {"id": id})

    return cursor.fetchone()
