import wrestlers
import circuits
import tag_teams
import stables
import Championships


def db_builder():

    wrestler_list = wrestlers.wrestler_serializer()
    wrestlers.seed_wrestlers(wrestler_list)

    circuit_rosters = circuits.circuit_serializer()
    circuits.seed_circuits(circuit_rosters)
    promotions = [circuit["name"] for circuit in circuits.get_all_circuits()]

    tags = tag_teams.tag_team_serializer()
    tag_teams.seed_tags(tags)

    stable_list = stables.stable_serializer()
    stables.seed_stables(stable_list)

    wrestlers.map_stables_to_wrestlers()
    wrestlers.map_tags_to_wrestlers()

    champion_list = Championships.championship_serializer(promotions)
    Championships.seed_championships(champion_list)
