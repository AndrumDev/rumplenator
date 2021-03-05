from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT_SECONDS
from bot.helpers.functions import get_message_content
from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from config import get_config
from typing import Dict, List, Tuple
from twitchio.dataclasses import Message
import time

DEFAULT_BREAK_TIME_MINS = 0
DEFAULT_NUM_SESSIONS = 1

MIN_WORK_MINUTES = 10
MIN_BREAK_MINUTES = 3
MAX_TOTAL_MINUTES = 300

__active_timers: Dict[str, PomoTimer] = {}


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

    if not args[0].isdigit():
        await __show_pomo_info(ctx)
        return

    work_time, break_time, sessions, topic = __get_pom_args(args)

    if work_time < MIN_WORK_MINUTES or (break_time != 0 and break_time < MIN_BREAK_MINUTES) or (work_time + break_time) * sessions > MAX_TOTAL_MINUTES:
        await ctx.channel.send(f"@{username}, oops! Please note min work is {MIN_WORK_MINUTES}, min break is {MIN_BREAK_MINUTES}, and max total minutes is {MAX_TOTAL_MINUTES}")
        return

    def on_complete():
        del __active_timers[username]
        # TODO tabi update pomo file here

    async def notify_user(username: str, message: str):
        time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
        await ctx.channel.send(f'@{username}, {message}')

    pomo_timer = PomoTimer(
        username=username,
        work_minutes=work_time,
        break_minutes=break_time,
        sessions=sessions,
        topic=topic,
        on_pomo_complete=on_complete,
        notify_user=notify_user
    )

    __active_timers[username] = pomo_timer

    # TODO tabi update pomo file here
    pomo_timer.begin()


async def warn_active_user(ctx: Message) -> None:
    pom_timer = __active_timers.get(ctx.author.name)
    if pom_timer and pom_timer.state == PomoState.WORK and pom_timer.minutes_remaining:
        await ctx.channel.send(f"@{ctx.author.name}, stay focussed! Only {pom_timer.minutes_remaining} minutes left. You got this!")

#

# private methods


async def __show_pomo_info(ctx: Message, message='') -> None:
    message = "Want to start your own pomodoro timer? Type !pomo[number] to set a personalised timer(mins). The full argument list is !pomo [work mins] [break mins] [# pomo sessions] [project name]. E.g. !pomo 25 5 4 Essay. Use [!pomo cancel] to cancel your sessions, and [!pomo check] to check your time. Good luck!!"
    await ctx.channel.send(message)


async def __show_pomo_update(pomo: PomoTimer, ctx: Message) -> None:
    if pomo.state == PomoState.WORK:
        await ctx.channel.send(f'@{pomo.username}, you have {pomo.minutes_remaining} minutes left on your work session. You got this!')
    else:
        await ctx.channel.send(f'@{pomo.username}, you still have {pomo.minutes_remaining} minutes left on your break. Prepare yourself')


def __cancel_pomo(username: str, cancelled_by: str = '') -> None:
    if __active_timers[username]:
        __active_timers[username].cancel(cancelled_by)


def __get_message_args(message: str) -> List[str]:
    m = get_message_content(message, 'pomo')
    args = m.split()
    return args


def __get_pom_args(args: List[str]) -> Tuple[int, int, int, str]:
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
    break_time = int(pom_times[1]) if len(pom_times) > 1 else DEFAULT_BREAK_TIME_MINS
    sessions = int(pom_times[2]) if len(pom_times) > 2 else DEFAULT_NUM_SESSIONS
    topic = ' '.join([str(n) for n in args[topic_idx:]]) if has_topic else ''

    return work_time, break_time, sessions, topic

#