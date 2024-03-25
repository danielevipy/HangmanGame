from random import choice


class WordsFileHandler:
    def __init__(self, file_name, pointer=0):
        self.pointer = pointer
        self.file_name = file_name

    # def get_new_word(self) -> str:
    #     word: str = ""
    #     with open(self.file_name) as file:
    #         file.seek(self.pointer)
    #         while True:
    #             char: str = file.read(1)
    #             if char != " ":
    #                 word += char
    #             else:
    #                 self.pointer = file.tell()
    #                 break
    #     return word

    def get_new_word(self) -> str:
        with open(self.file_name) as file:
            file.seek(self.pointer)
            line: list[str] = file.readline().strip().split(" ")
            word: str = choice(line)
            self.pointer = file.tell()
        return word


if __name__ == "__main__":
    file_handler = WordsFileHandler("words.txt", 0)
