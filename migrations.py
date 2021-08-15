import json
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename="migration.log",
    filemode="w",
    format="%(message)s",
)
logging.warning("migrations.py")
import psycopg2
import wrestlers
import circuits
import tag_teams
import database
import stables


def db_builder():

    database.wrestler_table()
    wrestler_list = wrestlers.wrestler_serializer()
    wrestlers.seed_wrestlers(wrestler_list)

    database.circuit_table()
    circuit_rosters = circuits.circuit_serializer()
    circuits.seed_circuits(circuit_rosters)

    database.tag_teams_table()
    tags = tag_teams.tag_team_serializer()
    tag_teams.seed_tags(tags)

    database.stables_table()
    stable_list = stables.stable_serializer()
    stables.seed_stables(stable_list)
