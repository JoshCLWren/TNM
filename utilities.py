import random
import logging


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
    gender_roll = roll()
    logging.warning("Gender Picker is below")
    if gender_roll > male and gender_roll < intergender:
        gender = "female"
    elif gender_roll < female:
        gender = "male"
    else:
        gender = "intergender"
    if show == "205":
        gender = "male"
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
):
    logging.warning("Team Sizer")
    team_sizer_roll = roll()
    genders = gender_picker(show=tv_show)
    if tv_show == "205" or tv_show == "ROH":
        genders = "male"
    if tv_show == "ROH":
        stables = 4
        stables_list = []
        for stable in range(1, stables):
            stables_list.append(stable)
        stable_1 = random.choice(stables_list)
        stables_list.remove(stable_1)
        stable_2 = random.choice(stables_list)
        stables_list.remove(stable_2)
        teams = f"team {stable_1} and team {stable_2}"
        logging.warning(f"team {stable_1} and team {stable_2}")
    if genders == "male" or genders == "intergender":
        if team_sizer_roll < three:
            team_size = "6-Man"
        elif team_sizer_roll > three and team_sizer_roll < five:
            team_size = "8-Man"
        elif team_sizer_roll > four and team_sizer_roll < six:
            team_size = "10-man"
        elif team_sizer_roll > five and team_sizer_roll < seven:
            team_size = "12-man"
        elif team_sizer_roll > six and team_sizer_roll < eight:
            team_size = "14-man"
        elif team_sizer_roll > seven and team_sizer_roll < nine:
            team_size = "16-man"
        elif team_sizer_roll > eight and team_sizer_roll < ten:
            team_size = "18-man"
        else:
            team_size = "20-man"
        if tv_show == "ROH":
            team_size = f"6-Man between {teams}"
            return team_size

    else:
        # I don't think there are enough women in each circuit to warrent more than 5 v 5
        if team_sizer_roll < three:
            team_size = "6-Woman"
        elif team_sizer_roll > three and team_sizer_roll < five:
            team_size = "8-Woman"
        else:
            team_size = "10-Woman"
    logging.warning(f"Team size = {team_size}")
    return team_size


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
