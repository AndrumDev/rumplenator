from pathlib import Path
from dotenv import load_dotenv
import logging
import os


# for more options see https://pypi.org/project/python-dotenv/
load_dotenv()

logging.basicConfig(level=logging.INFO)

if os.getenv('ENVIRONMENT') is None:
    raise Exception('environment variable ENVIRONMENT not set. Must be one of TEST, LOCAL, or PROD')

__conf = {
    'TEST': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': Path(__file__).resolve().parent / 'test' / 'resources',
        'storage_dir': Path(__file__).resolve().parent / 'storage',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator_test'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='channel_test'),
        'pun_url': 'https://pun.me/id/88/'
    },
    'LOCAL': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': Path(__file__).resolve().parent / 'bot' / 'resources',
        'storage_dir': Path(__file__).resolve().parent / 'storage',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator_dev'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='tabi_twitchett'),
        'pun_url': 'https://pun.me/random/'
    },
    'PROD': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': Path(__file__).resolve().parent / 'bot' / 'resources',
        'storage_dir': Path(__file__).resolve().parent / 'storage',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='AndRumpleteazer'),
        'pun_url': 'https://pun.me/random/'
    },
}


def get_config() -> dict:
    return __conf[os.environ['ENVIRONMENT']]
