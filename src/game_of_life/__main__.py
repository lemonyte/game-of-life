import argparse
import sys
from importlib.resources import files
from pathlib import Path
from typing import NoReturn

from game_of_life import Program, load_cells


def main() -> NoReturn:
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", type=str, default=None, nargs="?")
    parser.add_argument("--rate", type=int, default=0)
    args = parser.parse_args()
    program = Program()
    if args.pattern is not None:
        path = Path(args.pattern)
        if not path.is_file():
            path = files("game_of_life.patterns") / f"{args.pattern}.cells"
        try:
            cells = load_cells(path)
            program.setup(cells=cells)
        except FileNotFoundError as exc:
            print(f"Pattern file not found: {args.pattern}", file=sys.stderr)
            raise SystemExit(1) from exc
    program.play(rate=args.rate)


if __name__ == "__main__":
    main()
