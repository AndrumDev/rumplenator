import pathlib
import os
from dotenv import load_dotenv


# for more options see https://pypi.org/project/python-dotenv/
load_dotenv()

if os.getenv('ENVIRONMENT') is None:
    raise Exception('environment variable ENVIRONMENT not set. Must be one of TEST, LOCAL, or PROD')

__conf = {
    'TEST': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': pathlib.Path(__file__).parent / 'test' / 'resources',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator_test'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='channel_test')
    },
    'LOCAL': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': pathlib.Path(__file__) / 'bot' / 'resources',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator_dev'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='tabi_twitchett')
    },
    'PROD': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': pathlib.Path(__file__) / 'bot' / 'resources',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='AndRumpleteazer')
    },
}


def get_config() -> dict:
    return __conf[os.environ['ENVIRONMENT']]
