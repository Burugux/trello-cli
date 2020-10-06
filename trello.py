import sys
import requests
import click
import os
from dotenv import load_dotenv
load_dotenv()

KEY = os.environ.get('KEY')
TOKEN = os.environ.get('TOKEN')


baseurl = "https://api.trello.com"


@click.group()
def cli():
    """Trello command line tool"""
    pass


@cli.command()
@click.option('--board', '-b', type=str, help='The board the card will be added to')
@click.option('--list', '-l', 'list_', type=str, help='List that the card will be added to')
@click.option('--text', '-t', type=str, help='Text you want to add to a card')
def add_card(board, list_, text):
    """Work with trello cards"""

    if not text:
        sys.exit("A card's text can not be empty.")

    all_boards = get_boards()
    if not all_boards:
        click.echo("You do not have boards. Create a board to add cards to.")
        sys.exit(0)

    all_lists = []
    for b in all_boards:
        for k, v in b.items():
            if k == 'name' and v.lower() == board.lower():
                all_lists = get_lists(b['id'])

    list_id = None
    for l in all_lists:
        for k, v in l.items():
            if k == 'name' and v.lower() == list_.lower():
                list_id = l['id']

    query = {
        'key': KEY,
        'token': TOKEN,
        'idList': list_id,
        'name': text
    }

    cardsPath = "{}/{}".format(
                baseurl,
                '1/cards'
    )

    response = requests.request(
        "POST",
        cardsPath,
        params=query
    )
    if response.ok:
        click.echo("Card added")
    else:
        sys.exit("Failed to get all lists: {}".format(
            response.status_code))


def get_boards():
    """Returns all boards for a specific user"""
    boardsquery = {
        'key': KEY,
        'token': TOKEN,
        'fields': 'name'
    }
    boardsPath = "{}{}".format(
        baseurl,
        '/1/members/me/boards'
    )
    headers = {
        "Accept": "application/json"
    }

    response = requests.request(
        "GET",
        boardsPath,
        headers=headers,
        params=boardsquery
    )

    if response.ok:
        return response.json()
    else:
        sys.exit("Failed to get all boards: {}".format(response.status_code))


def get_lists(board_id):
    """Returns all boards for a specific lists"""
    url = "{}/1/boards/{}/lists".format(baseurl, board_id)

    query = {
        'key': KEY,
        'token': TOKEN
    }

    response = requests.request(
        "GET",
        url,
        params=query
    )
    if response.ok:
        return response.json()
    else:
        sys.exit("Failed to get all lists: {}".format(response.status_code))
