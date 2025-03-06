# Game of Life

[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), for the terminal.

This project was created as a demo for the [Pyco](https://github.com/lemonyte/pyco) library.

## Installation

With uv:

```shell
uv tool install git+https://github.com/lemonyte/game-of-life
```

With pip:

```shell
pip install git+https://github.com/lemonyte/game-of-life
```

Requires [Python 3.10](https://www.python.org/downloads/) or higher.

## Usage

### Command line

```shell
game-of-life <pattern> [--rate <int>]
```

When run without a pattern, one will be randomly generated.
For a list of available patterns see the [patterns](src/game_of_life/patterns) directory.

`rate` can be used to limit the refresh rate of the simulation in updates per second.

Example:

```shell
game-of-life snark_loop --rate 20
```

### Controls

| Key                            | Description                 |
| ------------------------------ | --------------------------- |
| <kbd>ESC</kbd> or <kbd>q</kbd> | Exit the program            |
| <kbd>SPACE</kbd>               | Pause the simulation        |
| <kbd>s</kbd>                   | Step the simulation forward |
| <kbd>r</kbd>                   | Reset the simulation        |

Resizing the terminal window will affect how fast the simulation runs, more cells equals slower simulation.
When resizing the terminal, press <kbd>r</kbd> to adjust the simulation size automatically.

## License

[MIT License](license.txt)
