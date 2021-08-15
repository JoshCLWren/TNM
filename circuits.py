import utilities
from database import con, cursor, circuit_table
import logging
import wrestlers
import circuit_assets

# This needs to be a method that maps over the tnm directory to find promotions in the future
circuits = ["AEW", "CMLL", "IMPACT", "MLW", "NJPW", "NXT", "ROH", "WWE"]


def circuit_serializer(
    circuits=["AEW", "CMLL", "IMPACT", "MLW", "NJPW", "NXT", "ROH", "WWE"]
):
    """Serializes the tnm circuit file into a list of dictionaries"""
    circuit_roster = []
    circuit_counter = 0

    logging.warning("Building Circuit Databases")
    for circuit in circuits:
        with open(
            f"TNM/tnm7se_build_13/tnm7se/TNM7SE/{circuit}/CIRCDB.DAT"
        ) as circuit_db:
            logging.warning(f"parsing {circuit}")
            circuit_roster.append(
                {
                    "name": circuit,
                    "wrestlers": [],
                    "tag_teams": [],
                    "stables": [],
                    "injuries": [],
                    "heels": [],
                    "faces": [],
                    "anti_heroes": [],
                    "tweeners": [],
                    "jobbers": [],
                    "championships": [],
                }
            )
            for index, line in enumerate(circuit_db):
                if index == 0:
                    circuit_wrestler_name_line_number = 1
                    contract_status = 3
                    personality = 4
                    circuit_roster_count = 0
                if index == circuit_wrestler_name_line_number:
                    wrestler = {}
                    circuit_roster[circuit_counter]["wrestlers"].append(
                        [{"name": line.strip()}]
                    )
                    logging.warning(f"adding {line.strip()} to {circuit}")
                    circuit_wrestler_name_line_number += 18
                if index == contract_status:
                    logging.warning("Adding Contract Status")
                    if int(line.strip()) > 0 and int(line.strip()) < 53:
                        circuit_roster[circuit_counter]["wrestlers"][
                            circuit_roster_count
                        ].append({"contract_length": int(line.strip())})
                    else:
                        circuit_roster[circuit_counter]["wrestlers"][
                            circuit_roster_count
                        ].append({"contract_length": 0})
                    contract_status += 18
                if index == personality:
                    logging.warning("Adding Personality")
                    line = int(line.strip())
                    persona = personality_switch(line)
                    circuit_roster[circuit_counter]["wrestlers"][
                        circuit_roster_count
                    ].append({"personality": persona})
                    if personality == "nothing":
                        raise Exception

                    personality += 18
                    circuit_roster_count += 1
        circuit_counter += 1

    for circuit in circuit_roster:
        circuit["wrestlers"] = [
            wrestler
            for wrestler in circuit["wrestlers"]
            if wrestler[1]["contract_length"] != 0
        ]
        circuit["championships"] = championship_serializer(circuit["name"])
    return circuit_roster


def seed_circuits(circuit_rosters, drop=True, create_table=True):
    """Maps over the serialized circuit roster list and seeds the database table"""
    if drop == True:
        cursor.execute("DROP TABLE circuits;")

    if create_table == True:
        circuit_table()

    for circuit in circuit_rosters:
        grapplers = []
        for grappler in circuit["wrestlers"]:
            if grappler[0]["name"] == "Adrian Jaoude":
                grappler[0]["name"] = "Arturo Ruas"

            wrestler = wrestlers.get_by_name(grappler[0]["name"])
            grapplers.append(wrestler["id"])
            if grappler[2]["personality"] == "anti-hero":
                circuit["anti_heroes"].append(wrestler["id"])
            else:
                circuit[f"{grappler[2]['personality']}s"].append(wrestler["id"])

        circuit["wrestlers"] = grapplers

        query = """
              INSERT INTO CIRCUITS (name, stables, tag_teams, wrestlers, injuries, heels, faces, anti_heroes, tweeners, jobbers, championships)
              values (%(name)s, %(stables)s, %(tag_teams)s, %(wrestlers)s, %(injuries)s, %(heels)s, %(faces)s, %(anti_heroes)s, %(tweeners)s, %(jobbers)s, %(championships)s)

              """
        with con:
            cursor.execute(query, circuit)


def get_all_circuits():
    """gets all the circuits"""
    with con:
        cursor.execute("Select * from circuits;")

    return cursor.fetchall()


def get_by_id(circuit_id):
    """Retrieves the circuit with the matching id"""
    with con:
        cursor.execute("Select * from circuits where id = %(id)s;", {"id": circuit_id})

    return cursor.fetchone()


def update_circuit(**kwargs):
    """Updates all passed fields"""

    sql = utilities.prepare_columns(table="circuits", **kwargs)

    with con:
        cursor.execute(sql, kwargs)

    circuit = cursor.fetchone()

    return circuit


def patch_circuit(circuit_id, column, new_value):
    """Update a single column on a circuit"""

    circuit = get_by_id(circuit_id)

    column_type = type(circuit[column])

    new_value_type = type(new_value)

    mistypes = []
    if isinstance(circuit[column], list):
        if new_value_type == int:
            utilities.check_dupes(circuit[column], new_value)
        elif new_value_type == list:
            for number in new_value:
                if isinstance(number, int):
                    utilities.check_dupes(circuit[column], number)
                else:
                    mistypes.append(number)
    else:
        if new_value_type == column_type:
            circuit[column] = new_value
        else:
            return circuit

    kwargs = {"id": circuit_id, column: circuit[column]}

    query = utilities.prepare_columns(table="circuits", **kwargs)

    cursor.execute(query, kwargs)

    circuit = cursor.fetchone()

    return circuit


def get_by_name(name):
    """Retrieves the circuit with the name"""
    wwe_products = ["Raw", "Smackdown", "205"]
    if name == "ROH":
        name = "CMLL"
    if name in wwe_products:
        name = "WWE"
    with con:
        cursor.execute("Select * from circuits where name = %(name)s;", {"name": name})

    return cursor.fetchone()


def personality_switch(argument):
    """returns the corresponding tnm value with a real text equivilant"""
    switcher = {0: "face", 1: "heel", 2: "tweener", 3: "jobber", 5: "anti-hero"}

    return switcher.get(argument, "nothing")


def championship_serializer(circuit):
    """maps over the circuit/details.ttl file and adds championships to the circuit table"""
    titles = []
    title_index_count = 0
    try:
        with open(
            f"TNM/tnm7se_build_13/tnm7se/TNM7SE/{circuit}/details.ttl"
        ) as championships:
            for index, line in enumerate(championships):
                if index == title_index_count:
                    titles.append(line.strip())
                    title_index_count += 3
    except FileNotFoundError:
        print(
            f"No titles found in {circuit}, try opening weight class wizard and trying again."
        )
        pass

    return titles
