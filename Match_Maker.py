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


def matches(tv_show, match_total, roster):
    twenty_four_seven_match = 15
    vanilla_singles = 50
    multi_man_tag = 73
    tag_match = 99
    handicap = 100
    if tv_show == "ROH":
        vanilla_singles = 33
        multi_man_tag = 66
        tag_match = 100
        handicap = 101

    wwe_shows = ["Raw", "Smackdown"]
    if tv_show == "IMPACT":
        teams = 11
    else:
        teams = 24
    if tv_show == "ROH":
        teams = 13
    for match in range(1, match_total):
        match_picker = roll()
        logging.warning(f"Match Roll for index {match} is {match_picker}")
        if match < match_total and "CMLL" not in tv_show:
            if match_picker < twenty_four_seven_match and tv_show in wwe_shows:
                print(
                    f"Match {match} will be a {combatent_picker()} 24/7 Title Defense"
                )
                logging.warning("24/7 match")
            elif match_picker < twenty_four_seven_match and tv_show not in wwe_shows:
                print(f"Match {match} will be a male one on one singles match")
                logging.warning("Singles Match non gendered")
            if (
                match_picker > twenty_four_seven_match
                and match_picker <= vanilla_singles
            ):
                print(
                    f"Match {match} will be a {gender_picker(show=tv_show)} singles match"
                )
                logging.warning(f"Singles Match gendered")
            if match_picker > vanilla_singles and match_picker <= multi_man_tag:
                print(f"Match {match} will be a {team_sizer(tv_show)} tag match")
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
            teams = 13
            trio = 70
            tag = 85
            singles_lightning = 100
            if match_picker <= trio:
                stables = 18
                stables_list = []
                for stable in range(1, stables):
                    stables_list.append(stable)
                stable_1 = random.choice(stables_list)
                stables_list.remove(stable_1)
                stable_2 = random.choice(stables_list)
                stables_list.remove(stable_2)
                teams = f"team {stable_1} and team {stable_2}"
                print(f"Match {match} will be a 2/3 falls trios match between {teams}")
                logging.warning("Trios Match")
            if match_picker > trio and match_picker <= tag:
                print(f"Match {match} will be a 2/3 {tag_match_maker(teams, tv_show)}")
                logging.warning("2/3 tag match")
            if match_picker > tag and match_picker <= singles_lightning:
                print(f"Match {match} will be a one fall lightning singles match!")
                logging.warning("cmll lightning single fall match")
    print(f"The Main Event will be a {main_event(tv_show)}")
