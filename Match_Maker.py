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
import Shows


def main_event(show):
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
        main_event = f"{team_sizer(show)} elimination match"
        logging.warning("X man elimation match")
    if (
        main_event_roll > elimination_match
        and main_event_roll < title_defense
        or main_event_roll == number_1_contender_match
    ):
        main_event = f"{combatent_picker()} #1 contender match for the {title(show)}"
        logging.warning("#1 contender match")

    if main_event_roll > number_1_contender_match and main_event_roll <= title_defense:
        main_event = f"{combatent_picker()} {title(show)}"
        logging.warning("Title match")
    return main_event


def twenty_four_seven(show, match):
    combatents = combatent_picker()
    people = combatents[0]
    roster_mutation = roster_selector(
        show=show,
        people=people,
        champion="24/7",
    )
    twenty_four_seven_match(roster_mutation, match, combatents)


def singles(show, match):
    roster_mutation = roster_selector(
        show=show,
        people=2,
        gender="Male",
    )
    singles_match(roster_mutation, match)
    logging.warning("Singles Match non gendered")


def big_tag(show, match):
    x_man_match = team_sizer(show["name"])
    roster_mutation = roster_selector(
        show=show,
        people=x_man_match["team_size"],
        gender=gender_picker(show=show["name"]),
        _stables=True,
        team1=x_man_match["team1"],
        team2=x_man_match["team2"],
    )
    multi_persons_match(x_man_match, match, roster_mutation, show)
    logging.warning("X man/woman Tag Match")


def match_switch(match_picker_roll, match_switcher):
    """returns the corresponding tnm value with a real text equivilant"""
    for value in match_switcher:
        if match_picker_roll > match_switcher[value]:
            pass
        elif match_picker_roll < match_switcher[value]:
            return value
        else:
            return "handicap"


def tag(match, show):
    print(f"Match {match} will be a {tag_match_maker(show=show['name'])}")


def handicap(match):
    handicap_1 = roll(1, 6)
    handicap_2 = roll(2, 6)
    if handicap_1 == handicap_2:
        handicap_2 = roll(2, 6)
    print(f"Match {match} will be a {handicap_1} on {handicap_2} handicap match")
    logging.warning(f"{handicap_1} on {handicap_2} Handicap match")


def matches(show, roll_override=None):
    match_switcher = {
        "_twenty_four_seven_match": 15,
        "vanilla_singles": 50,
        "multi_man_tag": 73,
        "tag_match": 90,
        "handicap": 100,
    }
    if show["name"] == "ROH":
        match_switcher = {"vanilla_singles": 33, "multi_man_tag": 66, "tag_match": 100}

    for match in [*range(show["matches"])]:
        match_picker = roll()
        if roll_override is not None:
            match_picker = roll_override
        if match < show["matches"] and "CMLL" in show["name"]:
            lucha(match_picker, show, gender="male", match=match)
        match_type = match_switch(match_picker, match_switcher)
        if match_type == "_twenty_four_seven_match":
            twenty_four_seven(show, match)
        elif match_type == "vanilla_singles":
            singles(show, match)
        elif match_type == "multi_man_tag":
            big_tag(show, match)
        elif match_type == "tag":
            tag(show, match)
        elif match_type == "handicap":
            handicap(match)
        else:
            singles(show, match)

    # don't think this is working
    Shows.patch_show_card(show["card"], show["id"])
    print(f"The Main Event will be a {main_event(show)}")


def lucha(match_picker, show, gender, match):
    trio = 70
    tag = 85
    singles_lightning = 100
    if match_picker <= trio:
        x_man_match = team_sizer(show["name"], trio=True)
        roster_mutation = roster_selector(
            show=show,
            people=x_man_match["team_size"],
            gender=gender,
            _stables=True,
            team1=x_man_match["team1"],
            team2=x_man_match["team2"],
        )
        multi_persons_match(x_man_match, match, roster_mutation)

        logging.warning("Trios Match")
    if match_picker > trio and match_picker <= tag:
        print(f"Match {match} will be a 2/3 {tag_match_maker(show=show)}")
        logging.warning("2/3 tag match")
    if match_picker > tag and match_picker <= singles_lightning:
        print(f"Match {match} will be a one fall lightning singles match!")
        roster_mutation = roster_selector(
            show=show,
            people=2,
            gender="Male",
        )
        singles_match(roster_mutation, match)
        logging.warning("cmll lightning single fall match")


def roster_selector_247(people, show, gender, roster):
    for _ in [*range(people)]:
        contestants = contestant_tracker(show, gender, contestants)
    Shows.patch_show_roster(roster, show["id"])
    return contestants


def roster_selector_stables(people, show, team1, roster, team2):
    people_on_each_side = people / 2
    people_on_each_side = int(people_on_each_side)
    stable1 = stable_member_mapper(show, team1)

    if stable1 is None:
        team_a = []
        spots_left = people_on_each_side - len(team_a)
        fillers = random.choices(roster, k=spots_left)
        for member in fillers:
            team_a.append(member)
            roster.remove(member)
    stable2 = stable_member_mapper(show, team2)
    if stable2 is None:
        team_b = []
        spots_left = people_on_each_side - len(team_a)
        fillers = random.sample(roster, k=spots_left)
        for member in fillers:
            team_a.append(member)
            roster.remove(member)

    if len(stable1) > people_on_each_side:
        team_a = random.sample(stable1, k=people_on_each_side)
        for member in team_a:
            roster.remove(member)
    elif len(stable1) < people_on_each_side:
        team_a = stable1
        for member in team_a:
            roster.remove(member)
        spots_left = people_on_each_side - len(team_a)
        try:
            fillers = random.choices(roster["male"], k=int(spots_left))
        except KeyError:
            pass
        for member in fillers:
            team_a.append(member)
            try:
                roster["male"].remove(member)
            except ValueError:
                pass
        print(team_a)
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
        fillers = random.choices(roster, k=int(spots_left))
        for member in fillers:
            team_b.append(member)
            roster.remove(member)
    else:
        team_b = stable2
    return {
        "contestants": {"team_a": team_a, "team_b": team_b},
        "eligible_participants": roster,
    }


def roster_selector(
    show,
    people,
    champion=None,
    gender=None,
    _stables=False,
    team1=[],
    team2=[],
):
    """Iterates through a given list of eligible ids and attempts to make matches that make sense"""

    roster = show["eligible_wrestlers"]
    contestants = []
    if champion == "24/7":
        contestants = roster_selector_247(people, show, gender, roster)
    if _stables == False:
        # singles one on one scenario likey or other similiar non tag match
        contestants = contestant_tracker(show, gender, contestants)
        for _ in [*range(1, people)]:
            # check the persona of contestant[0] and find matches that don't have the same persona
            contestant_one_persona = persona_finder(show, contestants[0])

            # check how many people are left to fight of the same gender

            flat_list = gender_divide(show, gender)

            opponents_left = len(flat_list)
            # if it's less than five don't worry about personas and fill up the match
            if opponents_left < 5:
                while len(contestants) != people:
                    contestants = contestant_tracker(show, gender, contestants)

            while len(contestants) != people:
                contestants = find_opponent(contestants, gender, show)
    if _stables == True:
        return roster_selector_stables(people, show, team1, roster, team2)

    return {"contestants": contestants, "eligible_participants": roster}


def match_string(roster_mutation):
    participants_string = ""
    if isinstance(roster_mutation["contestants"], list):
        participants = wrestlers.get_by_id(roster_mutation["contestants"])
        for participant in participants:
            participants_string += f"{participant['name']} "
    if isinstance(roster_mutation["contestants"], dict):
        team_1_string = "".join(
            f'{wrestlers.get_by_id(member)["name"]} '
            for member in roster_mutation["contestants"]["team_a"]
        )

        team_2_string = "".join(
            f'{wrestlers.get_by_id(member)["name"]} '
            for member in roster_mutation["contestants"]["team_b"]
        )

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


def multi_persons_match(x_man_match, match, roster_mutation, show):
    participants_string = match_string(roster_mutation)
    try:
        team_1_name = stables.get_by_id(x_man_match["team1"])["name"]
    except TypeError:
        team_1_name = ""
    try:
        team_2_name = stables.get_by_id(x_man_match["team2"])["name"]
    except TypeError:
        team_2_name = ""
    line_one = f"Match {match} will be a {x_man_match['team_size']} tag match"
    line_two = f"{team_1_name} vs {team_2_name}"
    line_three = f"- Match Participants are: {participants_string}"
    print(line_one)
    print(line_two)
    print(line_three)

    show["card"].append(f"{line_one}, {line_two}, {line_three}")

    return participants_string


def persona_finder(show, contestant):
    for column in show:
        if isinstance(column, list):
            for id in column:
                if id == contestant:

                    return


def roster_mapper(roster, show):

    heels = [
        heel
        for heel in roster["heels"]
        if heel in circuits.get_by_name(show["name"])["heels"]
    ]
    faces = [
        face
        for face in roster["faces"]
        if face in circuits.get_by_name(show["name"])["faces"]
    ]
    tweeners = [
        tweener
        for tweener in roster["tweeners"]
        if tweener in circuits.get_by_name(show["name"])["tweeners"]
    ]
    jobbers = [
        jobber
        for jobber in roster["jobbers"]
        if jobber in circuits.get_by_name(show["name"])["jobbers"]
    ]
    anti_heroes = [
        anti_heroe
        for anti_heroe in roster["anti_heroes"]
        if anti_heroe in circuits.get_by_name(show["name"])["anti_heroes"]
    ]
    try:
        males = [
            boy
            for boy in roster["male"]
            if wrestlers.get_by_id(boy)["gender"] == "male" and boy in roster
        ]
    except KeyError:
        males = []
    try:
        females = [
            girl
            for girl in roster["female"]
            if wrestlers.get_by_id(girl)["gender"] == "female" and girl in roster
        ]
    except KeyError:
        females = []
    return {
        "male": males,
        "female": females,
        "heels": heels,
        "faces": faces,
        "tweeners": tweeners,
        "jobbers": jobbers,
        "anti_heroes": anti_heroes,
    }


def gendered_persona(eligible_wrestlers, persona, gender):
    return list(set(eligible_wrestlers[persona]) & set(eligible_wrestlers[gender]))


# def opponent_dict(show, gender):
#     return {
#         "heels": gendered_persona(eligible_wrestlers, "heels", gender),
#         "faces": gendered_persona(eligible_wrestlers, "faces", gender),
#         "tweeners": gendered_persona(eligible_wrestlers, "tweeners", gender),
#         "jobbers": gendered_persona(eligible_wrestlers, "jobbers", gender),
#         "anti_heroes": gendered_persona(eligible_wrestlers, "anti_heroes", gender),
#     }


def stable_member_mapper(show, stable_id):

    employees = []

    stable = stables.get_by_id(stable_id)

    if stable is None:
        employees = show["eligible_wrestlers"]
    try:
        for member in stable["members"]:
            for wrestler in show["eligible_wrestlers"]:
                if member == wrestler:
                    employees.append(member)
    except TypeError:
        return []

    return employees


def contestant_tracker(show, gender, contestants=[]):
    """Adds a contestant at random to the contestants array and then removes them from the eligible roster"""
    flat_list = gender_divide(show, gender)
    contestant = random.choice(flat_list)
    contestants.append(contestant)
    show["eligible_wrestlers"].remove(contestant)
    return contestants


def gender_divide(show, gender):
    """takes a show and removes all non lists and then returns a flattened list of the gender passed left."""
    flat_list = []

    show.pop("name", None)
    show.pop("id", None)
    show.pop("matches", None)
    if gender == "Female":
        pool = [
            value for key, value in show.items() if "female" in key.lower()
        ]  # searches all keys for gender
        flat_list = [item for sublist in pool for item in sublist]  # flattens the list
    elif gender == "Male":
        pool = [
            value for key, value in show.items() if "female" not in key.lower()
        ]  # can't query if for 'male' here since it's a part of the word female

        flat_list = [item for sublist in pool for item in sublist]

    else:
        pool = [value for key, value in show.items() if "ready" in key.lower()]
        flat_list = [item for sublist in pool for item in sublist]
    return flat_list


def persona_switch(persona_filter, gender, show):
    """returns the personas a wrestler is not"""
    # iterate throuch the show lists by gender
    switcher = {"heels": ["faces", "tweners", "jobbers", "anti_heroes"]}
    # return the switcher.get(persona_filter)
    show.pop("name", None)
    show.pop("id", None)
    show.pop("matches", None)


def find_opponent(contestant, gender, show):
    """takes the persona passed and finds all wreslters left with no matching persona"""


def personality_switch(argument):
    """returns the corresponding tnm value with a real text equivilant"""
    switcher = {0: "face", 1: "heel", 2: "tweener", 3: "jobber", 5: "anti-hero"}

    return switcher.get(argument, "nothing")
