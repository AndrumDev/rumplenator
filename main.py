from bot.rumplenator import Rumplenator
from dotenv import load_dotenv
import config

# for more options see https://pypi.org/project/python-dotenv/
load_dotenv()

config.setup()
bot = Rumplenator()
bot.run()
