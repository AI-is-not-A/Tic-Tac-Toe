import random
import minimax


class Game:
    def __init__(self):
        self.table = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.player_types = "user", "AI"
        self.participants = [self.player_types[0], self.player_types[1]]
        self.participants_symbol = "X", "O"
        self.levels = "easy", "medium", "hard"
        self.AI_level = self.levels[0]
        # 0 = participant 1, 1 = participant 2
        self.next_move = 0
        self.initial_state = "         "

    def output_table(self):
        print("---------")
        for i in range(3):
            print(f"| {self.table[i][0]} {self.table[i][1]} {self.table[i][2]} |")
        print("---------")

    def only_numbers_and_space(self, _string):
        for char in _string:
            if not (char.isdigit() or char.isspace()):
                return False
        return True

    def get_free_space(self):
        free_space = []
        for y in range(3):
            for x in range(3):
                if self.table[y][x] == " ":
                    free_space.append(f"{y},{x}")
        return free_space

    def make_random_move_in_free_space(self):
        # make random move in free space
        free_space = self.get_free_space()
        choice = list(map(int, random.choice(free_space).split(",")))
        self.table[choice[0]][choice[1]] = self.participants_symbol[self.next_move]

    def get_vertical_row(self, x):
        vertical_row = []
        for row in self.table:
            vertical_row.append(row[x])
        return vertical_row

    def check_two_in_row(self, symbol):
        # check horizontal rows
        for y in range(3):
            if self.table[y].count(" ") == 1 and \
                    self.table[y].count(symbol) == 2:
                return y, self.table[y].index(" ")
        # check vertical rows
        for x in range(3):
            vertical_row = self.get_vertical_row(x)
            if vertical_row.count(" ") == 1 and \
                    vertical_row.count(symbol) == 2:
                return vertical_row.index(" "), x
        # check diagonals
        diagonal_row = [self.table[0][0], self.table[1][1], self.table[2][2]]
        if diagonal_row.count(" ") == 1 and diagonal_row.count(symbol) == 2:
            return diagonal_row.index(" "), diagonal_row.index(" ")
        diagonal_row = [self.table[0][2], self.table[1][1], self.table[2][0]]
        if diagonal_row.count(" ") == 1 and diagonal_row.count(symbol) == 2:
            col = 1
            row = diagonal_row.index(" ")
            if row != 1:
                if row == 2:
                    col = 0
                elif row == 0:
                    col = 2
            return row, col
        return None

    def next_AI_move(self):
        print(f'Making move level "{self.AI_level}"')

        if self.AI_level == self.levels[0]:
            self.make_random_move_in_free_space()
        if self.AI_level == self.levels[1]:
            symbols = self.participants_symbol
            if self.next_move == 1:
                symbols = symbols[::-1]

            for symbol in symbols:
                # check if two in a row and space
                result = self.check_two_in_row(symbol)
                if result is not None:
                    self.table[result[0]][result[1]] = self.participants_symbol[self.next_move]
                    return
            self.make_random_move_in_free_space()

        if self.AI_level == self.levels[2]:
            minimax.orig_board = []
            for i in range(9):
                value = self.table[i // 3][i % 3]
                if value == " ":
                    minimax.orig_board.append(i)
                else:
                    minimax.orig_board.append(self.table[i // 3][i % 3])
            # finding the ultimate play on the game that favors the computer
            best_spot = minimax.minimax(minimax.orig_board, self.participants_symbol[self.next_move])
            spot = best_spot["index"]
            self.table[spot // 3][spot % 3] = self.participants_symbol[self.next_move]

    def next_player_move(self):
        y, x = 0, 0
        while True:
            coordinates = input("Enter the coordinates: ")
            if not self.only_numbers_and_space(coordinates):
                print("You should enter numbers!")
                continue
            y, x = map(int, coordinates.split())
            if not (1 <= y <= 3) or not (1 <= x <= 3):
                print("Coordinates should be from 1 to 3!")
                continue
            if self.table[y - 1][x - 1] != " ":
                print("This cell is occupied! Choose another one!")
                continue
            break
        self.table[y - 1][x - 1] = self.participants_symbol[self.next_move]

    def get_initial_state(self):
        self.initial_state = input("Enter the cells: ").replace("_", " ")

    def get_state_of_game(self):

        # check horizontal rows
        for y in range(3):
            if (self.table[y][0] == self.table[y][1] == self.table[y][2]) and self.table[y][1] != " ":
                return f"{self.table[y][1]} wins"

        # check vertical rows
        for x in range(3):
            if (self.table[0][x] == self.table[1][x] == self.table[2][x]) and self.table[1][x] != " ":
                return f"{self.table[1][x]} wins"

        # check diagonals
        if (self.table[0][0] == self.table[1][1] == self.table[2][2]) and self.table[1][1] != " ":
            return f"{self.table[1][1]} wins"
        if (self.table[0][2] == self.table[1][1] == self.table[2][0]) and self.table[1][1] != " ":
            return f"{self.table[1][1]} wins"

        # check spaces
        for y in range(3):
            for x in range(3):
                if self.table[y][x] == " ":
                    return "Game not finished"

        return "Draw"

    def start_game(self):
        self.output_table()

        while True:
            if self.participants[self.next_move] == self.player_types[0]:
                self.next_player_move()
            else:
                self.next_AI_move()

            if self.next_move:
                self.next_move = 0
            else:
                self.next_move = 1

            self.output_table()

            if self.get_state_of_game() != "Game not finished":
                break

        print(self.get_state_of_game(), "\n")
        self.__init__()

    def start(self):

        while True:

            # check input (command + parameter)
            command = input("Input command: ").split()
            if command[0] == "exit" and len(command) == 1:
                exit()
            if command[0] != "start":
                print("Wrong command")
                continue
            if len(command) != 3:
                print("Bad parameters!")
                continue
            if (command[1] != "user" and command[1] not in self.levels) or \
                    (command[2] != "user" and command[2] not in self.levels):
                print("Bad parameters!")
                continue

            # save parameters as attribute
            if command[1] != "user":
                self.participants[0] = "AI"
                self.AI_level = command[1]
            else:
                self.participants[0] = "user"

            if command[2] != "user":
                self.participants[1] = "AI"
                self.AI_level = command[2]
            else:
                self.participants[1] = "user"

            self.start_game()


def main():
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
