import pygame as p


class BoardProperties:

    def __init__(self):
        self.width = self.height = 500
        self.dimension = 10
        self.piece_size = self.width // self.dimension
        self.IMAGES = {}
        self.inf_width = 500
        self.max_animation = 15

    def load_images(self):
        images = ['sp', 'gp', 'gK', 'sK']
        for i in images:
            self.IMAGES[i] = p.transform.scale(p.image.load(
                'images/' + i + '.jpeg'), (self.piece_size, self.piece_size))

    def draw_background(self, view):
        colors = p.Color((221, 190, 107))
        for r in range(self.dimension):
            for c in range(self.dimension):
                p.draw.rect(
                    view,
                    colors,
                    p.Rect(
                        c *
                        self.piece_size
                        + self.piece_size,
                        r *
                        self.piece_size + self.piece_size,
                        self.piece_size,
                        self.piece_size),
                    2)
        p.draw.rect(
            view,
            colors,
            p.Rect(
                self.width +
                self.piece_size + 50,
                self.piece_size +
                self.piece_size + 50,
                300,
                500 -
                self.piece_size *
                2))

    def draw_pieces(self, view, board, index_to_col, index_to_row):
        font = p.font.SysFont("Calibri", 15)
        half = self.piece_size / 2
        for row in range(1, self.dimension + 1):
            text = font.render(
                index_to_col[row - 1],
                True,
                p.Color("black"),
                p.Color(221, 190, 107))
            text_draw = text.get_rect()
            text_draw.center = (row * self.piece_size + half, half)
            view.blit(text, text_draw)

            text = font.render(
                index_to_row[row - 1],
                True,
                p.Color("black"),
                p.Color(221, 190, 107))
            text_draw = text.get_rect()
            text_draw.center = (half, row * self.piece_size + half)
            view.blit(text, text_draw)

        for row in range(self.dimension):
            for col in range(self.dimension):
                piece = board[row][col]
                if piece != '--':  # not empty square
                    view.blit(
                        self.IMAGES[piece],
                        p.Rect(
                            col *
                            self.piece_size +
                            self.piece_size,
                            row *
                            self.piece_size +
                            self.piece_size,
                            self.piece_size,
                            self.piece_size))
    ''' draw the animation of where the piece can move towards'''

    def draw_animation(self, view, gb, moves, click_chosen):
        if click_chosen != ():
            row, col = click_chosen
            if gb.board[row][col][0] == (
                    'g' if gb.black_to_move else 's'):
                s = p.Surface((self.piece_size, self.piece_size))
                s.set_alpha(99)
                if gb.black_to_move:
                    s.fill((p.Color('black')))
                else:
                    s.fill(p.Color(255, 0, 0))
                view.blit(
                    s,
                    (col *
                     self.piece_size +
                     self.piece_size,
                     row *
                     self.piece_size +
                     self.piece_size))
                if gb.black_to_move:
                    s.fill(p.Color('black'))
                else:
                    s.fill(p.Color(255, 0, 0))


                for move in moves:
                    if move.start_row == row and move.start_col == col:
                        view.blit(
                            s,
                            (self.piece_size *
                             move.end_col +
                             self.piece_size,
                             self.piece_size *
                             move.end_row +
                             self.piece_size))

    ''' draw the notations'''

    def draw_notations(self, view, text):
        font = p.font.SysFont('Calibri', 40, True, False)
        notation = font.render(text, 0, p.Color(221, 190, 107))
        notation_location = p.Rect(
            0,
            0,
            self.width,
            self.height).move(
            self.width /
            2 -
            notation.get_width() /
            2,
            self.height /
            2 -
            notation.get_height() /
            2)
        view.blit(notation, notation_location)
        notation = font.render(text, 0, p.Color('black'))
        view.blit(notation, notation_location.move(2, 2))

    '''draw the start interface'''

    def mode_selection(self, view):
        background_image = p.image.load('images/BG1.jpg')
        view.blit(background_image, (0, -5))
        center = p.display.get_surface().get_size()[0] / 2 - self.piece_size * 2
        # font = p.font.SysFont("Calibri", 40)
        # text = font.render("Cannons!", True, p.Color('black'))
        # text_rect = text.get_rect()
        # text_rect.center = (self.width + 19, self.piece_size * 1)
        # view.blit(text, text_rect)
        font = p.font.SysFont("malayalammn", 20)
        pos1 = p.draw.rect(
            view, p.Color('black'), p.Rect(
                center, (5 * self.piece_size), 199, 69), 2)
        text = font.render("DEMONSTRATION", True, p.Color('black'))
        text_rect = text.get_rect()
        text_rect.center = (pos1[0] + 100, pos1[1] + 35)
        view.blit(text, text_rect)
        pos2 = p.draw.rect(
            view, p.Color('black'), p.Rect(
                center, (7 * self.piece_size), 199, 69), 2)
        text = font.render("DARK", True, p.Color('black'))
        text_rect = text.get_rect()
        text_rect.center = (pos2[0] + 100, pos2[1] + 35)
        view.blit(text, text_rect)
        pos3 = p.draw.rect(
            view, p.Color('black'), p.Rect(
                center, (9 * self.piece_size), 199, 69), 2)
        text = font.render("LIGHT", True, p.Color('black'))
        text_rect = text.get_rect()
        text_rect.center = (pos3[0] + 100, pos3[1] + 35)
        view.blit(text, text_rect)
        return pos1, pos2, pos3

    '''draw the fight process'''

    def draw_process(self, view, turn, process, time):
        font = p.font.SysFont("Calibri", 15)
        turn = 'Dark team: ' if turn else 'Light team: '
        text = font.render(str(turn), True, p.Color(0, 0, 255))
        text_rect = text.get_rect()
        text_rect.center = (
            self.width + self.piece_size + 49,
            self.piece_size / 2 * 3)
        view.blit(text, text_rect)
        text = font.render(
            "Time:" +
            str(time) + 's',
            True,
            p.Color(0, 0, 255))
        text_rect = text.get_rect()
        text_rect.center = (
            self.width +
            self.piece_size *
            2 +
            self.inf_width /
            2,
            self.piece_size /
            2 *
            3)
        view.blit(text, text_rect)

        if len(process) != 0:
            for i in range(len(process)):
                text = font.render(
                    process[len(process) - i - 1], True, p.Color(0, 0, 255), p.Color(221, 190, 107))
                text_rect = text.get_rect()
                text_rect.center = (
                    self.width + self.piece_size + self.inf_width / 2, 512 - (i + 1) * 30)
                view.blit(text, text_rect)
                if i > 10:
                    break

    # draw the current state of the board

    def draw_game(self, view, gb, moves, captures, retreats, cannons, slides, click_chosen, time):
        self.draw_background(view)
        self.draw_process(view, gb.black_to_move, gb.process, time)
        self.draw_animation(view, gb, moves, click_chosen)
        self.draw_animation(view, gb, captures, click_chosen)
        self.draw_animation(view, gb, retreats, click_chosen)
        self.draw_animation(view, gb, cannons, click_chosen)
        self.draw_animation(view, gb, slides, click_chosen)
        self.draw_pieces(view, gb.board, gb.index_to_col, gb.index_to_row)
