from random import choice


def run_game():
    words: list[str] = ["hello", "banana", "apple", "code", "computer"]
    word: str = choice(words)

    username: str = input("What is your name? >> ")
    print(f"Welcome to Hangman, {username}! :)")

    # Setup
    guessed: str = ""
    tries: int = 7

    while tries > 0:
        blanks: int = 0
        print("Word: ", end="")

        for char in word:
            if char in guessed:
                print(char, end=" ")
            else:
                print('_', end=" ")
                blanks += 1
        print()  # Adds a blank line

        # no letter to guess the user won
        if blanks == 0:
            print("You save me!")
            break

        guess: str = input("Enter a letter >> ")
        if guess in guessed:
            print(f"You already used '{guess}' please try another letter.")
            continue  # Forgiven

        guessed += guess
        if guess not in word:
            tries -= 1
            print(f"Sorry, that was wrong... ({tries} tries remaining)")
            if tries == 0:
                print(f"No more tries remaining you lose!")
                break
