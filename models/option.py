from typing import List
from connections import create_connection
import db


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.id = _id
        self.text = option_text
        self.poll_id = poll_id

    def __repr__(self):
        return f"Option({self.text!r},{self.poll_id!r},{self.id!r})"

    def save(self):
        connection = create_connection()
        new_option_id = db.add_option(connection, self.text, self.poll_id)
        connection.close()
        self.id = new_option_id

    @classmethod
    def get(cls, option_id: int) -> "Option":
        connection = create_connection()
        option = db.get_option(connection, option_id)
        connection.close()

        return cls(option[1], option[2], option[0])

    def vote(self, username: str):
        connection = create_connection()
        db.add_poll_vote(connection, username, self.id)
        connection.close()

    @property
    def votes(self):
        connection = create_connection()
        votes = db.get_votes_for_option(connection, self.id)
        connection.close()
        return votes
