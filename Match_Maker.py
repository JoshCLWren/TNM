import logging
from utilities import (
    roll,
    combatent_picker,
    team_sizer,
    title,
    gender_picker,
    tag_match_maker,
)
import random
import circuits
import wrestlers
import stables


def main_event(tv_show):
    elimination_match = 10
    number_1_contender_match = 75
    title_defense = 99
    battle_royal = 100
    main_event_roll = roll()
    logging.warning(f"Main even roll = {main_event_roll}")
    main_event = f"debugger"
    if main_event_roll == battle_royal:
        main_event = "20 Man Battle Royal"
        logging.warning("Main Event20 man battle royal")
    if main_event_roll <= elimination_match:
        main_event = f"{team_sizer(tv_show)} elimination match"
        logging.warning("X man elimation match")
    if (
        main_event_roll > elimination_match
        and main_event_roll < title_defense
        or main_event_roll == number_1_contender_match
    ):
        main_event = f"{combatent_picker()} #1 contender match for the {title(tv_show)}"
        logging.warning("#1 contender match")

    if main_event_roll > number_1_contender_match and main_event_roll <= title_defense:
        main_event = f"{combatent_picker()} {title(tv_show)}"
        logging.warning("Title match")
    return main_event


def matches(tv_show, circuit, eligible_participants, match_total):
    print("*" * 88)
    print(match_total)
    _twenty_four_seven_match = 15
    vanilla_singles = 50
    multi_man_tag = 73
    tag_match = 99
    handicap = 100
    if tv_show == "ROH":
        vanilla_singles = 33
        multi_man_tag = 66
        tag_match = 100
        handicap = 101
    if tv_show == "IMPACT":
        teams = 11
    else:
        teams = 24
    if tv_show == "ROH":
        teams = 13
    for match in [*range(0, match_total)]:
        match_picker = roll()
        logging.warning(f"Match Roll for index {match} is {match_picker}")
        if match < match_total and "CMLL" not in tv_show:
            if match_picker < _twenty_four_seven_match and circuit["name"] == "WWE":
                combatents = combatent_picker()
                people = combatents[0]
                roster_mutation = roster_selector(
                    tv_show=tv_show,
                    people=people,
                    champion="24/7",
                    roster=eligible_participants,
                )
                twenty_four_seven_match(roster_mutation, match, combatents)
            elif match_picker < _twenty_four_seven_match and circuit["name"] != "WWE":
                roster_mutation = roster_selector(
                    tv_show=tv_show,
                    roster=eligible_participants,
                    people=2,
                    gender="Male",
                )
                singles_match(roster_mutation, match)
                logging.warning("Singles Match non gendered")
            if (
                match_picker > _twenty_four_seven_match
                and match_picker <= vanilla_singles
            ):
                gender = gender_picker(show=tv_show)
                roster_mutation = roster_selector(
                    tv_show=tv_show,
                    roster=eligible_participants,
                    people=2,
                    gender=gender,
                )
                singles_match(roster_mutation, match)
                logging.warning(f"Singles Match gendered")
            if match_picker > vanilla_singles and match_picker <= multi_man_tag:
                x_man_match = team_sizer(tv_show)
                roster_mutation = roster_selector(
                    tv_show=tv_show,
                    roster=eligible_participants,
                    people=x_man_match["team_size"],
                    gender=gender_picker(show=tv_show),
                    _stables=True,
                    team1=x_man_match["team1"],
                    team2=x_man_match["team2"],
                )
                multi_persons_match(x_man_match, match, roster_mutation)
                logging.warning("X man/woman Tag Match")
            if (
                match_picker > multi_man_tag
                and match_picker < handicap
                or match_picker == tag_match
            ):
                print(f"Match {match} will be a {tag_match_maker(teams, tv_show)}")
                logging.warning("Tag Match")
            if match_picker == handicap:
                handicap_1 = roll(1, 6)
                handicap_2 = roll(2, 6)
                if handicap_1 == handicap_2:
                    handicap_2 = roll(2, 6)
                print(
                    f"Match {match} will be a {handicap_1} on {handicap_2} handicap match"
                )
                logging.warning(f"{handicap_1} on {handicap_2} Handicap match")

        if match < match_total and "CMLL" in tv_show:
            trio = 70
            tag = 85
            singles_lightning = 100
            if match_picker <= trio:
                x_man_match = team_sizer(tv_show, trio=True)
                roster_mutation = roster_selector(
                    tv_show=tv_show,
                    roster=eligible_participants,
                    people=x_man_match["team_size"],
                    gender=gender,
                    _stables=True,
                    team1=x_man_match["team1"],
                    team2=x_man_match["team2"],
                )
                multi_persons_match(x_man_match, match, roster_mutation)

                logging.warning("Trios Match")
            if match_picker > trio and match_picker <= tag:
                print(f"Match {match} will be a 2/3 {tag_match_maker(teams, tv_show)}")
                logging.warning("2/3 tag match")
            if match_picker > tag and match_picker <= singles_lightning:
                print(f"Match {match} will be a one fall lightning singles match!")
                roster_mutation = roster_selector(
                    tv_show=tv_show,
                    roster=eligible_participants,
                    people=2,
                    gender="Male",
                )
                singles_match(roster_mutation, match)
                logging.warning("cmll lightning single fall match")
    print(f"The Main Event will be a {main_event(tv_show)}")


def roster_selector(
    tv_show,
    people,
    roster,
    champion=None,
    gender=None,
    _stables=False,
    team1=[],
    team2=[],
):
    """Iterates through a given list of eligible ids and attempts to make matches that make sense"""

    eligible_wrestlers = roster_mapper(roster, tv_show=tv_show)
    contestants = []
    if champion == "24/7":
        for grapplers in [*range(0, people)]:
            contestant = random.choice(roster)
            roster.remove(contestant)
            contestants.append(contestant)
            roster_mutation = {
                "contestants": contestants,
                "eligible_participants": roster,
            }

            return roster_mutation
    if _stables == False:
        for person in [*range(1, people)]:
            import pdb

            pdb.set_trace()
            opponents = opponent_dict(eligible_wrestlers, gender)
            if len(opponents) < 5:
                persona = persona_finder(opponents, person)
                opponents.pop(wrestlers.get_by_id(person)[persona])
            contestant = random.choice(eligible_wrestlers[gender])
            contestants.append(contestant)
            roster.remove(contestant)
            eligible_wrestlers = roster_mapper(roster, tv_show)
    if _stables == True:
        people_on_each_side = people / 2
        stable1 = stable_member_mapper(roster, team1)
        stable2 = stable_member_mapper(roster, team2)
        if len(stable1) > people_on_each_side:
            team_a = random.choices(stable1, k=people_on_each_side)
            for member in team_a:
                roster.remove(member)
        elif len(stable1) < people_on_each_side:
            team_a = stable1
            for member in team_a:
                roster.remove(member)
            spots_left = people_on_each_side - len(team_a)
            fillers = random.choices(roster, k=spots_left)
            for member in fillers:
                team_a.append(member)
                roster.remove(member)
        else:
            team_a = stable1
        if len(stable2) > people_on_each_side:
            team_b = random.choices(stable2, k=people_on_each_side)
            for member in team_b:
                roster.remove(member)
        elif len(stable2) < people_on_each_side:
            team_b = stable2
            for member in team_b:
                roster.remove(member)
            spots_left = people_on_each_side - len(team_b)
            fillers = random.choices(roster, k=spots_left)
            for member in fillers:
                team_b.append(member)
                roster.remove(member)
        else:
            team_b = stable2
        return {
            "contestants": {"team_a": team_a, "team_b": team_b},
            "eligible_participants": roster,
        }

    roster_mutation = {"contestants": contestants, "eligible_participants": roster}

    return roster_mutation


def match_string(roster_mutation):
    participants_string = ""
    if isinstance(roster_mutation["contestants"], list):
        participants = wrestlers.get_by_id(roster_mutation["contestants"])
        for participant in participants:
            participants_string += f"{participant['name']} "
    if isinstance(roster_mutation["contestants"], dict):
        team_1_string = ""
        for member in roster_mutation["contestants"]["team_a"]:
            team_1_string += f'{wrestlers.get_by_id(member)["name"]} '
        team_2_string = ""
        for member in roster_mutation["contestants"]["team_b"]:
            team_2_string += f'{wrestlers.get_by_id(member)["name"]} '
        participants_string = f"{team_1_string} vs {team_2_string}"
    return participants_string


def twenty_four_seven_match(roster_mutation, match, combatents):
    participants_string = match_string(roster_mutation)
    print(f"Match {match} will be a {combatents[1]} 24/7 Title Defense")
    print(f"- Match Participants are: {participants_string}")
    logging.warning("24/7 match")


def singles_match(roster_mutation, match):
    participants_string = match_string(roster_mutation)
    print(f"Match {match} will be a male one on one singles match")
    print(f"- Match Participants are: {participants_string}")


def multi_persons_match(x_man_match, match, roster_mutation):
    participants_string = match_string(roster_mutation)
    team_1_name = stables.get_by_id(x_man_match["team1"])["name"]
    team_2_name = stables.get_by_id(x_man_match["team2"])["name"]
    print(f"Match {match} will be a {x_man_match['team_size']} tag match")
    print(f"{team_1_name} vs {team_2_name}")
    print(f"- Match Participants are: {participants_string}")


def persona_finder(opponents, person):
    for persona in opponents:
        for id in opponents:
            if id == person:
                return persona


def roster_mapper(roster, tv_show):
    heels = [
        heel
        for heel in roster
        if wrestlers.get_by_id(heel)["id"] in circuits.get_by_name(tv_show)["heels"]
    ]
    faces = [
        face
        for face in roster
        if wrestlers.get_by_id(face)["id"] in circuits.get_by_name(tv_show)["faces"]
    ]
    tweeners = [
        tweener
        for tweener in roster
        if wrestlers.get_by_id(tweener)["id"]
        in circuits.get_by_name(tv_show)["tweeners"]
    ]
    jobbers = [
        jobber
        for jobber in roster
        if wrestlers.get_by_id(jobber)["id"] in circuits.get_by_name(tv_show)["jobbers"]
    ]
    anti_heroes = [
        anti_heroe
        for anti_heroe in roster
        if wrestlers.get_by_id(anti_heroe)["id"]
        in circuits.get_by_name(tv_show)["anti_heroes"]
    ]

    males = [
        girl
        for girl in roster
        if wrestlers.get_by_id(girl)["gender"] == "male" and girl in roster
    ]
    females = [
        girl
        for girl in roster
        if wrestlers.get_by_id(girl)["gender"] == "female" and girl in roster
    ]
    eligible_wrestlers = {
        "male": males,
        "female": females,
        "heels": heels,
        "faces": faces,
        "tweeners": tweeners,
        "jobbers": jobbers,
        "anti_heroes": anti_heroes,
    }
    return eligible_wrestlers


def gendered_persona(eligible_wrestlers, persona, gender):
    return list(set(eligible_wrestlers[persona]) & set(eligible_wrestlers[gender]))


def opponent_dict(eligible_wrestlers, gender):
    {
        "heels": gendered_persona(eligible_wrestlers, "heels", gender),
        "faces": gendered_persona(eligible_wrestlers, "faces", gender),
        "tweeners": gendered_persona(eligible_wrestlers, "tweeners", gender),
        "jobbers": gendered_persona(eligible_wrestlers, "jobbers", gender),
        "anti_heroes": gendered_persona(eligible_wrestlers, "anti_heroes", gender),
    }


def stable_member_mapper(roster, stable_id):
    stable = stables.get_by_id(stable_id)

    employees = []
    for member in stable["members"]:
        for wrestler in roster:
            if member == wrestler:
                employees.append(member)
    return employees
