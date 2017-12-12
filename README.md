# Ultimate Tic Tac Toe

Ultimate Tic-Tac-Toe is a modification of the traditional game of tic-tac-toe with a much more interesting ruleset.  A full description of the rules can be found [here](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).

This project includes:

  - A game engine for Ultimate Tic-Tac-Toe
  - An implementation of Monte Carlo Tree Search to play the game
  - An implementation of one (or more) bots that use minimax search to play the game
  - A tool for testing bots against other bots or human players

### Installation

This project requires [Python 3.5+](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installing/), and Oracle JDK 1.7+.  On Linux, the JAVA_HOME variable *must* be set.  On Windows, you may want to add python and pip to the system path.

Clone the repository:
```sh
$ git clone https://github.com/zachdj/ultimate-tic-tac-toe.git
```

Environment variables are stored in the `settings.py` file, which is ignored by default.  Make a copy of the included `settings.py.example` file and rename it to `settings.py`.  Open the file in a text editor and set any applicable variables.

Dependencies are managed using [pipenv](https://github.com/kennethreitz/pipenv).  Use pip to install pipenv:

```sh
$ pip install pipenv
```

Then cd to the project directory and install dependencies:

```sh
$ cd path/to/ultimate-tic-tac-toe
$ pipenv install
```

This will create a virtual environment for the project and install any required dependencies inside the virtual environment.  Finally, activate the virtual environment and run the main.py file:

```sh
$ pipenv shell
$ python main.py
```

### Usage

##### Using the GUI

Interacting with the program's graphical interface is straightforward.  Games can be played/visualized by clicking the "Play Game" button from the main menu.  Experiments (multiple games between bots) can be run from the "Run Experiment" menu.  If the "Record Result" option is enabled, the board states and their win rates will be stored in a local database specified by the `DB_LOCATION` option in `settings.py`.

##### Creating Minimax Bots
It is fairly simple to create bots that play using the minimax algorithm.  Create a new class in the `models.game.bots` package that extends the `MinimaxBot` class.  You need only provide a definition of the `__init__` method (see `MinimaxExample.py` for an example) and the `compute_score` method.  The `compute_score` method should return a score between -1 and 1 which describes the "goodness" the board **from the perspective of the X player**.

After your bot has been defined, add it to the `BotLoader.py` file to make it available for use in the "Play Game" and "Run Experiment" menus.  The `BotLoader.py` file contains a Python array defining loadable bots.  Each bot must specify the following parameters:

  - "title": A string with a human-readable name for the bot
  - "description": Human-readable string describing the bot
  - "difficulty": An integer from 1-10 describing how good the bot is at the game
  - "data": The Python class that implements this bot

### Development

Much of this codebase was developed as part of a class project for the course "CSCI 6550 - Intro to AI" at the University of Georgia in Fall 2017.  If you`re interested in contributing, you can contact me at zach.dean.jones@gmail.com.

Also if you aren't interested in contributing, but you have some good jokes, feel free to email me.

License
----

MIT
