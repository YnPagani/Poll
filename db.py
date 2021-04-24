# Queries
CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls(
    id SERIAL PRIMARY KEY,
    title TEXT,
    owner_username TEXT
    );"""

CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options(
    id SERIAL PRIMARY KEY,
    option_text TEXT,
    poll_id INTEGER,
    FOREIGN KEY(poll_id) REFERENCES polls(id)
    );"""

CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes(
    username TEXT,
    option_id INTEGER,
    FOREIGN KEY(option_id) REFERENCES options(id)
    );"""

SELECT_POLL = """SELECT * FROM polls WHERE id = %s;"""

SELECT_OPTION = """SELECT * FROM options WHERE id = %s"""

SELECT_ALL_POLLS = """SELECT * FROM polls;"""

SELECT_POLL_OPTIONS = """SELECT * FROM options WHERE poll_id = %s;"""

SELECT_LATEST_POLL = """SELECT * 
    FROM polls
    WHERE polls.id = (SELECT id FROM polls ORDER BY id DESC LIMIT 1);"""

SELECT_VOTES_FOR_OPTION = "SELECT * FROM votes WHERE option_id = %s"

INSERT_POLL_RETURN_ID = """INSERT INTO polls(title, owner_username)
    VALUES (%s, %s) RETURNING id;"""

INSERT_OPTION_RETURN_ID = """INSERT INTO options(option_text, poll_id) 
    VALUES %s RETURNING id;"""

INSERT_VOTE = """INSERT INTO votes(username, option_id)
    VALUES (%s, %s);"""


# Methods

def create_tables(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)


# -------- POLL ----------

def create_poll(connection, title, owner):
    with connection:
        with connection.cursor() as cursor:
            # cursor will have the id of the new poll
            cursor.execute(INSERT_POLL_RETURN_ID, (title, owner))

            # Fetch from the cursor the id of the new poll
            ID = 0
            poll_id = cursor.fetchone()[ID]
            return poll_id


def add_poll_vote(connection, username, option_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (username, option_id))


def get_polls(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()


def get_poll(connection, poll_id: int):
    with connection:
        with connection.cursor as cursor:
            cursor.execute(SELECT_POLL, (poll_id,))
            return cursor.fetchone()


def get_latest_poll(connection):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_LATEST_POLL)
            return cursor.fetchone()


# ---------- OPTIONS -----------

def get_option(connection, option_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_OPTION, (option_id,))
            return cursor.fetchone()


def add_option(connection, option_text: str, poll_id: id):
    ID = 0  # index
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_OPTION_RETURN_ID, (option_text, poll_id))
            option_id = cursor.fetchone()[ID]
            return option_id


# ---------- VOTES -------------

def get_votes_for_option(connection, option_id: int):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_VOTES_FOR_OPTION, (option_id,))
            return cursor.fetchall()


def get_poll_options(connection, poll_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_OPTIONS, (poll_id,))
            return cursor.fetchall()
