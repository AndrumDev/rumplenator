from bot.helpers.constants import MULTI_MESSAGE_TIMEOUT_SECONDS
from bot.helpers.functions import get_message_content
from os import stat
from typing import Dict, List, Literal
from twitchio.dataclasses import Message
import threading
import time
import asyncio

MIN_WORK_MINUTES = 10
MIN_BREAK_MINUTES = 3

MAX_TOTAL_MINUTES = 300

#####


class PomoTimerThread (threading.Thread):

    username: str
    work_minutes: int
    break_minutes: int
    minutes_remaining: int
    total_sessions: int
    sessions_remaining: int
    topic: str

    state: Literal['break', 'work'] = 'work'

    __ctx: Message
    __cancelled = False

    @property
    def sessions_done(self):
        return self.total_sessions - self.sessions_remaining

    def __init__(self, username: str, ctx: Message, work_minutes: int, break_minutes: int, sessions: int, topic: str, on_complete):
        threading.Thread.__init__(self)

        self.__ctx = ctx
        self.name = username
        self.username = username

        self.work_minutes = work_minutes
        self.break_minutes = break_minutes
        self.total_sessions = sessions
        self.sessions_remaining = sessions
        self.topic = topic
        self.__on_complete = on_complete

    def run(self):
        asyncio.run(self.__start_pomo())
        self.__on_complete()

    def cancel(self):
        self.__cancelled = True

    async def __start_pomo(self):

        while(self.sessions_remaining and not self.__cancelled):
            work_start_message = self.__get_work_start_text()

            await self.__notify_user(work_start_message)
            await self.__start_countdown('work')
            self.sessions_remaining -= 1

            only_one_break = self.total_sessions == 1 and self.break_minutes != 0
            several_sessions_left = self.total_sessions > 1 and self.sessions_remaining > 0

            if((only_one_break or several_sessions_left) and not self.__cancelled):
                break_start_message = self.__get_break_start_text()
                await self.__notify_user(break_start_message)
                await self.__start_countdown('break')

        if(self.__cancelled):
            await self.__notify_user(f"pomo session cancelled")
        else:
            await self.__notify_user(f"Your pomodoro sessions have finished, well done!")

    async def __start_countdown(self, state: Literal['break', 'work'] = 'work'):
        self.state = state
        self.minutes_remaining = self.work_minutes if self.state == 'work' else self.break_minutes
        seconds = self.minutes_remaining * 60
        while seconds and not self.__cancelled:
            time.sleep(1)
            seconds -= 1
            self.minutes_remaining = (seconds // 60) + 1

    async def __notify_user(self, message: str):
        time.sleep(MULTI_MESSAGE_TIMEOUT_SECONDS)
        await self.__ctx.channel.send(f"@{self.username}, {message}")

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


__pomo_users: Dict[str, PomoTimerThread] = {}


async def handle_pomo(ctx: Message):
    args: List[str] = __get_message_args(ctx.content)
    username = ctx.author.name

    current_pomo = __pomo_users.get(username)

    if current_pomo:
        if len(args) and args[0] == 'cancel':
            __cancel_pomo(username)
        else:
            if current_pomo.state == 'work':
                await ctx.channel.send(f'@{username}, stay focussed! Only {current_pomo.minutes_remaining} minutes left. You got this!')
            else:
                await ctx.channel.send(f'@{username}, you still have {current_pomo.minutes_remaining} minutes left on your break. Prepare yourself')
        return

    if len(args) == 0:
        await __show_pomo_info(username, ctx)
        return

    if not args[0].isdigit():
        if args[0] == 'cancel':
            await ctx.channel.send(f'@{username}, you do not have a running pomo session')
        else:
            await __show_pomo_info(username, ctx)

        return

    work_time, break_time, sessions, topic = __get_pom_args(args)

    if work_time < MIN_WORK_MINUTES or (break_time != 0 and break_time < MIN_BREAK_MINUTES) or (work_time + break_time) * sessions > MAX_TOTAL_MINUTES:
        await ctx.channel.send(f"@{username}, oops! Please note min work is 10, min break is 3, and max total minutes is 300")

    def on_complete():
        del __pomo_users[username]

    timerThread = PomoTimerThread(
        username,
        ctx,
        work_time,
        break_time,
        sessions,
        topic,
        on_complete
    )
    __pomo_users[username] = timerThread
    timerThread.start()


async def check_active_user(ctx: Message):
    pom_timer = __pomo_users.get(ctx.author.name)
    if pom_timer and pom_timer.state == 'work' and pom_timer.minutes_remaining:
        await ctx.channel.send(f"@{ctx.author.name}, stay focussed! Only {pom_timer.minutes_remaining} minutes left. You got this!")


async def __show_pomo_info(username: str, ctx: Message, message=''):
    message = f"Want to start your own pomodoro timer? Type !pomo[number] to set a personalised timer(mins). The full argument list is !pomo [work mins] [break mins] [# pomo sessions] [project name]. E.g. !pomo 25 5 4 Essay. Use [!pomo cancel] to cancel your sessions. Good luck!!"
    await ctx.channel.send(message)


def __cancel_pomo(username: str):
    if __pomo_users[username]:
        __pomo_users[username].cancel()


def __get_message_args(message: str):
    m = get_message_content(message, 'pomo')
    args = m.split()
    return args


def __get_pom_args(args: List[str]):

    topic_idx = -1
    for idx, val in enumerate(args):
        if not val.isdigit():
            topic_idx = idx
            break

        if idx > 2:
            topic_idx = idx
            break

    break_time = 0
    sessions = 1
    topic = ''

    pom_times = args[:topic_idx] if topic_idx != -1 else args

    work_time = int(pom_times[0])

    if len(pom_times) >= 2:
        break_time = int(pom_times[1])

    if len(pom_times) >= 3:
        sessions = int(pom_times[2])

    if topic_idx != -1:
        topic = ' '.join([str(n) for n in args[topic_idx:]])

    return work_time, break_time, sessions, topic
