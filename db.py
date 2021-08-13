import sqlite3 as sl

con = sl.connect("my-test.db")


with con:
    con.execute(
        """
      CREATE TABLE IF NOT EXISTS WRESTLERS(
        wrestler_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        work_rate INTEGER,
        push INTEGER,
        charisma INTEGER,
        weight INTEGER,
        gender TEXT,
        tnm_index INTEGER
      );
      """
    )
with con:
    con.execute(
        """
      CREATE TABLE IF NOT EXISTS CIRCUITS(
        circuit_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
      );
    """
    )
with con:
    con.execute(
        """
      CREATE TABLE IF NOT EXISTS TAGTEAMS(
        tag_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
        partner_1 INTEGER REFERENCES WRESTLER(wrestler_id),
        partner_2 INTEGER REFERENCES WRESTLER(wrestler_id)
      );
          """
    )
with con:
    con.execute(
        """

      CREATE TABLE IF NOT EXISTS STABLES(
        stable_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
      );
          """
    )
with con:
    con.execute(
        """

      CREATE TABLE IF NOT EXISTS CIRCUIT_ROSTERS(
        roster_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        wrestler_id INTEGER REFERENCES WRESTLER(wrestler_id),
        circuit_id INTEGER REFERENCES CIRCUIT(circuit_id)
      );
          """
    )
with con:
    con.execute(
        """

      CREATE TABLE IF NOT EXISTS CIRCUIT_INJURIES(
        injury_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        circuit_id INTEGER REFERENCES CIRCUIT(circuit_id),
        wrestler_id INTEGER REFERENCES WRESTLER(wrestler_id),
        duration INTEGER
      );
          """
    )
with con:
    con.execute(
        """

      CREATE TABLE IF NOT EXISTS CIRCUIT_CONTRACTS(
        contract_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        circuit_id INTEGER REFERENCES CIRCUIT(circuit_id),
        wrestler_id INTEGER REFERENCES WRESTLER(wrestler_id),
        term INTEGER
      );
          """
    )
with con:
    con.execute(
        """

      CREATE TABLE IF NOT EXISTS CIRCUIT_PERSONALITIES(
        personality_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        circuit_id INTEGER REFERENCES CIRCUIT(circuit_id),
        wrestler_id INTEGER REFERENCES WRESTLER(wrestler_id),
        personality TEXT
      );
          """
    )
with con:
    con.execute(
        """

      CREATE TABLE IF NOT EXISTS STABLE_MEMBERS(
        stable_member_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        wrestler_id INTEGER REFERENCES WRESTLER(wrestler_id),
        stable_id INTEGER REFERENCES STABLE(stable_id)
      );

    """
    )

con.commit()
con.close()
