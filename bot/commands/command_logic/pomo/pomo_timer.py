from config import get_config
from threading import Event, Thread, current_thread
from queue import Queue
from typing import Callable
from pathlib import Path
from typing import Callable, Optional
from twitchio.dataclasses import User
import enum
import asyncio
import time
import math
import logging


class PomoState(enum.Enum):
    '''
    A timer can be in any of of these states
    '''
    WORK = 'work'
    BREAK = 'break'
    CANCELLED = 'cancelled'
    COMPLETE = 'complete'


class PomoOperation(enum.Enum):
    '''
    A timer's remaining time can be modified using these operations,
    or it can be cancelled.
    '''
    ADD = 'add'
    SUBTRACT = 'subtract'
    CANCEL = 'cancel'


class PomoTimerError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PomoTimer():

    def __init__(self, user: User, work_minutes: int, break_minutes: Optional[int], sessions: int, topic: str, on_pomo_complete: Callable, notify_user: Callable):
        self.user: str = User
        self.username: str = user.name

        self.work_minutes: int = work_minutes
        self.break_minutes: Optional[int] = break_minutes
        self.total_sessions: int = sessions
        self.sessions_remaining: int = sessions
        self.topic: str = topic
        self.state: PomoState = None
        self.mod_mode = False
        
        self.__cancelled_by: str = None
        self.__on_pomo_complete: Callable = on_pomo_complete
        self.__notify_user: Callable = notify_user

        # per-countdown state properties:
        self.__current_timer: Countdown = None
        self.__ops_queue: Queue = None

    @property
    def minutes_remaining(self) -> int:
        '''
        Returns the minutes remaining in the current phase (work or break)
        '''
        return seconds_to_mins(self.__current_timer.seconds_remaining)


    @property
    def sessions_done(self) -> int:
        '''
        Returns the number of work sessions remaining until the pomo is complete
        '''
        return self.total_sessions - self.sessions_remaining


    def reset_countdown(self):
        self.__ops_queue = None
        self.__current_timer = None


    async def begin(self):
        logging.info(f'{current_thread()}: beginning pomo for {self.username}')

        self.state = PomoState.WORK
        await self.__start_countdown()
        

    def cancel(self, username=''):
        if self.__current_timer:
            if username != '':
                self.__cancelled_by = username

            self.__ops_queue.put((PomoOperation.CANCEL, None, None))


    def increase_mins(self, mins):
        '''
        Ad-hoc extension of the current countdown by the given mins.
        Any subsequent WORK or BREAK timers in the session are unaffected.
        '''
        async def notify_user_callback(seconds_remaining: int):
           await self.__notify_user(self.username, f'your current timer has been increased to {seconds_to_mins(seconds_remaining)}!')

        if self.__current_timer:
            self.__ops_queue.put((PomoOperation.ADD, mins, notify_user_callback))

    
    def decrease_mins(self, mins):
        '''
        Ad-hoc reduction of the current countdown by the given mins.
        Any subsequent WORK or BREAK timers in the session are unaffected.
        '''
        async def notify_user_callback(seconds_remaining: int):
           await self.__notify_user(self.username, f'your current timer has been decreased to {seconds_to_mins(seconds_remaining)}!')
        if self.__current_timer:
            self.__ops_queue.put((PomoOperation.SUBTRACT, mins, notify_user_callback))


    async def __start_countdown(self):
        '''
        Starts a single countdown in a new worker thread. A countdown can be one work or break session.
        The worker thread waits for a given time interval and then invokes a callback function.
        
        The main thread can modify the status of the countdown by sending operation commands through a Queue, 
        which are consumed by the worker thread.
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

        self.__ops_queue = Queue()
        self.__current_timer = Countdown(
            countdown_minutes,
            self.__ops_queue,
            event_loop,
            self.__on_countdown_complete,
            self.__on_countdown_cancelled
        )
        self.__current_timer.start()


    async def __on_countdown_complete(self):
        '''
        Handler called at the end of every countdown (i.e. when an individual work or break session is over)
        '''
        logging.info(f'{current_thread()}: countdown complete for user {self.username}')
        self.reset_countdown()

        # the session boundary is after the BREAK countdown, unless there is only one work session
        # in which case there is no break, and the pomo completes
        if self.state == PomoState.BREAK or self.total_sessions == 1:
            self.sessions_remaining -= 1

        if self.sessions_remaining > 0:
            self.state = PomoState.BREAK if self.state == PomoState.WORK else PomoState.WORK
            await self.__start_countdown()
        else:
            self.state = PomoState.COMPLETE
            await self.__notify_user(self.username, f"your pomodoro sessions on {self.topic} have finished, well done on all your hard work!")
            self.__on_pomo_complete()


    async def __on_countdown_cancelled(self):
        '''
        Handler called when a user or mod cancels the countdown with !pomo cancel
        '''
        logging.info(f'{current_thread()}: countdown cancelled for user {self.username}')

        self.reset_countdown()
        self.state = PomoState.CANCELLED
        if self.__cancelled_by:
            await self.__notify_user(self.username, f"your pomo session has been cancelled by {self.__cancelled_by}.")
        else:
            await self.__notify_user(self.username, f"your pomo session {self.topic} is complete. Well done!")

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


class Countdown(Thread):
    '''
    Runs a single countdown in a new thread.
    self.seconds_remaining can be read to get the remaining time.
    Items can be pushed to the Queue to instruct the thread to add/subtract time or cancel the countdown.
    '''

    INCREMENT_SECONDS: int = 1

    def __init__(self, timeout_mins: int, queue: Queue, event_loop, on_complete: Callable, on_cancel: Callable):
        super().__init__(daemon=True)
        self.__timeout_seconds: int = timeout_mins * 60
        self.__on_complete: Callable = on_complete
        self.__on_cancel: Callable = on_cancel

        # this property is exposed and read by the main thread
        self.seconds_remaining: int = None

        # the asyncio event loop that runs on the main thread
        self.__main_event_loop = event_loop

        # the main thread sends commands to the countdown thread through this thread-safe queue.
        # through this the main thread can modify the seconds_remaining property, or cancel the countdown
        self.__ops_queue = queue


    def run(self) -> None:
        '''
        Timer method which is run on a separate thread
        '''
        logging.info(f'{current_thread()}: counting down {self.__timeout_seconds / 60} minutes')

        self.seconds_remaining = self.__timeout_seconds
        cancelled = False

        while (self.seconds_remaining > 0):
            if not self.__ops_queue.empty():
                (operation, mins, notify_done) = self.__ops_queue.get(block=False)
                if operation == PomoOperation.CANCEL:
                    cancelled = True
                    break
                if operation == PomoOperation.ADD:
                    self.__add(mins)
                    asyncio.run_coroutine_threadsafe(notify_done(self.seconds_remaining), self.__main_event_loop)
                if operation == PomoOperation.SUBTRACT:
                    self.__subtract(mins)
                    asyncio.run_coroutine_threadsafe(notify_done(self.seconds_remaining), self.__main_event_loop)


            self.seconds_remaining -= Countdown.INCREMENT_SECONDS
            time.sleep(Countdown.INCREMENT_SECONDS - time.time() % 1) # sleep until a whole second boundary

        # run the callbacks on the main thread
        logging.info(f'{current_thread()} countdown completed, cancelled = {cancelled}')
        if cancelled:
            asyncio.run_coroutine_threadsafe(self.__on_cancel(), self.__main_event_loop)
        else:
            asyncio.run_coroutine_threadsafe(self.__on_complete(), self.__main_event_loop)


    def __add(self, mins: int) -> None:
        logging.info(f'{current_thread()} countdown adding mins: {mins}')
        self.seconds_remaining += (mins * 60)


    def __subtract(self, mins: int) -> None:
        logging.info(f'{current_thread()} countdown subtracting mins: {mins}')
        substract_seconds = mins * 60
        if substract_seconds > self.seconds_remaining:
            self.seconds_remaining = 0
        else:
            self.seconds_remaining -= substract_seconds


def seconds_to_mins(seconds: int) -> int:
    return math.ceil(seconds / 60)

#####

