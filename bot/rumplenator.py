from twitchio.dataclasses import Message
from bot.commands.redemptions import RedemptionCommands
from bot.commands.channel import ChannelCommands
from twitchio.ext import commands
import os


class Rumplenator(commands.Bot):

    # init

    def __init__(self):
        super().__init__(
            irc_token=os.environ['TMI_TOKEN'],
            client_id=os.environ['CLIENT_ID'],
            nick=os.environ['BOT_NICK'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=[os.environ['CHANNEL']]
        )

    #

    # events
    # events don't need decorators when subclassed

    async def event_ready(self):
        print(f'Ready | {self.nick}')
        await self._ws.send_privmsg(os.environ['CHANNEL'], "/me has landed!")

    async def event_message(self, message: Message):
        print(message.content)
        await ChannelCommands.check_pom_state(message)
        await self.handle_commands(message)

    #

    # channel commands

    @commands.command(name=ChannelCommands.HI)
    async def hi(self, ctx: Message):
        await ChannelCommands.hi(ctx)

    @commands.command(name=ChannelCommands.KILL)
    async def kill(self, ctx: Message):
        await ChannelCommands.kill(ctx)

    @commands.command(name=ChannelCommands.BOT_LOVE)
    async def bot_love(self, ctx: Message):
        await ChannelCommands.bot_love(ctx)

    @commands.command(name=ChannelCommands.RAID)
    async def raid(self, ctx: Message):
        await ChannelCommands.raid(ctx)

    @commands.command(name=ChannelCommands.SSIMP)
    async def ssimp(self, ctx: Message):
        await ChannelCommands.ssimp(ctx)

    @commands.command(name=ChannelCommands.SIMP)
    async def simp(self, ctx: Message):
        await ChannelCommands.simp(ctx)

    @commands.command(name=ChannelCommands.WOWIE)
    async def wowie(self, ctx: Message):
        await ChannelCommands.wowie(ctx)

    @commands.command(name=ChannelCommands.HYPE)
    async def hype(self, ctx: Message):
        await ChannelCommands.hype(ctx)

    @commands.command(name=ChannelCommands.POMO)
    async def pomo(self, ctx: Message):
        await ChannelCommands.pomo(ctx)

    #

    # redemption commands

    @commands.command(name=RedemptionCommands.UNDEFINED_DYSON)
    async def dyson(self, ctx: Message):
        await RedemptionCommands.dyson(ctx)

    @commands.command(name=RedemptionCommands.UNDEFINED_ONLYFANS)
    async def onlyfans(self, ctx: Message):
        await RedemptionCommands.onlyfans(ctx)

    @commands.command(name=RedemptionCommands.FLIP_FLIP)
    async def flip(self, ctx: Message):
        await RedemptionCommands.flip(ctx)

    @commands.command(name=RedemptionCommands.GRANT_SKWIRL)
    async def mrskwirl(self, ctx: Message):
        await RedemptionCommands.mrskwirl(ctx)

    @commands.command(name=RedemptionCommands.MCLOVIN_MCLOVIN)
    async def mclovinscommand(self, ctx: Message):
        await RedemptionCommands.mclovin(ctx)

    @commands.command(name=RedemptionCommands.UNDEFINED_TOM)
    async def tom2(self, ctx: Message):
        await RedemptionCommands.tom2(ctx)

    @commands.command(name=RedemptionCommands.UNDEFINED_GIVE_UP)
    async def giveup(self, ctx: Message):
        await RedemptionCommands.giveup(ctx)

    @commands.command(name=RedemptionCommands.MABLE_SLEEPY)
    async def sleepy(self, ctx: Message):
        await RedemptionCommands.sleepy(ctx)

    @commands.command(name=RedemptionCommands.FLAWER_PAT)
    async def pat(self, ctx: Message):
        await RedemptionCommands.pat(ctx)

    @commands.command(name=RedemptionCommands.SKY_DROPKICK)
    async def dropkick(self, ctx: Message):
        await RedemptionCommands.dropkick(ctx)

    @commands.command(name=RedemptionCommands.SKP_DROPKISS)
    async def dropkiss(self, ctx: Message):
        await RedemptionCommands.dropkiss(ctx)

    @commands.command(name=RedemptionCommands.MABLE_COINTOSS)
    async def cointoss(self, ctx: Message):
        await RedemptionCommands.cointoss(ctx)

    #
