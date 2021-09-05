import Match_Maker
import random
import Shows
import circuits
import tag_teams
import Championships
import wrestlers


def roster_selector_247(people, show, gender, roster, contestants):
    for _ in [*range(people)]:
        contestants = Match_Maker.contestant_tracker(show, gender, contestants)
    title_holder = Championships.get_some({"name": "WWE 24/7 Championship"})[
        "title_holder"
    ]
    champ = wrestlers.get_by_name(title_holder)
    contestants.append(champ["id"])
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
    for person in wrestlers_in_tags:
        try:
            roster.remove(person)
        except ValueError:
            pass
    Shows.patch_show_roster(roster, show["id"])
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
    stable1 = Match_Maker.stable_member_mapper(show, team1)

    if stable1 is None:
        team_a = []
        spots_left = people_on_each_side - len(team_a)
        fillers = random.sample(roster, k=spots_left)
        for member in fillers:
            team_a.append(member)
            roster.remove(member)
    stable2 = Match_Maker.stable_member_mapper(show, team2)
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

        fillers = random.sample(show["males"], k=int(spots_left))

        for member in fillers:
            team_a.append(member)

            show["males"].remove(member)

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
    Shows.patch_show_roster(roster, show["id"])
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
        contestants = Match_Maker.contestant_tracker(show, gender, contestants)
        for _ in [*range(1, people)]:
            # check the persona of contestant[0]
            contestant_one_persona = Match_Maker.persona_finder(show, contestants[0])

            # check how many people are left to fight of the same gender

            matching_gender = show["males"] if gender == "Male" else show["females"]
            flat_list = list(set(matching_gender) & set(show["eligible_wrestlers"]))

            opponents_left = len(flat_list)
            # if it's less than five don't worry about personas and fill up the match
            if opponents_left < 5:
                while len(contestants) != people:
                    contestants = Match_Maker.contestant_tracker(
                        show, gender, contestants
                    )
            else:
                # fill the match up with non matching personas
                personas = {"faces", "heels", "jobbers", "tweeners", "anti_heroes"}
                personas.remove(contestant_one_persona)
                opponent_pool = []
                for personality in personas:
                    opponent_pool += Match_Maker.gendered_persona(
                        flat_list, show, personality
                    )
                contestant = random.choice(opponent_pool)
                contestants.append(contestant)
                show["eligible_wrestlers"].remove(contestant)
    if _stables == True:
        return roster_selector_stables(people, show, team1, roster, team2)

    return {"contestants": contestants, "eligible_participants": roster}
