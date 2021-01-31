from collections import defaultdict
from random import randint
import sys


def __get_dyson_data():
    quotes_dict = __read_dyson_file()
    quote_params = list(quotes_dict.keys())
    return quotes_dict, quote_params


def __read_dyson_file():
    dysontext = sys.argv[1]
    f = open(dysontext, "r")
    quotesdict = defaultdict(lambda: [])
    for line in f:
        line = line.split('#')[0].strip()
        if line == '':
            continue
        instance = line.split()
        category = instance[0]
        quote = instance[1:]
        quotesdict[category].extend([quote])

    return quotesdict


def get_dyson_message(param=''):
    quotes, params = __get_dyson_data()
    if param == '':
        param = params[randint(0, len(params)-1)]
    if param in params:
        return (' '.join(quotes[param][randint(0, len(quotes[param])-1)])).encode("utf-8").decode("utf-8")
    else:
        return 'We currently do not have that in stock. Please choose from our current range: hand, heat, dry, fan, style, and vac.'
