from config import get_config
from collections import defaultdict
from random import randint


dyson_file_path = get_config().get('resource_dir') / 'dyson_pog.txt'


def __get_dyson_data() -> dict, list(str):
    quotes_dict = __read_dyson_file()
    quote_params = list(quotes_dict.keys())
    return quotes_dict, quote_params


def __read_dyson_file() -> dict:
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


def get_dyson_message(param='') -> str:
    quotes, params = __get_dyson_data()
    if param == '':
        param = params[randint(0, len(params)-1)]
    if param in params:
        return ' '.join(quotes[param][randint(0, len(quotes[param])-1)])
    else:
        return 'We currently do not have that in stock. Please choose from our current range: hand, heat, dry, fan, style, and vac.'
