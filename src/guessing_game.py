import json
import random
from pathlib import Path

HIGHSCORE_PATH = Path(__file__).with_name("highscores.json")

DIFFICULTIES = {
    "1": ("easy",   50,    8),
    "2": ("medium", 100,   7),
    "3": ("hard",   500,   9),
    "4": ("insane", 1000, 10),
}


def load_highscores():
    if not HIGHSCORE_PATH.exists():
        return {}
    try:
        return json.loads(HIGHSCORE_PATH.read_text())
    except json.JSONDecodeError:
        return {}


def save_highscores(scores):
    HIGHSCORE_PATH.write_text(json.dumps(scores, indent=2))


def proximity_hint(guess, secret, range_max):
    ratio = abs(guess - secret) / range_max
    if ratio < 0.02:
        return "burning hot"
    if ratio < 0.05:
        return "very hot"
    if ratio < 0.10:
        return "hot"
    if ratio < 0.20:
        return "warm"
    if ratio < 0.35:
        return "cool"
    return "cold"


def pick_difficulty():
    print("\nDifficulty:")
    print("  1) easy    1-50    8 attempts")
    print("  2) medium  1-100   7 attempts")
    print("  3) hard    1-500   9 attempts")
    print("  4) insane  1-1000  10 attempts")
    while True:
        choice = input("Pick 1-4: ").strip()
        if choice in DIFFICULTIES:
            return DIFFICULTIES[choice]
        print("Please enter 1, 2, 3, or 4.")


def ask_adversarial():
    raw = input(
        "Adversarial mode? Computer doesn't commit to a number and answers to drag\n"
        "the game out as long as possible. Forces optimal play. [y/N]: "
    ).strip().lower()
    return raw in ("y", "yes")


def read_guess(low, high, attempts_left):
    while True:
        raw = input(
            f"Your guess [{low}-{high}, {attempts_left} left, q to quit]: "
        ).strip().lower()
        if raw in ("q", "quit", "exit"):
            return None
        try:
            guess = int(raw)
        except ValueError:
            print("  -> not a number, try again.")
            continue
        if not low <= guess <= high:
            print(f"  -> out of range. Stay between {low} and {high}.")
            continue
        return guess


class HonestGame:
    def __init__(self, range_max):
        self.secret = random.randint(1, range_max)

    def answer(self, guess):
        if guess == self.secret:
            return "correct"
        return "low" if guess < self.secret else "high"

    def reveal(self):
        return self.secret


class AdversarialGame:
    def __init__(self, range_max):
        self.candidates = set(range(1, range_max + 1))

    def answer(self, guess):
        lower = {n for n in self.candidates if n < guess}
        higher = {n for n in self.candidates if n > guess}
        if not lower and not higher:
            return "correct"
        if len(lower) >= len(higher):
            self.candidates = lower
            return "high"
        self.candidates = higher
        return "low"

    def reveal(self):
        return random.choice(list(self.candidates)) if self.candidates else None


def play_round(difficulty, adversarial):
    name, range_max, max_attempts = difficulty
    game = AdversarialGame(range_max) if adversarial else HonestGame(range_max)

    tag = " [adversarial]" if adversarial else ""
    print(f"\n--- {name}{tag} ---")
    print(f"Number between 1 and {range_max}. {max_attempts} attempts.\n")

    low, high = 1, range_max
    for attempt in range(1, max_attempts + 1):
        guess = read_guess(low, high, max_attempts - attempt + 1)
        if guess is None:
            print("Quit round.")
            return 0

        result = game.answer(guess)
        if result == "correct":
            remaining = max_attempts - attempt
            score = (remaining + 1) * range_max // 10
            if adversarial:
                score *= 2
            print(f"\nGot it in {attempt}! +{score}")
            return score

        if result == "low":
            low = max(low, guess + 1)
            arrow = "too low"
        else:
            high = min(high, guess - 1)
            arrow = "too high"

        suffix = ""
        if not adversarial:
            suffix = f" ({proximity_hint(guess, game.secret, range_max)})"
        print(f"  -> {arrow}{suffix}. Range now {low}-{high}.\n")

    print(f"\nOut of attempts. The number was {game.reveal()}.")
    return 0


def main():
    print("=== Number Guessing Game ===")
    highscores = load_highscores()
    total = 0

    while True:
        difficulty = pick_difficulty()
        adversarial = ask_adversarial()
        score = play_round(difficulty, adversarial)
        total += score

        key = difficulty[0] + (" [adv]" if adversarial else "")
        best = highscores.get(key, 0)
        if score > best:
            print(f"New best for {key}: {score} (was {best}).")
            highscores[key] = score
            save_highscores(highscores)
        elif score:
            print(f"Best for {key}: {best}.")

        print(f"Session total: {total}")
        again = input("\nPlay again? [Y/n]: ").strip().lower()
        if again in ("n", "no", "q", "quit"):
            break

    print(f"\nFinal session total: {total}. Bye!")


if __name__ == "__main__":
    main()
