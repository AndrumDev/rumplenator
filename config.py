from pathlib import Path
from dotenv import load_dotenv
from logging import handlers
import logging
import os
import sys


# env convig
# for more options see https://pypi.org/project/python-dotenv/
load_dotenv()

if os.getenv('ENVIRONMENT') is None:
    raise Exception('environment variable ENVIRONMENT not set. Must be one of TEST, LOCAL, or PROD')


def setup():
    # logging config
    log_dir = Path(__file__).resolve().parent / 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = log_dir / 'debug.log'
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            handlers.RotatingFileHandler(log_path, maxBytes=2000, backupCount=5, encoding='utf-8')
        ]
    )


__conf = {
    'TEST': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': Path(__file__).resolve().parent / 'test' / 'resources',
        'overlay_dir': Path(__file__).resolve().parent / 'pomo_overlay_source',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator_test'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='channel_test'),
        'pun_url': 'https://pun.me/id/88/'
    },
    'LOCAL': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': Path(__file__).resolve().parent / 'bot' / 'resources',
        'overlay_dir': Path(__file__).resolve().parent / 'pomo_overlay_source',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator_dev'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='tabi_twitchett'),
        'pun_url': 'https://pun.me/random/'
    },
    'PROD': {
        'irc_token': os.environ['TMI_TOKEN'],
        'client_id': os.environ['CLIENT_ID'],
        'resource_dir': Path(__file__).resolve().parent / 'bot' / 'resources',
        'overlay_dir': Path(__file__).resolve().parent / 'pomo_overlay_source',
        'bot_nick': os.getenv('BOT_NICK', default='rumplenator'),
        'bot_prefix': '!',
        'channel': os.getenv('CHANNEL', default='AndRumpleteazer'),
        'pun_url': 'https://pun.me/random/'
    },
}


def get_config() -> dict:
    return __conf[os.environ['ENVIRONMENT']]


if __name__ == "__main__":
   pass