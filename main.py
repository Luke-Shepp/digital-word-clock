from datetime import datetime
import time
import os
import copy

letters = [
    # 0    1    2    3    4    5    6    7    8    9   10
    ['I', 'T', 'C', 'I', 'S', 'Q', 'L', 'T', 'E', 'M', 'P'],  # 0

    ['T', 'W', 'E', 'N', 'T', 'Y', 'P', 'F', 'I', 'V', 'E'],  # 1
    ['T', 'E', 'N', 'Z', 'Q', 'U', 'A', 'R', 'T', 'E', 'R'],  # 2
    ['H', 'A', 'L', 'F', 'X', 'P', 'A', 'S', 'T', 'O', 'P'],  # 3

    ['T', 'W', 'O', 'N', 'E', 'T', 'H', 'R', 'E', 'E', 'C'],  # 4
    ['F', 'O', 'U', 'R', 'T', 'S', 'F', 'S', 'I', 'X', 'M'],  # 5
    ['P', 'F', 'I', 'V', 'E', 'I', 'G', 'H', 'T', 'E', 'N'],  # 6
    ['S', 'E', 'V', 'E', 'N', 'I', 'N', 'E', 'K', 'L', 'A'],  # 7
    ['T', 'W', 'E', 'L', 'V', 'E', 'L', 'E', 'V', 'E', 'N'],  # 8
    ['O', 'C', 'L', 'O', 'C', 'K', 'B', 'A', 'M', 'P', 'M'],  # 9
    ['L', 'U', 'K', 'E', 'M', 'T', 'W', 'T', 'F', 'S', 'S']   # 10
]

combos = {
    'hours': {
        1: [[4, 2], [4, 3], [4, 4]],
        2: [[4, 0], [4, 1], [4, 2]],
        3: [[4, 5], [4, 6], [4, 7], [4, 8], [4, 9]],
        4: [[5, 0], [5, 1], [5, 2], [5, 3]],
        5: [[6, 1], [6, 2], [6, 3], [6, 4]],
        6: [[5, 7], [5, 8], [5, 9]],
        7: [[7, 0], [7, 1], [7, 2], [7, 3], [7, 4]],
        8: [[6, 4], [6, 5], [6, 6], [6, 7], [6, 8]],
        9: [[7, 4], [7, 5], [7, 6], [7, 7]],
        10: [[6, 8], [6, 9], [6, 10]],
        11: [[8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [8, 10]],
        12: [[8, 0], [8, 1], [8, 2], [8, 3], [8, 4], [8, 5]],
    },

    'minutes': {
        5: [[1, 7], [1, 8], [1, 9], [1, 10]],
        10: [[2, 0], [2, 1], [2, 2]],
        15: [[2, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9], [2, 10]],
        20: [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]],
        25: [[1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 7], [1, 8], [1, 9], [1, 10]],
        30: [[3, 0], [3, 1], [3, 2], [3, 3]],
    },

    'past_to': {
        'past': [[3, 5], [3, 6], [3, 7], [3, 8]],
        'to': [[3, 8], [3, 9]],
    },

    'am_pm': {
        'am': [[9, 7], [9, 8]],
        'pm': [[9, 9], [9, 10]]
    },

    'luke': [[10, 0], [10, 1], [10, 2], [10, 3]],

    'o_clock': [[9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5]],

    'it_is': [[0, 0], [0, 1], [0, 3], [0, 4]],

    'temp': [[0, 7], [0, 8], [0, 9], [0, 10]],

    # 'degree': [[2, 8], [2, 9], [3, 8], [3, 9]],

    'hi': [
        # | (h)
        [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0],
        [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1],

        # - (h)
        [4, 2], [4, 3], [4, 4],
        [5, 2], [5, 3], [5, 4],

        # | (h)
        [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5],
        [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6],

        # | (I)
        [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9],
        [1, 10], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10],
    ],
}


def clear_board():
    output([])


def scroll_hi():
    ptr = -12

    while True:
        ptr += 1

        to_light = []

        for coord in combos['hi']:
            x = copy.copy(coord)
            x[1] -= ptr
            to_light.append(x)

        output(to_light)
        time.sleep(0.2)

        if ptr >= 11:
            break


def show_time():
    while True:
        clear_board()

        now = datetime.now()

        hour = int(now.strftime("%I"))

        minute = round_num(int(now.strftime("%M")))
        is_am = now.strftime("%p") == "AM"
        past_to = 'past'

        if minute > 30:
            hour += 1
            minute = 60 - minute
            past_to = 'to'

        if hour > 12:
            hour -= 12

        # IT IS
        to_light = combos['it_is']

        # hour
        to_light += combos['hours'][hour]

        # minute
        if minute > 0:
            to_light += combos['minutes'][minute]

        # PAST / TO
        if minute > 0:
            to_light += combos['past_to'][past_to]

        # AM / PM
        if is_am:
            to_light += combos['am_pm']['am']
        else:
            to_light += combos['am_pm']['pm']

        if minute == 0:
            to_light += combos['o_clock']

        output(to_light)

        time.sleep(10)


def output(light):
    os.system('clear')

    for rowI, row in enumerate(letters):
        for colI, letter in enumerate(row):
            if [rowI, colI] in light:
                print "\033[1;31;40m" + letter + " ",
            else:
                print "\033[1;37;40m" + letter + " ",
        print


def round_num(x, base=5):
    return int(base * round(float(x)/base))


def test():
    test_rows()
    test_cols()
    test_diag_1()
    test_diag_2()
    test_each_combo()


def test_rows():
    for rowI, row in enumerate(letters):
        to_light = []
        for colI, letter in enumerate(row):
            to_light += [[rowI, colI]]
            # print to_light
        output(to_light)
        time.sleep(0.5)
    clear_board()


def test_cols():
    for rowI, row in enumerate(letters):
        to_light = []
        for colI, letter in enumerate(row):
            to_light += [[colI, rowI]]
            # print to_light
        output(to_light)
        time.sleep(0.5)
    clear_board()


def test_diag_1():
    colN = 0
    rowN = 0
    to_light = []
    while True:
        for i in range(0, colN):
            for y in range(0, rowN):
                to_light += [[i, y]]
        output(to_light)
        # print(colN, rowN)
        time.sleep(0.22)
        colN += 1
        rowN += 1
        if colN > 11:
            break
    clear_board()


def test_diag_2():
    colN = 11
    rowN = 11
    to_light = []
    while True:
        for i in range(colN, 11):
            for y in range(rowN, 11):
                to_light += [[i, y]]
        output(to_light)
        # print(colN, rowN)
        time.sleep(0.25)
        colN -= 1
        rowN -= 1
        if colN < 0:
            break
    clear_board()


def test_each_combo():
    for key, lights in combos['hours'].items():
        output(lights)
        time.sleep(0.5)

    for key, lights in combos['minutes'].items():
        output(lights)
        time.sleep(0.5)

    for key, lights in combos['past_to'].items():
        output(lights)
        time.sleep(0.5)

    for key, lights in combos['am_pm'].items():
        output(lights)
        time.sleep(0.5)

    output(combos['luke'])
    time.sleep(0.5)

    output(combos['o_clock'])
    time.sleep(0.5)

    output(combos['it_is'])
    time.sleep(0.5)

    clear_board()


if __name__ == '__main__':
    # scroll_hi()
    test()
    show_time()

