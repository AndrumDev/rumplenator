from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from config import get_config
from typing import List

__FILE = get_config().get('storage_dir') / 'pomo_overlay_text.txt'


def update_timers(pomo_timers: List[PomoTimer]):
    with open(__FILE, 'w+', newline='') as overlay_file:
        contents = list()
        for timer in sorted(pomo_timers, key=lambda t: t.start_time):
            contents.append(__build_pomo_text(timer))
        overlay_file.write('\n'.join(contents))


def __build_pomo_text(pomo: PomoTimer) -> str:
    if (pomo.state == PomoState.WORK):
        on_topic = f'on {pomo.topic} ' if pomo.topic != '' else ''
        return f'{pomo.username} working for {pomo.work_minutes} mins {on_topic}({pomo.sessions_done + 1} of {pomo.sessions_remaining})'
    if (pomo.state == PomoState.BREAK):
        return f'{pomo.username} relax for {pomo.break_minutes} mins ({pomo.sessions_done + 1} of {pomo.sessions_remaining})'
