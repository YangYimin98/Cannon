import time
from copy import deepcopy
import random


class AI:
    def __init__(self, max_depth, IDS):
        self.time_consumed = 0
        self.TT = dict({})
        self.table = [[[random.randint(1, 2 ** 64 - 1)
                        for i in range(4)]
                       for j in range(10)]
                      for k in range(10)]
        self.terminal_nodes = 0
        self.max_depth = max_depth
        self.ids_timer = 5
        self.IDS = IDS

    def evaluation_function(self, board, black_to_move):
        evaluation = 0
        """get the location of black town and white town"""
        row_black_town_location, col_black_town_location = board.black_town_loc_row, board.black_town_loc_col
        """all the pieces which can kill the town"""
        threaten_black_town_piece_position = [[row_black_town_location - 1, col_black_town_location],
                                              [row_black_town_location, col_black_town_location - 1],
                                              [row_black_town_location, col_black_town_location + 1],
                                              [row_black_town_location - 1, col_black_town_location + 1],
                                              [row_black_town_location - 1, col_black_town_location - 1],
                                              ]
        row_white_town_location, col_white_town_location = board.white_town_loc_row, board.white_town_loc_col

        threaten_white_town_piece_position = [[row_white_town_location + 1, col_white_town_location],
                                              [row_white_town_location, col_white_town_location - 1],
                                              [row_white_town_location, col_white_town_location + 1],
                                              [row_white_town_location + 1, col_white_town_location - 1],
                                              [row_white_town_location + 1, col_white_town_location + 1],
                                              ]

        if black_to_move:
            for r in range(len(board.board)):
                for c in range(len(board.board[0])):
                    start = board.board[r][c][1]
                    if start == 'gp' and r - 1 >= 0 and c - 1 >= 0 and c + 1 <= 9:
                        if board.board[r - 1][c] == 'sK' or board.board[r - 1][c - 1] == 'sK' or board.board[r - 1][
                            c + 1] == 'sK' \
                                or board.board[r][c - 1] == 'sK' or board.board[r][c + 1] == 'sK':
                            evaluation = 200
                        elif board.board[r - 1][c] == 'sp' or board.board[r - 1][c - 1] == 'sp' or board.board[r - 1][
                            c + 1] == 'sp' \
                                or board.board[r][c - 1] == 'sp' or board.board[r][c + 1] == 'sp':
                            evaluation = 50
        else:
            for r in range(len(board.board)):
                for c in range(len(board.board[0])):
                    start = board.board[r][c]
                    if start == 'sp' and r + 1 <= 9 and c - 1 >= 0 and c + 1 <= 9:
                        if board.board[r + 1][c] == 'gK' or board.board[r + 1][c - 1] == 'gK' or board.board[r + 1][
                            c + 1] == 'gK' \
                                or board.board[r][c - 1] == 'gK' or board.board[r][c + 1] == 'gK':
                            evaluation = 200
                        elif board.board[r + 1][c] == 'gp' or board.board[r + 1][c - 1] == 'gp' or board.board[r + 1][
                            c + 1] == 'gp' \
                                or board.board[r][c - 1] == 'gp' or board.board[r][c + 1] == 'gp':
                            evaluation = 50

        capture_black_town, capture_white_town = 0, 0
        for i in threaten_black_town_piece_position:
            """because the town's position is stable, so no need to judge if it is in the board"""
            if board.board[i[0]][i[1]] == 'sp':
                capture_black_town += 1
        for j in threaten_white_town_piece_position:
            if board.board[j[0]][j[1]] == 'gp':
                capture_white_town += 1
        if capture_white_town > 0 or capture_black_town > 0:
            evaluation = -1000
        # if black_to_move:
        #     if capture_white_town > 0:
        #         evaluation = 100
        #     if capture_black_town > 0:
        #         evaluation = -100
        # else:
        #     black_to_move = not black_to_move
        #     if capture_black_town > 0:
        #         evaluation = 100
        #     if capture_white_town > 0:
        #         evaluation = -100

        if black_to_move:
            evaluation += 4 * board.black_town + 4 * board.black_pieces - board.white_town - board.white_pieces
        else:
            evaluation += 4 * board.white_town + 4 * board.white_pieces - board.black_town - board.black_pieces

        print('Evaluation score for this move is {0}'.format(evaluation))

        return evaluation

    def minimax_function_with_alpha_beta(self, max_depth, board, game_continue, black_to_move, alpha, beta):
        hash = self.zobrist_hash(board)
        alpha_initial, beta_initial = alpha, beta
        self.terminal_nodes += 1
        best_value = float('-inf') if black_to_move else float('inf')
        best_move = ""
        moves, captures, retreats, cannons, slides = board.valid_moves()
        result = self.check_transposition_table(hash)
        if result != -1:
            if result[0] >= max_depth:
                if result[3] == "continue":
                    return result[1], result[2]
                elif result[3] == "high":
                    alpha = max(alpha, result[1])
                elif result[3] == "low":
                    beta = min(beta, result[1])
                if alpha >= beta:
                    return result[1], result[2]
        if max_depth == 0 or not game_continue:
            return self.evaluation_function(board, board.black_to_move), ""
        for move in captures:
            moves.append(move)
        for move in retreats:
            moves.append(move)
        for move in cannons:
            moves.append(move)
        for move in slides:
            moves.append(move)

        for move in moves:
            new_board = update_board(move, board)
            tree_child, action_child = self.minimax_function_with_alpha_beta(
                max_depth - 1, new_board, new_board.game_continue, new_board.black_to_move, alpha, beta)
            if black_to_move and best_value < tree_child:
                best_value = tree_child
                best_move = move
                alpha = max(alpha, best_value)
                # beta = min(beta, best_value)
                if beta <= alpha:
                    break
            elif (not black_to_move) and best_value > tree_child:
                best_value = tree_child
                best_move = move
                # alpha = max(alpha, best_value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        if best_value <= alpha_initial:
            flag = "low"
        elif best_value >= beta_initial:
            flag = "high"
        else:
            flag = "continue"

        hash = self.zobrist_hash(board)
        cache = (max_depth, best_value, best_move, flag)
        self.store(hash, cache)
        return best_value, best_move

    def minimax_function_with_alpha_beta_and_ids(self, max_depth, board, game_continue, gold_move, alpha, beta):
        start_time = time.time()
        hash = self.zobrist_hash(board)
        alpha_initial, beta_initial = alpha, beta
        self.terminal_nodes += 1
        result = self.check_transposition_table(hash)
        if result != -1:
            if result[0] >= max_depth:
                if result[3] == "continue":
                    return result[1], result[2]
                elif result[3] == "high":
                    alpha = max(alpha, result[1])
                elif result[3] == "low":
                    beta = min(beta, result[1])
                if alpha >= beta:
                    return result[1], result[2]
        if max_depth == 0 or not game_continue or self.ids_timer < 0:
            return self.evaluation_function(board, board.gold_move), ""

        moves, captures = board.valid_moves()
        for move in captures:
            moves.append(move)

        best_value = float('-inf') if gold_move else float('inf')
        best_move = ""

        for move in moves:
            new_board = update_board(move, board)
            tree_child, action_child = self.minimax_function_with_alpha_beta_and_ids(
                max_depth - 1, new_board, new_board.game_continue, new_board.gold_move, alpha, beta)

            if gold_move and best_value < tree_child:
                best_value = tree_child
                best_move = move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif (not gold_move) and best_value > tree_child:
                best_value = tree_child
                best_move = move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        if best_value <= alpha_initial:
            flag = "low"
        elif best_value >= beta_initial:
            flag = "high"
        else:
            flag = "continue"
        end_time = time.time()
        time_spent = end_time - start_time
        self.ids_timer -= time_spent
        hash = self.zobrist_hash(board)
        cache = (max_depth, best_value, best_move, flag)
        self.store(hash, cache)
        return best_value, best_move

    def ids(self, board):
        best_value = float("-inf") if board.gold_move else float("inf")
        best_move = ""
        total_times = 20
        current_depth = 1
        while True:
            start_time = time.time()
            self.ids_timer = 10
            score, move = self.minimax_function_with_alpha_beta_and_ids(
                current_depth, board, board.game_continue, board.gold_move, float('-inf'), float('inf'))
            end_time = time.time()
            time_spent = end_time - start_time
            total_times -= time_spent
            if board.gold_move:
                if score > best_value:
                    best_value = score
                    best_move = move
            else:
                if score < best_value:
                    best_value = score
                    best_move = move
            current_depth += 1
            if current_depth > self.max_depth:
                break
            if total_times < 0:
                break
        return best_value, best_move

    def check_transposition_table(self, hash):
        result = self.TT.get(hash)
        if result is not None:
            return result
        return -1

    def zobrist_hash(self, board):

        board = board.board
        hash = 0
        for r in range(len(board)):
            for c in range(len(board[0])):
                piece = board[r][c]
                if piece != "--":
                    # XOR according to position
                    hash ^= self.table[r][c][piece_index(
                        piece)]
        return hash

    def store(self, hash, cache):
        self.TT[hash] = cache

    def ai_move(self, board):
        start_time = time.time()
        self.terminal_nodes = 0
        print('------------AI is thinking about the next move------------')
        new_board = deepcopy(board)
        if self.IDS:
            score, move = self.ids(new_board)
        else:
            score, move = self.minimax_function_with_alpha_beta(
            self.max_depth, new_board, new_board.game_continue, new_board.black_to_move, float('-inf'), float('inf'))
        print('------------The node has been visited is{0}------------'.format(self.terminal_nodes))
        time_consumed = time.time() - start_time
        self.time_consumed += time_consumed
        self.time_consumed = round(self.time_consumed, 2)
        moves, captures, retreats, cannons, slides = board.valid_moves()
        if move != '':
            if move in moves or move in captures or move in retreats or move in slides:
                board.execute_move(move, flag=True)
                # print(board.board)
            elif move in cannons:
                board.execute_move(move, flag=False)
                # print(board.board)
        return move


def piece_index(piece):
    if piece == "sp":
        return 0
    elif piece == "gp":
        return 1
    elif piece == 'gK':
        return 2
    elif piece == 'sK':
        return 3


def update_board(move, board):

    moves, captures, retreats, cannons, slides = board.valid_moves()
    if move in moves or move in captures or move in retreats or move in slides:
        next_state = deepcopy(board)
        next_state.running = False
        next_state.execute_move(move, flag=True)
        return next_state
    elif move in cannons:
        next_state = deepcopy(board)
        next_state.running = False
        next_state.execute_move(move, flag=False)
        return next_state
