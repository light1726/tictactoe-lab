"""
board.py -- the shared pieces every Tic-Tac-Toe brain needs.

This file has no "brain" of its own. It provides:
  * the board (cells 0..8), the rules of the game, and helpers
  * three TEST OPPONENTS (Randomo, Greedy, Minimax) used to grade your brain
  * a self_test() that plays your brain against those opponents
  * an export_brain() that saves your brain so index.html can use it

Board layout:
     0 | 1 | 2
    ---+---+---
     3 | 4 | 5
    ---+---+---
     6 | 7 | 8

You normally don't need to edit this file. The four brains are in
heuristics.py, probability.py, search.py and rl.py.
"""

import json
import os
import random

# ---------------------------------------------------------------- the board

EMPTY, X, O = " ", "X", "O"

# The 8 winning lines (three cells each).
LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6),              # diagonals
)

CORNERS = (0, 2, 6, 8)
EDGES = (1, 3, 5, 7)
CENTER = 4


def opponent(player):
    return O if player == X else X


def winner(board):
    """Return X, O or None (game not finished)."""
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_full(board):
    return EMPTY not in board


def legal_moves(board):
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def play(board, move, player):
    """Return a new board with `player`'s mark placed at `move`."""
    cells = list(board)
    cells[move] = player
    return tuple(cells)


# ---------------------------------------------------------------- symmetries
#
# Rotating or mirroring a Tic-Tac-Toe position doesn't change anything
# important -- the same moves are good everywhere. The RL brain folds all
# 8 versions into ONE canonical form, which keeps its table 8x smaller.

def _rot90(p):
    i, j = divmod(p, 3)
    return j * 3 + (2 - i)


def _mirror(p):
    i, j = divmod(p, 3)
    return i * 3 + (2 - j)


def _compose(f, g):
    return lambda p: f(g(p))


def _table_for(transform):
    """table[i] = the original cell that lands at position i."""
    table = [None] * 9
    for p in range(9):
        table[transform(p)] = p
    return tuple(table)


_TABLES = []
_rot = lambda p: p            # start with the identity
for _ in range(4):
    _TABLES.append(_table_for(_rot))
    _TABLES.append(_table_for(_compose(_mirror, _rot)))
    _rot = _compose(_rot90, _rot)


def canonical(board):
    """The lexicographically smallest of the 8 rotations/mirrors."""
    return min(tuple(board[t[i]] for i in range(9)) for t in _TABLES)


# ------------------------------------------------------- the test opponents
#
# These three players grade every brain with the same scorecard.
# The stronger the opponent, the more your brain has to "know".

def random_move(board):
    """Randomo: plays a uniformly random empty square."""
    return random.choice(legal_moves(board))


def greedy_move(board, player):
    """Greedy: win now if possible, otherwise block, then center/corner/edge."""
    for move in legal_moves(board):
        if winner(play(board, move, player)) == player:
            return move
    foe = opponent(player)
    for move in legal_moves(board):
        if winner(play(board, move, foe)) == foe:
            return move
    if board[CENTER] == EMPTY:
        return CENTER
    for group in (CORNERS, EDGES):
        options = [m for m in legal_moves(board) if m in group]
        if options:
            return random.choice(options)
    return random.choice(legal_moves(board))


# Minimax, the perfect player: it looks at every possible future.
# Values are memoized (remembered) so it is only solved once -- after that
# it answers in a split second. Value: +1 = this player wins,
# 0 = draw, -1 = this player loses (both sides playing perfectly).
_perfect_value = {}


def perfect_value(board, player):
    key = (board, player)
    if key in _perfect_value:
        return _perfect_value[key]

    won = winner(board)
    if won:
        value = 1 if won == player else -1
    elif is_full(board):
        value = 0
    else:
        value = -1
        for move in legal_moves(board):
            reply = -perfect_value(play(board, move, player), opponent(player))
            if reply > value:
                value = reply
                if value == 1:      # can't do better than a win
                    break
    _perfect_value[key] = value
    return value


def perfect_move(board, player):
    """Minimax's move: win if possible, otherwise hold the draw."""
    # After my move it is the FOE's turn, so the value of the new position
    # for me is -perfect_value(new_board, foe).
    foe = opponent(player)
    for move in legal_moves(board):
        if -perfect_value(play(board, move, player), foe) == 1:
            return move
    for move in legal_moves(board):
        if -perfect_value(play(board, move, player), foe) == 0:
            return move
    return legal_moves(board)[0]


# ------------------------------------------------------------- a whole game

def play_game(x_move_fn, o_move_fn):
    """Play one full game between two move-picking functions. Returns X, O or 'draw'."""
    board, player = (EMPTY,) * 9, X
    while True:
        fn = x_move_fn if player == X else o_move_fn
        board = play(board, fn(board, player), player)
        won = winner(board)
        if won:
            return won
        if is_full(board):
            return "draw"
        player = opponent(player)


# ------------------------------------------------------- the scorecard test

def self_test(name, choose_move, games=20):
    """
    Play `games` games (once as X, once as O) against each test opponent
    and print a scorecard. Returns the same numbers as a dict for export.
    """
    opponents = {
        "Randomo": lambda b, p: random_move(b),
        "Greedy": greedy_move,
        "Minimax": perfect_move,
    }
    print("\n=== %s: scorecard (%d games per side) ===" % (name, games))
    results = {}
    for opp_name, opp_fn in opponents.items():
        score = {"win": 0, "draw": 0, "loss": 0}
        for _ in range(games):
            for side in (X, O):
                outcome = play_game(choose_move, opp_fn) if side == X \
                    else play_game(opp_fn, choose_move)
                if outcome == side:
                    score["win"] += 1
                elif outcome == "draw":
                    score["draw"] += 1
                else:
                    score["loss"] += 1
        results[opp_name] = score
        print("  vs %-8s  win %3d   draw %3d   loss %3d"
              % (opp_name, score["win"], score["draw"], score["loss"]))
    print()
    return results


# -------------------------------------------------------- saving the brain
#
# Each brain file calls export_brain(...). This writes TWO files:
#   brains/<name>.json  -- for you to read
#   brains/<name>.js    -- the same data, loaded by index.html
# (The .js twin lets index.html work when you simply double-click it,
# no server needed.)

BRAINS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brains")


def export_brain(name, data):
    os.makedirs(BRAINS_DIR, exist_ok=True)
    with open(os.path.join(BRAINS_DIR, name + ".json"), "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    js = ("window.BRAINS_DATA = window.BRAINS_DATA || {};\n"
          "window.BRAINS_DATA[%r] = %s;\n" % (name, json.dumps(data)))
    with open(os.path.join(BRAINS_DIR, name + ".js"), "w") as f:
        f.write(js)
    print("saved -> brains/%s.json and brains/%s.js" % (name, name))
