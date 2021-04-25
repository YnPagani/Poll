from connections import pool
import db


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.id = _id
        self.text = option_text
        self.poll_id = poll_id

    def __repr__(self):
        return f"Option({self.text!r},{self.poll_id!r},{self.id!r})"

    def save(self):
        connection = pool.getconn()
        new_option_id = db.add_option(connection, self.text, self.poll_id)
        pool.putconn(connection)
        self.id = new_option_id

    @classmethod
    def get(cls, option_id: int) -> "Option":
        connection = pool.getconn()
        option = db.get_option(connection, option_id)
        pool.putconn(connection)

        return cls(option[1], option[2], option[0])

    def vote(self, username: str):
        connection = pool.getconn()
        db.add_poll_vote(connection, username, self.id)
        pool.putconn(connection)

    @property
    def votes(self):
        connection = pool.getconn()
        votes = db.get_votes_for_option(connection, self.id)
        pool.putconn(connection)
        return votes
