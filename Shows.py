from database import cursor, con
import circuits
import Match_Maker


def create_show(name, match_total):
    """Creates a new show table"""
    circuit = circuits.get_by_name(name)

    eligble_participants = []

    for wrestler in circuit["wrestlers"]:
        if wrestler not in circuit["injuries"]:
            eligble_participants.append(wrestler)

    Match_Maker.matches(name, circuit, eligble_participants, match_total=match_total)
    Match_Maker.main_event(tv_show=name)
