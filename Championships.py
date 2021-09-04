from psycopg2.extras import RealDictRow
import utilities
from database import con, cursor, circuit_table
import wrestlers
import circuit_assets
import circuits
import database
import utilities


def championship_serializer(promotions):
    """Parses titles and title holders for each circuit"""
    titles = []
    title_count = 0
    for circuit in promotions:
        with open(f"TNM/tnm7se_build_13/tnm7se/TNM7SE/{circuit}/CARD.TTL") as champs:

            title_total = 0
            champ_line = 1
            title_name = 2
            flag = 3

            for index, line in enumerate(champs):
                if index == title_total:
                    title_total = line.strip()
                if index == champ_line:
                    titles.append({"title_holder": line.strip()})
                    titles[title_count]["circuit_id"] = circuits.get_by_name(circuit)[
                        "id"
                    ]
                    titles[title_count]["name"] = ""
                    titles[title_count]["type"] = ""
                    champ_line += 3

                if index == title_name:

                    titles[title_count]["name"] = line.strip()
                    title_name += 3

                if index == flag:
                    types = {1: "singles", 2: "tag", 3: "trio"}

                    titles[title_count]["type"] = types.get(int(line.strip()))
                    flag += 3

                    title_count += 1

    return titles


def seed_championships(title_list, drop=True, create_table=True):
    """Turn the list of titles into rows in the championships table"""
    if drop == True:
        cursor.execute("DROP TABLE championships;")

    if create_table == True:
        database.championships_table()
    query = """
            INSERT INTO championships (title_holder, circuit_id, name, type)
            VALUES (%(title_holder)s, %(circuit_id)s, %(name)s, %(type)s);
            """

    for title in title_list:

        with con:
            cursor.execute(query, title)


def get_some(columns, many=False):
    """return either one or more matching rows for fields passed"""

    with con:
        cursor.execute(utilities.get_by_column("championships", **columns))

    if many is False:
        return cursor.fetchone()
    else:
        return cursor.fetchall()
