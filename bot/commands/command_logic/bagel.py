from config import get_config
from random import randint


bagel_file_path = get_config().get('resource_dir') / 'bagel_fillings.txt'


def __read_bagel_file():
    bagel_file = open(bagel_file_path, "r")
    bagel_fillings = []
    for line in bagel_file:
        line = line.split('#')[0].strip()
        if line == '': continue
        bagel_fillings.append(line)

    return bagel_fillings


def get_bagel_message() -> str:
    fillings = __read_bagel_file()
    return fillings[randint(0, len(fillings)-1)]
    