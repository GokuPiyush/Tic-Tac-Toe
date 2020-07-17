import random

class TicTacToe:

    def __init__(self):
        self.grid = [[' ', ' ', ' '],
                     [' ', ' ', ' '],
                     [' ', ' ', ' ']]

    def result(self):
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != ' ':
                return self.grid[i][0] + ' wins'
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != ' ':
                return self.grid[0][i] + ' wins'
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != ' ':
            return self.grid[0][0] + ' wins'
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != ' ':
            return self.grid[0][2] + ' wins'
        for i in self.grid:
            for j in i:
                if(j == ' '):
                    return 'Game not finished'
        return 'Draw'
    
    def convert(self, x, y):
        if y == 1:
            y += 2
        elif y == 3:
            y -= 2
        return y, x

    def user(self, chr):
        coordinates = input("Enter the coordinates: ")
        x, y = '', ''
        if len(list(coordinates.split())) != 2:
            x = coordinates
        else:
            x, y = coordinates.split()
        if not x.isdigit() or not y.isdigit():
            print("You should enter numbers!")
            self.user(chr)
        elif int(x) < 1 or int(x) > 3 or int(y) < 1 or int(y) > 3:
            print("Coordinates should be from 1 to 3!")
            self.user(chr)
        else:
            i, j = self.convert(int(x), int(y))
            if self.grid[i-1][j-1] != ' ':
                print("This cell is occupied! Choose another one!")
                self.user(chr)
            else:
                self.grid[i-1][j-1] = chr

    def AI_easy(self, chr, diff='easy'):
        if diff == 'easy':
            print(f'Making move level "{diff}"')

        available = [[i,j] for i in range(3) for j in range(3) if self.grid[i][j] == ' ']
        choice = random.choice(available)
        i, j = choice[0], choice[1]
        self.grid[i][j] = chr
        return

    def AI_medium(self, chr, diff='medium'):
        if diff == 'medium':
            print(f'Making move level "{diff}"')

        # horizontal
        for i in range(3):
            count_empty, empty_index, count_chr, count_opp = 0, 0, 0, 0
            for j in range(3):
                if self.grid[i][j] == ' ':
                    empty_index = j
                    count_empty += 1
                elif self.grid[i][j] == chr:
                    count_chr += 1
                else:
                    count_opp += 1
            if count_empty == 1 and (count_chr == 2 or count_opp == 2):
                self.grid[i][empty_index] = chr
                return
        
        # vertical
        for j in range(3):
            count_empty, empty_index, count_chr, count_opp = 0, 0, 0, 0
            for i in range(3):
                if self.grid[i][j] == ' ':
                    empty_index = i
                    count_empty += 1
                elif self.grid[i][j] == chr:
                    count_chr += 1
                else:
                    count_opp += 1
            if count_empty == 1 and (count_chr == 2 or count_opp == 2):
                self.grid[empty_index][j] = chr
                return
        
        # principal diogonal
        count_empty, empty_index, count_chr, count_opp = 0, 0, 0, 0
        for i in range(3):
            if self.grid[i][i] == ' ':
                empty_index = i
                count_empty += 1
            elif self.grid[i][i] == chr:
                count_chr += 1
            else:
                count_opp += 1
        if count_empty == 1 and (count_chr == 2 or count_opp == 2):
            self.grid[empty_index][empty_index] = chr
            return
        
        # off diogonal
        count_empty, empty_index_i, empty_index_j, count_chr, count_opp = 0, 0, 0, 0, 0
        for _ in range(3):
            i, j = 0, 2
            if self.grid[i][j] == ' ':
                empty_index_i, empty_index_j = i, j
                count_empty += 1
            elif self.grid[i][j] == chr:
                count_chr += 1
            else:
                count_opp += 1
            i += 1
            j -= 1
        if count_empty == 1 and (count_chr == 2 or count_opp == 2):
            self.grid[empty_index_i][empty_index_j] = chr
            return
        
        self.AI_easy(chr, 'medium')

    def minimax(self, chr, is_maximizer=False):
        terminal_state = self.result()
        if terminal_state != 'Game not finished':
            if terminal_state == 'Draw':
                return 0
            elif terminal_state == chr + ' wins':
                return 10
            else:
                return -10
        if is_maximizer:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j] == ' ':
                        self.grid[i][j] = chr
                        score = self.minimax(chr, not is_maximizer)
                        best_score = max(best_score, score)
                        self.grid[i][j] = ' '
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j] == ' ':
                        self.grid[i][j] = 'X' if chr != 'X' else 'O'
                        score = self.minimax(chr, not is_maximizer)
                        best_score = min(best_score, score)
                        self.grid[i][j] = ' '
            return best_score

    def AI_hard(self, chr, diff='hard'):
        print(f'Making move level "{diff}"')
        
        best_score, index = float('-inf'), {}
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    self.grid[i][j] = chr
                    score = self.minimax(chr)
                    self.grid[i][j] = ' '
                    if(score > best_score):
                        best_score = score
                        index = {'i': i, 'j': j}
        self.grid[index['i']][index['j']] = chr

    def print_(self):
        pos = 0
        print('-' * 9)
        for i in range(3):
            pos = 0
            print(f"| {self.grid[i][pos]} {self.grid[i][pos + 1]} {self.grid[i][pos + 2]} |")
        print('-' * 9)
        
    def play(self, move_X, move_O):
        self.print_()
        while(True):
            move_X('X')
            self.print_()
            if self.result() == 'Game not finished':
                move_O('O')
                self.print_()
                if self.result() == 'Game not finished':
                    continue
                print(self.result())
                break
            print(self.result())
            break


while(True):
    command = input("Input command: ").lower()
    if command == 'exit':
        break
    if len(command.split()) == 3:
        command, user1, user2 = command.split()
        if command == 'start':
            ob = TicTacToe()
            dispatch = {'user': ob.user, 'easy': ob.AI_easy, 'medium': ob.AI_medium, 'hard': ob.AI_hard}
            try:
                ob.play(dispatch[user1], dispatch[user2])
            except:
                print('Bad parameters!')
        else:
            print('Bad parameters!')
    else:
        print('Bad parameters!')