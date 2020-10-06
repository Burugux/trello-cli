from click.testing import CliRunner
from trello import add_card

runner = CliRunner()


def test_add_card_without_comment():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one", "-t", "card without any comment or label"])
    assert response.exit_code == 0
    assert "Card created\n" in response.output


def test_add_card_with_comment_only():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one", "-t", "card with comment only", "-c", "tag"])
    assert response.exit_code == 0
    assert "Card created with comment\n" in response.output


def test_add_card_with_one_Label_only():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one", "-t", "card with one label only", "-a", "Test"])
    assert response.exit_code == 0
    assert "Card created\n" in response.output


def test_add_card_with_more_than_one_label():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one", "-t", "card with multiple labels only", "-a", "Test", "-a", "Important"])
    assert response.exit_code == 0
    assert "Card created\n" in response.output


def test_add_card_with_one_label_and_comment():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one", "-t", "card with one label and comment", "-c", "tag", "-a", "Test"])
    assert response.exit_code == 0
    assert "Card created with comment\n" in response.output


def test_add_card_with_multiple_labels_and_comment():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one", "-t", "card with multiple labels and a comment", "-a", "Test", "-a", "Important", "-c", "tag"])
    assert response.exit_code == 0
    assert "Card created with comment\n" in response.output


def test_add_card_without_board_name():
    response = runner.invoke(
        add_card, ["-l", "list one", "-t", "test card"])
    assert response.exit_code == 1
    assert "Please specify a board name\n" in response.output


def test_add_card_without_list_name():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-t", "test card"])
    assert response.exit_code == 1
    assert "Please specify a list name\n" in response.output


def test_add_card_without_card_text():
    response = runner.invoke(
        add_card, ["-b", "cloud test", "-l", "list one"])
    assert response.exit_code == 1
    assert "A card's text can not be empty\n" in response.output
