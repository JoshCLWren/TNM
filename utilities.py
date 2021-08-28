import random
import logging
import circuits


def combatent_picker(one_on_one_seed=10, triangle_seed=60, four_way_seed=100):
    picker = roll()
    logging.warning("Combatent Picker")
    combatents = ""
    if picker < one_on_one_seed:
        combatents = [2, "One on One"]
    elif picker > one_on_one_seed and picker < triangle_seed:
        combatents = [3, "Triangle Match"]
    else:
        combatents = [4, "Fatal Four Way"]
    logging.warning(combatents)
    return combatents


def gender_picker(male=70, female=99, intergender=100, show="205"):
    if show in ["205", "cmll"]:
        return "male"
    gender_roll = roll()
    logging.warning("Gender Picker is below")
    if gender_roll > male and gender_roll < intergender:
        gender = "female"
    elif gender_roll < female:
        gender = "male"
    else:
        gender = "intergender"
    logging.warning(gender)
    return gender


def roll(start=1, end=101):
    the_roll = random.randrange(start, end)
    logging.warning(f"{the_roll} was rolled with {start} and {end} indexes")
    return the_roll


def tag_match_maker(teams=24, show="205"):

    logging.warning("Tag Match Maker")
    genders = gender_picker(show=show)
    team_1 = roll(1, teams)
    team_2 = roll(1, teams)
    if team_1 == team_2:
        team_2 = team_2 + 1
        team_2 = team_1 - 1
    if show == "205":
        genders = "male"
        return f"male tag-team contest between {team_1} and team {team_2}."
    if genders == "intergender":
        tag = "n unprecedented intergender tag-team contest"
    if genders == "female":
        tag = "female tag-team contest"
    if genders == "male":
        tag = f"male tag-team contest between team {team_1} and team {team_2}."
    return tag


def team_sizer(
    tv_show,
    three=500,
    four=994,
    five=995,
    six=996,
    seven=997,
    eight=998,
    nine=999,
    ten=1000,
    trio=False,
):
    logging.warning("Team Sizer")
    team_sizer_roll = roll()
    genders = gender_picker(show=tv_show)
    if tv_show in ["205", "ROH"]:
        genders = "male"
    circuit = circuits.get_by_name(tv_show)
    if len(circuit["stables"]) > 2:
        teams = random.sample(circuit["stables"], 2)
        team1, team2 = teams
        # do we need to remove stables anymore?
        # circuit["stables"].remove(team1)
        # circuit["stables"].remove(team2)

    else:
        team1 = circuit["stables"][0]
        team2 = []
    if trio == True:
        return {"team_size": 6, "team1": team1, "team2": team2}
    if genders == "male" or genders == "intergender" and trio == False:
        if team_sizer_roll < three:
            team_size = 6
        elif team_sizer_roll > three and team_sizer_roll < five:
            team_size = 8
        elif team_sizer_roll > four and team_sizer_roll < six:
            team_size = 10
        elif team_sizer_roll > five and team_sizer_roll < seven:
            team_size = 12
        elif team_sizer_roll > six and team_sizer_roll < eight:
            team_size = 14
        elif team_sizer_roll > seven and team_sizer_roll < nine:
            team_size = 16
        elif team_sizer_roll > eight and team_sizer_roll < ten:
            team_size = 18
        else:
            team_size = 20

        return {"team_size": team_size, "team1": team1, "team2": team2}

    else:
        # I don't think there are enough women in each circuit to warrent more than 5 v 5
        if team_sizer_roll < three:
            team_size = 6
        elif team_sizer_roll > three and team_sizer_roll < five:
            team_size = 8
        else:
            team_size = 10
    logging.warning(f"Team size = {team_size}")
    return {"team_size": team_size, "team1": team1, "team2": team2}


def title(tv_show="Raw"):
    titles = ["Championship"]
    if tv_show == "Raw":
        titles = [
            "World Championship",
            "Raw Women's Championship",
            "US Championship",
            "Raw Tag Championship",
        ]
    if tv_show == "Smackdown":
        titles = [
            "Universal Championship",
            "Smackdown Women's Championship",
            "Intercontinental Championship",
            "Women's Tag Championship",
            "Smackdown Tag Championship",
        ]
    if tv_show == "205":
        titles = ["Cruiserweight Championship"]
    if tv_show == "IMPACT":
        titles = [
            "IMPACT World Championship",
            "IMPACT X Division Championship",
            "IMPACT World Tag Team Championship",
            "IMPACT Knockout Championship",
        ]
    if tv_show == "CMLL":
        titles = (["CMLL World Tag Team Championship"],)
    if tv_show == "ROH":
        titles = [
            "ROH World Championship",
            "ROH World Tag Team Championship",
            "ROH World Tag Team Championship",
            "ROH Six-Man Tag Team Championship",
            "Women of Honor World Championship",
        ]
    random_title = random.choice(titles)
    logging.warning(f"Title is {random_title}")
    return random_title


def check_dupes(list, item):
    if item not in list:
        list.append(item)
    else:
        return list
    return list


def prepare_columns(table, **kwargs):
    field_string = ""

    for field in kwargs:
        field_string += f"{field} = %({field})s, "

    field_string = field_string[: len(field_string) - 2]

    sql = f"""UPDATE {table}
            SET {field_string} WHERE id = %(id)s
            RETURNING *;"""
    return sql
