import psycopg2.extras

con = psycopg2.connect("dbname=tnm user=postgres")
cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def wrestler_table():
    with con:
        cursor.execute(
            """
          CREATE TABLE IF NOT EXISTS WRESTLERS(
          id bigserial PRIMARY KEY,
          name VARCHAR,
          work_rate INTEGER,
          push INTEGER,
          charisma INTEGER,
          weight INTEGER,
          gender VARCHAR,
          tnm_index INTEGER,
          circuits INTEGER[] DEFAULT '{}',
          tag_teams INTEGER[] DEFAULT '{}',
          stables INTEGER[] DEFAULT '{}'
          );
          """
        )


def circuit_table():
    with con:
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS CIRCUITS(
          id bigserial PRIMARY KEY,
          name VARCHAR,
          stables INTEGER[] DEFAULT '{}',
          tag_teams INTEGER[] DEFAULT '{}',
          wrestlers INTEGER[] DEFAULT '{}',
          injuries INTEGER[] DEFAULT '{}',
          heels INTEGER[] DEFAULT '{}',
          faces INTEGER[] DEFAULT '{}',
          anti_heroes INTEGER[] DEFAULT '{}',
          tweeners INTEGER[] DEFAULT '{}',
          jobbers INTEGER[] DEFAULT '{}',
          championships VARCHAR[] DEFAULT '{}'
        );
      """
        )


def tag_teams_table():
    with con:
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS TAGTEAMS(
          id bigserial PRIMARY KEY,
          name VARCHAR,
          tag_team_members INTEGER[2] DEFAULT '{}'
        );
            """
        )


def stables_table():
    with con:
        cursor.execute(
            """

        CREATE TABLE IF NOT EXISTS STABLES(
          id bigserial PRIMARY KEY,
          name VARCHAR,
          members INTEGER[] DEFAULT '{}'
        );
            """
        )


def shows_table():
    with con:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS SHOWS(
                    id bigserial PRIMARY KEY,
                    name VARCHAR,
                    participants integer[] DEFAULT '{}',
                    matches integer[] DEFAULT '{}'
                )
            """
        )


# stable tags?
# championships?
# brands?
# are matches another table with Show ids?
# how to not repeat matches from "Week to week"?
