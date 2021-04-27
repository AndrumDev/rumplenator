from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from config import get_config
from typing import List

__FILE = get_config().get('storage_dir') / 'pomo_overlay_text.txt'
MAX_LINE_CHARS = 50

def update_timers(pomo_timers: List[PomoTimer]):
    with open(__FILE, 'w+', newline='') as overlay_file:
        contents = list()
        for timer in sorted(pomo_timers, key=lambda t: t.start_time):
            contents.append(__build_pomo_text(timer))
        overlay_file.write('\n'.join(contents))


def __build_pomo_text(pomo: PomoTimer) -> str:
    if (pomo.state == PomoState.WORK):
        topic = pomo.topic if pomo.topic != '' else 'work'
        sessions_count = __get_sessions_count_text(pomo)
        line = f'{pomo.username} - {topic} {pomo.work_minutes}{sessions_count}'
        if len(line) > MAX_LINE_CHARS:
            trim_length = MAX_LINE_CHARS - len(sessions_count) - 5
            username_topic_str = f'{pomo.username} - {topic}'
            return username_topic_str[:trim_length] + f'... {pomo.work_minutes}{sessions_count}'
        else:
            return line

    if (pomo.state == PomoState.BREAK):
        sessions_count = __get_sessions_count_text(pomo)
        return f'{pomo.username} - relax! {pomo.break_minutes}{sessions_count}'

def __get_sessions_count_text(pomo: PomoTimer) -> str:
    return f' ({pomo.sessions_done + 1} of {pomo.total_sessions})' if pomo.total_sessions > 1 else ''
