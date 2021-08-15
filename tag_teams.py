from types import resolve_bases
from database import cursor, con, tag_teams_table
import utilities
import wrestlers
import collections


def tag_team_serializer():
    """Maps over the TEAMS.DAT file from TNM and makes tag team rows"""
    tag_team_name = 3
    tag_team_count = 0
    tag_teams = []
    member_1 = 1
    member_2 = 2

    with open("TNM/tnm7se_build_13/tnm7se/TNM7SE/DATA/TEAMS.DAT") as tags:
        for index, line in enumerate(tags):
            if index == member_1:
                tag_teams.append({"Member 1": line.strip()})
                member_1 += 10
            if index == member_2:
                tag_teams[tag_team_count]["Member 2"] = line.strip()
                member_2 += 10
            if index == tag_team_name:
                tag_teams[tag_team_count]["Tag Team Name"] = line.strip()
                tag_team_name += 10
                tag_team_count += 1
    teams = []
    for tag in tag_teams:
        member_1 = wrestlers.get_by_name(tag["Member 1"])
        member_2 = wrestlers.get_by_name(tag["Member 2"])
        if member_1 is None:
            continue
        elif member_2 is None:
            continue
        else:
            if tag["Tag Team Name"] == "":
                tag["Tag Team Name"] = f"{tag['Member 1']}/{tag['Member 2']}"
            members = [member_1["id"], member_2["id"]]

            teams.append(
                {
                    "name": tag["Tag Team Name"],
                    "members": members,
                }
            )

    return teams


def seed_tags(tag_teams, drop=True, create_table=True):
    """Maps over a list of wrestlers and adds them to the wrestlers pg table"""
    if drop == True:
        cursor.execute("DROP TABLE tagteams;")

    if create_table == True:
        tag_teams_table()

    for tag in tag_teams:

        query = """
                INSERT INTO TAGTEAMS (name, tag_team_members)
                VALUES (%(name)s, %(tag_team_members)s);
                """

        with con:

            cursor.execute(
                query, {"name": tag["name"], "tag_team_members": tag["members"]}
            )

    # joins the tagteams table to itself and delete and duplicate tags

    with con:
        cursor.execute(
            """
            DELETE FROM
                tagteams a
                    USING tagteams b
            WHERE
                a.id < b.id
                AND a.tag_team_members = b.tag_team_members;
        """
        )


def get_all_tags():
    """Returns all tag teams in the db"""

    with con:
        cursor.execute("Select * from tagteams;")

    return cursor.fetchall()
