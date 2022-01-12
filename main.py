import json
from time import sleep
from random import randrange
from copy import deepcopy
from typing import Union
from pyco import cursor, color, terminal
from pyco.utils import getch, kbhit
from pyco.constants import ESC
from pyco.color import RESET


class Field:
    def __init__(self, width: int, height: int, cells: Union[list[list[bool]], list[tuple[int, int]]] = None, chars: dict = {True: '##', False: '  '}, wrap: bool = True):
        self.width = width
        self.height = height
        self.chars = chars
        self.wrap = wrap
        if cells and isinstance(cells, list):
            if isinstance(cells[0], list):
                if isinstance(cells[0][0], bool):
                    self.cells = cells
            elif isinstance(cells[0], tuple):
                if isinstance(cells[0][0], int):
                    self.cells = [[False for y in range(self.height)] for x in range(self.width)]
                    self.set_many(cells)
        else:
            self.cells = self.random_field()

    def update(self):
        cells = deepcopy(self.cells)
        for x in range(self.width):
            for y in range(self.height):
                cells[x][y] = self.next(x, y)
        self.cells = cells

    def next(self, x: int, y: int) -> bool:
        alive = 0
        i = -1
        while i <= 1:
            j = -1
            while j <= 1:
                a = x + i
                b = y + j
                if not self.wrap:
                    if a < 0 or a >= self.width or b < 0 or b >= self.height:
                        j += 1
                        continue
                if (i != 0 or j != 0) and self.alive(a, b):
                    alive += 1
                j += 1
            i += 1
        return (alive == 2 and self.alive(x, y)) or alive == 3

    def alive(self, x: int, y: int) -> bool:
        x += self.width
        x %= self.width
        y += self.height
        y %= self.height
        return self.cells[x][y]

    def set(self, x: int, y: int, state: bool):
        x += self.width
        x %= self.width
        y += self.height
        y %= self.height
        self.cells[x][y] = state

    def set_many(self, cells: list[tuple[int, int]]):
        for coord in cells:
            self.set(coord[0], coord[1], True)

    def clear(self):
        cells = [[False for y in range(self.height)] for x in range(self.width)]
        self.cells = cells

    def random_field(self) -> list[list[bool]]:
        cells = [[False for y in range(self.height)] for x in range(self.width)]
        for i in range(self.width * self.height // randrange(6, 11)):
            cells[randrange(self.width)][randrange(self.height)] = True
        return cells

    def __str__(self):
        strings = []
        for y in range(self.height):
            string = ''
            for x in range(self.width):
                string += self.chars[self.cells[x][y]]
            strings.append(string)
        return '\n'.join(strings)


class Game:
    def __init__(self, config_path: str = 'config.json'):
        with open(config_path, 'r') as config_file:
            self.config = json.load(config_file)
        self.keybinds = self.config['keybinds']
        self.running = True

    def play(self):
        self.running = True
        while self.running:
            self.field = Field(self, self.config)
            while self.running:
                key = self.get_key()
                if key is not None:
                    key = key.upper()
                    key = self.keybinds.get(key, key)
                    if key in self.keybinds.values():
                        self.field.snake.change_direction(key)
                    elif key == ESC:
                        self.exit()
                    elif key == ' ':
                        getch()
                self.field.update()

    def end(self, *messages: str):
        # terminal.bell()
        for i, message in enumerate(messages):
            self.add_string(((self.field.real_size.x - len(message)) // 2, ((self.field.real_size.y - len(messages)) // 2) + i), message + RESET)
        key = getch().upper()
        if key == '\x1b':
            self.exit()
        else:
            self.play()

    def exit(self):
        terminal.clear_screen()
        self.running = False

    def add_string(self, pos: tuple[int], string: str):
        cursor.set_position(*pos)
        print(string, end='')

    def get_key(self) -> str:
        if kbhit():
            key = getch()
            if key in ['\000', '\x00', '\xe0']:
                key = getch()
            return key


# if __name__ == '__main__':
#     game = Game()
#     game.play()


def get_key() -> str:
    if kbhit():
        key = getch()
        if key in ['\000', '\x00', '\xe0']:
            key += getch()
        return key


if __name__ == '__main__':
    chars = {
        True: color.Fore.BRIGHT_YELLOW + '██',
        False: '  '
    }
    terminal_size = terminal.get_size()
    import lexicon
    field = Field(terminal_size.columns // 2, terminal_size.lines, chars=chars, cells=lexicon.acorn)
    cursor.hide()
    while True:
        key = get_key()
        if key == '\x1b':
            break
        elif key == ' ':
            field = Field(terminal_size.columns // 2, terminal_size.lines, chars=chars)
        print(field, end='')
        sleep(1 / 20)
        field.update()
        cursor.set_position(0, 0)
