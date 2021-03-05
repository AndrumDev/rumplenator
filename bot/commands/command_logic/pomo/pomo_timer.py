from threading import Event, Thread
from typing import Callable
import enum
import asyncio
import time


class PomoState(enum.Enum):
    WORK = 'work'
    BREAK = 'break'
    CANCELLED = 'cancelled'
    COMPLETE = 'complete'


class PomoTimerError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PomoTimer():

    def __init__(self, username: str, work_minutes: int, break_minutes: int, sessions: int, topic: str, on_pomo_complete: Callable, notify_user: Callable):
        self.name: str = username
        self.username: str = username

        self.work_minutes: int = work_minutes
        self.break_minutes: int = break_minutes
        self.total_sessions: int = sessions
        self.sessions_remaining: int = sessions
        self.topic: str = topic
        self.state: PomoState = None
        
        self.__countdown_cancelled_event: Event = None
        self.__cancelled_by: str = None
        self.__on_pomo_complete: Callable = on_pomo_complete
        self.__notify_user: Callable = notify_user


    @property
    def sessions_done(self):
        return self.total_sessions - self.sessions_remaining


    def begin(self):
        self.state = PomoState.WORK
        self.__start_countdown()
        

    def cancel(self, username=''):
        if username != '':
            self.__cancelled_by = username

        # setting this event interrupts the countdown timer thread
        self.__countdown_cancelled_event.set()


    def __start_countdown(self):
        '''
        Starts a single countdown. A countdown can be one work or break session. This method spawns a thread that waits until the countdown is over, 
        and then invokes a callback function. An Event object is used to share state between the timer thread and the main thread.
        By calling event.set() from the main thread, the timer can be cancelled.
        '''
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
        
        asyncio.create_task(self.__notify_user(self.username, start_message))

        # https://docs.python.org/3/library/threading.html#threading.Event
        self.__countdown_cancelled_event = Event()
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
        if self.state == PomoState.BREAK:
            self.sessions_remaining -= 1

        if self.sessions_remaining > 0:
            self.state = PomoState.BREAK if self.state == PomoState.WORK else PomoState.WORK
            self.__start_countdown()
        else:
            self.state = PomoState.COMPLETE
            await self.__notify_user(self.username, "your pomodoro sessions have finished, well done!")
            self.__on_pomo_complete()


    async def __on_countdown_cancelled(self):
        '''
        Handler called when a user or mod cancels the countdown with !pomo cancel
        '''
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
            return f"work session {self.sessions_done + 1} is complete! Enjoy your {self.break_minutes} minute break!"

    @staticmethod
    def __countdown(event: Event, timeout: int, event_loop, on_complete: Callable = None, on_cancel: Callable = None):
        timeout_seconds = timeout * 60
        # blocking call
        cancelled = event.wait(timeout=timeout_seconds)
        if not cancelled:
            asyncio.run_coroutine_threadsafe(on_complete(), event_loop)
        else:
            asyncio.run_coroutine_threadsafe(on_cancel(), event_loop)

#####
