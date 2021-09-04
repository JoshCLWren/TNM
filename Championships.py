from psycopg2.extras import RealDictRow
import utilities
from database import con, cursor, circuit_table
import wrestlers
import circuit_assets
import circuits

promotions = ["AEW", "CMLL", "IMPACT", "MLW", "NJPW", "NXT", "ROH", "WWE"]


def championship_serializer(promotions):
    """Parses titles and title holders for each circuit"""
    titles = []
    for circuit in promotions:
        with open(f"TNM/tnm7se_build_13/tnm7se/TNM7SE/{circuit}/CARD.TTL") as champs:

            title_total = 0
            champ_line = 1
            title_name = 2
            flag = 3
            title_count = 0
            for index, line in enumerate(champs):
                if index == title_total:
                    title_total = line.strip()
                if index == champ_line:
                    titles.append({"title_holder": line.strip()})
                    champ_line += 3

                if index == title_name:

                    titles[title_count]["name"] = line.strip()
                    title_name += 3

                    titles[title_count]["circuit_id"] = circuits.get_by_name(circuit)[
                        "id"
                    ]
                    title_count += 1
    import pdb

    pdb.set_trace()
    return titles


championship_serializer(promotions)
