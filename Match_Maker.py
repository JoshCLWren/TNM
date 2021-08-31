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
from match_types import twenty_four_seven, big_tag, singles, tag, handicap


def main_event(show, main_event_roll_override=None):
    elimination_match = 10
    number_1_contender_match = 75
    title_defense = 99
    battle_royal = 100
    main_event_roll = roll()
    if main_event_roll_override is not None:
        main_event_roll = main_event_roll_override
    if main_event_roll == battle_royal:
        if len(show["males"]) > 20:
            participants = random.sample(show["males"], 20)
        else:
            participants = random.sample(show["males"], len(show["males"]))
        main_event = f"""{len(participants)} Man Battle Royal featuring: """
        for person in participants:
            main_event += f"{wrestlers.get_by_id(person)['name']}, "
    if main_event_roll <= elimination_match:
        main_event = f"{team_sizer(show)} elimination match"
    if (
        main_event_roll > elimination_match
        and main_event_roll < title_defense
        or main_event_roll == number_1_contender_match
    ):
        combatents = combatent_picker()
        main_event = f"{combatents[1]} #1 contender match for the {title(show)}"

    if main_event_roll > number_1_contender_match and main_event_roll <= title_defense:
        combatents = combatent_picker()
        main_event = f"{combatents[1]} {title(show)}"
    show["card"].append(main_event)
    Shows.patch_show_card(show["card"], show["id"])
    return main_event


def match_switch(match_picker_roll, match_switcher):
    """returns the corresponding tnm value with a real text equivilant"""
    for value in match_switcher:
        if match_picker_roll > match_switcher[value]:
            pass
        elif match_picker_roll < match_switcher[value]:
            return value
        else:
            return "handicap"


def matches(show, roll_override=None, main_event_roll_override=None):
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

    undercard = [*range(1, show["matches"])]

    match_sorter(undercard, roll_override, match_switcher, show)

    show = Shows.get_by_id(show["id"])
    main_event(show, main_event_roll_override)
    for match in show["card"]:
        print(match)


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
    Shows.patch_show_roster(show["eligible_wrestlers"], show["id"])
    return contestants


def match_sorter(
    undercard,
    roll_override,
    match_switcher,
    show,
):
    for match in undercard:
        show = Shows.get_by_id(show["id"])
        match_picker = roll()
        if roll_override is not None:
            match_picker = roll_override
        match_type = match_switch(match_picker, match_switcher)
        if match_type == "_twenty_four_seven_match":
            if len(show["eligible_wrestlers"]) > 4:
                twenty_four_seven(show, match)
            elif len(show["eligible_wrestlers"]) > 1:
                singles(show, match)
            else:
                continue
        elif match_type in ["trio", "multi_man_tag"]:
            if len(show["eligible_wrestlers"]) > 6:
                big_tag(show, match)
            elif len(show["eligible_wrestlers"]) > 1:
                singles(show, match)
            else:
                continue
        elif match_type == "vanilla_singles":
            if len(show["eligible_wrestlers"]) > 1:
                singles(show, match)
            else:
                continue
        elif match_type == "tag_match":
            if len(show["eligible_wrestlers"]) > 4:
                tag(match, show)
            elif len(show["eligible_wrestlers"]) > 1:
                singles(show, match)
            else:
                continue
        elif match_type == "handicap":
            if len(show["eligible_wrestlers"]) > 6:
                handicap(show, match)
            elif len(show["eligible_wrestlers"]) > 1:
                singles(show, match)
            else:
                continue
        else:
            singles(show, match)
