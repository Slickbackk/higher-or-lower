# Higher or Lower - Number Guessing Game

A Python number guessing game with difficulty levels, proximity hints, persistent
high scores, and an optional adversarial mode that forces optimal binary search.

## How to Play

```bash
python src/guessing_game.py
```

1. Pick a difficulty:

   | # | Name   | Range  | Attempts |
   |---|--------|--------|----------|
   | 1 | easy   | 1-50   | 8        |
   | 2 | medium | 1-100  | 7        |
   | 3 | hard   | 1-500  | 9        |
   | 4 | insane | 1-1000 | 10       |

2. Choose whether to enable **adversarial mode**.
3. Guess. After each guess you get:
   - `too high` / `too low`
   - the current valid range (narrowed by your prior guesses)
   - a proximity hint: `burning hot`, `very hot`, `hot`, `warm`, `cool`, `cold`
     (honest mode only)
4. At the end of the round you get a score; play again to accumulate a session total.

Type `q` at any guess prompt to quit the round.

## Adversarial mode

The computer does **not** pick a number at the start. It keeps the full set of
possibilities and, on each guess, answers in whatever direction keeps the larger
set alive. Proximity hints are disabled (there's no committed number to compare
to). Maximum attempts at each difficulty are tuned so optimal play is required
to win. Score is doubled.

## Scoring

Per round: `(attempts_remaining + 1) * range_max / 10`, doubled in adversarial
mode. Best score per difficulty is persisted to `src/highscores.json`.

## Project Structure

```
higher-or-lower/
├── README.md
└── src/
    ├── guessing_game.py
    └── highscores.json   (created on first win)
```

## Requirements

- Python 3.x (standard library only)
