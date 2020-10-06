import sys
import requests
import click
import os
import json
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
@click.option('--label', '-a', multiple=True, type=str, help='Adds a label to a card', required=False)
@click.option('--comment', '-c', type=str, help='Adds a comment to a card', required=False)
def add_card(board, list_, text, label, comment):
    """Work with trello cards"""
    if not text:
        sys.exit("A card's text can not be empty.")

    all_boards = get_boards()
    if not all_boards:
        click.echo("You do not have boards. Create a board to add cards to.")
        sys.exit(0)

    all_lists = []
    board_id = None
    for b in all_boards:
        for k, v in b.items():
            if k == 'name' and v.lower() == board.strip().lower():
                board_id = b['id']
                all_lists = get_lists(board_id)

    list_id = None
    for l in all_lists:
        for k, v in l.items():
            if k == 'name' and v.lower() == list_.strip().lower():
                list_id = l['id']
    if label:
        labels = get_labels(board_id)
        label_ids = []
        for i in labels:
            for k, v in i.items():
                if k == 'name' and v.strip() in label:
                    label_ids.append(i['id'])
                    query = {
                        'key': KEY,
                        'token': TOKEN,
                        'idList': list_id,
                        'name': text,
                        'idLabels': label_ids
                    }
    else:
        query = {
            'key': KEY,
            'token': TOKEN,
            'idList': list_id,
            'name': text
        }

    create_card(query, comment)


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


def get_labels(board_id):
    """Returns all labels"""

    url = "{}/1/boards/{}/labels".format(baseurl, board_id)

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
        sys.exit("Failed to get all labels: {}".format(response.status_code))


def add_comment(card_id, comment):
    url = "{}/1/cards/{}/actions/comments".format(baseurl, card_id)

    query = {
        'key': KEY,
        'token': TOKEN,
        'id': card_id,
        'text': comment
    }

    response = requests.request(
        "POST",
        url,
        params=query
    )

    if response.ok:
        return True, response.status_code
    else:
        return False, response.status_code


def create_card(query, comment):
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
        if comment:
            resp_dict = response.json()
            if resp_dict.get('id'):
                created, status = add_comment(resp_dict.get('id'), comment)
                if created:
                    click.echo("Card created with comment")
                else:
                    sys.exit(
                        "Card created, but failed to add your comment: {}".format(status))
        else:
            click.echo("Card created")

    else:
        sys.exit("Failed to get all lists: {}".format(
            response.status_code))
