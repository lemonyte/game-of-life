from enum import Enum
from random import randrange
from typing import Optional

from pyco import color, cursor, terminal
from pyco.utils import getch, kbhit


class Event(Enum):
    EXIT = '\x1b'
    PAUSE = ' '
    RESET = 'r'


class Field:
    def __init__(self):
        self.cells = set()
        self.text = ''
        self.reset()

    @property
    def width(self) -> int:
        return terminal.get_size().columns

    @property
    def height(self) -> int:
        return terminal.get_size().lines * 2

    def reset(self):
        self.cells = set()
        for _ in range(self.width * self.height // randrange(6, 11)):
            self.cells.add((randrange(self.width), randrange(self.height)))

    def alive(self, x: int, y: int) -> bool:
        return (x, y) in self.cells

    def next(self, x: int, y: int) -> bool:
        alive = 0
        i = -1
        while i <= 1:
            j = -1
            while j <= 1:
                a = x + i
                b = y + j
                if self.alive(a, b) and not (i == 0 and j == 0):
                    alive += 1
                j += 1
            i += 1
        return alive == 3 or (alive == 2 and self.alive(x, y))

    def update(self):
        rows = []
        for y in range(0, self.height, 2):
            row = ''
            for x in range(self.width):
                if self.next(x, y):
                    self.cells.add((x, y))
                else:
                    self.cells.discard((x, y))
                if y + 1 < self.height and self.next(x, y + 1):
                    self.cells.add((x, y + 1))
                else:
                    self.cells.discard((x, y + 1))
                row += (
                    (str(color.Fore.BRIGHT_YELLOW) if self.alive(x, y) else str(color.Fore.BLACK))
                    + (
                        str(color.Back.BRIGHT_YELLOW)
                        if y + 1 < self.height and self.alive(x, y + 1)
                        else str(color.Back.BLACK)
                    )
                    + '▀'
                    + str(color.RESET)
                )
            rows.append(row)
        self.text = '\n'.join(rows)


class Game:
    def __init__(self):
        self.field = Field()
        terminal.set_window_title("Conway's Game of Life")
        terminal.clear_screen()
        cursor.hide()

    def reset(self):
        self.field.reset()

    def exit(self):
        terminal.clear_screen()
        cursor.set_position(0, 0)
        cursor.show()
        raise SystemExit

    def get_event(self) -> Optional[Event]:
        key = ''
        while kbhit():
            key += getch()
        if key:
            key = key.lower()
            try:
                return Event(key)
            except ValueError:
                return None

    def play(self):
        try:
            while True:
                event = self.get_event()
                if event is Event.EXIT:
                    self.exit()
                elif event is Event.PAUSE:
                    getch()
                elif event is Event.RESET:
                    self.reset()
                self.field.update()
                cursor.set_position(0, 0)
                for line in self.field.text.splitlines(keepends=True):
                    print(line, end='', flush=True)
        except KeyboardInterrupt:
            self.exit()


if __name__ == '__main__':
    Game().play()
