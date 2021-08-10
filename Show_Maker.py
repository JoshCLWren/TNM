# Objects:
# Circuits.
# Circuits have brands
# Brands have shows
# Shows have matches
# Circuits also have super shows
# Shows have regular matches and main events.
# Matches have Wrestlers
# Wrestlers have a Circuit/Brand/Gender/Name/Tag Teams/Stables
# Tag Teams have two Wrestlers
# Stables have more than two Wrestlers
# Regular matches are single/tag/multi-man/battle royal/ and are 1v1/triangle/4way
# Main Events are single/tag/multi-man/ with #1 contender spot or title shot and are 1v1/triangle/4way
# Feuds are a wrestler/tag-team/stable vs wrestler/tag-team/stable
# Super shows have multiple main events and gimmick matches
# Royal Rumbles/war games/elimination chambers have wrestlers and are only on Super Shows
import random
import migrations


def Show(tv_show, match_total=3):

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
    print(f"Welcome to {tv_show}!")
    wwe_shows = ["Raw", "Smackdown"]
    if tv_show == "IMPACT":
        teams = 11
    else:
        teams = 24
    if tv_show == "ROH":
        teams = 13
    for match in range(1, match_total):
        match_picker = roll()
        if match < match_total and "CMLL" not in tv_show:
            if match_picker < twenty_four_seven_match and tv_show in wwe_shows:
                print(
                    f"Match {match} will be a {combatent_picker()} 24/7 Title Defense"
                )
            elif match_picker < twenty_four_seven_match and tv_show not in wwe_shows:
                print(f"Match {match} will be a male one on one singles match")
            if (
                match_picker > twenty_four_seven_match
                and match_picker <= vanilla_singles
            ):
                print(f"Match {match} will be a {gender_picker()} singles match")
            if match_picker > vanilla_singles and match_picker <= multi_man_tag:
                print(f"Match {match} will be a {team_sizer(tv_show)} tag match")
            if (
                match_picker > multi_man_tag
                and match_picker < handicap
                or match_picker == tag_match
            ):
                print(f"Match {match} will be a {tag_match_maker(teams)}")
            if match_picker == handicap:
                handicap_1 = roll(1, 5)
                handicap_2 = roll(2, 5)
                if handicap_1 == handicap_2:
                    handicap_2 = roll(2, 5)
                print(
                    f"Match {match} will be a {handicap_1} on {handicap_2} handicap match"
                )

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
            if match_picker > trio and match_picker <= tag:
                print(f"Match {match} will be a 2/3 {tag_match_maker(teams)}")
            if match_picker > tag and match_picker <= singles_lightning:
                print(f"Match {match} will be a one fall lightning singles match!")

    elimination_match = 10
    number_1_contender_match = 75
    title_defense = 99
    battle_royal = 100
    main_event_roll = roll()
    main_event = f"debugger"
    if main_event_roll == battle_royal:
        main_event = "20 Man Battle Royal"
    if main_event_roll <= elimination_match:
        main_event = f"{team_sizer(tv_show)} elimination match"
    if (
        main_event_roll > elimination_match
        and main_event_roll < title_defense
        or main_event_roll == number_1_contender_match
    ):
        main_event = f"{combatent_picker()} #1 contender match for the {title(tv_show)}"

    if main_event_roll > number_1_contender_match and main_event_roll <= title_defense:
        main_event = f"{combatent_picker()} {title(tv_show)} "

    print(f"The Main Event will be a {main_event}")


def roll(start=1, end=100):
    the_roll = random.randrange(start, end)
    return the_roll


def combatent_picker(one_on_one_seed=10, triangle_seed=60, four_way_seed=100):
    picker = random.randrange(1, 100)
    combatents = ""
    if picker < one_on_one_seed:
        combatents = "One on One"
    elif picker > one_on_one_seed and picker < triangle_seed:
        combatents = "Triangle Match"
    else:
        combatents = "Fatal Four Way"
    return combatents


def gender_picker(male=70, female=99, intergender=100):
    gender_roll = roll()
    if gender_roll > male and gender_roll < intergender:
        gender = "female"
    elif gender_roll < female:
        gender = "male"
    else:
        gender = "intergender"
    if Show == "205":
        gender = "male"
    return gender


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
    team_sizer_roll = roll()
    genders = gender_picker()
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
    return team_size


def tag_match_maker(teams=24):
    genders = gender_picker()
    team_1 = roll(1, teams)
    team_2 = roll(1, teams)
    if team_1 == team_2:
        team_2 = team_2 + 1
        team_2 = team_1 - 1
    if Show == "205":
        genders = "male"
        return f"male tag-team contest between {team_1} and team {team_2}."
    if genders == "intergender":
        tag = "n unprecedented intergender tag-team contest"
    if genders == "female":
        tag = "female tag-team contest"
    if genders == "male":
        tag = f"male tag-team contest between team {team_1} and team {team_2}."
    return tag


# title isn't working right now...
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
    return random.choice(titles)


cont = "yes"
while cont == "yes" or cont == "y":
    print("Build/Update Databases?")
    build_db = input()
    if build_db == "y":
        migrations.db_builder()
    else:
        "Please Proceed"
    print("Which show are you making?")
    print("1. Raw")
    print("2. Smackdown")
    print("3. 205")
    print("4. IMPACT")
    print("5. CMLL")
    print("6. ROH")
    tv_input = int(input())

    if tv_input == 1:
        tv_show = "Raw"
    elif tv_input == 2:
        tv_input = "Smackdown"
    elif tv_input == 3:
        tv_show = "205"
    elif tv_input == 4:
        tv_show = "IMPACT"
    elif tv_input == 5:
        tv_show = "CMLL"
    elif tv_input == 6:
        tv_show = "ROH"
    print(f"How many matches will {tv_show} have?")
    match_amount = int(input())
    Show(tv_show, match_amount)
    print("Again?")
    cont = input()
