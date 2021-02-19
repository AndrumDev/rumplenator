from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT_SECONDS
from bot.helpers.functions import get_message_content
from typing import Dict, List, Tuple
from twitchio.dataclasses import Message
import threading
import time
import asyncio
import enum


DEFAULT_BREAK_TIME_MINS = 0
DEFAULT_NUM_SESSIONS = 1

MIN_WORK_MINUTES = 10
MIN_BREAK_MINUTES = 3
MAX_TOTAL_MINUTES = 300

#####


class PomoState(enum.Enum):
    WORK = 0
    BREAK = 1


class PomoTimerThread (threading.Thread):

    username: str
    work_minutes: int
    break_minutes: int
    minutes_remaining: int
    total_sessions: int
    sessions_remaining: int
    topic: str

    state: PomoState = PomoState.WORK

    __cancelled: bool = False
    __cancelled_by: str = None

    @property
    def sessions_done(self):
        return self.total_sessions - self.sessions_remaining

    def __init__(self, username: str, work_minutes: int, break_minutes: int, sessions: int, topic: str, on_complete, notify_user):
        threading.Thread.__init__(self)

        self.name = username
        self.username = username

        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.total_sessions = sessions
        self.sessions_remaining = sessions
        self.topic = topic

        self.__on_complete = on_complete
        self.__notify_user = notify_user

    def run(self):
        asyncio.run(self.__start_pomo())
        self.__on_complete()

    def cancel(self, username=''):
        if username != '':
            self.__cancelled_by = username

        self.__cancelled = True

    async def __start_pomo(self):

        while(self.sessions_remaining and not self.__cancelled):
            work_start_message = self.__get_work_start_text()

            await self.__notify_user(self.username, work_start_message)
            await self.__start_countdown(PomoState.WORK)
            self.sessions_remaining -= 1

            only_one_break = self.total_sessions == 1 and self.break_minutes != 0
            several_sessions_left = self.total_sessions > 1 and self.sessions_remaining > 0

            if((only_one_break or several_sessions_left) and not self.__cancelled):
                break_start_message = self.__get_break_start_text()
                await self.__notify_user(self.username, break_start_message)
                await self.__start_countdown(PomoState.BREAK)

        if(self.__cancelled):
            if self.__cancelled_by:
                await self.__notify_user(self.username, f"Your pomo session has been cancelled by {self.__cancelled_by}")
            else:
                await self.__notify_user(self.username, "Your pomo session has been cancelled")
        else:
            await self.__notify_user(self.username, "Your pomodoro sessions have finished, well done!")

    async def __start_countdown(self, state: PomoState):
        self.state = state
        self.minutes_remaining = self.work_minutes if self.state == PomoState.WORK else self.break_minutes
        seconds = self.minutes_remaining * 60
        while seconds and not self.__cancelled:
            time.sleep(1)
            seconds -= 1
            self.minutes_remaining = (seconds // 60) + 1

    def __get_work_start_text(self):
        if self.total_sessions == 1:
            if self.topic != '':
                return f"starting work session on {self.topic} for {self.work_minutes} minutes. Good luck!"
            else:
                return f"starting work session for {self.work_minutes} minutes. Good luck!"
        else:
            if self.topic != '':
                if self.sessions_done == 0:
                    return f"starting work session {self.sessions_done + 1} of {self.total_sessions} on {self.topic} for {self.work_minutes} minutes. Good luck!"
                else:
                    return f"breaktime is over! Starting work session {self.sessions_done + 1} of {self.total_sessions} on {self.topic} for {self.work_minutes} minutes. Good luck!"
            else:
                if self.sessions_done == 0:
                    return f"starting work session {self.sessions_done + 1} of {self.total_sessions} for {self.work_minutes} minutes. Good luck!"
                else:
                    return f"breaktime is over! Starting work session {self.sessions_done + 1} of {self.total_sessions} for {self.work_minutes} minutes. Good luck!"

    def __get_break_start_text(self):
        if self.total_sessions == 1:
            return f"work session is complete! Enjoy your {self.break_minutes} minute break!"
        else:
            return f"work session {self.sessions_done} is complete! Enjoy your {self.break_minutes} minute break!"
#####


__active_timers: Dict[str, PomoTimerThread] = {}

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

    async def notify_user(username: str, message: str):
        time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
        await ctx.channel.send(f'@{username}, {message}')

    timerThread = PomoTimerThread(
        username=username,
        work_minutes=work_time,
        break_minutes=break_time,
        sessions=sessions,
        topic=topic,
        on_complete=on_complete,
        notify_user=notify_user
    )

    __active_timers[username] = timerThread
    timerThread.start()


async def check_active_user(ctx: Message) -> None:
    pom_timer = __active_timers.get(ctx.author.name)
    if pom_timer and pom_timer.state == PomoState.WORK and pom_timer.minutes_remaining:
        await ctx.channel.send(f"@{ctx.author.name}, stay focussed! Only {pom_timer.minutes_remaining} minutes left. You got this!")

#

# private methods


async def __show_pomo_info(ctx: Message, message='') -> None:
    message = "Want to start your own pomodoro timer? Type !pomo[number] to set a personalised timer(mins). The full argument list is !pomo [work mins] [break mins] [# pomo sessions] [project name]. E.g. !pomo 25 5 4 Essay. Use [!pomo cancel] to cancel your sessions. Good luck!!"
    await ctx.channel.send(message)


async def __show_pomo_update(pomo: PomoTimerThread, ctx: Message) -> None:
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