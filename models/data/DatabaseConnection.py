from settings import DB_LOCATION
import sqlite3

"""
    The DatabaseConnection module provides a slightly higher-level abstraction for making database queries.
    When the module is loaded, a database connection is initialized and scripts are run to ensure the database tables exist.
    
    TODO: we may at some point want to replace this with something more robust
"""

CREATE_GAME_TABLE_SCRIPT = '''
    CREATE TABLE IF NOT EXISTS game(
      p1_type TEXT,
      p2_type TEXT,
      date_played DATE,
      num_moves INTEGER
    );
'''

CREATE_BOARD_TABLE_SCRIPT = '''
    CREATE TABLE IF NOT EXISTS board(
      p00 TINYINT, p01 TINYINT, p02 TINYINT, p03 TINYINT, p04 TINYINT, p05 TINYINT, p06 TINYINT, p07 TINYINT, p08 TINYINT,
      p10 TINYINT, p11 TINYINT, p12 TINYINT, p13 TINYINT, p14 TINYINT, p15 TINYINT, p16 TINYINT, p17 TINYINT, p18 TINYINT,
      p20 TINYINT, p21 TINYINT, p22 TINYINT, p23 TINYINT, p24 TINYINT, p25 TINYINT, p26 TINYINT, p27 TINYINT, p28 TINYINT,
      p30 TINYINT, p31 TINYINT, p32 TINYINT, p33 TINYINT, p34 TINYINT, p35 TINYINT, p36 TINYINT, p37 TINYINT, p38 TINYINT,
      p40 TINYINT, p41 TINYINT, p42 TINYINT, p43 TINYINT, p44 TINYINT, p45 TINYINT, p46 TINYINT, p47 TINYINT, p48 TINYINT,
      p50 TINYINT, p51 TINYINT, p52 TINYINT, p53 TINYINT, p54 TINYINT, p55 TINYINT, p56 TINYINT, p57 TINYINT, p58 TINYINT,
      p60 TINYINT, p61 TINYINT, p62 TINYINT, p63 TINYINT, p64 TINYINT, p65 TINYINT, p66 TINYINT, p67 TINYINT, p68 TINYINT,
      p70 TINYINT, p71 TINYINT, p72 TINYINT, p73 TINYINT, p74 TINYINT, p75 TINYINT, p76 TINYINT, p77 TINYINT, p78 TINYINT,
      p80 TINYINT, p81 TINYINT, p82 TINYINT, p83 TINYINT, p84 TINYINT, p85 TINYINT, p86 TINYINT, p87 TINYINT, p88 TINYINT,
      next_player TINYINT,
      wins INTEGER,
      losses INTEGER,
      ties INTEGER,
      PRIMARY KEY (
        p00, p01, p02, p03, p04, p05, p06, p07, p08,
        p10, p11, p12, p13, p14, p15, p16, p17, p18,
        p20, p21, p22, p23, p24, p25, p26, p27, p28,
        p30, p31, p32, p33, p34, p35, p36, p37, p38,
        p40, p41, p42, p43, p44, p45, p46, p47, p48,
        p50, p51, p52, p53, p54, p55, p56, p57, p58,
        p60, p61, p62, p63, p64, p65, p66, p67, p68,
        p70, p71, p72, p73, p74, p75, p76, p77, p78,
        p80, p81, p82, p83, p84, p85, p86, p87, p88,
        next_player
      )
    ) WITHOUT ROWID;
'''

_connection = None
_connection_open = False


def init():
    """ Initializes tables used by this application """
    global _connection, _connection_open
    connection = None
    if _connection and _connection_open:
        connection = _connection
    else:
        connection = sqlite3.connect(DB_LOCATION)
        _connection = connection
        _connection_open = True

    cursor = connection.cursor()
    cursor.execute(CREATE_GAME_TABLE_SCRIPT)
    cursor.execute(CREATE_BOARD_TABLE_SCRIPT)

    connection.commit()


def query(sql):
    """ Executes the given sql statement and returns the cursor object with the results """
    global _connection, _connection_open
    if not (_connection and _connection_open):
        close()
        init()

    cursor = _connection.cursor()
    return cursor.execute(sql)


def execute(sqlscript):
    """ Executes the given sql statement """
    global _connection, _connection_open
    if not (_connection and _connection_open):
        close()
        init()

    cursor = _connection.cursor()
    cursor.executescript(sqlscript)
    _connection.commit()


def close():
    """ Closes the connection until init, query, or execute is called again"""
    global _connection, _connection_open
    if _connection:
        _connection.close()
        _connection_open = False

    _connection = None


def purge_boards(min_games):
    # removes board states from the database where fewer than min_games have been played
    PURGE_SCRIPT = "DELETE FROM board WHERE (wins + losses + ties) < %s" % min_games
    return execute(PURGE_SCRIPT)


# Call init when the module is loaded
init()
