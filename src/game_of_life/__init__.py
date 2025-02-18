from __future__ import annotations

import random
import time
from enum import Enum
from typing import TYPE_CHECKING, NoReturn

from pyco import color, cursor, terminal
from pyco.utils import getch, kbhit

if TYPE_CHECKING:
    from importlib.abc import Traversable

Cell = tuple[int, int]
CellGrid = dict[Cell, bool]


def load_cells(path: Traversable, /) -> CellGrid:
    cells: CellGrid = {}
    for y, line in enumerate(filter(lambda line: not line.startswith("!"), path.read_text().splitlines())):
        for x, char in enumerate(line):
            cells[(x, y)] = char == "O"
    return cells


class Event(Enum):
    EXIT = "\x1b"
    QUIT = "q"
    PAUSE = " "
    STEP = "s"
    RESET = "r"


class GameOfLife:
    def __init__(self) -> None:
        self.cells: CellGrid = {}
        self.colors = tuple(
            map(
                str,
                (
                    color.Fore.BLACK,
                    color.Fore.BRIGHT_YELLOW,
                    color.Back.BLACK,
                    color.Back.BRIGHT_YELLOW,
                ),
            ),
        )
        self.width = 0
        self.height = 0
        self.update_size()
        self.reset(self.random_grid())

    def update_size(self) -> None:
        terminal_size = terminal.get_size()
        self.width = terminal_size.columns
        self.height = terminal_size.lines * 2

    def empty_grid(self) -> CellGrid:
        return {(x, y): False for x in range(self.width) for y in range(self.height)}

    def random_grid(self) -> CellGrid:
        return {(x, y): not random.randint(0, 10) for x in range(self.width) for y in range(self.height)}

    def reset(self, cells: CellGrid, /) -> None:
        self.cells = self.empty_grid() | cells

    def cell_state(self, x: int, y: int, /) -> bool:
        # This turns out to be slightly faster than using `get()`.
        try:
            return self.cells[(x, y)]
        except KeyError:
            return False

    def next_cell_state(self, x: int, y: int, /) -> bool:
        neighbors = 0
        # Iterating a tuple is faster than `range()`.
        for xd in (-1, 0, 1):
            for yd in (-1, 0, 1):
                if xd == yd == 0:
                    continue
                neighbors += self.cell_state(x + xd, y + yd)
        if self.cell_state(x, y):
            return 2 <= neighbors <= 3
        return neighbors == 3

    def step(self) -> None:
        cells = self.cells.copy()
        for cell in self.cells:
            cells[cell] = self.next_cell_state(*cell)
        self.cells = cells

    def __str__(self) -> str:
        rows = []
        for y in range(0, self.height, 2):
            row = []
            for x in range(self.width):
                cell_top_state = self.cells[(x, y)]
                cell_bottom_state = self.cells[(x, y + 1)]
                row.append(self.colors[cell_top_state] + self.colors[2 + cell_bottom_state] + "▀")
            rows.append("".join(row))
        return "\n".join(rows) + str(color.RESET)


class Program:
    def __init__(self) -> None:
        self.field = GameOfLife()
        self.starting_cells: CellGrid = {}

    def get_event(self) -> Event | None:
        key = ""
        while kbhit():
            key += getch()
        if key:
            try:
                return Event(key.lower())
            except ValueError:
                return None
        return None

    def handle_event(self, event: Event | None, /) -> None:
        if event in (Event.EXIT, Event.QUIT):
            self.exit()
        elif event is Event.PAUSE:
            self.pause()
        elif event is Event.RESET:
            self.reset()
        elif event is Event.STEP:
            self.step()

    def pause(self) -> None:
        while True:
            event = self.get_event()
            if event is Event.PAUSE:
                return
            self.handle_event(event)

    def setup(self, *, cells: CellGrid) -> None:
        self.starting_cells = cells
        self.field.reset(cells)

    def draw(self) -> None:
        cursor.set_position(0, 0)
        print(str(self.field), end="", flush=True)

    def step(self) -> None:
        self.field.step()
        self.draw()

    def reset(self) -> None:
        self.field.update_size()
        self.field.reset(self.starting_cells or self.field.random_grid())
        self.draw()

    def exit(self) -> NoReturn:
        cursor.show()
        terminal.main_screen_buffer()
        raise SystemExit

    def play(self, *, rate: int = 0) -> NoReturn:
        terminal.alt_screen_buffer()
        terminal.set_window_title("Conway's Game of Life")
        cursor.hide()
        self.draw()
        try:
            while True:
                if rate:
                    time.sleep(1 / rate)
                self.handle_event(self.get_event())
                self.step()
        except KeyboardInterrupt:
            self.exit()
