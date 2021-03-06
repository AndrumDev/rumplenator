from bot.commands import bot_commands
from bot.commands.bot_commands import CommandKeys
from bot.commands.command_logic.pomo.pomo_command import warn_active_user
from bot.helpers.functions import get_message_command
from config import get_config
from twitchio.dataclasses import Message, Context
from twitchio.ext import commands


class Rumplenator(commands.Bot):

    # init

    def __init__(self):
        config = get_config()
        super().__init__(
            irc_token=config['irc_token'],
            client_id=config['client_id'],
            nick=config['bot_nick'],
            prefix=config['bot_prefix'],
            initial_channels=[config['channel']]
        )
        self.register_commands()


    async def event_ready(self):
        print(f'Ready | {self.nick}')
        await self._ws.send_privmsg(get_config().get('channel'), "/me has landed!")


    async def event_message(self, message: Message):
        await self.check_pom_state(message)
        await self.handle_commands(message)
     

    def register_commands(self):
        '''
        Registers all command names in the commands list with the generic run_command method.
        This is the equivalent of using the decorator
        @commands.command(name='dyson') on individual methods.
        '''
        run_command_method = getattr(self, 'run_command')
        command_list = [e.value for e in CommandKeys if e.name.startswith('CMD')]
        for command_name in command_list:
            self.add_command(commands.command(name=command_name)(run_command_method))


    async def run_command(self, ctx: Context):
        '''
        Generic run command method. Given a Message object, it looks up the command
        invoked and calls the corresponding method from the bot_commands module. 
        Throws and error if a method with the command name was not found.
        '''
        command_key = get_message_command(ctx.content)
        command_method = None
        try:
            command_method = getattr(bot_commands, command_key)
            await command_method(ctx)
        except AttributeError:
            raise NotImplementedError(f"Class `{bot_commands.__name__}` does not implement `{command_key}`.")

    
    async def check_pom_state(self, msg: Message):
        if get_message_command(msg.content) != CommandKeys.CMD_POMO.value:
            await warn_active_user(msg)
