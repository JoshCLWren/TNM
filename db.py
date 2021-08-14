import psycopg2

# Connect to your postgres DB
con = psycopg2.connect("dbname=test user=postgres")

# Open a cursor to perform database operations
cursor = con.cursor()


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
          circuits INTEGER[],
          tag_teams INTEGER[],
          stables INTEGER[]
        );
        """
    )
with con:
    cursor.execute(
        """
      CREATE TABLE IF NOT EXISTS CIRCUITS(
        id bigserial PRIMARY KEY,
        name VARCHAR,
        stables INTEGER[],
        tag_teams INTEGER[],
        wrestlers INTEGER[],
        injuries INTEGER[],
        heels INTEGER[],
        faces INTEGER[],
        anti_heroes INTEGER[],
        tweeners INTEGER[],
        jobbers INTEGER[]
      );
    """
    )
with con:
    cursor.execute(
        """
      CREATE TABLE IF NOT EXISTS TAGTEAMS(
        id bigserial PRIMARY KEY,
        name VARCHAR,
        tag_team_members INTEGER[2]
      );
          """
    )
with con:
    cursor.execute(
        """

      CREATE TABLE IF NOT EXISTS STABLES(
        id bigserial PRIMARY KEY,
        name VARCHAR,
        members INTEGER[]
      );
          """
    )
