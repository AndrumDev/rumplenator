from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT_SECONDS
from bot.helpers.functions import get_message_content, has_pomo_mod_flag
from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from config import get_config
from typing import Dict, List, Tuple, Optional, Iterable
from twitchio.dataclasses import Message, Context, User
import time
import asyncio

DEFAULT_NUM_SESSIONS = 1
MIN_WORK_MINUTES = 10
MIN_BREAK_MINUTES = 3
MAX_TOTAL_MINUTES = 300
MAX_TOPIC_LENGTH = 120

MOD_BYPASS_FLAG = '[pomo mod]'

__active_timers: Dict[str, PomoTimer] = {}


def get_active_pomo_timers() -> Iterable:
    '''
    this returns a view on the pomos dict: its values change when the underlying dict changes
    '''
    return __active_timers.values()


# public methods

async def handle_pomo(ctx: Message) -> None:
    args: List[str] = __get_message_args(ctx.content)
    username = ctx.author.name
    current_pomo = __active_timers.get(username)

    if len(args) == 0:
        if current_pomo:
            await __show_pomo_update(current_pomo, ctx)
        else:
            await __show_pomo_info(ctx)

        return

    if args[0] == 'cancel':
        if ctx.author.is_mod and len(args) >= 2 and args[1][0] == '@':
            target_user_name = args[1][1::]
            target_pomo = __active_timers.get(target_user_name)
            if not target_pomo:
                await ctx.channel.send(f'@{username}, {target_user_name} does not have an active pomo timer')
            else:
                __cancel_pomo(target_user_name, username)
        elif current_pomo:
            __cancel_pomo(username)
        else:
            await ctx.channel.send(f'@{username}, you do not have a running pomo session')

        return

    if args[0] == 'check':
        if current_pomo:
            await __show_pomo_update(current_pomo, ctx)
        else:
            await ctx.channel.send(f'@{username}, you do not have a running pomo session')

        return

    if args[0] == 'skip':
        if current_pomo:
            await current_pomo.skip()
        else:
            await ctx.channel.send(f'@{username}, you do not have a running pomo session')

        return

    if args[0] == 'mod':
        if current_pomo:
            current_pomo.mod_mode = not current_pomo.mod_mode
            status = 'on' if current_pomo.mod_mode else 'off'
            await ctx.channel.send(f'@{username}, mod mode is {status}')
        else:
            await ctx.channel.send(f'@{username}, you do not have a running pomo session')

        return

    if args[0].startswith('-') or args[0].startswith('+'):
        if current_pomo:
            operation = args[0][0]
            mins = args[0][1:]
            if not mins.isdigit():
                await ctx.channel.send(f"@{username}, that doesn't work")
                return
            if operation == '-':
                current_pomo.decrease_mins(int(mins))
            else:
                current_pomo.increase_mins(int(mins))
        else:
            await ctx.channel.send(f'@{username}, you do not have a running pomo session')

        return

    if not args[0].isdigit():
        await __show_pomo_info(ctx)
        return


    work_time, break_time, sessions, topic = __get_pom_args(args)

    if current_pomo:
        await ctx.channel.send(f'@{username} you already have a pomo running! Check your status with !pomo check, or use !pomo cancel to stop')
        return

    invalid_work_time = work_time < MIN_WORK_MINUTES
    invalid_break_time = break_time is not None and break_time < MIN_BREAK_MINUTES
    invalid_total_time = ((work_time + break_time) if break_time is not None else work_time) * sessions > MAX_TOTAL_MINUTES
    invalid_topic_length = len(topic) > MAX_TOPIC_LENGTH
    if invalid_work_time or invalid_break_time or invalid_total_time:
        await ctx.channel.send(f"@{username}, oops! Please note min work is {MIN_WORK_MINUTES}, min break is {MIN_BREAK_MINUTES}, and max total minutes is {MAX_TOTAL_MINUTES}")
        return
    if invalid_topic_length:
        await ctx.channel.send(f"sorry, @{username}! Max topic length is {MAX_TOPIC_LENGTH} characters, yours was {len(topic)}")
        return 

    def on_complete():
        del __active_timers[username]
    
    async def notify_user(username: str, message: str):
        time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
        await ctx.channel.send(f'@{username}, {message}')

    pomo_timer = PomoTimer(
        user=ctx.author,
        work_minutes=work_time,
        break_minutes=break_time,
        sessions=sessions,
        topic=topic,
        on_pomo_complete=on_complete,
        notify_user=notify_user
    )

    __active_timers[username] = pomo_timer

    asyncio.create_task(pomo_timer.begin())


async def check_pomo_state(msg: Message) -> None:
    pomo = __active_timers.get(msg.author.name)
    if pomo and pomo.state == PomoState.WORK and not __has_mod_bypass(msg, pomo):
        if pomo.minutes_remaining > 1:
            await msg.channel.send(f"@{msg.author.name}, stay focussed! Only {pomo.minutes_remaining} minutes left. You got this!")
        else:
            await msg.channel.send(f"@{msg.author.name} your work session is ALMOST complete! sit tight!")
 

def __has_mod_bypass(msg: Message, pomo: PomoTimer):
    return (msg.author.is_mod and has_pomo_mod_flag(msg)) or pomo.mod_mode
    

async def __show_pomo_info(ctx: Message, message='') -> None:
    message = f"@{ctx.author.name} want to start your own pomo? Type !pomo [number] to set a single timer. The full argument list is !pomo [work mins] [break mins] [num sessions] [topic]. E.g. !pomo 25 5 4 Essay. Use [!pomo cancel] to cancel your sessions, and [!pomo check] to check your time. Good luck!!"
    await ctx.channel.send(message)


async def __show_pomo_update(pomo: PomoTimer, ctx: Message) -> None:
    if pomo.state == PomoState.WORK:
        await ctx.channel.send(f'@{pomo.username}, you have {__get_mins_remaining_string(pomo)} left on your work session. You got this!')
    elif pomo.state == PomoState.BREAK:
        await ctx.channel.send(f'@{pomo.username}, you still have {__get_mins_remaining_string(pomo)} left on your break. Prepare yourself')


def __get_mins_remaining_string(pomo: PomoTimer) -> str:
    if pomo.minutes_remaining > 1:
        return f'{pomo.minutes_remaining} minutes'
    elif pomo.minutes_remaining == 1:
        return f'{pomo.minutes_remaining} minute'
    else:
        return 'under a minute'


def __cancel_pomo(username: str, cancelled_by: str = '') -> None:
    if __active_timers[username]:
        __active_timers[username].cancel(cancelled_by)


def __get_message_args(message: str) -> List[str]:
    m = get_message_content(message, 'pomo')
    args = m.split()
    return args


def __get_pom_args(args: List[str]) -> Tuple[int, Optional[int], int, str]:
    topic_idx = -1
    for idx, val in enumerate(args):
        if not val.isdigit():
            topic_idx = idx
            break

        if idx > 2:
            topic_idx = idx
            break

    has_topic = topic_idx != -1
    pom_times = args[:topic_idx] if has_topic else args

    work_time = int(pom_times[0])
    break_time = int(pom_times[1]) if len(pom_times) > 1 else None
    sessions = int(pom_times[2]) if len(pom_times) > 2 else DEFAULT_NUM_SESSIONS
    topic = ' '.join([str(n) for n in args[topic_idx:]]) if has_topic else ''

    return work_time, break_time, sessions, topic

#