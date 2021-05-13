from bot.commands.command_logic.pomo.pomo_command import get_active_pomo_timers
from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from config import get_config
from typing import List, Callable, Awaitable
import asyncio
import logging
from contextlib import suppress

# the location of the text file used as the overlay source
__FILE = get_config().get('overlay_dir') / 'pomo_overlay_text.txt'

# how long a line can be before getting truncated
MAX_LINE_CHARS = 55

# how frequently the pomo data will be written to the file
UPDATE_INTERVAL_SECONDS = 10


async def start_pomo_overlay() -> Awaitable:
    __update_timers()
    return asyncio.ensure_future(__repeat_task_at_interval(__update_timers, UPDATE_INTERVAL_SECONDS))


async def __repeat_task_at_interval(task: Callable, interval: int):
    while True:
        await asyncio.sleep(interval)
        task()


def __update_timers():
    pomo_timers = get_active_pomo_timers()
    logging.info(f'pomo overlay updating with ({len(pomo_timers)} running pomos)')
    with open(__FILE, 'w+', newline='', encoding='utf-8') as overlay_file:
        contents = list()
        for timer in sorted(pomo_timers, key=lambda t: t.minutes_remaining):
            line = __build_pomo_text(timer)
            contents.append(line)
        logging.info(f'pomo overlay writing contents to file: {contents}')
        overlay_file.write('\n'.join(contents))


def __build_pomo_text(pomo: PomoTimer) -> str:
    if (pomo.state == PomoState.WORK):
        topic = pomo.topic if pomo.topic != '' else 'work'
        sessions_count = __get_sessions_count_text(pomo)
        line = f'{pomo.username} - {topic} {pomo.minutes_remaining}{sessions_count}'
        if len(line) > MAX_LINE_CHARS:
            trim_length = MAX_LINE_CHARS - len(sessions_count) - 5
            username_topic_str = f'{pomo.username} - {topic}'
            return username_topic_str[:trim_length] + f'... {pomo.minutes_remaining}{sessions_count}'
        else:
            return line

    if (pomo.state == PomoState.BREAK):
        sessions_count = __get_sessions_count_text(pomo)
        return f'{pomo.username} - relax! {pomo.minutes_remaining}{sessions_count}'


def __get_sessions_count_text(pomo: PomoTimer) -> str:
    return f' ({pomo.sessions_done + 1} of {pomo.total_sessions})' if pomo.total_sessions > 1 else ''
