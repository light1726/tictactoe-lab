"""
BRAIN 1: HEURISTICS -- "the computer knows what YOU told it."

How it works
------------
You write a list of RULES. Each rule is (points, action).
For every empty square, the brain adds up the points of every rule
that likes that square. It plays the square with the most points.

No searching, no learning, no randomness -- just your rules.

MAKE it yours: edit the RULES list in CONFIG below, then run:

    python3 heuristics.py

The script grades your brain against three opponents and saves it for
index.html. Open index.html to play against it.

Ideas to try
------------
  * Remove the "block their line" rule. What happens to the scorecard?
  * Give "block their line" MORE points than "finish my line".
    Does the brain still win games it should win?
  * Add a rule: (15, "take the opposite corner"). Does it help vs Minimax?
  * Switch "mode" to "priority": now the FIRST rule that matches wins,
    and the ORDER of the rules matters. Move "take the center" above
    "block their line" and watch the brain forget how to defend.
"""

import board
from board import X, O, EMPTY, legal_moves, play, winner, self_test, export_brain

CONFIG = {
    # "points": every rule votes, highest total wins.
    # "priority": the first rule in the list that applies wins.
    "mode": "points",

    # Your rules. Each one: (points, action).
    # Actions: "finish my line", "block their line", "take the center",
    #          "take the opposite corner", "take a corner", "take an edge",
    #          "take any square"
    "rules": [
        (100, "finish my line"),
        (90,  "block their line"),
        (10,  "take the center"),
        (5,   "take a corner"),
        (2,   "take an edge"),
        # try adding this one:
        # (15, "take the opposite corner"),
    ],
}


def rule_moves(b, p, action):
    """Which squares does this action like? Empty list = it doesn't apply."""
    lm = legal_moves(b)
    foe = board.opponent(p)

    if action == "finish my line":
        return [m for m in lm if winner(play(b, m, p)) == p]

    if action == "block their line":
        return [m for m in lm if winner(play(b, m, foe)) == foe]

    if action == "take the center":
        return [board.CENTER] if board.CENTER in lm else []

    if action == "take the opposite corner":
        # If the opponent owns exactly one corner, take the corner opposite it.
        their_corners = [c for c in board.CORNERS if b[c] == foe]
        if len(their_corners) == 1:
            opposite = 8 - their_corners[0]   # 0<->8, 2<->6, 4<->4
            return [opposite] if opposite in lm else []
        return []

    if action == "take a corner":
        return [m for m in lm if m in board.CORNERS]

    if action == "take an edge":
        return [m for m in lm if m in board.EDGES]

    if action == "take any square":
        return lm

    raise ValueError("unknown action: %r" % action)


def choose_move(b, p):
    """The brain's one job: pick a move for player p on board b."""
    rules = CONFIG["rules"]

    if CONFIG["mode"] == "points":
        scores = {m: 0 for m in legal_moves(b)}
        for points, action in rules:
            for m in rule_moves(b, p, action):
                scores[m] += points
        return max(scores, key=scores.get)   # ties: lowest cell number wins

    # "priority" mode: first rule that applies decides.
    for _points, action in rules:
        moves = rule_moves(b, p, action)
        if moves:
            return moves[0]
    return legal_moves(b)[0]


if __name__ == "__main__":
    results = self_test("Heuristics brain", choose_move, games=20)
    export_brain("heuristics", {
        "method": "heuristics",
        "config": {
            "mode": CONFIG["mode"],
            "rules": [list(rule) for rule in CONFIG["rules"]],
        },
        "scorecard": results,
    })
