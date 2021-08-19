from database import cursor, con
import circuits
import Match_Maker
import wrestlers
import utilities


def create_show(name, match_total):
    """Creates a new show table"""
    circuit = circuits.get_by_name(name)

    males = []
    females = []

    eligble_wrestlers = []
    ready_male_heels = []
    ready_male_faces = []
    ready_male_tweeners = []
    ready_male_jobbers = []
    ready_male_anti_heroes = []
    ready_female_heels = []
    ready_female_faces = []
    ready_female_tweeners = []
    ready_female_jobbers = []
    ready_female_anti_heroes = []

    for wrestler in circuit["wrestlers"]:
        if wrestler not in circuit["injuries"]:
            eligble_wrestlers.append(wrestler)
        gender = "male"
        if wrestlers.get_by_id(wrestler)["gender"] == gender:
            males.append(wrestler)
            if wrestler in circuit["heels"]:
                ready_male_heels.append(wrestler)
            elif wrestler in circuit["faces"]:
                ready_male_faces.append(wrestler)
            elif wrestler in circuit["tweeners"]:
                ready_male_tweeners.append(wrestler)
            elif wrestler in circuit["jobbers"]:
                ready_male_jobbers.append(wrestler)
            else:
                ready_male_anti_heroes.append(wrestler)
        else:
            females.append(wrestler)
            if wrestler in circuit["heels"]:
                ready_female_heels.append(wrestler)
            elif wrestler in circuit["faces"]:
                ready_female_faces.append(wrestler)
            elif wrestler in circuit["tweeners"]:
                ready_female_tweeners.append(wrestler)
            elif wrestler in circuit["jobbers"]:
                ready_female_jobbers.append(wrestler)
            else:
                ready_female_anti_heroes.append(wrestler)
    show = {
        "name": name,
        "busy_wrestlers": [],
        "eligble_wrestlers": eligble_wrestlers,
        "matches": [match_total],
    }

    show["ready_male_heels"] = ready_male_heels
    show["ready_male_faces"] = ready_male_faces
    show["ready_male_tweeners"] = ready_male_tweeners
    show["ready_male_jobbers"] = ready_male_jobbers
    show["ready_male_anti_heroes"] = ready_female_anti_heroes
    show["ready_female_heels"] = ready_female_heels
    show["ready_female_faces"] = ready_female_faces
    show["ready_female_tweeners"] = ready_female_tweeners
    show["ready_female_jobbers"] = ready_female_jobbers
    show["ready_female_anti_heroes"] = ready_male_anti_heroes

    sql = """INSERT INTO SHOWS
        (name, busy_wrestlers, matches, eligble_wrestlers, ready_male_heels, ready_male_faces,
        ready_male_tweeners, ready_male_jobbers, ready_male_anti_heroes, ready_female_heels,
        ready_female_faces, ready_female_tweeners, ready_female_jobbers, ready_female_anti_heroes)
        VALUES
        (%(name)s, %(busy_wrestlers)s, %(matches)s, %(eligble_wrestlers)s, %(ready_male_heels)s,
        %(ready_male_faces)s,
        %(ready_male_tweeners)s, %(ready_male_jobbers)s, %(ready_male_anti_heroes)s,
        %(ready_female_heels)s,
        %(ready_female_faces)s, %(ready_female_tweeners)s, %(ready_female_jobbers)s,
        %(ready_female_anti_heroes)s) RETURNING *;
        """

    with con:
        cursor.execute(sql, show)

    show = cursor.fetchone()

    Match_Maker.matches(show)
    Match_Maker.main_event(tv_show=name)


def patch_show_roster(eligble_wrestlers, id):
    """Takes an updated list of of wrestlers and updates the match row"""
    kwargs = {"eligble_wrestlers": eligble_wrestlers, "id": id}
    query = utilities.prepare_columns(table="matches", **kwargs)

    cursor.execute(query, kwargs)

    show = cursor.fetchone()

    return show
