from utilities import (
    roll,
    combatent_picker,
    team_sizer,
    title,
    gender_picker,
    tag_match_maker,
)
import stables
import roster_selectors
import Match_Maker
import Shows
import Championships
import utilities


def twenty_four_seven(show, match):
    combatents = combatent_picker()
    people = combatents[0] - 1
    roster_mutation = roster_selectors.roster_selector(
        show=show,
        people=people,
        champion="24/7",
    )
    twenty_four_seven_match(roster_mutation, match, combatents, show)


def singles(show, match, gender="Male"):
    roster_mutation = roster_selectors.roster_selector(
        show=show,
        people=2,
        gender=gender,
    )
    singles_match(roster_mutation, match, show, gender)


def big_tag(show, match):
    x_man_match = team_sizer(show["name"])
    roster_mutation = roster_selectors.roster_selector(
        show=show,
        people=x_man_match["team_size"],
        gender=gender_picker(show=show["name"]),
        _stables=True,
        team1=x_man_match["team1"],
        team2=x_man_match["team2"],
    )
    multi_persons_match(x_man_match, match, roster_mutation, show)


def tag(match, show):
    roster_mutation = roster_selectors.roster_selector(
        show=show,
        people=4,
        gender=gender_picker(show=show["name"]),
        _stables=False,
        _tags=True,
    )
    participants_string = Match_Maker.match_string(roster_mutation)
    line1 = f"Match {match} will be a tag team match."
    line2 = f"-Match Participants are: {participants_string}"
    show["card"].append(f"{line1} {line2}")
    Shows.patch_show_card(show["card"], show["id"])


def handicap(show, match):
    handicap_1 = roll(1, 6)
    handicap_2 = roll(2, 6)
    if handicap_1 == handicap_2:
        handicap_2 = roll(2, 6)
    line1 = f"Match {match} will be a {handicap_1} on {handicap_2} handicap match"
    show["card"].append(f"{line1}")
    Shows.patch_show_card(show["card"], show["id"])


def twenty_four_seven_match(roster_mutation, match, combatents, show):

    participants_string = Match_Maker.match_string(roster_mutation)
    line1 = f"Match {match} will be a {combatents[1]} 24/7 Title Defense"
    line2 = "".join(f"{person} vs " for person in participants_string[:-1])
    line2 += f"the defending champion: {participants_string[-1]}"
    show["card"].append(f"{line1} {line2}")
    Shows.patch_show_card(show["card"], show["id"])


def singles_match(roster_mutation, match, show, gender):
    participants_string = Match_Maker.match_string(roster_mutation)
    line1 = f"Match {match} will be a {gender} one on one singles match!"
    line2 = f"{participants_string[0]} vs {participants_string[1]}"
    show["card"].append(f"{line1} {line2}")
    Shows.patch_show_card(show["card"], show["id"])


def multi_persons_match(x_man_match, match, roster_mutation, show):
    participants_string = Match_Maker.match_string(roster_mutation)
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

    show["card"].append(f"{line_one} {line_two} {line_three}")

    Shows.patch_show_card(show["card"], show["id"])
