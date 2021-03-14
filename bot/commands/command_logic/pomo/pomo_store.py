from bot.commands.command_logic.pomo.pomo_timer import PomoTimer, PomoState
from config import get_config
from threading import Thread
from queue import Queue
from random import randint
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple
from csv import DictReader, DictWriter
from datetime import datetime, timezone


# CSV writer setup goes here

queue: "Queue[PomoTimer]" = Queue()


__HEADER_FIELDS = ['username', 'work_minutes', 'break_minutes', 'total_sessions', 'topic', 'num_violations', 'start_time']
__FILE = get_config().get('storage_dir') / 'current_pomos.csv'


def add_timer(pomo_timer: PomoTimer):
    with open(__FILE, 'a', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=__HEADER_FIELDS)
        writer.writerow(__get_csv_row(pomo_timer))


def update_timers(pomo_timers: List[PomoTimer]):
    with open(__FILE, 'w', newline='') as csvfile:
        writer = DictWriter(csvfile, fieldnames=__HEADER_FIELDS)
        contents = list()
        for timer in pomo_timers:
            contents.append(__get_csv_row(timer))
        writer.writerows(contents)


def read_timers(pomo_timers: List[PomoTimer]) -> List[Dict]:
    with open(__FILE, 'r', newline='') as csvfile:
        reader = DictReader(csvfile, fieldnames=__HEADER_FIELDS)
        return [timer for timer in reader]


def __get_csv_row(pomo_timer: PomoTimer) -> Dict:
    return {
        'username': pomo_timer.username,
        'work_minutes': pomo_timer.work_minutes,
        'break_minutes': pomo_timer.break_minutes,
        'total_sessions': pomo_timer.total_sessions,
        'topic': pomo_timer.topic,
        'num_violations': 0,  # TODO Jay :)
        'start_time': pomo_timer.start_time
    }


# def consume():
#     while True:
#         if not queue.empty():
#             pomo_timer = queue.get()

#             if pomo_timer.state == PomoState.COMPLETE or pomo_timer.state == PomoState.CANCELLED:
#                 user = pomo_timer.username
#                 contents = list()
#                 with open(FILENAME, 'r') as readFile:
#                     reader = DictReader(readFile)
#                     contents = [row for row in reader if row.get('username') != user]

#                 with open('mycsv.csv', 'w') as writeFile:
#                     writer = DictWriter(writeFile, fieldnames=HEADER_FIELDS)
#                     writer.writerows(contents)
#             else:
#                 row = {
#                     'username': pomo_timer.username,
#                     'work_minutes': pomo_timer.work_minutes,
#                     'break_minutes': pomo_timer.break_minutes,
#                     'total_sessions': pomo_timer.total_sessions,
#                     'topic': pomo_timer.topic,
#                     'num_violations': 0  # TODO Jay :)
#                 }
#                 with open(FILENAME, 'a', newline='') as csvfile:
#                     writer = DictWriter(csvfile, fieldnames=HEADER_FIELDS)
#                     writer.writerow(row)


# consumer = Thread(target=consume)
# consumer.setDaemon(True)
# consumer.start()


# with ThreadPoolExecutor(max_workers=10) as executor:
#     for i in range(5000):
#         executor.submit(produce, i)

# consumer.join()