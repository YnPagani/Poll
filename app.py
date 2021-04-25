import random
from connections import pool
from models.option import Option
from models.poll import Poll
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


def prompt_create_poll():
    poll_title = input("\nEnter poll title: ")
    poll_owner = input("\nEnter poll owner: ")
    poll = Poll(poll_title, poll_owner)
    poll.save()

    while new_option := input(NEW_OPTION_PROMPT):
        poll.add_option(new_option)


def list_open_polls():
    for poll in Poll.all():
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")


def prompt_vote_poll():
    poll_id = int(input("\nEnter poll you would like to vote on: "))
    print_poll_options(Poll.get(poll_id).options)
    option_id = int(input("\nOption ID you will to vote for: "))
    username = input("\nEnter username you would like to vote as: ")
    Option.get(option_id).vote(username)


def print_poll_options(options):
    """Helper Function"""
    print("\n")
    for option in options:
        print(f"{option.id}: {option.text}")


def show_poll_votes():
    poll_id = int(input("\nEnter poll you would like to see votes for: "))
    poll = Poll.get(poll_id)
    options = poll.options
    votes_per_option = [len(option.votes) for option in options]
    total_votes = sum(votes_per_option)

    try:
        for option, votes in zip(options, votes_per_option):
            percentage = (votes / total_votes) * 100
            print(f"{option.text} got {votes} votes ({percentage: .2f} of total)")

    except ZeroDivisionError:
        print("No votes cast for this poll yet")


def randomize_poll_winner():
    poll_id = int(input("\nEnter poll you would like to pick a winner for: "))
    print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("\nEnter which is the winning option, (we will "
                          "pick a random winner from voters): "))
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
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
    connection = pool.putconn()
    db.create_tables(connection)

    while (selection := input(MENU_PROMPT)) != "6":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("\nInvalid option, try again.")


menu()
