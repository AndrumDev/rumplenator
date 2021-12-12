import random
from config import get_config


__quotes_file_path = get_config().get('resource_dir') / 'motivational_quotes.txt'


def get_motivational_quote() -> str:
    with open(__quotes_file_path, "r") as file:
        lines = file.readlines()
        return random.choice(lines)
    