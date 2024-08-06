from numpy import array_split

from text import game_response_template


def process_subscribe_games_data(games: str):
    stripped_data = []
    if games:
        data = games.split(',')
        stripped_data = list(map(lambda item: ({'game': item.strip()}), data))

    return stripped_data


def format_data(data: list):
    formatted_data = []

    for item in data:
        formatted_data.append(game_response_template.format(**item))

    return formatted_data


def prepare_data_for_creating_response_message(data: list):
    list_length_limit = 20
    formatted_data = format_data(data)
    formatted_data_length = len(formatted_data)
    prepared_data = []

    if formatted_data_length > list_length_limit:
        number_of_splits = round(formatted_data_length / list_length_limit)
        prepared_data = list(array_split(formatted_data, number_of_splits))
    else:
        prepared_data.append(formatted_data)

    return prepared_data


def form_response_message(data: list):
    prepared_data = prepare_data_for_creating_response_message(data)
    messages = []
    for data in prepared_data:
        messages.append('\n'.join(data))
    return messages
