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
import tag_teams


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
    twenty_four_seven_match(roster_mutation, match, combatents, show)


def singles(show, match):
    roster_mutation = roster_selector(
        show=show,
        people=2,
        gender="Male",
    )
    singles_match(roster_mutation, match, show)
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
    roster_mutation = roster_selector(
        show=show,
        people=4,
        gender=gender_picker(show=show["name"]),
        _stables=False,
        _tags=True,
    )
    participants_string = match_string(roster_mutation)
    line1 = f"- Match Participants are: {participants_string}"
    line2 = f"Match {match} will be a {tag_match_maker(show=show['name'])}"
    show["card"].append(f"{line1}, {line2}")


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
    if show["name"] == "roh":
        match_switcher = {"vanilla_singles": 33, "multi_man_tag": 66, "tag_match": 100}
    if show["name"] == "cmll":
        match_switcher = {"trio": 70, "tag": 85, "singles": 100}

    for match in [*range(show["matches"])]:
        match_picker = roll()
        if roll_override is not None:
            match_picker = roll_override
        match_type = match_switch(match_picker, match_switcher)
        if match_type == "_twenty_four_seven_match":
            twenty_four_seven(show, match)
        elif match_type == "trio":
            big_tag(show, match)
        elif match_type == "vanilla_singles":
            singles(show, match)
        elif match_type == "multi_man_tag":
            big_tag(show, match)
        elif match_type == "tag_match":
            tag(match, show)
        elif match_type == "handicap":
            handicap(match)
        else:
            singles(show, match)

    Shows.patch_show_card(show["card"], show["id"])
    print(f"The Main Event will be a {main_event(show)}")


def roster_selector_247(people, show, gender, roster, contestants):
    for _ in [*range(people)]:
        contestants = contestant_tracker(show, gender, contestants)
    Shows.patch_show_roster(roster, show["id"])
    return contestants


def roster_selector_tags(show, roster):
    circuit = circuits.get_by_name(show["name"])
    team1, team2 = random.sample(circuit["tag_teams"], 2)

    circuit["tag_teams"].remove(team1)
    circuit["tag_teams"].remove(team2)
    circuits.patch_circuit(circuit["id"], "tag_teams", circuit["tag_teams"])
    wrestlers_in_tags = []

    teams = [team1, team2]
    for team in teams:
        tag = tag_teams.get_by_id(team)
        wrestlers_in_tags += tag["tag_team_members"]
    # show["busy_wrestlers"] = list(set(show["busy_wrestlers"] + wrestlers_in_tags))
    for person in wrestlers_in_tags:
        roster.remove(person)

    return {
        "contestants": {
            "team_a": tag_teams.get_by_id(team1)["tag_team_members"],
            "team_b": tag_teams.get_by_id(team2)["tag_team_members"],
        },
        "eligible_participants": roster,
    }


def roster_selector_stables(people, show, team1, roster, team2):
    people_on_each_side = people / 2
    people_on_each_side = int(people_on_each_side)
    stable1 = stable_member_mapper(show, team1)

    if stable1 is None:
        team_a = []
        spots_left = people_on_each_side - len(team_a)
        fillers = random.sample(roster, k=spots_left)
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
            fillers = random.sample(roster["male"], k=int(spots_left))
        except KeyError:
            pass
        for member in fillers:
            team_a.append(member)
            try:
                roster["male"].remove(member)
            except ValueError:
                pass
    else:
        team_a = stable1
    if len(stable2) > people_on_each_side:
        team_b = random.sample(stable2, k=people_on_each_side)
        for member in team_b:
            roster.remove(member)
    elif len(stable2) < people_on_each_side:
        team_b = stable2
        for member in team_b:
            roster.remove(member)
        spots_left = people_on_each_side - len(team_b)
        fillers = random.sample(roster, k=int(spots_left))
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
    _tags=False,
    team1=[],
    team2=[],
):
    """Iterates through a given list of eligible ids and attempts to make matches that make sense"""

    roster = show["eligible_wrestlers"]
    contestants = []
    if _tags == True:
        return roster_selector_tags(show, roster)
    if champion == "24/7":
        contestants = roster_selector_247(people, show, gender, roster, contestants)
        return {
            "contestants": contestants,
            "eligible_participants": show["eligible_wrestlers"],
        }
    if _stables == False:

        # singles one on one scenario likey or other similiar non tag match
        contestants = contestant_tracker(show, gender, contestants)
        for _ in [*range(1, people)]:
            # check the persona of contestant[0]
            contestant_one_persona = persona_finder(show, contestants[0])

            # check how many people are left to fight of the same gender

            matching_gender = show["males"] if gender == "Male" else show["females"]
            flat_list = list(set(matching_gender) & set(show["eligible_wrestlers"]))

            opponents_left = len(flat_list)
            # if it's less than five don't worry about personas and fill up the match
            if opponents_left < 5:
                while len(contestants) != people:
                    contestants = contestant_tracker(show, gender, contestants)
            else:
                # fill the match up with non matching personas
                personas = {"faces", "heels", "jobbers", "tweeners", "anti_heroes"}
                personas.remove(contestant_one_persona)
                opponent_pool = []
                for personality in personas:
                    opponent_pool += gendered_persona(flat_list, show, personality)
                contestant = random.choice(opponent_pool)
                contestants.append(contestant)
                show["eligible_wrestlers"].remove(contestant)
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


def twenty_four_seven_match(roster_mutation, match, combatents, show):
    participants_string = match_string(roster_mutation)
    line1 = f"Match {match} will be a {combatents[1]} 24/7 Title Defense"
    line2 = f"- Match Participants are: {participants_string}"
    print(line1)
    print(line2)
    show["card"].append(f"{line1}, {line2}")
    return participants_string


def singles_match(roster_mutation, match, show):
    participants_string = match_string(roster_mutation)
    line1 = f"Match {match} will be a male one on one singles match"
    line2 = f"- Match Participants are: {participants_string}"
    print(line1)
    print(line2)
    show["card"].append(f"{line1}, {line2}")


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
        if isinstance(show[column], list):
            for id in show[column]:
                if id == contestant:
                    return column


def gendered_persona(flat_list, show, persona):

    return list(set(flat_list) & set(show[persona]))


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


def contestant_tracker(show, gender="Male", contestants=[]):
    """Adds a contestant at random to the contestants array and then removes them from the eligible roster"""
    gender_pool = show["males"] if gender == "Male" else show["females"]
    flat_list = [
        wrestler for wrestler in show["eligible_wrestlers"] if wrestler in gender_pool
    ]

    contestant = random.choice(flat_list)

    contestants.append(contestant)
    show["eligible_wrestlers"].remove(contestant)

    return contestants
