"""
BRAIN 3: SEARCH -- "the computer looks into the future."

How it works
------------
The brain imagines every possible move, then every possible reply,
then every reply to that... building a tree of futures. Finished games
are scored (+1000 win, -1000 loss, 0 draw). Positions that are still
unfinished at the search horizon are scored by the EVALUATION function:
your best guess of how good a position looks. The brain assumes the
opponent always picks the reply that is worst for it, and climbs the
tree to the move with the best guaranteed outcome. (Minimax.)

Depth is the key: at depth 1 the evaluation does ALL the thinking; at
depth 9 (the full game) the evaluation barely matters -- only the real
endings count. Alpha-beta skips branches that cannot change the answer,
so it explores far fewer nodes but returns the exact same move.

MAKE it yours: edit CONFIG below, then run:

    python3 search.py

Ideas to try
------------
  * depth = 1  -> the brain is now "blind": it judges positions only by
    the evaluation. Is it still hard to beat?
  * alpha_beta = False -> same moves, but watch the node counter explode.
  * Zero out "open_lines" and "two_in_a_row". At depth 9 the brain is
    STILL perfect (only finished games matter). At depth 1 it falls apart.
  * Find the smallest depth where your brain still beats Greedy.
"""

import random

import board
from board import X, O, EMPTY, legal_moves, play, winner, is_full, \
    opponent, self_test, export_brain

CONFIG = {
    # How many half-moves ahead to look. 9 = until every game finishes.
    "depth": 9,

    # Skip parts of the tree that cannot change the answer?
    "alpha_beta": True,

    # Caution (0-100): how carefully it plays. 100 = it never slips and can
    # never lose. Lower = sometimes it plays a random square instead of its
    # best move -- the AI becomes beatable (and more fun to play against).
    "caution": 100,

    # The evaluation: how good an UNFINISHED position looks for me.
    #   open_lines:   each line I could still win  (+1 each)
    #   two_in_a_row: a line where I already have two (extra points)
    #   center:       I hold the center square
    # It is always: me minus you (so a good position for you is bad for me).
    "evaluation": {
        "open_lines": 1,
        "two_in_a_row": 5,
        "center": 2,
    },
}

# A finished game is worth far more than any evaluation of an unfinished one.
WIN_SCORE = 1000

nodes = 0   # how many positions the last search looked at


def evaluate(b, p):
    """Guess how good this unfinished position is for player p."""
    e = CONFIG["evaluation"]
    foe = opponent(p)

    def open_lines(pl):
        return sum(1 for line in board.LINES if all(b[i] != opponent(pl) for i in line))

    def two_in_lines(pl):
        return sum(
            1 for line in board.LINES
            if sum(1 for i in line if b[i] == pl) == 2
            and all(b[i] != opponent(pl) for i in line)
        )

    score = e["open_lines"] * (open_lines(p) - open_lines(foe))
    score += e["two_in_a_row"] * (two_in_lines(p) - two_in_lines(foe))
    if b[board.CENTER] == p:
        score += e["center"]
    elif b[board.CENTER] == foe:
        score -= e["center"]
    return score


def negamax(b, p, depth, alpha, beta):
    """Best score p can guarantee from b, looking `depth` half-moves ahead."""
    global nodes
    nodes += 1

    won = winner(b)
    if won:
        return WIN_SCORE if won == p else -WIN_SCORE
    if is_full(b):
        return 0
    if depth == 0:
        return evaluate(b, p)

    # Look at strong-looking moves first: it makes alpha-beta prune more.
    ordered = sorted(legal_moves(b), key=lambda m: 0 if m == board.CENTER else 1)

    best = -10 ** 9
    for move in ordered:
        value = -negamax(play(b, move, p), opponent(p), depth - 1, -beta, -alpha)
        if value > best:
            best = value
        if CONFIG["alpha_beta"]:
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break   # the rest of this branch can't matter
    return best


def choose_move(b, p):
    """Search every first move and pick the one with the best guaranteed score."""
    global nodes
    nodes = 0
    best_move, best_value = None, None
    for move in legal_moves(b):
        value = -negamax(play(b, move, p), opponent(p), CONFIG["depth"] - 1,
                         -10 ** 9, 10 ** 9)
        if best_value is None or value > best_value:
            best_move, best_value = move, value
    # Caution: occasionally slip and play a random square instead.
    if random.random() * 100 >= CONFIG["caution"]:
        return random.choice(legal_moves(b))
    return best_move


if __name__ == "__main__":
    # Fewer test games than usual: searching every move takes a moment.
    results = self_test("Search brain", choose_move, games=6)
    # How big is a full search? Count positions visited for the empty board.
    nodes = 0
    choose_move((EMPTY,) * 9, X)
    print("(one full search from the empty board visits %d positions)" % nodes)
    export_brain("search", {
        "method": "search",
        "config": {
            "depth": CONFIG["depth"],
            "alpha_beta": CONFIG["alpha_beta"],
            "caution": CONFIG["caution"],
            "evaluation": CONFIG["evaluation"],
        },
        "scorecard": results,
    })
