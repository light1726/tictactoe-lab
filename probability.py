"""
BRAIN 2: PROBABILITY -- "the computer plays dice, then counts."

How it works
------------
The brain knows NOTHING about strategy. For each empty square it just
IMAGINES the game: it places its mark there, finishes the game many times
with random moves (the "simulations"), and counts how often it wins,
draws and loses. It plays the square with the best score.

This is called Monte Carlo simulation: rolling dice many times and
counting outcomes instead of trying to reason about the game.

MAKE it yours: edit CONFIG below, then run:

    python3 probability.py

Ideas to try
------------
  * simulations = 10  -> the brain is noisy. Run twice: does it change
    its opening move? Then try 1000 and watch it settle down.
  * Change the score: make "draw" worth 0.8. The brain stops gambling
    and plays not-to-lose. Make "win" worth 3 and it goes for glory.
  * imagined_player = "greedy": the brain now dreams about a smart
    opponent instead of a random one. Watch how its opinion changes.
    (A brain is only as smart as the games it imagines!)
"""

import board
from board import X, O, EMPTY, legal_moves, play, winner, is_full, \
    opponent, random_move, greedy_move, self_test, export_brain

CONFIG = {
    # How many random games to imagine for EACH candidate move.
    "simulations": 200,

    # How to turn the imagined results into a score for a move.
    # score = wins * win + draws * draw + losses * loss
    "score": {"win": +1, "draw": 0, "loss": -1},

    # Who plays inside the imagined games: "random" or "greedy".
    "imagined_player": "random",
}


def imagined_move(b, p):
    if CONFIG["imagined_player"] == "random":
        return random_move(b)
    return greedy_move(b, p)


def playout(b, p):
    """Finish the game with imagined moves; return X, O or 'draw'."""
    while True:
        won = winner(b)
        if won:
            return won
        if is_full(b):
            return "draw"
        b = play(b, imagined_move(b, p), p)
        p = opponent(p)


def score_of_move(b, p, move):
    """Imagine `simulations` games after playing `move`; return its score."""
    b_after = play(b, move, p)
    nxt = opponent(p)
    tally = {"win": 0, "draw": 0, "loss": 0}
    for _ in range(CONFIG["simulations"]):
        result = playout(b_after, nxt)
        if result == p:
            tally["win"] += 1
        elif result == "draw":
            tally["draw"] += 1
        else:
            tally["loss"] += 1
    w = CONFIG["score"]
    return w["win"] * tally["win"] + w["draw"] * tally["draw"] + w["loss"] * tally["loss"]


def choose_move(b, p):
    """Score every empty square and play the best one."""
    best_move, best_score = None, None
    for move in legal_moves(b):
        s = score_of_move(b, p, move)
        if best_score is None or s > best_score:
            best_move, best_score = move, s
    return best_move


if __name__ == "__main__":
    results = self_test("Probability brain", choose_move, games=15)
    export_brain("probability", {
        "method": "probability",
        "config": {
            "simulations": CONFIG["simulations"],
            "score": CONFIG["score"],
            "imagined_player": CONFIG["imagined_player"],
        },
        "scorecard": results,
    })
