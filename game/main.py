from game.words_file_handler import WordsFileHandler
from game.score_table import ScoreTable, User
import random
import re
import sys


class Game:
    words_path: str = "/Users/danielevi/Python/Projects/hangman/game/words.txt"
    score_table_path: str = "/Users/danielevi/Python/Projects/hangman/game/score.txt"

    def __init__(self):
        self.user: User = User(0, None)
        self.score_table = ScoreTable(Game.score_table_path)
        self.words_file_handler = None
        self.round = None
        self.total_points = 0

    def main_menu(self):

        def is_valid_option(number: str):
            pattern = '^[123]$'
            return bool(re.match(pattern, number))

        print()  # Adds a blank line
        self.user.username = input("Hello!, What is your name? >> ")
        print(f"Welcome to Hangman, {self.user.username}! :) \n")
        self.score_table.set_current_username_record(self.user)
        self.score_table.update_score_table_file()

        while True:
            try:
                menu: str = (
                    "* * * Menu * * *\n\n"
                    f"Username: {self.user.username}\n\n"
                    "1. New Game\n"
                    "2. Score Table\n"
                    "3. Exit\n\n"
                    "Please enter the number of the desired option >> "
                )

                user_option = input(menu)

                if is_valid_option(user_option):
                    match user_option:
                        case '1':
                            print()  # Adds a blank line
                            print("--------\n")
                            self.start_game()
                        case '2':
                            print()  # Adds a blank line
                            print(f"{self.score_table} \n")
                        case '3':
                            print(f"Thanks for playing {self.username}, see you next time ! :) \n")
                            sys.exit()

            except ValueError:
                print("Invalid input. Please enter an number from 1 to 3.")

    def start_game(self):
        self.words_file_handler = WordsFileHandler(Game.words_path, 0)
        self.round = Round(self.words_file_handler.get_new_word())
        while self.round.new_round():
            self.total_points += self.round.get_points()
            print(f"Username: {self.user.username} \nScore: {self.total_points}")
            self.round.level_up()
            self.round.reset()
            self.round.set_word(new_word=self.words_file_handler.get_new_word())
            self.round.difficulty()

        self.round = None
        self.words_file_handler = None
        user_record = self.score_table.get_current_user_record()
        if self.total_points > user_record.user.score:
            user_record.user.update_score(self.total_points)
            self.score_table.update_score_table_file()


class Round:
    def __init__(self, word):
        self.level = 1
        self.guessed: str = ""
        self.hangman = Hangman()
        self.word = word
        self.points = 0

    def difficulty(self):
        three_hints = [14, 17]  # 3 chars
        two_hints = [2, 5, 8, 11, 15, 18]  # 2 chars
        one_hints = [3, 6, 9, 12, 16, 19]  # 1 char

        if self.level in three_hints:
            self.guessed += ''.join(random.sample(self.word, 3))
        elif self.level in two_hints:
            self.guessed += ''.join(random.sample(self.word, 2))
        elif self.level in one_hints:
            self.guessed += random.choice(self.word)
        else:
            self.guessed = ""

    def get_points(self):
        if self.level == 1:
            self.points = 10
        elif 1 < self.level <= 4:
            self.points = 30
        elif 4 < self.level <= 7:
            self.points = 40
        elif 7 < self.level <= 10:
            self.points = 50
        elif 10 < self.level <= 13:
            self.points = 60
        elif 13 < self.level <= 16:
            self.points = 100
        elif 16 < self.level <= 19:
            self.points = 200
        elif self.level == 20:
            self.points = 1000
        else:
            self.points = 0
        return self.points

    def set_word(self, new_word):
        self.word = new_word

    def level_up(self):
        self.level += 1

    def reset(self):
        self.guessed = ""
        self.hangman.state = 0

    def new_round(self) -> bool:
        if self.level > 20:
            print(f"You won the game!")
            return True

        def is_valid_letter(letter):
            regex = '^[A-Za-z_][A-Za-z0-9_]*'
            if re.search(regex, letter):
                return True
            return False

        print()  # Adds a blank line
        print("Enter 'return' to return to the menu. ")
        print("Enter 'exit' to exit the game. ")
        print()  # Adds a blank line

        print(f"* * * Round number {self.level} * * *")
        print(self.hangman.get_current_hangman())

        wrong_guesses: list[str] = []
        while self.hangman.state < 7:
            blanks: int = 0
            print("Wrong guesses: ", *wrong_guesses, sep=" ")
            print()  # Adds a blank line
            print("Word: ", end="")
            for char in self.word:
                if char in self.guessed:
                    print(char, end=" ")
                else:
                    print('_', end=" ")
                    blanks += 1
            print()  # Adds a blank line

            print(f"You guessed {len(self.word) - blanks} of {len(self.word)} letters.")

            # no letter to guess the user won
            if blanks == 0:
                print("You saved me!")
                return True

            guess: str = input("Enter a letter >> ")

            # User want to return to menu
            if guess == 'return':
                return False

            if guess == "exit":
                print("Thanks for playing, see you :)")
                sys.exit()

            # Char validation
            if len(guess) != 1:
                print("One letter at a time.")
                continue
            if guess in self.guessed:
                print(f"You already used '{guess}' please try another letter.")
                continue
            if not is_valid_letter(guess):
                print(f"'{guess}' is not a valid letter, please enter valid letter from A-Z.")
                continue

            if guess.islower():
                inverse: str = guess.upper()
            else:
                inverse: str = guess.lower()

            self.guessed += guess + inverse

            if guess not in self.word and inverse not in self.word:
                self.hangman.update_hangman_state()
                wrong_guesses.append(guess)
                print(self.hangman.get_current_hangman())
                print(f"Sorry, that was wrong... ({7 - self.hangman.state} tries remaining)")
            if self.hangman.state == 7:
                print(f"The word was '{self.word}'.")
                print(f"No more tries remaining you lose!")
                return False


class Hangman:
    def __init__(self):
        self.state = 0

    def get_current_hangman(self):
        draws: dict = {
            0: """
          ______
          |    |     
          |          
          |     
          |    
          |   
         _|_
        |   |______
        |__________|
        |__________|
            """,

            1: """
          ______
          |    |     
          |    o      
          |     
          |    
          |   
         _|_
        |   |______
        |__________|
        |__________|
            """,
            2: """
           ______
          |    |     
          |    o      
          |    |   
          |    
          |   
         _|_
        |   |______
        |__________|
         """, 3:
                """
          ______
          |    |     
          |    o      
          |   /|   
          |    
          |   
         _|_
        |   |______
        |__________|
            """,
            4: """
           ______
          |    |     
          |    o      
          |   /|\\   
          |    
          |   
         _|_
        |   |______
        |__________|
         """, 5:
                """
          ______
          |    |     
          |    o      
          |   /|\\   
          |    |
          |   
         _|_
        |   |______
        |__________|
            """, 6:
                """
           ______
          |    |     
          |    o      
          |   /|\\   
          |    |
          |   / 
         _|_
        |   |______
        |__________|
         """, 7:
                """
          ______
          |    |     
          |    o      
          |   /|\\   
          |    |
          |   / \\
         _|_
        |   |______
        |__________|
        """
        }

        return draws[self.state]

    def update_hangman_state(self) -> bool:
        self.state += 1
