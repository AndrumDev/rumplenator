from .command_logic.pomo import check_active_user, handle_pomo
from .command_logic.simp import get_simp_quote
from random import randint
from twitchio.dataclasses import Message


class ChannelCommands():

    ### CONSTANTS ###

    HI = 'hi'
    KILL = 'kill'
    BOT_LOVE = 'botlove'
    RAID = 'raid'
    SSIMP = 'ssimp'
    SIMP = 'simp'
    WOWIE = 'wowie'
    HYPE = 'hype'
    POMO = 'pomo'

    CHANNEL_COMMAND_LIST = [
        HI,
        KILL,
        BOT_LOVE,
        RAID,
        SSIMP,
        SIMP,
        WOWIE,
        HYPE,
        POMO
    ]

    ###############

    ### FUNCTIONS ###

    async def hi(ctx: Message):
        await ctx.send(f'Hello {ctx.author.name}!')

    async def kill(ctx: Message):
        await ctx.send(f'I cannot be killed™'.encode("utf-8").decode("utf-8"))

    async def bot_love(ctx: Message):
        await ctx.send(f'aaawh thank you {ctx.author.name} andrumHeart If I was sentient I would love you too! xxx')

    async def raid(ctx: Message):
        await ctx.send(f' Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype Rumple Raid! andrumHeart andrumHype')

    async def ssimp(ctx: Message):
        await ctx.send(f'does she speak? notice me. u r beetiful asian quenn. can i wife u? oh you have a bf? im out.')

    async def simp(ctx: Message):
        message = await get_simp_quote()
        await ctx.send(message)

    async def wowie(ctx: Message):
        await ctx.send(f'Thats awesome! But ur not just awesome, ur WOWIE! andrumHeart ')

    async def hype(ctx: Message):
        await ctx.send(f'andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype andrumHype')

    async def pomo(ctx: Message):
        await handle_pomo(ctx)

    async def check_pom_state(ctx: Message):
        if not f"!{ChannelCommands.POMO}" in ctx.content:
            await check_active_user(ctx)

    #################
