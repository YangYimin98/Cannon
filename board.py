import move_recordings


class GameBoard:
    def __init__(self):
        self.board = [
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', 'sp', '--', 'sp', '--', 'sp', '--', 'sp', '--', 'sp'],
            ['--', 'sp', '--', 'sp', '--', 'sp', '--', 'sp', '--', 'sp'],
            ['--', 'sp', '--', 'sp', '--', 'sp', '--', 'sp', '--', 'sp'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
            ['gp', '--', 'gp', '--', 'gp', '--', 'gp', '--', 'gp', '--'],
            ['gp', '--', 'gp', '--', 'gp', '--', 'gp', '--', 'gp', '--'],
            ['gp', '--', 'gp', '--', 'gp', '--', 'gp', '--', 'gp', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--', '--', '--'],
        ]
        self.index_to_col = (
            ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
        self.index_to_row = (
            ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"])
        self.black_to_move = True
        self.move_log = []
        self.turn_team = 0
        self.process = []
        self.white_pieces = 15
        self.black_pieces = 15
        self.game_continue = True
        self.result = ''
        self.black_town = 1
        self.white_town = 1
        self.running = True
        self.piece_captured = []
        self.random_black_town_loc = True
        self.random_white_town_loc = True
        self.black_town_loc_row, self.black_town_loc_col = 0, 0
        self.white_town_loc_row, self.white_town_loc_col = 0, 0
        self.control = True

    def town_selection(self):
        """dont forget to throw exception"""
        if self.black_to_move:
            r = 9
            if not self.random_black_town_loc:
                c = int(input('The col of DARK town, c_black: '))
            else:
                c = 4
            if c != 0 and c != 9:
                self.board[r][c] = 'gK'
            else:
                while c == 0 or c == 9:
                    c = int(input('Corner is not allowed, please reset the value: '))
                    continue
                self.board[r][c] = 'gK'
            self.black_town_loc_row, self.black_town_loc_col = r, c
            # print(self.black_town_loc_row, self.black_town_loc_col)
        else:
            r = 0
            if not self.random_white_town_loc:

                c = int(input('The col of LIGHT town, c_white: '))
            else:
                c = 5
            if c != 0 and c != 9:
                self.board[r][c] = 'sK'
            else:
                while c == 0 or c == 9:
                    c = int(input('Corner is not allowed, please reset the value: '))
                    continue
                self.board[r][c] = 'sK'
            self.white_town_loc_row, self.white_town_loc_col = r, c
            # print(self.white_town_loc_row, self.white_town_loc_col)

    def valid_moves(self):
        moves, capture, retreats, cannons, slides = [], [], [], [], []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                start = self.board[r][c][0]
                if (start == 'g' and self.black_to_move) or (start == 's' and not self.black_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.rules_for_pieces_moves(r, c, moves)
                        self.rules_for_pieces_capture(r, c, capture)
                        self.rules_for_pieces_retreat(r, c, retreats)
                        self.rules_for_combine_cannon_and_bomb(r, c, cannons)
                        self.rules_for_cannon_slides(r, c, slides)
                    else:  # town can not move
                        break

        return moves, capture, retreats, cannons, slides

    def rules_for_pieces_moves(self, r, c, moves):  # remember to break
        pre = len(moves)
        if self.black_to_move:
            if r - 1 >= 0:
                if self.board[r - 1][c] == '--':
                    moves.append(move_recordings.MyMoveRecording(
                        (r, c), (r - 1, c), self.board))
            if c - 1 >= 0 and r - 1 >= 0:
                if self.board[r - 1][c - 1] == '--':
                    moves.append(move_recordings.MyMoveRecording(
                        (r, c), (r - 1, c - 1), self.board))
            if c + 1 <= 9 and r - 1 >= 0:
                if self.board[r - 1][c + 1] == '--':
                    moves.append(move_recordings.MyMoveRecording(
                        (r, c), (r - 1, c + 1), self.board))
        else:
            if r + 1 <= 9:
                if self.board[r + 1][c] == '--':
                    moves.append(move_recordings.MyMoveRecording(
                        (r, c), (r + 1, c), self.board))
            if r + 1 <= 9 and c - 1 >= 0:
                if self.board[r + 1][c - 1] == '--':
                    moves.append(move_recordings.MyMoveRecording(
                        (r, c), (r + 1, c - 1), self.board))
            if c + 1 <= 9 and r + 1 <= 9:
                if self.board[r + 1][c + 1] == '--':
                    moves.append(move_recordings.MyMoveRecording(
                        (r, c), (r + 1, c + 1), self.board))

        return len(moves) - pre

    def rules_for_pieces_capture(self, r, c, capture):
        if self.black_to_move:
            if r - 1 >= 0:
                if self.board[r - 1][c][0] == 's':
                    capture.append(move_recordings.MyMoveRecording(
                        (r, c), (r - 1, c), self.board
                    ))
                if c - 1 >= 0:
                    if self.board[r - 1][c - 1][0] == 's':
                        capture.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 1, c - 1), self.board
                        ))
                if c + 1 <= 9:
                    if self.board[r - 1][c + 1][0] == 's':
                        capture.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 1, c + 1), self.board
                        ))
            if c - 1 >= 0:
                if self.board[r][c - 1][0] == 's':
                    capture.append(move_recordings.MyMoveRecording(
                        (r, c), (r, c - 1), self.board
                        ))

            if c + 1 <= 9:
                if self.board[r][c + 1][0] == 's':
                    capture.append(move_recordings.MyMoveRecording(
                        (r, c), (r, c + 1), self.board
                            ))

        elif not self.black_to_move:
            if r + 1 <= 9:
                if self.board[r + 1][c][0] == 'g':
                    capture.append(move_recordings.MyMoveRecording(
                        (r, c), (r + 1, c), self.board
                    ))
                if c - 1 >= 0:
                    if self.board[r + 1][c - 1][0] == 'g':
                        capture.append(move_recordings.MyMoveRecording(
                            (r, c), (r + 1, c - 1), self.board
                        ))
                if c + 1 <= 9:
                    if self.board[r + 1][c + 1][0] == 'g':
                        capture.append(move_recordings.MyMoveRecording(
                            (r, c), (r + 1, c + 1), self.board
                        ))
            if c + 1 <= 9:
                if self.board[r][c + 1][0] == 'g':
                    capture.append(move_recordings.MyMoveRecording(
                            (r, c), (r, c + 1), self.board
                        ))
            if c - 1 >= 0:
                if self.board[r][c - 1][0] == 'g':
                    capture.append(move_recordings.MyMoveRecording(
                            (r, c), (r, c - 1), self.board
                        ))

    def black_retreat(self, r, c, retreats):
        if r + 2 <= 9:
            if self.board[r + 1][c] == '--':
                if self.board[r + 2][c] == '--':
                    retreats.append(move_recordings.MyMoveRecording(
                        (r, c), (r + 2, c), self.board))
            if c + 2 <= 9:
                if self.board[r + 1][c + 1] == '--':
                    if self.board[r + 2][c + 2] == '--':
                        retreats.append(move_recordings.MyMoveRecording(
                            (r, c), (r + 2, c + 2), self.board))
            if c - 2 >= 0:
                if self.board[r + 1][c - 1] == '--':
                    if self.board[r + 2][c - 2] == '--':
                        retreats.append(move_recordings.MyMoveRecording(
                            (r, c), (r + 2, c - 2), self.board))

    def white_retreat(self, r, c, retreats):
        if 0 <= r - 2:
            if self.board[r - 1][c] == '--':
                if self.board[r - 2][c] == '--':
                    retreats.append(move_recordings.MyMoveRecording(
                        (r, c), (r - 2, c), self.board))
            if c + 2 <= 9:
                if self.board[r - 1][c + 1] == '--':
                    if self.board[r - 2][c + 2] == '--':
                        retreats.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 2, c + 2), self.board))
            if c - 2 >= 0:
                if self.board[r - 1][c - 1] == '--':
                    if self.board[r - 2][c - 2] == '--':
                        retreats.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 2, c - 2), self.board))

    def rules_for_pieces_retreat(self, r, c, retreats):
        """pre-requisite for retreat, threaten by opponent"""
        if self.black_to_move:
            if r - 1 >= 0:
                if self.board[r - 1][c] == 'sp':
                    self.black_retreat(r, c, retreats)
                if c - 1 >= 0:
                    if self.board[r - 1][c - 1] == 'sp' or self.board[r][c - 1] == 'sp':
                        self.black_retreat(r, c, retreats)
                if c + 1 <= 9:
                    if self.board[r - 1][c + 1] == 'sp' or self.board[r][c + 1] == 'sp':
                        self.black_retreat(r, c, retreats)

            if r + 1 <= 9:
                if self.board[r + 1][c] == 'sp':
                    self.black_retreat(r, c, retreats)

                if c - 1 >= 0:
                    if self.board[r + 1][c - 1] == 'sp':
                        self.black_retreat(r, c, retreats)

                if c + 1 <= 9:
                    if self.board[r + 1][c + 1] == 'sp':
                        self.black_retreat(r, c, retreats)

        else:
            if r + 1 <= 9:
                if self.board[r + 1][c] == 'gp':
                    self.white_retreat(r, c, retreats)
                if c - 1 >= 0:
                    if self.board[r + 1][c - 1] == 'gp' or self.board[r][c - 1] == 'gp':
                        self.white_retreat(r, c, retreats)
                if c + 1 <= 9:
                    if self.board[r + 1][c + 1] == 'gp' or self.board[r][c + 1] == 'gp':
                        self.white_retreat(r, c, retreats)

            if r - 1 >= 0:
                if self.board[r - 1][c] == 'gp':
                    self.white_retreat(r, c, retreats)
                if c - 1 >= 0:
                    if self.board[r - 1][c - 1] == 'gp':
                        self.white_retreat(r, c, retreats)
                if c + 1 <= 9:
                    if self.board[r - 1][c + 1] == 'gp':
                        self.white_retreat(r, c, retreats)

    def rules_for_cannon_slides(self, r, c, slides):
        piece, town = self.move_team()
        if r - 1 >= 0 and r + 1 <= 9:  # vertical
            if self.board[r - 1][c] == piece and self.board[r + 1][c] == piece and self.board[r][c] == piece:
                if r - 2 >= 0 and r + 1 <= 9:
                    if self.board[r - 2][c] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r + 1, c), (r - 2, c), self.board))
                if r - 1 >= 0 and r + 2 <= 9:
                    if self.board[r + 2][c] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r - 1, c), (r + 2, c), self.board))
        if c - 1 >= 0 and c + 1 <= 9:  # horizontal
            if self.board[r][c - 1] == piece and self.board[r][c + 1] == piece and self.board[r][c] == piece:
                if c - 1 >= 0 and c + 2 <= 9:
                    if self.board[r][c + 2] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r, c - 1), (r, c + 2), self.board))
                if c - 2 >= 0 and c + 1 <= 9:
                    if self.board[r][c - 2] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r, c + 1), (r, c - 2), self.board))
        if c - 1 >= 0 and c + 1 <= 9 and r - 1 >= 0 and r + 1 <= 9:  # right orthogonal
            if self.board[r - 1][c - 1] == piece and self.board[r + 1][c + 1] == piece and self.board[r][c] == piece:
                if r - 2 >= 0 and c - 2 >= 0:
                    if self.board[r - 2][c - 2] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r + 1, c + 1), (r - 2, c - 2), self.board))
                if r + 2 <= 9 and c + 2 <= 9:
                    if self.board[r + 2][c + 2] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r - 1, c - 1), (r + 2, c + 2), self.board))

        if c - 1 >= 0 and c + 1 <= 9 and r - 1 >= 0 and r + 1 <= 9:  # left orthogonal
            if self.board[r - 1][c + 1] == piece and self.board[r + 1][c - 1] == piece and self.board[r][c] == piece:
                if r - 2 >= 0 and c + 2 <= 9:
                    if self.board[r - 2][c + 2] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r + 1, c - 1), (r - 2, c + 2), self.board))
                if r + 2 <= 9 and c - 2 >= 0:
                    if self.board[r + 2][c - 2] == '--':
                        slides.append(move_recordings.MyMoveRecording(
                            (r - 1, c + 1), (r + 2, c - 2), self.board))

    def rules_for_combine_cannon_and_bomb(self, r, c, cannons):  # dont forget to add animation for the cannons
        piece, town = self.move_team()

        if r - 1 >= 0 and r + 1 <= 9:  # vertical
            if self.board[r - 1][c] == piece and self.board[r + 1][c] == piece and self.board[r][c] == piece:
                if r - 3 >= 0:
                    if self.board[r - 2][c] == '--':
                        if self.board[r - 3][c] != '--' and self.board[r - 3][c] != piece and self.board[r - 3][c] != town:
                            cannons.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 3, c), self.board))
                        if r - 4 >= 0:
                            if self.board[r - 3][c] == '--':
                                if self.board[r - 4][c] != '--' and self.board[r - 4][c] != piece and self.board[r - 4][c] != town:
                                    cannons.append(move_recordings.MyMoveRecording(
                                        (r, c), (r - 4, c), self.board))
                if r + 3 <= 9:
                    if self.board[r + 2][c] == '--':
                        if self.board[r + 3][c] != '--' and self.board[r + 3][c] != piece and self.board[r + 3][c] != town:
                            cannons.append(move_recordings.MyMoveRecording(
                                (r, c), (r + 3, c), self.board))
                        if r + 4 <= 9:
                            if self.board[r + 3][c] == '--':
                                if self.board[r + 4][c] != '--' and self.board[r + 4][c] != piece and self.board[r + 4][c] != town:
                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r + 4, c), self.board))
        if c - 1 >= 0 and c + 1 <= 9:  # horizontal
            if self.board[r][c - 1] == piece and self.board[r][c + 1] == piece and self.board[r][c] == piece:
                if c - 3 >= 0:
                    if self.board[r][c - 2] == '--':
                        if self.board[r][c - 3] != '--' and self.board[r][c - 3] != piece and self.board[r][c - 3] != town:
                            cannons.append(move_recordings.MyMoveRecording(
                                (r, c), (r, c - 3), self.board))
                        if c - 4 >= 0:
                            if self.board[r][c - 3] == '--':
                                if self.board[r][c - 4] != '--' and self.board[r][c - 4] != piece and self.board[r][c - 4] != town:
                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r, c - 4), self.board))
                if c + 3 <= 9:
                    if self.board[r][c + 2] == '--':
                        if self.board[r][c + 3] != '--' and self.board[r][c + 3] != piece and self.board[r][c + 3] != town:
                            cannons.append(move_recordings.MyMoveRecording(
                            (r, c), (r, c + 3), self.board))
                        if c + 4 <= 9:

                            if self.board[r][c + 3] == '--':
                                if self.board[r][c + 4] != '--' and self.board[r][c + 4] != piece and self.board[r][c + 4] != town:

                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r, c + 4), self.board))
        if c - 1 >= 0 and c + 1 <= 9 and r - 1 >= 0 and r + 1 <= 9:  # right orthogonal
            if self.board[r - 1][c - 1] == piece and self.board[r + 1][c + 1] == piece and self.board[r][c] == piece:
                if c - 3 >= 0 and r - 3 >= 0:
                    if self.board[r - 2][c - 2] == '--':
                        if self.board[r - 3][c - 3] != '--' and self.board[r - 3][c - 3] != piece and self.board[r - 3][c - 3] != town:

                            cannons.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 3, c - 3), self.board))
                        if c - 4 >= 0 and r - 4 >= 0:
                            if self.board[r - 3][c - 3] == '--':
                                if self.board[r - 4][c - 4] != '--' and self.board[r - 4][c - 4] != piece and self.board[r - 4][c - 4] != town:

                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r - 4, c - 4), self.board))
                if c + 3 <= 9 and r + 3 <= 9:
                    if self.board[r + 2][c + 2] == '--':
                        if self.board[r + 3][c + 3] != '--' and self.board[r + 3][c + 3] != piece and self.board[r + 3][c + 3] != town:
                            cannons.append(move_recordings.MyMoveRecording(
                            (r, c), (r + 3, c + 3), self.board))
                        if c + 4 <= 9 and r + 4 <= 9:

                            if self.board[r + 3][c + 3] == '--':
                                if self.board[r + 4][c + 4] != '--' and self.board[r + 4][c + 4] != piece and self.board[r + 4][c + 4] != town:

                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r + 4, c + 4), self.board))
        if c - 1 >= 0 and c + 1 <= 9 and r - 1 >= 0 and r + 1 <= 9:  # left orthogonal
            if self.board[r - 1][c + 1] == piece and self.board[r + 1][c - 1] == piece and self.board[r][c] == piece:
                if c + 3 <= 9 and r - 3 >= 0:
                    if self.board[r - 2][c + 2] == '--':
                        if self.board[r - 3][c + 3] != '--' and self.board[r - 3][c + 3] != piece and self.board[r - 3][c + 3] != town:

                            cannons.append(move_recordings.MyMoveRecording(
                            (r, c), (r - 3, c + 3), self.board))
                        if r - 4 >= 0 and c + 4 <= 9:
                            if self.board[r - 3][c + 3] == '--':
                                if self.board[r - 4][c + 4] != '--' and self.board[r - 4][c + 4] != piece and self.board[r - 4][c + 4] != town:

                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r - 4, c + 4), self.board))
                if r + 3 <= 9 and c - 3 >= 0:
                    if self.board[r + 2][c - 2] == '--':
                        if self.board[r + 3][c - 3] != '--' and self.board[r + 3][c - 3] != piece and self.board[r + 3][c - 3] != town:

                            cannons.append(move_recordings.MyMoveRecording(
                            (r, c), (r + 3, c - 3), self.board))
                        if r + 4 <= 9 and c - 4 >= 0:
                            if self.board[r + 3][c - 3] == '--':
                                if self.board[r + 4][c - 4] != '--' and self.board[r + 4][c - 4] != piece and self.board[r + 4][c - 4] != town:

                                    cannons.append(move_recordings.MyMoveRecording(
                                    (r, c), (r + 4, c - 4), self.board))

    def move_team(self):
        if self.black_to_move:
            piece = 'gp'
            town = 'gK'
        else:
            piece = 'sp'
            town = 'sK'
        return piece, town

    def change_team(self):
        self.black_to_move = not self.black_to_move
        self.turn_team += 1

    def calculate_pieces(self, moves):
        if moves.piece_capture != '--':
            self.piece_captured.append(moves.piece_capture)
            if moves.piece_capture == 'gK':
                self.black_town = 0
            elif moves.piece_capture == 'sK':
                self.white_town = 0
            elif moves.piece_capture == 'gp':
                self.black_pieces -= 1
            else:
                self.white_pieces -= 1

    def execute_move(self, moves, flag):
        turn = 'Dark team' if self.black_to_move else 'Light team'

        if flag:
            self.board[moves.start_row][moves.start_col] = '--'
            if self.running:
                if moves.piece_capture == '--':
                    self.process.append(
                        turn + ' made a normal move:   ' + moves.piece_move + ' ' + moves.get_notations())
                elif moves.piece_capture == 'gK':
                    self.process.append(
                        turn +
                        " captured " +
                        moves.piece_capture +
                        ":   " +
                        moves.piece_move +
                        " " +
                        moves.get_notations())
                    self.result = 'Light team wins the game.'
                    self.game_continue = False
                elif moves.piece_capture == 'sK':
                    self.process.append(
                        turn +
                        " captured " +
                        moves.piece_capture +
                        ":   " +
                        moves.piece_move +
                        " " +
                        moves.get_notations())
                    self.result = 'Dark team wins the game.'
                    self.game_continue = False
                else:
                    self.process.append(
                        turn +
                        " captured " +
                        moves.piece_capture +
                        ":   " +
                        moves.piece_move +
                        " " +
                        moves.get_notations())
            self.calculate_pieces(moves)

            if self.white_pieces == 0:
                self.game_continue = False
                self.result = 'Dark Team wins the game!'
            if self.black_pieces == 0:
                self.game_continue = False
                self.result = 'Light Team wins the game!'
            if self.black_town == 0:
                self.game_continue = False
                self.result = 'Light Team wins the game!'
            if self.white_town == 0:
                self.game_continue = False
                self.result = 'Dark Team wins the game!'
            self.board[moves.end_row][moves.end_col] = moves.piece_move
            self.move_log.append(moves)
            self.change_team()
        elif not flag:
            if self.running:
                if moves.piece_capture == '--':
                    self.process.append(
                        turn + ':   ' + moves.piece_move + ' ' + moves.get_notations())
                elif moves.piece_capture == 'gK':
                    self.process.append(
                        turn +
                        " used the CANNONS to capture " +
                        moves.piece_capture +
                        ":   " +
                        moves.piece_move +
                        " " +
                        moves.get_notations())
                    self.result = 'Light team wins the game.'
                    self.game_continue = False
                elif moves.piece_capture == 'sK':
                    self.process.append(
                        turn +
                        " used the CANNONS to capture " +
                        moves.piece_capture +
                        ":   " +
                        moves.piece_move +
                        " " +
                        moves.get_notations())
                    self.result = 'Dark team wins the game.'
                    self.game_continue = False
                else:
                    self.process.append(
                        turn +
                        " used the CANNONS to capture " +
                        moves.piece_capture +
                        ":   " +
                        moves.piece_move +
                        " " +
                        moves.get_notations())
            self.calculate_pieces(moves)
            if self.white_pieces == 0:
                self.game_continue = False
                self.result = 'Dark Team wins the game!'
            if self.black_pieces == 0:
                self.game_continue = False
                self.result = 'Light Team wins the game!'
            if self.black_town == 0:
                self.game_continue = False
                self.result = 'Light Team wins the game!'
            if self.white_town == 0:
                self.game_continue = False
                self.result = 'Dark Team wins the game!'
            self.board[moves.end_row][moves.end_col] = '--'
            self.move_log.append(moves)
            self.change_team()

