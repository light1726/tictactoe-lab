"""
BRAIN 1: LOGIC -- "the computer knows what YOU told it."

How it works
------------
You write an ORDERED list of IF-THEN rules. The brain checks the rules
from top to bottom and uses the FIRST rule that applies.

No searching, no learning, no randomness -- just your rules, in order.

MAKE it yours: edit the RULES list in CONFIG below, then run:

    python3 heuristics.py

The script grades your brain against three opponents and saves it for
index.html. Open index.html to play against it.

Ideas to try
------------
  * The default is missing the "block their line" rule -- on purpose, for
    the classroom demo: add it back (in the Make tab or here) and watch the
    scorecard recover.
  * Move "take the center" ABOVE "block their line" and watch the
    brain forget how to defend.
  * Add "take the opposite corner" somewhere in the list. Does it help
    against Minimax?
"""

import board
from board import X, O, EMPTY, legal_moves, play, winner, self_test, export_brain

CONFIG = {
    # The rules are checked in ORDER: the first one that applies decides.
    # Actions: "finish my line", "block their line", "take the center",
    #          "take the opposite corner", "take a corner", "take an edge",
    #          "take any square"
    "rules": [
        "finish my line",
        # "block their line",   # <- removed! add it back during class to
        #                        show what one rule can do: IF the opponent
        #                        has two in a line THEN play the blocking square
        "take the center",
        "take a corner",
        "take an edge",
        # try adding this one:
        # "take the opposite corner",
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
    for action in CONFIG["rules"]:
        moves = rule_moves(b, p, action)
        if moves:
            return moves[0]          # ties: lowest cell number wins
    return legal_moves(b)[0]


if __name__ == "__main__":
    results = self_test("Heuristics brain", choose_move, games=20)
    export_brain("heuristics", {
        "method": "heuristics",
        "config": {
            "mode": "priority",
            "rules": list(CONFIG["rules"]),
        },
        "scorecard": results,
    })
