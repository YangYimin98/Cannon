from utils import *
from board import GameBoard
from move_recordings import MyMoveRecording
import sys
import ai


def main():
    p.init()
    bp = BoardProperties()
    p.display.set_caption('Cannon')
    screen = p.display.set_mode(
        (bp.width + bp.piece_size + bp.inf_width,
         bp.height + bp.piece_size))
    gb = GameBoard()
    bp.load_images()
    game_start = True
    track = True
    click_chosen = ()
    click_chosen_set = []
    moves, capture, retreats, cannons, slides = gb.valid_moves()
    start_play = False
    screen.fill(p.Color(221, 190, 107))
    mode_selection = True
    clock = p.time.Clock()
    max_depth = 2
    ids = False
    AI = ai.AI(max_depth, ids)
    AI.choose_team = 0

    while mode_selection:
        pos = bp.mode_selection(screen)
        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                sys.exit()
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if pos[0].collidepoint(location):
                    AI.choose_team = 0
                    """set the town's position, move to mode selection pat later"""
                    gb.town_selection()
                    gb.black_to_move = not gb.black_to_move
                    gb.town_selection()
                    gb.black_to_move = not gb.black_to_move
                elif pos[1].collidepoint(location):
                    AI.choose_team = 1
                    gb.town_selection()
                    gb.black_to_move = not gb.black_to_move
                    gb.random_white_town_loc = False
                    gb.town_selection()
                    gb.black_to_move = not gb.black_to_move
                elif pos[2].collidepoint(location):
                    gb.random_black_town_loc = False
                    AI.choose_team = 2
                    gb.town_selection()
                    gb.black_to_move = not gb.black_to_move
                    gb.town_selection()
                    gb.black_to_move = not gb.black_to_move
                mode_selection = False
        screen.fill(p.Color(204, 153, 0))
        bp.mode_selection(screen)
        clock.tick(bp.max_animation)
        p.display.flip()

    while game_start:
        time_consumed = AI.time_consumed
        bp.draw_game(screen, gb, moves, capture, retreats, cannons, slides, click_chosen, time_consumed)
        if gb.game_continue:
            if gb.turn_team != 0:
                for e in p.event.get():
                    if len(moves) == 0 and len(capture) == 0 and len(slides) == 0 and len(cannons) == 0 and len(
                            retreats) == 0:
                        print("STALEMATE!")
                    if e.type == p.QUIT:
                        game_start = False

                    elif gb.black_to_move and AI.choose_team == 1 and track:
                        track = False
                        AI.ai_move(gb)
                        bp.draw_game(screen, gb, moves, capture, retreats, cannons, slides, click_chosen, time_consumed)
                        start_play = True
                        click_chosen = ()
                        click_chosen_set = []

                    elif not gb.black_to_move and AI.choose_team == 2 and track:
                        if len(moves) == 0 and len(capture) == 0 and len(slides) == 0 and len(cannons) == 0 and len(
                                retreats) == 0:
                            print("STALEMATE!")
                        track = False
                        AI.ai_move(gb)
                        bp.draw_game(screen, gb, moves, capture, retreats, cannons, slides, click_chosen, time_consumed)
                        start_play = True
                        click_chosen = ()
                        click_chosen_set = []

                    elif e.type == p.MOUSEBUTTONDOWN and track:
                        location = p.mouse.get_pos()  # (x, y) location of mouse
                        col = (location[0] - bp.piece_size) // bp.piece_size
                        row = (location[1] - bp.piece_size) // bp.piece_size
                        if col > 9 or row > 9:
                            click_chosen = ()
                            click_chosen_set = []
                            break
                        if click_chosen == (
                                row, col):
                            click_chosen = ()
                            click_chosen_set = []
                        else:
                            click_chosen = (row, col)
                            click_chosen_set.append(click_chosen)
                        if len(click_chosen_set) == 2:
                            move = MyMoveRecording(
                                click_chosen_set[0], click_chosen_set[1], gb.board)
                            if len(moves) == 0 and len(capture) == 0 and len(slides) == 0 and len(cannons) == 0 and len(retreats) == 0:
                                print("STALEMATE!")
                            if move in moves:
                                # gb.board[move.start_row][move.start_col] = '--'
                                gb.execute_move(move, flag=True)
                                # gb.board[move.end_row][move.end_col] = move.piece_move
                                start_play = True
                                click_chosen = ()
                                click_chosen_set = []
                            elif move in capture:
                                # gb.board[move.start_row][move.start_col] = '--'
                                gb.execute_move(move, flag=True)
                                # gb.board[move.end_row][move.end_col] = move.piece_move
                                start_play = True
                                click_chosen = ()
                                click_chosen_set = []
                            elif move in retreats:
                                # gb.board[move.start_row][move.start_col] = '--'
                                gb.execute_move(move, flag=True)
                                # gb.board[move.end_row][move.end_col] = move.piece_move
                                start_play = True
                                click_chosen = ()
                                click_chosen_set = []
                            elif move in cannons:
                                gb.execute_move(move, flag=False)
                                start_play = True
                                # gb.board[move.end_row][move.end_col] = '--'
                                click_chosen = ()
                                click_chosen_set = []
                            elif move in slides:
                                # gb.board[move.start_row][move.start_col] = '--'
                                gb.execute_move(move, flag=True)
                                # gb.board[move.end_row][move.end_col] = move.piece_move
                                start_play = True
                                click_chosen = ()
                                click_chosen_set = []
                            else:
                                click_chosen_set = [click_chosen]
                if start_play:
                    moves, capture, retreats, cannons, slides = gb.valid_moves()
                    track = True
                    start_play = False
            screen.fill(p.Color(221, 190, 107))
            bp.draw_game(screen, gb, moves, capture, retreats, cannons, slides, click_chosen, time_consumed)
            clock.tick(bp.max_animation)
            p.display.flip()
            if gb.turn_team == 0:
                gb.turn_team = 1
        else:
            font = p.font.SysFont("calibri", 50)
            text = font.render(
                gb.result,
                True,
                p.Color(0, 0, 255),
                p.Color(221, 190, 107))
            text_rect = text.get_rect()
            text_rect.center = (
                (bp.width + bp.piece_size + bp.inf_width) / 2,
                bp.width / 2)
            bp.draw_game(screen, gb, moves, capture, retreats, cannons, slides, click_chosen, time_consumed)
            screen.blit(text, text_rect)
            p.display.flip()
            for e in p.event.get():
                if e.type == p.QUIT:
                    game_start = False

    p.quit()


if __name__ == '__main__':
    main()
