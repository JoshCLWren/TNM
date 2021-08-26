from database import cursor, con
import circuits
import Match_Maker
import wrestlers
import utilities


def create_show(name, match_total):
    """Creates a new show table"""
    circuit = circuits.get_by_name(name)
    if circuit is None:
        import pdb

        pdb.set_trace()
    males = []
    females = []

    eligible_wrestlers = []
    heels = []
    faces = []
    tweeners = []
    jobbers = []
    anti_heroes = []

    for wrestler in circuit["wrestlers"]:
        if wrestler not in circuit["injuries"]:
            eligible_wrestlers.append(wrestler)
        if wrestler in circuit["heels"]:
            heels.append(wrestler)
        elif wrestler in circuit["faces"]:
            faces.append(wrestler)
        elif wrestler in circuit["tweeners"]:
            tweeners.append(wrestler)
        elif wrestler in circuit["jobbers"]:
            jobbers.append(wrestler)
        else:
            anti_heroes.append(wrestler)
        if wrestlers.get_by_id(wrestler)["gender"] == "male":
            males.append(wrestler)
        else:
            females.append(wrestler)

    show = {
        "name": name,
        "busy_wrestlers": [],
        "eligible_wrestlers": eligible_wrestlers,
        "matches": match_total,
        "males": males,
        "females": females,
        "heels": heels,
        "faces": faces,
        "tweeners": tweeners,
        "jobbers": jobbers,
        "anti_heroes": anti_heroes,
        "card": [],
    }

    sql = """INSERT INTO SHOWS
        (name, busy_wrestlers, eligible_wrestlers, matches, males, females, heels,
         faces, tweeners, jobbers, anti_heroes, card)
        VALUES
        (%(name)s, %(busy_wrestlers)s, %(eligible_wrestlers)s, %(matches)s, %(males)s,
        %(females)s, %(faces)s, %(tweeners)s, %(jobbers)s, %(anti_heroes)s, %(heels)s, %(card)s) RETURNING *;
        """

    with con:
        cursor.execute(sql, show)

    show = cursor.fetchone()

    return show


# Match_Maker.matches(show)
# Match_Maker.main_event(tv_show=name)


def patch_show_roster(eligible_wrestlers, id):
    """Takes an updated list of of wrestlers and updates the show row"""

    kwargs = {"eligible_wrestlers": eligible_wrestlers, "id": id}
    query = utilities.prepare_columns(table="shows", **kwargs)

    cursor.execute(query, kwargs)

    show = cursor.fetchone()

    return show


def patch_show_card(card, id):
    """Adds the card list to the show"""

    kwargs = {"card": card, "id": id}
    query = utilities.prepare_columns(table="shows", **kwargs)

    cursor.execute(query, kwargs)

    show = cursor.fetchone()

    return show
