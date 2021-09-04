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
                    busy_wrestlers integer[] DEFAULT '{}',
                    matches integer,
                    eligible_wrestlers integer[] DEFAULT '{}',
                    heels integer[] DEFAULT '{}',
                    faces integer[] DEFAULT '{}',
                    tweeners integer[] DEFAULT '{}',
                    jobbers integer[] DEFAULT '{}',
                    anti_heroes integer[] DEFAULT '{}',
                    males integer[] DEFAULT '{}',
                    females integer[] DEFAULT '{}',
                    card text[] default '{}');
            """
        )


def reset_and_delete(table):
    """resets id to zero and deletes the table data"""
    query = "DELETE FROM"
    cursor.execute(f"{query} {table};")
    cursor.execute(f"SELECT SETVAL(pg_get_serial_sequence('{table}', 'id'), 1, false);")


def championship():
    # draft for potential championship table
    with con:
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS CHAMPIONSHIPS(
                    id bigserial PRIMARY KEY,
                    name VARCHAR,
                    weightclass VARCHAR,
                    brand_id INTEGER,
                    circuit_id INTEGER,
                    title_holder INTEGER
                    type VARCHAR
                );
            """
        )


# stable tags?
# championships?
# brands?
# are matches another table with Show ids?
# how to not repeat matches from "Week to week"?
