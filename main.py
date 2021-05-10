from bot.rumplenator import Rumplenator
from dotenv import load_dotenv

# for more options see https://pypi.org/project/python-dotenv/
load_dotenv()

bot = Rumplenator()
bot.run()
