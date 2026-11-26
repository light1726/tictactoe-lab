"""
BRAIN 4: REINFORCEMENT LEARNING -- "the computer is born knowing nothing,
and learns by playing thousands of games."

How it works
------------
The brain keeps a big table: for every position it has ever seen, a
number for each move -- the Q-value, meaning "how good do I think this
move is here?" Every position starts unknown (value 0).

Each training game it:
  1. Picks moves it currently believes in... but sometimes
     (with probability `exploration`) plays a random move instead,
     to discover new ideas.
  2. At the end it gets a reward: +1 win, 0 draw, -1 loss.
  3. It walks the game backwards and nudges the Q-values toward the
     reward, using the Q-learning update (see the comment in the code).

Over thousands of games the Q-values slowly become real knowledge.

MAKE it yours: edit CONFIG below, then run:

    python3 rl.py

Ideas to try
------------
  * exploration = 0.0 -> the brain never experiments. Does it get stuck
    on its first idea? (Try it early: episodes = 2000.)
  * rewards: draw = 8 -> winning and drawing look similar... lazy brain?
  * train_against = "greedy" -> learn to beat a smarter opponent.
  * train_against = "minimax" -> train against a PERFECT player. Then
    check the scorecard: the brain draws Minimax but may lose to Randomo!
    (It learned to expect perfect replies, so random moves surprise it.)
  * train_against = "self" -> the brain plays against itself. No teacher
    needed at all.
  * train_against = "mix" -> each game a random partner (random, greedy or
    minimax). The all-rounder recipe: it wins vs Randomo, mostly draws
    Greedy, and still draws Minimax every single game.

Note: the brain practices both sides of the board. To use ONE table for
both, it uses the "mirror trick": when it plays O, every X and O on the
board is swapped, so the position looks like an X-position again.
(See state_key below.)
"""

import random

import board
from board import X, O, EMPTY, legal_moves, play, winner, is_full, \
    opponent, random_move, greedy_move, perfect_move, canonical, \
    self_test, export_brain

CONFIG = {
    # How many training games to play.
    "episodes": 50000,

    # Q-learning update:  Q = Q + learning_rate * (target - Q)
    # Bigger = believe each new experience more strongly.
    "learning_rate": 0.2,

    # How much to care about FUTURE reward vs immediate reward (0..1).
    "discount": 0.9,

    # Exploration: how often to play a RANDOM move instead of the
    # believed-best one. This is the STARTING value — it fades toward 0.01
    # as the brain gains experience. (Early on it must explore to discover
    # ideas; near the end it should mostly use what it learned.)
    "exploration": 0.5,

    # What the game result is worth.
    "rewards": {"win": +10, "draw": 0, "loss": -10},

    # Who the brain trains against:
    # "random" | "greedy" | "self" | "minimax" | "mix"
    # ("mix" picks a random partner for each game: it practices against
    #  messy, tricky AND perfect opponents — the all-rounder recipe.)
    "train_against": "mix",

    # Record a point of the learning curve every this many games.
    "log_every": 5000,
}

# The Q-table: position -> {move: value}.  Position keys are canonical
# (rotations and mirrors count as the SAME position, so the table stays
# 8x smaller).  The brain always thinks of itself as X (mirror trick).
Q = {}


def state_key(b, p):
    """Same board viewed as an X-position: swap marks if we are O, then
    fold all 8 rotations/mirrors into one canonical form."""
    if p == O:
        swap = {X: O, O: X, EMPTY: EMPTY}
        b = tuple(swap[c] for c in b)
    return "".join(canonical(b))


def q_values(b, p):
    return Q.setdefault(state_key(b, p), {})


def best_known_move(b, p):
    """Greedy on the Q-table: the highest-valued move we know so far."""
    moves = legal_moves(b)
    qs = q_values(b, p)
    best = max(qs.get(m, 0) for m in moves)
    return random.choice([m for m in moves if qs.get(m, 0) == best])


_partner_mode = CONFIG["train_against"]


def opponent_move(b, p):
    """The training partner's reply, chosen by CONFIG["train_against"]."""
    mode = _partner_mode
    if mode == "random":
        return random_move(b)
    if mode == "greedy":
        return greedy_move(b, p)
    if mode == "minimax":
        return perfect_move(b, p)
    if mode == "self":
        return best_known_move(b, p)     # the same Q-table, both sides
    raise ValueError("unknown training partner: %r" % mode)


def current_exploration(episode, total):
    """Exploration fades from its start value toward 0.02 during training."""
    eps = CONFIG["exploration"] * (1 - episode / total)
    return max(0.01, eps)


def play_episode(brain_player, eps):
    """One training game in which the brain plays as `brain_player`."""
    b = (EMPTY,) * 9
    player = X
    path = []
    while True:
        if player == brain_player:
            # --- the brain's move ------------------------------------
            key = state_key(b, player)
            if random.random() < eps:
                move = random.choice(legal_moves(b))
            else:
                move = best_known_move(b, player)
            path.append((key, move))
        else:
            # --- the training partner's reply -------------------------
            move = opponent_move(b, player)
        b = play(b, move, player)

        won = winner(b)
        if won:
            reward = CONFIG["rewards"]["win"] if won == brain_player \
                else CONFIG["rewards"]["loss"]
            return path, reward
        if is_full(b):
            return path, CONFIG["rewards"]["draw"]
        player = opponent(player)


def learn(path, reward):
    """Walk the game backwards, nudging every Q-value toward the reward.

    Q(s,a) <- Q(s,a) + alpha * ( target - Q(s,a) )
    where target = reward for the last move, and for earlier moves
    target = gamma * value of the position we actually reached next.
    """
    target = reward
    for key, move in reversed(path):
        qs = Q.setdefault(key, {})
        qs[move] = qs.get(move, 0) + CONFIG["learning_rate"] * (target - qs.get(move, 0))
        target *= CONFIG["discount"]


def win_rate_vs_random(games=100):
    """Win rate against Randomo, playing half the games as X and half as O."""
    wins = 0
    half = games // 2
    for _ in range(half):
        if board.play_game(lambda b, p: best_known_move(b, p),
                           lambda b, p: random_move(b)) == X:
            wins += 1
    for _ in range(games - half):
        if board.play_game(lambda b, p: random_move(b),
                           lambda b, p: best_known_move(b, p)) == O:
            wins += 1
    return wins / games


def train():
    global Q, _partner_mode
    Q = {}
    curve = []
    total = CONFIG["episodes"]
    for episode in range(1, total + 1):
        # Alternate roles so the brain practices BOTH sides of the board.
        if CONFIG["train_against"] == "mix":
            # A different training partner for each game.
            _partner_mode = random.choice(["random", "greedy", "minimax"])
        eps = current_exploration(episode, total)
        path, reward = play_episode(X if episode % 2 == 1 else O, eps)
        learn(path, reward)
        if episode % CONFIG["log_every"] == 0:
            curve.append([episode, round(win_rate_vs_random(), 2)])
            print("  episode %6d   win rate vs Randomo: %.2f" % tuple(curve[-1]))
    return curve


if __name__ == "__main__":
    print("Training %d episodes against %s..."
          % (CONFIG["episodes"], CONFIG["train_against"]))
    curve = train()
    print("\nThe Q-table now contains %d different positions." % len(Q))

    results = self_test("RL brain", lambda b, p: best_known_move(b, p), games=20)

    export_brain("rl", {
        "method": "rl",
        "config": {
            "episodes": CONFIG["episodes"],
            "learning_rate": CONFIG["learning_rate"],
            "discount": CONFIG["discount"],
            "exploration": CONFIG["exploration"],
            "rewards": CONFIG["rewards"],
            "train_against": CONFIG["train_against"],
        },
        "qtable": {key: {str(m): v for m, v in qs.items()} for key, qs in Q.items()},
        "positions_learned": len(Q),
        "learning_curve": curve,
        "scorecard": results,
    })
