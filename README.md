# Tic-Tac-Toe Lab

Four brains, one game. Each brain plays perfect Tic-Tac-Toe… no wait — each brain
plays Tic-Tac-Toe **its own way**, and the whole point is to look inside their heads
and see where their "cleverness" comes from.

| Brain | File | Where its knowledge comes from |
|---|---|---|
| Logic | `heuristics.py` | **Facts and IF–THEN rules a human wrote** — every square gets points from your rules |
| Probability | `probability.py` | **Statistics** — it rolls dice, imagines random games, counts outcomes |
| Search | `search.py` | **Looking ahead** — it plays out every possible future |
| RL | `rl.py` | **Experience** — it starts blank and learns from thousands of games |

One game, four different sources of knowledge. The lab is built around the question:
*where does the computer's cleverness actually come from?*

## Quick start

1. Build the brains (from this folder, in a terminal):

   ```bash
   python3 heuristics.py
   python3 probability.py
   python3 search.py
   python3 rl.py
   ```

   Each prints a scorecard and saves itself to `brains/`. (This takes a few seconds;
   `rl.py` is the longest at ~1 second of training.)
   Ready-made brains are already in `brains/`, so you can skip this step at first.

2. Open **`index.html`** — double-click it, or run:

   ```bash
   python3 -m http.server 8000
   # then open http://localhost:8000/index.html
   ```

3. Play! Then edit a brain and do it again.

## The playground

- **Play** — pick an AI (Logic, Probability, Search or RL), play as X or O.
  After every AI move, the purple panel walks through its thinking **step by
  step**, in the same four-step shape as the course slides: the facts → how it
  reasoned → the scores/values → the decision.
- **Make** — keep it simple. Logic lets you edit the rule list (reorder, add /
  remove). Probability has one knob, the simulated games per move;
  Search has one knob, the look-ahead depth; RL has training games, learning
  rate and a **Train now!** button that trains it live in the browser and
  draws its learning curve. **Apply** makes the Play tab use your version
  (marked ✏️); **Reset to default** brings the original back.

## PLAY → THINK → MAKE → REFLECT

### Logic (`heuristics.py`)

- **PLAY** a game or two against it. It never loses — annoying, right?
- **THINK** the purple panel shows the rules being checked in order, with a ✓
  on the first rule that applies. All of its smarts are *your* rules, nothing more.
- **MAKE** edit the `rules` list inside `CONFIG` at the top of the file — the
  rules are checked top to bottom and the first one that applies decides:
  * Delete the `"block their line"` rule → rerun → check the scorecard. It's broken!
  * Move `"take the center"` ABOVE `"block their line"` → it forgets to defend.
  * Add `"take the opposite corner"` somewhere in the list → does it help vs Minimax?
- **REFLECT** where did this AI's knowledge come from? What happens in a
  situation no rule covers?

### Probability (`probability.py`)

- **PLAY** — it's beatable! But it clearly "wants" the center…
- **THINK** it imagines N random games after each move and counts wins/draws/losses
  (the W·D·L bars). It knows no strategy at all — only statistics.
- **MAKE** the `CONFIG`:
  * `simulations` 10 → noisy (reload and its opening changes). 1000 → confident.
  * `score` — make `draw` worth 0.8: it stops gambling, plays not-to-lose.
  * `imagined_player` `"greedy"` → it dreams of a smart opponent. The brain is only
    as smart as the games it imagines!
- **REFLECT** why is it weak against Greedy even though it beats Randomo?

### Search (`search.py`)

- **PLAY** — you cannot beat it. It is impossible to beat. (It's a solved game.)
- **THINK** the panel shows +1000 / 0 / −1000 for every move: win, draw, lose.
  It assumes *you* play perfectly too — which is why it never gambles.
- **MAKE** the `CONFIG`:
  * `depth` 1 → the brain goes almost blind (the evaluation does all the thinking now).
  * `alpha_beta` False → same moves, but watch the position counter explode
    (~23,000 positions with it on, ~550,000 without).
  * Zero out `evaluation` weights → at depth 9 it's *still* perfect (only real
    endings matter); at depth 1 it falls apart.
  * Find the smallest depth where your brain still beats Greedy.
- **REFLECT** why does it draw everything in the tournament? Why won't it trick you?

### RL (`rl.py`)

- **PLAY** — it's good… mostly. Walk it into a position it has never seen and watch
  it confess: "I have never seen this position before!"
- **THINK** the Q-values show how good it *believes* each move is. The learning
  curve shows it improving while it trained. It was born knowing nothing.
- **MAKE** the `CONFIG`:
  * `exploration` 0.0 → it never experiments, and gets stuck on its first idea.
  * `rewards` draw 0.5 → winning and drawing look alike… does it get lazy?
  * `train_against` `"greedy"` → it learns to beat a smarter teacher.
  * `train_against` `"minimax"` → then check the scorecard: it draws Minimax but
    *loses to Randomo*! It learned to expect perfect replies, so random moves
    surprise it.
  * `train_against` `"self"` → no teacher at all, it just plays against itself.
- **REFLECT** what did it learn that the other brains were *given*?

### After the tournament…

Why did **Search** finish with zero losses but almost no wins, while **Heuristics**
took the crown? (Search assumes everyone plays perfectly — it never gambles.
Heuristics happily beats the weak brains.) Which brain's cleverness is easiest to
explain? Which one feels the most "alive"?

### RL recipes that actually work

Community-tested Q-learning recipes for Tic-Tac-Toe (all fit the Make tab's knobs;
γ = 0.9 and α = 0.3 work everywhere — the **training partner** is the real lever):

| Recipe | Train against | Episodes | ε | Rewards | What you get |
|---|---|---|---|---|---|
| Beat the weak | random | 30k | 0.3 → fades | +1 / 0 / −1 | crushes Randomo, loses to smart players |
| Beat Greedy | greedy | 30k | 0.3 → fades | +1 / 0 / −1 | ~25% wins, few losses vs Greedy — but worse vs Randomo |
| All-rounder | self | 100k | 0.9 → fades | +1 / 0 / −1 | strong vs Randomo, mostly draws vs Greedy |
| Never lose | minimax | 30k | 0.3 → fades | +1 / 0 / −1 | **draws Minimax 100%** — but brittle vs everyone else! |
| ⭐ Best overall | **mix** | 50k | 0.5 → fades | +1 / 0 / −1 | 34-4-2 vs Randomo · 33 draws vs Greedy · **draws Minimax 40/40** |

Two traps found in the wild: making a draw worth +0.5 (one published paper's recipe)
turned our agent lazy — 34 losses to Greedy. And the "train vs minimax" row: a perfect
teacher never lets you practice *winning* (it never leaves a win open) or casual
*blocking* (it kills you the instant you slip), so the brain is flawless against Minimax
yet clueless against messy players. The **mix** recipe (each game a random partner from
random/greedy/minimax) fixes exactly that — it practices everything, and it's the one
recipe that is strong against all three test opponents at once. RL specializes in its
practice partners — no single fixed partner is best at everything.
(Sources: [CRAN tictactoe](https://search.r-project.org/CRAN/refmans/tictactoe/html/ttt_qlearn.html), [fcarsten's tabular Q player](https://github.com/fcarsten/tic-tac-toe), [MDPI Q-learning paper](https://www.mdpi.com/2218-6581/15/3/50/pdf), [MauroLuzzatto self-play](https://github.com/MauroLuzzatto/learn-tictactoe-through-self-play), [IEEE 4×4 Q-learning paper](https://ieeexplore.ieee.org/document/11493322).)

## Files

```
board.py          the game, the test opponents, the scorecard & export helper
heuristics.py     brain 1 — rules with points
probability.py    brain 2 — Monte Carlo playouts
search.py         brain 3 — minimax + alpha-beta
rl.py             brain 4 — tabular Q-learning
index.html        the playground (open in a browser)
brains/*.json     exported brains (readable)
brains/*.js       same data, loaded by index.html (generated)
```

## Troubleshooting

- **"python3: command not found"** — try `python` instead. Any Python 3.6+ works.
- **A brain shows "not built" in the playground** — run its `.py` file, then reload the page.
- **Fonts look plain** — the page uses Google Fonts; offline it falls back to system fonts.
- **Everything plays but the scorecard is slow** — lower `simulations` in
  `probability.py`, or use fewer games on the slider.

## Where these ideas come from

- The priority rules (win → block → center → …) come from Allen Newell & Herbert
  Simon's 1972 analysis of how humans play Tic-Tac-Toe.
- The probability method is Monte Carlo simulation, in the spirit of Donald
  Michie's 1961 matchbox machine MENACE — beads in boxes, no strategy at all.
- Minimax/alpha-beta is the classic game-tree search (used in chess engines).
- The RL brain is Q-learning, the idea from Sutton & Barto's
  *Reinforcement Learning* book — whose very first example is Tic-Tac-Toe.

## License

Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) —
you may share and adapt this material for non-commercial use, with attribution,
under the same license. Fonts used by the playground are under the SIL Open
Font License (Fredoka, Nunito, DM Mono).

## Try it online

The playground is deployed at **https://light1726.github.io/tictactoe-lab/** —
play in the browser, train the RL brain with *Train now!*, and use the
Make tab without installing anything. For the full experience (editing the
Python brains), download this repository and run the `.py` files locally.
