import pygame
import threading

from DemoAIs.BOAIapi import BOAIapi
from DemoAIs.BOAIapi import GameState

from DemoAIs.core import turn


class Menu:

    black = (20, 20, 20)
    white = (200, 200, 200)
    green = (130, 220, 130)
    red = (220, 130, 130)
    yellow = (220, 220, 130)
    board_color = (64, 64, 64)
    background_color = (32, 32, 32)

    display_width = 800
    display_height = 600

    board_width = 100
    board_height = 100

    api = BOAIapi(turn)

    game_ids = api.get_games(own=True, game_state=GameState.ANY)
    game_ids.sort()
    game_ids.append("NEW")
    game_ids.reverse()
    game_ids = game_ids[:18]
    game_pos = {}
    games_drawn = {game_id: False for game_id in game_ids}

    def __init__(self):

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        self.gameDisplay.fill(self.background_color)
        pygame.display.set_caption('CoRe - Battle Of AI')
        self.clock = pygame.time.Clock()

    def game_loop(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game_id = self.pos_to_game(pygame.mouse.get_pos())
                        if game_id:

                            if game_id == "NEW":
                                game_ids = self.api.get_games(game_state=GameState.WAITING)
                                if game_ids:
                                    game_id = game_ids[0]
                                else:
                                    game_id = self.api.create_game()

                                self.api.join(game_id)

                            Game(game_id).game_loop()
                            self.gameDisplay.fill(self.background_color)
                            self.games_drawn = {game_id: False for game_id in self.game_ids}

            threading.Thread(target=self.draw_ui).start()
            threading.Thread(target=self.draw_all_games).start()

            pygame.display.update()
            self.clock.tick(1)

    def pos_to_game(self, pos):

        for game in self.game_pos:
            if self.game_pos[game][0] < pos[0] < self.game_pos[game][0]+100 and self.game_pos[game][1] < pos[1] < self.game_pos[game][1]+100:
                return game

    def draw_ui(self):

        # Headline

        label_headline = pygame.font.SysFont("Comic Sans MS", 48).render("Your Recent Games:", True, self.white)
        self.gameDisplay.blit(label_headline, (75, 50))

    def draw_all_games(self):

        x, y = 75, 100

        for game_id in self.game_ids:

            if x >= self.display_width - 100:
                x = 75
                y += 150

            if y >= self.display_height - 100:
                break

            # threading.Thread(target=self.draw_board, args=(game_id, x, y)).start()
            if not self.games_drawn[game_id]:
                self.game_pos.update({game_id: (x, y)})
                threading.Thread(target=self.draw_board, args=(game_id, x, y)).start()
            x += 110

        y += 150

    def draw_board(self, game_id, board_x, board_y):

        self.games_drawn[game_id] = True

        pygame.draw.rect(self.gameDisplay, self.board_color, [board_x, board_y, self.board_width, self.board_height])

        for row in range(7):
            pygame.draw.line(self.gameDisplay, self.black,
                             [board_x, board_y + (row + 1) * (self.board_height / 8)],
                             [board_x + self.board_width, board_y + (row + 1) * (self.board_height / 8)]
                             )

        for column in range(7):
            pygame.draw.line(self.gameDisplay, self.black,
                             [board_x + (column + 1) * (self.board_width / 8), board_y],
                             [board_x + (column + 1) * (self.board_width / 8), board_y + self.board_height]
                             )

        if game_id == "NEW":
            label_game_state = pygame.font.SysFont("Comic Sans MS", 32).render(str(game_id), True, self.white)
            self.gameDisplay.blit(label_game_state, (board_x + 25, board_y + 105))
            return

        # game = json.loads(subprocess.run(
        #     ['curl', '-X', 'GET', 'https://games.battleofai.net/api/games/' + str(game_id), '-H',
        #      '"accept: application/json"'],
        #     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode("UTF-8"))

        game = self.api.status(game_id)
        board = game["history"][-1]["board"]

        for y in range(8):
            for x in range(8):

                if board[y][x] == "O":
                    pygame.draw.circle(self.gameDisplay, self.white,
                                       [
                                           int(board_x + ((self.board_width / 8) * x) + (self.board_width / 8) / 2),
                                           int(board_y + ((self.board_height / 8) * y) + (self.board_height / 8) / 2)
                                       ],
                                       int((self.board_width / 8) / 2) - 1
                                       )

                if board[y][x] == "X":
                    pygame.draw.circle(self.gameDisplay, self.black,
                                       [
                                           int(board_x + ((self.board_width / 8) * x) + (self.board_width / 8) / 2),
                                           int(board_y + ((self.board_height / 8) * y) + (self.board_height / 8) / 2)
                                       ],
                                       int((self.board_width / 8) / 2) - 1
                                       )

        if game["winning_player"] is not None:

            if game["players"][game["winning_player"]]["id"] == self.api.player_id:
                color = self.green

            elif game["players"][game["winning_player"]]["id"] is not None:
                color = self.red

        else: color = self.yellow

        label_game_state = pygame.font.SysFont("Comic Sans MS", 32).render(str(game_id), True, color)
        self.gameDisplay.blit(label_game_state, (board_x + 30, board_y + 105))


class Game:

    black = (20, 20, 20)
    white = (200, 200, 200)
    board_color = (64, 64, 64)
    background_color = (32, 32, 32)

    display_width = 800
    display_height = 600

    board_x = 50
    board_y = 50
    board_width = 500
    board_height = 500

    api = BOAIapi(turn)

    is_ongoing = True
    pointer = -1

    def __init__(self, game_id):

        self.game_id = game_id
        # self.api.wait_for_participants(self.game_id)
        self.game = self.api.status(game_id)

        # self.player1 = self.game["players"][0]["id"]
        # self.player2 = self.game["players"][1]["id"]

        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('CoRe - Battle Of AI')
        self.clock = pygame.time.Clock()

        self.gameDisplay.fill(self.background_color)
        self.draw_game_info()
        self.draw_board()

    def game_loop(self):

        while self.is_ongoing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        btn = self.pos_to_btn(pygame.mouse.get_pos())
                        if btn == "back":
                            self.pointer -= 1
                            self.draw_board()
                        elif btn == "next":
                            self.pointer += 1
                            self.draw_board()
                        elif btn == "return":
                            self.is_ongoing = False

            if self.game["winning_player"] is None:
                threading.Thread(target=self.api.handle_available, args=([self.game_id])).start()
                # self.api.handle_available([self.game_id])
                self.game = self.api.status(self.game_id)
                self.draw_board()
                self.draw_game_score()
                self.draw_players()

            pygame.display.update()
            self.clock.tick(1)

    @staticmethod
    def pos_to_btn(pos):

        if 600 < pos[0] < 651 and 410 < pos[1] < 442:
            return "back"
        elif 680 < pos[0] < 731 and 410 < pos[1] < 442:
            return "next"
        elif 600 < pos[0] < 760 and 510 < pos[1] < 544:
            return "return"
        else:
            return None

    def draw_board(self):

        pygame.draw.rect(self.gameDisplay, self.board_color, [self.board_x, self.board_y, self.board_width, self.board_height])

        for row in range(7):
            pygame.draw.line(self.gameDisplay, self.black,
                             [self.board_x, self.board_y + (row + 1) * (self.board_height / 8)],
                             [self.board_x + self.board_width, self.board_y + (row + 1) * (self.board_height / 8)]
                             )

        for column in range(7):
            pygame.draw.line(self.gameDisplay, self.black,
                             [self.board_x + (column + 1) * (self.board_width / 8), self.board_y],
                             [self.board_x + (column + 1) * (self.board_width / 8), self.board_y + self.board_height]
                             )

        if self.pointer >= 0:
            self.pointer = -1
        elif self.pointer + len(self.game["history"]) < 0:
            self.pointer = -len(self.game["history"])

        board = self.game["history"][self.pointer]["board"]

        for y in range(8):
            for x in range(8):

                if board[y][x] == "O":
                    pygame.draw.circle(self.gameDisplay, self.white,
                                       [
                                           int(self.board_x + ((self.board_width / 8) * x) + (self.board_width / 8) / 2),
                                           int(self.board_y + ((self.board_height / 8) * y) + (self.board_height / 8) / 2)
                                       ],
                                       int((self.board_width / 8) / 2) - 4
                                       )

                if board[y][x] == "X":
                    pygame.draw.circle(self.gameDisplay, self.black,
                                       [
                                           int(self.board_x + ((self.board_width / 8) * x) + (self.board_width / 8) / 2),
                                           int(self.board_y + ((self.board_height / 8) * y) + (self.board_height / 8) / 2)
                                       ],
                                       int((self.board_width / 8) / 2) - 4
                                       )

    def draw_game_info(self):

        # Game ID

        label_game_id = pygame.font.SysFont("Comic Sans MS", 52).render(f"Game {self.game_id}", True, self.white)
        self.gameDisplay.blit(label_game_id, (600, 75))

        # Player Label

        label_players = pygame.font.SysFont("Comic Sans MS", 36).render("Players:", True, self.white)
        self.gameDisplay.blit(label_players, (600, 175))

        # Player IDs

        self.draw_players()

        # Score Label

        label_score = pygame.font.SysFont("Comic Sans MS", 36).render("Score:", True, self.white)
        self.gameDisplay.blit(label_score, (600, 300))

        # Scores

        self.draw_game_score()

        # History (Back)

        pygame.draw.rect(self.gameDisplay, self.white, [600, 410, 51, 32], 3)
        label_next = pygame.font.SysFont("Comic Sans MS", 60).render("<", True, self.white)
        self.gameDisplay.blit(label_next, (612, 403))

        # History (Next)

        pygame.draw.rect(self.gameDisplay, self.white, [680, 410, 51, 32], 3)
        label_back = pygame.font.SysFont("Comic Sans MS", 60).render(">", True, self.white)
        self.gameDisplay.blit(label_back, (696, 403))

        # Return Menu

        pygame.draw.rect(self.gameDisplay, self.white, [600, 510, 160, 34], 3)
        label_back = pygame.font.SysFont("Comic Sans MS", 32).render("Back to Menu", True, self.white)
        self.gameDisplay.blit(label_back, (609, 517))

    def draw_game_score(self):

        pygame.draw.rect(self.gameDisplay, self.background_color, [600, 325, 100, 50])
        score1, score2 = self.board_count()
        label_score = pygame.font.SysFont("Comic Sans MS", 42).render(f"{score1} : {score2}", True, self.white)
        self.gameDisplay.blit(label_score, (600, 325))

    def draw_players(self):

        pygame.draw.rect(self.gameDisplay, self.background_color, [600, 200, 100, 50])

        player1 = self.game["players"][0]["id"]
        if len(self.game["players"]) == 2:
            player2 = self.game["players"][1]["id"]
        else:
            player2 = "?"
            label_wating = pygame.font.SysFont("Comic Sans MS", 42).render("Waiting for Second Player!", True, self.white)
            self.gameDisplay.blit(label_wating, (115, 275))

        label_players = pygame.font.SysFont("Comic Sans MS", 42).render(f"{player1} vs {player2}", True, self.white)
        self.gameDisplay.blit(label_players, (600, 200))

    def board_count(self):

        score1, score2 = 0, 0
        board = self.game["history"][-1]["board"]

        for y in range(8):
            for x in range(8):

                if board[y][x] == "X":
                    score1 += 1
                if board[y][x] == "O":
                    score2 += 1

        return score1, score2


if __name__ == '__main__':
    Menu().game_loop()

# the_blaggy$ #
