### CONSTANTS ###

from .command_logic.dyson import get_dyson_message
from .command_logic.tom2 import get_tom2_message
from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT
from bot.helpers.functions import get_message_content
from twitchio.dataclasses import Message
from random import randint
import time


class RedemptionCommands():

    # CONSTANTS

    UNDEFINED_DYSON = 'dyson'
    UNDEFINED_ONLYFANS = 'onlyfans'
    UNDEFINED_TOM = 'tom2'
    UNDEFINED_GIVE_UP = 'giveup'
    FLIP_FLIP = 'flip'
    GRANT_SKWIRL = 'mrskwirl'
    MCLOVIN_MCLOVIN = 'mclovin'
    MABLE_SLEEPY = 'sleepy'
    MABLE_COINTOSS = 'cointoss'
    FLAWER_PAT = 'pat'
    SKY_DROPKICK = 'dropkick'
    SKP_DROPKISS = 'dropkiss'

    REDEMPTION_COMMAND_LIST = [
        UNDEFINED_DYSON,
        UNDEFINED_ONLYFANS,
        UNDEFINED_TOM,
        UNDEFINED_GIVE_UP,
        FLIP_FLIP,
        GRANT_SKWIRL,
        MCLOVIN_MCLOVIN,
        MABLE_SLEEPY,
        MABLE_COINTOSS,
        FLAWER_PAT,
        SKY_DROPKICK,
        SKP_DROPKISS
    ]

    # FUNCTIONS

    async def dyson(ctx: Message):
        message = get_dyson_message()
        await ctx.send(message)

    async def onlyfans(ctx: Message):
        message = get_dyson_message('fan')
        await ctx.send(f'FANS YOU SAY?')
        time.sleep(MULTI_MESSAGE_TIMEOUT)
        await ctx.send(message)

    async def tom2(ctx: Message):
        bf_message, wtf_message = get_tom2_message()
        await ctx.send(bf_message)
        time.sleep(MULTI_MESSAGE_TIMEOUT)
        await ctx.send(wtf_message)

    async def giveup(ctx: Message):
        await ctx.send(f'NEVER GIVE UP https://www.youtube.com/watch?v=tYzMYcUty6s&ab_channel=MetalGearFro')

    async def flip(ctx: Message):
        message = get_message_content(ctx.content, FLIP_FLIP)
        if "!" not in message:
            await ctx.send(f'{message[::-1]}')
        else:
            await ctx.send(f'are you tryna do something sneaky..?')

    async def mrskwirl(ctx: Message):
        await ctx.send(f'Every Skwirl needs its NUT :peanuts:')

    async def mclovin(ctx: Message):
        await ctx.send(f'According to Urban Dictionary Colored McLovin is the cutest E-girl known to man. His uwus have created peace in times of turmoil, and his gamer girl bath water quenched the thirst of people without clean water. McLovin truly is the queen of all.')

    async def sleepy(ctx: Message):
        message = get_message_content(ctx.content, MABLE_SLEEPY)
        await ctx.send(message + ' is so so so sleeeepppyyyy!!!!')

    async def cointoss(ctx: Message):
        flip = randint(0, 1)
        if (flip == 0):
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")

    async def pat(ctx: Message):
        message = get_message_content(ctx.content, FLAWER_PAT)
        await ctx.send(f'/me gentle pats on ' + message + '\'s head. well done! you\'re doin great my friend (ｏ・・)ノ”(ᴗ ᴗ。) <3 ')

    async def dropkick(ctx: Message):
        message = get_message_content(ctx.content, SKY_DROPKICK)
        await ctx.send(f'/me '+message+f' has been dropkicked by {ctx.author.name} and sent into the abyss never to be loved again (•̀ᴗ•́ )و')

    async def dropkiss(ctx: Message):
        message = get_message_content(ctx.content, SKP_DROPKISS)
        await ctx.send(f'/me {ctx.author.name} has dropkissed ' + message + ' (on the cheeks cuz we are PG) and now ' + message + ' is not alone in this vast abyss  (ᵔᴥᵔ)')
