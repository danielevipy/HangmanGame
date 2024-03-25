class User:
    def __init__(self, score=0, username=None):
        self.score: int = score
        self.username = username

    def update_username(self, new_username):
        self.username = new_username

    def update_score(self, new_score):
        self.score = new_score


class ScoreRecord:
    def __init__(self, number, user: User):
        self.number = number
        self.user = user

    def __del__(self):  # delete user
        ...

    def __str__(self):
        return f"{self.number:<5} {self.user.score:<10} {self.user.username:<20}"


class ScoreTable:
    def __init__(self, file_name):
        self.file_name: str = file_name
        self.records: list[ScoreRecord] = self.get_score_table_from_file()
        self.current_user_record: ScoreRecord = None

    def get_score_table_from_file(self) -> list[ScoreRecord]:
        records: list[ScoreRecord] = []
        with open(self.file_name, "r") as file:
            for line in file:
                columns = line.strip().split(" ")
                if len(columns) != 3:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
                number, score, username = columns
                user = User(int(score), username)
                record = ScoreRecord(int(number), user)
                records.append(record)
        return records

    def set_current_username_record(self, user: User):
        for record in self.records:
            if record.user.username == user.username:
                self.current_user_record = record
                print(f"Your last score: {self.current_user_record.user.score}.\n")
        if self.current_user_record is None:
            new_record = ScoreRecord(len(self.records) + 1, user)
            self.current_user_record = new_record
            self.records.append(new_record)

    def get_current_user_record(self) -> ScoreRecord:
        return self.current_user_record

    def sort_records(self):
        self.records.sort(key=lambda score_record: score_record.user.score, reverse=True)
        for index, record in enumerate(self.records, start=1):
            record.number = index

    def update_score_table_file(self):
        self.sort_records()
        with open(self.file_name, "w") as file:
            for record in self.records:
                line: str = f"{record.number} {record.user.score} {record.user.username}\n"
                file.write(line)

    def __str__(self):
        print("* * * Score Table * * * \n")
        table_header = f"{'Number':<5} {'Score':<10} {'Username':<20}"
        table_header += '\n' + '-' * 37  # Adjust the number based on your table width

        table_rows = '\n'.join(str(record) for record in self.records)
        return f"{table_header}\n{table_rows}"

# if __name__ == "__main__":
#     score_table = ScoreTable("score.txt")
#     print(score_table)
