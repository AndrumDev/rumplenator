from bot.commands.command_logic.dyson import get_dyson_message
from bot.commands.command_logic.tom2 import get_tom2_message
from bot.commands.command_logic.pomo.pomo_command import handle_pomo
from bot.commands.command_logic.simp import get_simp_quote
from bot.commands.command_logic.pun import fetch_pun
from bot.commands.command_logic.bagel import get_bagel_message
from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT_SECONDS
from bot.helpers.functions import get_message_content
from config import get_config
from twitchio.dataclasses import Context
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
    CMD_UNDEFINED_LMGTFY = 'lmgtfy'
    CMD_FLIP_FLIP = 'flip'
    CMD_FLIP_WHIP = 'whip'
    CMD_GRANT_SKWIRL = 'mrskwirl'
    CMD_MCLOVIN_MCLOVIN = 'mclovin'
    CMD_MABLE_SLEEPY = 'sleepy'
    CMD_MABLE_BOOP = 'boop'
    CMD_MABLE_COINTOSS = 'cointoss'
    CMD_FABE_BAN = 'ban'
    CMD_FLAWER_PAT = 'pat'
    CMD_FLAWER_TUCK = 'tuck'
    CMD_SKY_DROPKICK = 'dropkick'
    CMD_SKP_DROPKISS = 'dropkiss'
    CMD_TEACHERLY_CONGRATS = 'congrats'
    CMD_KARANT_VIBE = 'vibe'
    CMD_HAM_FOCUS = 'focus'
    CMD_TIME_LURKY = 'lurky'
    CMD_DUCKIE_TWIN = 'duckietwin'
    CMD_HUTCH_HUTCH = 'hutch'
    CMD_HAMLIN_TEAZE = 'teaze'
    CMD_FABE_PUN = 'pun'
    CMD_STEVIE_BRB = 'brb'
    CMD_BIK_RELAX = 'relax'
    CMD_SPHYNX_WELCOMEJK = 'welcomejk'
    CMD_LENNY_HELLO = 'hello'
    CMD_EVEREST_EVEREST = 'everest'
    CMD_SPHYNX_PAP = 'pap'
    CMD_UNWAZ_SIGH = 'sigh'
    CMD_JED_SMILEJAY = 'smilejay'
    CMD_KP_FLUG = 'flug'
    CMD_LENNY_JOKE = 'joke'
    CMD_KIRBY_KIRBY = 'kirby'
    CMD_GAIA_GAIA = 'gaia'
    CMD_SUMO_BAGEL = 'bagel'
    CMD_SOKURI_FORCE = 'force'
    CMD_EGG_DAY = 'day'
    CMD_SAKO_BREAK = 'breaktime' 
    CMD_FLIP_GODKINGMABL = 'godkingmable'
    CMD_STEVIE_HI = 'hi'
    CMD_LENNY_SOKUWORK = 'sokuwork'
    CMD_VAN_VAN = 'van'
    CMD_FLIP_WAKEY = 'wakey'


### Channel commands ###


async def kill(ctx: Context):
    await ctx.send('I cannot be killed™'.encode("utf-8").decode("utf-8"))

async def bot_love(ctx: Context):
    await ctx.send(f'aaawh thank you {ctx.author.name} andrumHeart If I was sentient I would love you too! xxx')

async def raid(ctx: Context):
    await ctx.send(' Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype')

async def ssimp(ctx: Context):
    await ctx.send('does she speak? notice me. u r beetiful asian quenn. can i wife u? oh you have a bf? im out.')

async def simp(ctx: Context):
    message = await get_simp_quote()
    await ctx.send(message)

async def wowie(ctx: Context):
    await ctx.send('Thats awesome! But ur not just awesome, ur WOWIE! andrumHeart ')

async def hype(ctx: Context):
    await ctx.send('andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype')

async def pomo(ctx: Context):
    await handle_pomo(ctx)


### Redemption commands ###


async def onlyfans(ctx: Context):
    message = get_dyson_message('fan')
    await ctx.send('FANS YOU SAY?')
    time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
    await ctx.send(message)

async def dyson(ctx: Context):
    message = get_dyson_message()
    await ctx.send(message)

async def tom2(ctx: Context):
    bf_message, wtf_message = get_tom2_message()
    await ctx.send(bf_message)
    time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
    await ctx.send(wtf_message)

async def giveup(ctx: Context):
    await ctx.send('NEVER GIVE UP https://www.youtube.com/watch?v=tYzMYcUty6s&ab_channel=MetalGearFro')

async def flip(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLIP_FLIP.value)
    if "!" not in message:
        await ctx.send(f'{message[::-1]}')
    else:
        await ctx.send('are you tryna do something sneaky..?')

async def mrskwirl(ctx: Context):
    await ctx.send('Every Skwirl needs its NUT :peanuts:')

async def mclovin(ctx: Context):
    await ctx.send('According to Urban Dictionary Colored McLovin is the cutest E-girl known to man. His uwus have created peace in times of turmoil, and his gamer girl bath water quenched the thirst of people without clean water. McLovin truly is the queen of all.')

async def sleepy(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_MABLE_SLEEPY.value)
    await ctx.send(message + ' is so so so sleeeepppyyyy!!!!')

async def cointoss(ctx: Context):
    flip = randint(0, 1)
    if (flip == 0):
        await ctx.send("Heads")
    else:
        await ctx.send("Tails")

async def pat(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLAWER_PAT.value)
    await ctx.send(f'/me gentle pats on {message}\'s head. well done! you\'re doin great my friend (ｏ・・)ノ”(ᴗ ᴗ。) <3 ')

async def dropkick(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_SKY_DROPKICK.value)
    await ctx.send(f'/me {message} has been dropkicked by {ctx.author.name} and sent into the abyss never to be loved again (•̀ᴗ•́ )و')

async def dropkiss(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_SKP_DROPKISS.value)
    await ctx.send(f'/me {ctx.author.name} has dropkissed {message} (on the cheeks cuz we are PG) and now {message} is not alone in this vast abyss (ᵔᴥᵔ)')

async def boop(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_MABLE_BOOP.value)
    if "rumplenator" in message:
        await ctx.send('/me I got booped ☆ヾ(￣ω ￣｡)ノ')
    else:
        await ctx.send(f'/me {message} got booped ☆ヾ(￣ω ￣｡)ノ')

async def tuck(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLAWER_TUCK.value)
    if message == '':
        return()
    else:
        await ctx.send(f"/me it\'s {message}\'s bedtime! get comfy in bed and have sweet dreams my friend! thanks for being here, we\'ll miss you! (︶｡︶✽)zzz")

async def whip(ctx: Context):
    await ctx.send(f'/me *cracks whip* BACK TO WORK!')

async def vibe(ctx: Context):
    await ctx.send(f'/me We vibin\'! andrumHype andrumSmug blobDance We vibin\'! andrumHype andrumSmug blobDance We vibin\'! andrumHype andrumSmug blobDance ')

async def congrats(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_TEACHERLY_CONGRATS.value)
    await ctx.send(f'/me Hurray for {message}! Compliments, cheers, and congratulations on your wonderful accomplishment! andrumHype andrumHeart andrumHype ')

async def focus(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_HAM_FOCUS.value)
    if message == '':
        await ctx.send(f'/me {ctx.author.name} is requesting that Rumple focus on the task at hand! Never give up!')
    else: 
        await ctx.send(f'/me {ctx.author.name} is requesting that {message} focus on the task at hand! Never give up!')

async def lurky(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_TIME_LURKY.value)
    await ctx.send(f'/me if you aint lurking ~(˘▾˘~) you aint working (~˘▾˘)~')

duckietwin_counter = 0 
async def duckietwin(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_DUCKIE_TWIN.value)
    duckietwin_counter += 1
    await ctx.send(f'/me Rumpy and Duckie have been the same person {duckietwin_counter} times!（ ＾○＾）人（＾○＾ ）')

async def lmgtfy(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_UNDEFINED_LMGTFY.value)
    message = message.split(" ")
    username = "".join([name for name in message if "@" in name])
    search_term = "+".join([words for words in message if "@" not in words])
    await ctx.send(f'Here you go {username}: https://letmegooglethat.com/?q={search_term}')

async def ban(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_FABE_BAN.value)
    await ctx.send(f'/me {ctx.author.name} tried to banish {message} with the ban hammer! But {message} dodges ε=ε=ε=ε=┏( ￣▽￣)┛ hehe')

async def hutch(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_HUTCH_HUTCH.value)
    await ctx.send(f'/me The resident best D.Va player who got an epic team kill on OW, is an elder of the stream, and an overall legend KEKW' )

async def teaze(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_HAMLIN_TEAZE.value)
    word = str.capitalize(message)
    await ctx.send(f'/me And{word}teazer')

async def pun(ctx: Context):
    pun_text = fetch_pun(get_config().get('pun_url'))
    await ctx.send(f'/me {pun_text}')

async def brb(ctx: Context):
    if ctx.author.name == 'andrumpleteazer':
        await ctx.send(f'/Rumple will be right back! Yakky will watch over you while she\'s gone. Best behaviour now everyone... andrumSmug')
    else:
        await ctx.send(f'/Okiedokie {ctx.author.name}, catch you later! We\'ll miss you in the meantime~ andrumHeart')

async def relax(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_BIK_RELAX.value)
    await ctx.send(f'/me {ctx.author.name} has finished their work and is here to relax and chill~ goodluck to everyone else!')

async def welcomejk(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_SPHYNX_WELCOMEJK.value)
    await ctx.send(f'/me Welcome {message} to the Co-Procrastinating Stream. Where we attempt to... Wait... What was I supposed to be doing?')

async def hello(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_LENNY_HELLO.value)
    if message == '':
        await ctx.send(f'/me Well, hello there you magnificent people! Hope you are having a good day and getting your work done! Pls eat well, drink water and be mind-full! andrumHeart ')
    else:
        await ctx.send(f'/me Well, hello there you {message}! Hope you are having a good day and getting your work done! Pls eat well, drink water and be mind-full! andrumHeart ')
   
async def everest(ctx: Context):
    await ctx.send(f'/me Everest gives a hug to everyone in the chat and requests all to hug him back. andrumHeart ' )

async def pap(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_SPHYNX_PAP.value)
    await ctx.send(f'/me No... just no... stop! Go. Away. Please... andrumNotLikeThis ' ) 

async def sigh(ctx: Context):
    await ctx.send(f'/me (* ´ Д｀)=з   ( ￣_￣)    (ᇂ_ᇂ|||)    (;¬_¬)' ) 

async def smilejay(ctx: Context):
    await ctx.send(f'/me Hey Jay! andrumHeart Just a reminder: You so precious when you S-M-I-L-E andrumSmug' )

async def flug(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_KP_FLUG.value)
    await ctx.send(f'/me hwy {message} ley ne hokd ypu tiggt tught tighy, I gorchu my frwn uwy')

async def joke(ctx: Context):
    await ctx.send(f'/me Why did the chicken cross the Moebius strip?........To get to the same side!')

async def kirby(ctx: Context):
    await ctx.send(f'/me I like when you call me Kirbs andrumAw')

async def gaia(ctx: Context):
    await ctx.send(f'/me Gaia needs to focus!')

async def bagel(ctx: Context):
    message = get_bagel_message()
    await ctx.send(message)

async def force(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_SOKURI_FORCE.value)
    await ctx.send(f'/me {message} WITH SUCH FORCE! andrumLetsGo ')

async def day(ctx: Context):
    await ctx.send(f'/me it\'s like Wednesday or something... andrumOO ')

async def breaktime(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_SAKO_BREAK.value)
    await ctx.send(f'/me Why not do something nice for yourself today {message}? Find some quiet, sit in stillness, breathe. Put your problems on pause. You deserve a break andrumCosy ')

async def godkingmable(ctx: Context):
    await ctx.send(f'/me TwitchLit A Cosmic Entity. They were here for the beginning of time... and will be there for the end... TwitchLit ')

async def hi(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_STEVIE_HI.value)
    await ctx.send(f'Hi {message}, I\'m {ctx.author.name}, nice to meet you andrumWave !')

async def sokuwork(ctx: Context):
    await ctx.send(f'/me @sokuri_ is going to "work".... he is working hard.....or hardly working? We\'ll never know! But good luck andrumFlawer ')


async def van(ctx: Context):
    await ctx.send(f'/me duckPls beepbeep duckPls')

async def wakey(ctx: Context):
    message = get_message_content(ctx.content, CommandKeys.CMD_FLIP_WAKEY.value)
    await ctx.send(f'/me andrumFlawer The Pandamonium gives positive vibes to {message} to help them out of their weary state! andrumFlawer ')