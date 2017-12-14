# Ultimate Tic Tac Toe

Ultimate Tic-Tac-Toe is a modification of the traditional game of tic-tac-toe with a much more interesting ruleset.  A full description of the rules can be found [here](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).  This repo is an older copy of [my UTTT program](https://github.com/zachdj/ultimate-tic-tac-toe) which includes all the nasty stuff needed to import and run models built with Weka.  This software is not terribly stable, especially under non-Linux operating systems and with non-Oracle JDKs.

This project includes:

  - A game engine for Ultimate Tic-Tac-Toe
  - An implementation of Monte Carlo Tree Search to play the game
  - Several models that attempt to score boards based on heuristics learned from recorded games
  - Dependencies and code to import and run Weka models
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


### Development

Much of this codebase was developed as part of a class project for the course "CSCI 6550 - Intro to AI" at the University of Georgia in Fall 2017.  If you're interested in contributing, you can contact me at zach.dean.jones@gmail.com.

License
----

MIT
