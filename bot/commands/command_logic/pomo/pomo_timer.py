from config import get_config
from threading import Event, Thread, current_thread
from typing import Callable
from pathlib import Path
from typing import Callable, Optional
from datetime import datetime, timezone, timedelta
from twitchio.dataclasses import User
import enum
import asyncio
import time
import math
import logging


class PomoState(enum.Enum):
    WORK = 'work'
    BREAK = 'break'
    CANCELLED = 'cancelled'
    COMPLETE = 'complete'


class PomoTimerError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PomoTimer():

    def __init__(self, user: User, work_minutes: int, break_minutes: Optional[int], sessions: int, topic: str, on_pomo_complete: Callable, notify_user: Callable, on_countdown_start: Callable):
        self.user: str = User
        self.username: str = user.name

        self.work_minutes: int = work_minutes
        self.break_minutes: Optional[int] = break_minutes
        self.total_sessions: int = sessions
        self.sessions_remaining: int = sessions
        self.topic: str = topic
        self.state: PomoState = None
        self.start_time: datetime = None
        
        self.__countdown_cancelled_event: Event = None
        self.__countdown_started_time: datetime = None
        self.__cancelled_by: str = None
        self.__on_pomo_complete: Callable = on_pomo_complete
        self.__on_countdown_start: Callable = on_countdown_start
        self.__notify_user: Callable = notify_user


    @property
    def minutes_remaining(self) -> int:
        '''
        Returns the minutes remaining in the current work or break timer
        '''
        if self.state == PomoState.WORK:
            return self.__calculate_remaining_minutes(self.__countdown_started_time, self.work_minutes)
        if self.state == PomoState.BREAK:
            return self.__calculate_remaining_minutes(self.__countdown_started_time, self.break_minutes)

    @property
    def sessions_done(self) -> int:
        return self.total_sessions - self.sessions_remaining


    async def begin(self):
        logging.info(f'{current_thread()}: beginning pomo for {self.username}')

        self.start_time = datetime.now(timezone.utc)
        self.state = PomoState.WORK
        await self.__start_countdown()
        

    def cancel(self, username=''):
        if username != '':
            self.__cancelled_by = username

        # setting this event interrupts the countdown timer thread
        self.__countdown_cancelled_event.set()


    async def __start_countdown(self):
        '''
        Starts a single countdown in a new thread. A countdown can be one work or break session. The thread waits until the countdown is over, 
        and then invokes a callback function. An Event object is used to share state between the timer thread and the main thread.
        By calling event.set() from the main thread, the timer can be cancelled.
        '''
        logging.info(f'{current_thread()}: creating new thread for {self.state} countdown for {self.username}')

        start_message = None
        countdown_minutes = None
        event_loop = asyncio.get_running_loop()

        if self.state == PomoState.WORK:
            start_message = self.__get_work_start_text()
            countdown_minutes = self.work_minutes
        elif self.state == PomoState.BREAK:
            start_message = self.__get_break_start_text()
            countdown_minutes = self.break_minutes
        else:
            raise PomoTimerError(f"Cannot start countdown, PomoTimer is invalid state (state = {self.state})")
        
        await self.__notify_user(self.username, start_message)
        self.__on_countdown_start()

        # https://docs.python.org/3/library/threading.html#threading.Event
        self.__countdown_cancelled_event = Event()
        self.__countdown_started_time = datetime.now(timezone.utc)
        Thread(
            target=PomoTimer.__countdown,
            args=(self.__countdown_cancelled_event, countdown_minutes, event_loop),
            kwargs={
                'on_complete': self.__on_countdown_complete,
                'on_cancel': self.__on_countdown_cancelled
            },
            daemon=True
        ).start()


    async def __on_countdown_complete(self):
        '''
        Handler called at the end of every countdown (i.e. when an individual work or break session is over)
        '''
        logging.info(f'{current_thread()}: countdown complete for user {self.username}')

        # the session boundary is after the BREAK countdown, unless there is only one work session
        # in which case there is no break, and the pomo completes
        if self.state == PomoState.BREAK or self.total_sessions == 1:
            self.sessions_remaining -= 1

        if self.sessions_remaining > 0:
            self.state = PomoState.BREAK if self.state == PomoState.WORK else PomoState.WORK
            await self.__start_countdown()
        else:
            self.state = PomoState.COMPLETE
            await self.__notify_user(self.username, "your pomodoro sessions have finished, well done!")
            self.__on_pomo_complete()


    async def __on_countdown_cancelled(self):
        '''
        Handler called when a user or mod cancels the countdown with !pomo cancel
        '''
        logging.info(f'{current_thread()}: countdown cancelled for user {self.username}')

        self.state = PomoState.CANCELLED
        if self.__cancelled_by:
            await self.__notify_user(self.username, f"your pomo session has been cancelled by {self.__cancelled_by}")
        else:
            await self.__notify_user(self.username, "your pomo session has been cancelled")

        self.__on_pomo_complete()


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
            return f"work session {self.sessions_done + 1} of {self.total_sessions} is complete! Enjoy your {self.break_minutes} minute break!"


    def __calculate_remaining_minutes(self, time_started, total_minutes):
        end_time = time_started + timedelta(minutes = total_minutes)
        return round((end_time - datetime.now(timezone.utc)).total_seconds() / 60)


    @staticmethod
    def __countdown(event: Event, timeout: int, event_loop, on_complete: Callable = None, on_cancel: Callable = None):
        '''
        Timer method which is run on a separate thread
        '''
        logging.info(f'{current_thread()}: counting down {timeout} minutes')
        timeout_seconds = timeout * 60

        # blocking call
        cancelled = event.wait(timeout=timeout_seconds)
        # run the callbacks on the main thread
        if not cancelled:
            asyncio.run_coroutine_threadsafe(on_complete(), event_loop)
        else:
            asyncio.run_coroutine_threadsafe(on_cancel(), event_loop)


    def set_countdown_started(self, started_time: datetime):
        '''
        Allow private variable __countdown_started_time to be modified by unit tests
        '''
        self.__countdown_started_time = started_time

#####
