import hashlib
import hmac
import random
import sys
import os


class KeyGenerator:
    @staticmethod
    def generate_key():
        return hashlib.sha256(os.urandom(32)).hexdigest()


class HmacCalculator:
    @staticmethod
    def calculate_hmac(key, message):
        h = hmac.new(bytes.fromhex(key), message.encode(), hashlib.sha256)
        return h.hexdigest()


class MoveEvaluator:
    def __init__(self, moves):
        self.moves = moves
        self.num_moves = len(moves)

    def evaluate(self, player_move, computer_move):
        player_index = self.moves.index(player_move)
        computer_index = self.moves.index(computer_move)

        if player_index == -1 or computer_index == -1:
            raise ValueError('Invalid moves!')

        half_num_moves = self.num_moves // 2

        winning_moves = []
        for i in range(1, half_num_moves + 1):
            prev_move_index = (player_index - i) % self.num_moves
            next_move_index = (player_index + i) % self.num_moves
            winning_moves.append(self.moves[prev_move_index])
            winning_moves.append(self.moves[next_move_index])

        if computer_move in winning_moves:
            return 'Player wins!'
        elif player_move == computer_move:
            return 'It\'s a draw!'
        else:
            return 'Computer wins!'


class HelpTableGenerator:
    @staticmethod
    def generate_table(moves):
        num_moves = len(moves)
        table = [[' ' for _ in range(num_moves + 1)]
                 for _ in range(num_moves + 1)]
        table[0][0] = 'Moves'

        for i, move in enumerate(moves, 1):
            table[0][i] = move
            table[i][0] = move

        for i, move1 in enumerate(moves, 1):
            for j, move2 in enumerate(moves, 1):
                if i == j:
                    table[i][j] = 'Draw'
                else:
                    result = evaluator.evaluate(move1, move2)
                    table[i][j] = 'Win' if result == 'Player wins!' else 'Lose'

        return table


moves = sys.argv[1:]

if len(moves) < 3 or len(moves) % 2 == 0:
    print('Incorrect number of moves! Example: python game.py rock paper scissors')
    sys.exit(1)


key_generator = KeyGenerator()
hmac_calculator = HmacCalculator()
evaluator = MoveEvaluator(moves)
help_table_generator = HelpTableGenerator()


key = key_generator.generate_key()


computer_move = random.choice(moves)


hmac_value = hmac_calculator.calculate_hmac(key, computer_move)

# Display HMAC to the user
print(f'HMAC: {hmac_value}')

# Display available moves
print('Available moves:')
for i, move in enumerate(moves, 1):
    print(f'{i} - {move}')
print('0 - exit')
print('? - help')

while True:
    # Get user's move
    user_input = input('Enter your move: ')

    if user_input == '0':
        sys.exit(0)
    elif user_input == '?':
        # Generate and display help table
        help_table = help_table_generator.generate_table(moves)
        for row in help_table:
            print('\t'.join(row))
        continue

    try:
        user_move = moves[int(user_input) - 1]
    except (ValueError, IndexError):
        print('Invalid input!')
        continue

    # Calculate the result
    result = evaluator.evaluate(user_move, computer_move)

    # Display the result, computer's move, and the original key
    print(f'Your move: {user_move}')
    print(f'Computer move: {computer_move}')
    print(result)
    print(f'HMAC key: {key}')
