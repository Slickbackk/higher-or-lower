import random

MAX_ATTEMPTS = 10
RANGE_MAX = 1000

print("=== Number Guessing Game ===")
print(f"I'm thinking of a number between 1 and {RANGE_MAX}.")
print(f"You have {MAX_ATTEMPTS} attempts. Good luck!\n")

secret = random.randint(1, RANGE_MAX)
attempts = 0

while attempts < MAX_ATTEMPTS:
    remaining = MAX_ATTEMPTS - attempts
    guess = input(f"Your guess [{remaining} attempt{'s' if remaining != 1 else ''} left]: ")

    if not guess.isdigit():
        print("Please enter a valid number.")
        continue

    guess = int(guess)
    attempts += 1

    if guess == secret:
        print(f"\nYou got it in {attempts} attempt{'s' if attempts != 1 else ''}!")
        break

    if attempts == MAX_ATTEMPTS:
        print(f"\nGame over! The number was {secret}.")
    elif guess < secret:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")
