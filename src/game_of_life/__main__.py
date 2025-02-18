import argparse
from importlib.resources import files
from typing import NoReturn

from game_of_life import Program, load_cells


def main() -> NoReturn:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", type=str, default="random", nargs="?")
    parser.add_argument("--rate", type=int, default=0)
    args = parser.parse_args()
    program = Program()
    if args.pattern != "random":
        path = files("game_of_life.patterns") / f"{args.pattern}.cells"
        try:
            cells = load_cells(path)
            program.setup(cells=cells)
        except FileNotFoundError as exc:
            print(f"Pattern file not found: {path}")
            raise SystemExit(1) from exc
    program.play(rate=args.rate)


if __name__ == "__main__":
    main()
