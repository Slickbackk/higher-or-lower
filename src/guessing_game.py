import random

print("=== Number Guessing Game ===")
print("I'm thinking of a number between 1 and 100.")

secret = random.randint(1, 100)
attempts = 0

while True:
    guess = input("Your guess: ")

    if not guess.isdigit():
        print("Please enter a valid number.")
        continue

    guess = int(guess)
    attempts += 1

    if guess < secret:
        print("Too low! Try again.")
    elif guess > secret:
        print("Too high! Try again.")
    else:
        print(f"You got it in {attempts} attempts!")
        break
