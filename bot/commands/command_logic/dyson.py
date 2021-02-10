from config import get_config
from typing import Dict, List, Tuple
from collections import defaultdict
from random import randint


dyson_file_path = get_config().get('resource_dir') / 'dyson_pog.txt'


def __read_dyson_file() -> Dict:
    dyson_file = open(dyson_file_path, "r")
    quotesdict = defaultdict(lambda: [])
    for line in dyson_file:
        line = line.split('#')[0].strip()
        if line == '':
            continue
        instance = line.split()
        category = instance[0]
        quote = instance[1:]
        quotesdict[category].extend([quote])

    return quotesdict


def get_dyson_message(category=None) -> str:
    quotes = __read_dyson_file()
    categories = list(quotes.keys())
    if not category:
        category = categories[randint(0, len(categories)-1)]
    if category in categories:
        return ' '.join(quotes[category][randint(0, len(quotes[category])-1)])
    else:
        return 'We currently do not have that in stock. Please choose from our current range: hand, heat, dry, fan, style, and vac.'
