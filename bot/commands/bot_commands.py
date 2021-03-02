from bot.commands.command_logic.dyson import get_dyson_message
from bot.commands.command_logic.tom2 import get_tom2_message
from bot.commands.command_logic.pomo import check_active_user, handle_pomo
from bot.commands.command_logic.simp import get_simp_quote
from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT_SECONDS
from bot.helpers.functions import get_message_content
from twitchio.dataclasses import Message
from random import randint
from enum import Enum
import time


class CommandKeys(Enum):
    '''
    This set of properties defines the commands that can be invoked from chat, e.g. !hi

    The enum value is the command itself and MUST match a name of a method in this file,
    otherwise there will be an error when the command is invoked
    '''

    # channel commands
    CMD_HI = 'hi'
    CMD_KILL = 'kill'
    CMD_BOT_LOVE = 'botlove'
    CMD_RAID = 'raid'
    CMD_SSIMP = 'ssimp'
    CMD_SIMP = 'simp'
    CMD_WOWIE = 'wowie'
    CMD_HYPE = 'hype'
    CMD_POMO = 'pomo'

    # redemption commands
    CMD_UNDEFINED_DYSON = 'dyson'
    CMD_UNDEFINED_ONLYFANS = 'onlyfans'
    CMD_UNDEFINED_TOM = 'tom2'
    CMD_UNDEFINED_GIVE_UP = 'giveup'
    CMD_FLIP_FLIP = 'flip'
    CMD_FLIP_WHIP = 'whip'
    CMD_GRANT_SKWIRL = 'mrskwirl'
    CMD_MCLOVIN_MCLOVIN = 'mclovin'
    CMD_MABLE_SLEEPY = 'sleepy'
    CMD_MABLE_BOOP = 'boop'
    CMD_MABLE_COINTOSS = 'cointoss'
    CMD_FLAWER_PAT = 'pat'
    CMD_FLAWER_TUCK = 'tuck'
    CMD_SKY_DROPKICK = 'dropkick'
    CMD_SKP_DROPKISS = 'dropkiss'
    CMD_TEACHERLY_CONGRATS = 'congrats'
    CMD_KARANT_VIBE = 'vibe'
    CMD_HAM_FOCUS = 'focus'


### Channel commands ###


async def hi(ctx: Message):
    await ctx.send(f'Hello {ctx.author.name}!')

async def kill(ctx: Message):
    await ctx.send('I cannot be killed™'.encode("utf-8").decode("utf-8"))

async def bot_love(ctx: Message):
    await ctx.send(f'aaawh thank you {ctx.author.name} andrumHeart If I was sentient I would love you too! xxx')

async def raid(ctx: Message):
    await ctx.send(' Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype')

async def ssimp(ctx: Message):
    await ctx.send('does she speak? notice me. u r beetiful asian quenn. can i wife u? oh you have a bf? im out.')

async def simp(ctx: Message):
    message = await get_simp_quote()
    await ctx.send(message)

async def wowie(ctx: Message):
    await ctx.send('Thats awesome! But ur not just awesome, ur WOWIE! andrumHeart ')

async def hype(ctx: Message):
    await ctx.send('andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype')

async def pomo(ctx: Message):
    await handle_pomo(ctx)


### Redemption commands ###


async def onlyfans(ctx: Message):
    message = get_dyson_message('fan')
    await ctx.send('FANS YOU SAY?')
    time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
    await ctx.send(message)

async def dyson(ctx: Message):
        message = get_dyson_message()
        await ctx.send(message)

async def tom2(ctx: Message):
    bf_message, wtf_message = get_tom2_message()
    await ctx.send(bf_message)
    time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
    await ctx.send(wtf_message)

async def giveup(ctx: Message):
    await ctx.send('NEVER GIVE UP https://www.youtube.com/watch?v=tYzMYcUty6s&ab_channel=MetalGearFro')

async def flip(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLIP_FLIP.value)
    if "!" not in message:
        await ctx.send(f'{message[::-1]}')
    else:
        await ctx.send('are you tryna do something sneaky..?')

async def mrskwirl(ctx: Message):
    await ctx.send('Every Skwirl needs its NUT :peanuts:')

async def mclovin(ctx: Message):
    await ctx.send('According to Urban Dictionary Colored McLovin is the cutest E-girl known to man. His uwus have created peace in times of turmoil, and his gamer girl bath water quenched the thirst of people without clean water. McLovin truly is the queen of all.')

async def sleepy(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_MABLE_SLEEPY.value)
    await ctx.send(message + ' is so so so sleeeepppyyyy!!!!')

async def cointoss(ctx: Message):
    flip = randint(0, 1)
    if (flip == 0):
        await ctx.send("Heads")
    else:
        await ctx.send("Tails")

async def pat(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLAWER_PAT.value)
    await ctx.send(f'/me gentle pats on {message}\'s head. well done! you\'re doin great my friend (ｏ・・)ノ”(ᴗ ᴗ。) <3 ')

async def dropkick(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_SKY_DROPKICK.value)
    await ctx.send(f'/me {message} has been dropkicked by {ctx.author.name} and sent into the abyss never to be loved again (•̀ᴗ•́ )و')

async def dropkiss(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_SKP_DROPKISS.value)
    await ctx.send(f'/me {ctx.author.name} has dropkissed {message} (on the cheeks cuz we are PG) and now {message} is not alone in this vast abyss (ᵔᴥᵔ)')

async def boop(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_MABLE_BOOP.value)
    if "rumplenator" in message:
        await ctx.send('/me I got booped ☆ヾ(￣ω ￣｡)ノ')
    else:
        await ctx.send(f'/me {message} got booped ☆ヾ(￣ω ￣｡)ノ')

async def tuck(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLAWER_TUCK.value)
    if message == '':
        return()
    else:
        await ctx.send(f"/me it\'s {message}\'s bedtime! get comfy in bed and have sweet dreams my friend! thanks for being here, we\'ll miss you! (︶｡︶✽)zzz")

async def whip(ctx: Message):
    await ctx.send(f'/me *cracks whip* BACK TO WORK!')

async def vibe(ctx: Message):
    await ctx.send(f'/me We vibin\'! andrumHype andrumSmug blobDance We vibin\'! andrumHype andrumSmug blobDance We vibin\'! andrumHype andrumSmug blobDance ')

async def congrats(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_TEACHERLY_CONGRATS.value)
    await ctx.send(f'/me Hurray for {message}! Compliments, cheers, and congratulations on your wonderful accomplishment! andrumHype andrumHeart andrumHype ')

async def focus(ctx: Message):
    message = get_message_content(ctx.content, CommandKeys.CMD_HAM_FOCUS.value)
    await ctx.send(f'/me {ctx.author.name} is requesting that {message} focus on the task at hand! Never give up!')
