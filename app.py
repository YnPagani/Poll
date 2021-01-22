import os
import psycopg2
from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
import db

MENU_PROMPT = """
--- MENU ---

1) Create new poll.
2) List open polls.
3) Vote on a poll.
4) Show poll votes.
5) Select a random winner from a poll option.
6) Exit

Enter your option: """

NEW_OPTION_PROMPT = "Enter new option text (or leave it blank to stop): "


def prompt_create_poll(connection):
    poll_title = input("\nEnter poll title: ")
    poll_owner = input("\nEnter poll owner: ")
    options = []

    while new_option := input(NEW_OPTION_PROMPT):
        options.append(new_option)

    db.create_poll(connection, poll_title, poll_owner, options)


def list_open_polls(connection):
    polls = db.get_polls(connection)

    for _id, title, owner in polls:
        print(f"{_id}: {title} (created by {owner})")


def prompt_vote_poll(connection):
    poll_id = int(input("\nEnter poll you would like to vote on: "))

    poll_options = db.get_polls_details(connection, poll_id)
    print_poll_options(poll_options)

    option_id = input("\nOption ID you will to vote for: ")
    username = input("\nEnter username you would like to vote as: ")

    db.add_poll_vote(connection, username, option_id)


def print_poll_options(options):
    """Helper Function"""
    ID = 3
    TEXT = 4
    print("\n")
    for option in options:
        print(f"{option[ID]}: {option[TEXT]}")


def show_poll_votes(connection):
    poll_id = int(input("\nEnter poll you would like to see votes for: "))
    try:
        poll_and_votes = db.get_poll_and_results(connection, poll_id)
    except DivisionByZero:
        print("\nNo votes cast for this poll.")
    else:
        print("\n")
        for _id, option_text, count, percentage in poll_and_votes:
            print(f"'{option_text}' got {count} votes ({percentage: .2f}%)")


def randomize_poll_winner(connection):
    poll_id = int(input("\nEnter poll you would like to pick a winner for: "))

    poll_options = db.get_polls_details(connection, poll_id)
    print_poll_options(poll_options)

    option_id = int(input("\nEnter which is the winning option, (we will "
                          "pick a random winner from voters): "))
    winner = db.get_random_poll_vote(connection, option_id)

    NAME = 0
    print(f"\nThe randomly selected winner is: {winner[NAME]}")


MENU_OPTIONS = {
    "1": prompt_create_poll,
    "2": list_open_polls,
    "3": prompt_vote_poll,
    "4": show_poll_votes,
    "5": randomize_poll_winner
}


def menu():
    load_dotenv()
    db_uri = os.environ["DATABASE_URI"]

    connection = psycopg2.connect(db_uri)
    db.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection](connection)
        except KeyError:
            print("\nInvalid option, try again.")


menu()
