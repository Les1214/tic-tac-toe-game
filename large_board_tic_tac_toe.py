"""
PLEASE READ THE COMMENTS BELOW AND THE HOMEWORK DESCRIPTION VERY CAREFULLY BEFORE YOU START CODING

 The file where you will need to create the GUI which should include (i) drawing the grid, (ii) call your Minimax/Negamax functions
 at each step of the game, (iii) allowing the controls on the GUI to be managed (e.g., setting board size, using 
																				 Minimax or Negamax, and other options)
 In the example below, grid creation is supported using pygame which you can use. You are free to use any other 
 library to create better looking GUI with more control. In the __init__ function, GRID_SIZE (Line number 36) is the variable that
 sets the size of the grid. Once you have the Minimax code written in multiAgents.py file, it is recommended to test
 your algorithm (with alpha-beta pruning) on a 3x3 GRID_SIZE to see if the computer always tries for a draw and does 
 not let you win the game. Here is a video tutorial for using pygame to create grids http://youtu.be/mdTeqiWyFnc
 
 
 PLEASE CAREFULLY SEE THE PORTIONS OF THE CODE/FUNCTIONS WHERE IT INDICATES "YOUR CODE BELOW" TO COMPLETE THE SECTIONS
 
"""
import pygame
import numpy as np
from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random

mode = "player_vs_ai" # default mode for playing the game (player vs AI)

PANEL_HEIGHT = 160
class RandomBoardTicTacToe:
	def __init__(self, size=(600, 600)):

		self.size = self.width, self.height = size

		self.screen_size = (self.width, self.height + PANEL_HEIGHT)

		# Define some colors
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.GREEN = (0, 255, 0)
		self.RED = (255, 0, 0)
		self.BLUE = (0, 0, 255)
		self.GRAY = (80, 80, 80)
		self.LIGHT_BLUE = (100, 160, 230)
		self.ORANGE = (230, 150, 30)
		self.YELLOW = (240, 220, 50)
		self.PANEL_COLOR = (30, 30, 50)

		# Grid Size
		self.GRID_SIZE = 3
		self.OFFSET = 5


		# Set the Width and Height of Grid
		self.WIDTH = (self.size[0] - self.OFFSET*2) / self.GRID_SIZE
		self.HEIGHT = (self.size[1] - self.OFFSET*2) / self.GRID_SIZE

		# Margin between each grid cell
		self.MARGIN = 5

		# Track algorithm choice and scores
		self.use_negamax = False
		self.human_score = 0
		self.computer_score = 0
		self.status_msg = ""

		# Human symbol: True = human plays X, False = human plays O
		self.human_is_X = True

		# Initialize pygame
		pygame.init()

		# Fonts for the panel
		self.font_large  = pygame.font.SysFont("Arial", 20, bold=True)
		self.font_small  = pygame.font.SysFont("Arial", 15)
		self.font_menu   = pygame.font.SysFont("Arial", 26, bold=True)
		self.font_title  = pygame.font.SysFont("Arial", 40, bold=True)

		# This creates initial gamestate class
		board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
		self.game_state = GameStatus(board, False)


	def _recalc_dims(self):
		"""Recalculate cell width/height after GRID_SIZE changes."""
		self.WIDTH  = (self.size[0] - self.OFFSET*2) / self.GRID_SIZE
		self.HEIGHT = (self.size[1] - self.OFFSET*2) / self.GRID_SIZE



	# Main Menu
	def show_main_menu(self):
		"""
		Displays the main menu screen where the player selects:
		  - Board size (3x3, 4x4, 5x5)
		  - Mode (vs AI, vs Human)
		  - Symbol (X or O)
		  - Algorithm (Minimax, Negamax)
		Then clicks Play to start the game.
		Returns the chosen (mode, grid_size, human_is_X, use_negamax).
		"""
		screen = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption("Tic-Tac-Toe | Main Menu")

		# Local selections (default values)
		sel_size    = 3
		sel_mode    = "player_vs_ai"
		sel_is_X    = True
		sel_negamax = False

		clock = pygame.time.Clock()

		while True:
			screen.fill(self.PANEL_COLOR)

			# Title
			title = self.font_title.render("Tic-Tac-Toe", True, self.WHITE)
			screen.blit(title, (self.screen_size[0] // 2 - title.get_width() // 2, 40))

			subtitle = self.font_small.render("Large Board Edition  |  CSE 5120", True, (180, 180, 180))
			screen.blit(subtitle, (self.screen_size[0] // 2 - subtitle.get_width() // 2, 95))

			
			pygame.draw.line(screen, self.GRAY, (40, 125), (self.screen_size[0] - 40, 125), 2)

			# Board Size
			lbl = self.font_menu.render("Board Size", True, self.WHITE)
			screen.blit(lbl, (40, 145))

			size_rects = {}
			bx = 40
			for sz in [3, 4, 5]:
				col = self.LIGHT_BLUE if sel_size == sz else self.GRAY
				r = pygame.Rect(bx, 185, 90, 45)
				pygame.draw.rect(screen, col, r, border_radius=8)
				t = self.font_menu.render(f"{sz}x{sz}", True, self.WHITE)
				screen.blit(t, (bx + 90//2 - t.get_width()//2, 185 + 45//2 - t.get_height()//2))
				size_rects[sz] = r
				bx += 105

			# Mode
			lbl2 = self.font_menu.render("Mode", True, self.WHITE)
			screen.blit(lbl2, (40, 255))

			mode_rects = {}
			mx = 40
			for label, m in [("vs AI", "player_vs_ai"), ("vs Human", "player_vs_player")]:
				col = self.LIGHT_BLUE if sel_mode == m else self.GRAY
				r = pygame.Rect(mx, 295, 150, 45)
				pygame.draw.rect(screen, col, r, border_radius=8)
				t = self.font_menu.render(label, True, self.WHITE)
				screen.blit(t, (mx + 150//2 - t.get_width()//2, 295 + 45//2 - t.get_height()//2))
				mode_rects[m] = r
				mx += 165

			# Symbol (X or O)
			lbl3 = self.font_menu.render("Your Symbol", True, self.WHITE)
			screen.blit(lbl3, (40, 365))

			sym_rects = {}
			sx = 40
			for label, is_x in [("X  (cross)", True), ("O  (nought)", False)]:
				col = self.LIGHT_BLUE if sel_is_X == is_x else self.GRAY
				r = pygame.Rect(sx, 405, 165, 45)
				pygame.draw.rect(screen, col, r, border_radius=8)
				t = self.font_menu.render(label, True, self.WHITE)
				screen.blit(t, (sx + 165//2 - t.get_width()//2, 405 + 45//2 - t.get_height()//2))
				sym_rects[is_x] = r
				sx += 180

			# Algorithm
			lbl4 = self.font_menu.render("Algorithm", True, self.WHITE)
			screen.blit(lbl4, (40, 475))

			algo_rects = {}
			ax = 40
			for label, val in [("Minimax", False), ("Negamax", True)]:
				col = self.LIGHT_BLUE if sel_negamax == val else self.GRAY
				r = pygame.Rect(ax, 515, 150, 45)
				pygame.draw.rect(screen, col, r, border_radius=8)
				t = self.font_menu.render(label, True, self.WHITE)
				screen.blit(t, (ax + 150//2 - t.get_width()//2, 515 + 45//2 - t.get_height()//2))
				algo_rects[val] = r
				ax += 165

			# Play Button
			play_rect = pygame.Rect(
				self.screen_size[0]//2 - 100, 
				self.screen_size[1] - 90, 
				200, 55
			)
			pygame.draw.rect(screen, self.GREEN, play_rect, border_radius=10)
			play_lbl = self.font_title.render("PLAY", True, self.BLACK)
			screen.blit(play_lbl, (play_rect.centerx - play_lbl.get_width()//2,
								   play_rect.centery - play_lbl.get_height()//2))

			pygame.display.update()

			# Event Handling
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()

					# Board size
					for sz, r in size_rects.items():
						if r.collidepoint(pos):
							sel_size = sz

					# Mode
					for m, r in mode_rects.items():
						if r.collidepoint(pos):
							sel_mode = m

					# Symbol
					for is_x, r in sym_rects.items():
						if r.collidepoint(pos):
							sel_is_X = is_x

					# Algorithm
					for val, r in algo_rects.items():
						if r.collidepoint(pos):
							sel_negamax = val

					# Play button - apply selections and return
					if play_rect.collidepoint(pos):
						self.GRID_SIZE   = sel_size
						self.human_is_X  = sel_is_X
						self.use_negamax = sel_negamax
						self._recalc_dims()
						return sel_mode

			clock.tick(30)


	# Game Functions

	def draw_game(self):
		# Create a 2 dimensional array using the column and row variables
		pygame.init()
		self.screen = pygame.display.set_mode(self.screen_size)
		pygame.display.set_caption("Tic Tac Toe Random Grid")
		self.screen.fill(self.WHITE)

		"""
		YOUR CODE HERE TO DRAW THE GRID OTHER CONTROLS AS PART OF THE GUI
		"""

		pygame.draw.rect(self.screen, self.PANEL_COLOR, (0, 0, self.screen_size[0], PANEL_HEIGHT))

		# Title
		title = self.font_large.render("Tic-Tac-Toe | Large Board", True, self.WHITE)
		self.screen.blit(title, (10, 8))

		# Board size buttons
		lbl = self.font_small.render("Board size:", True, (180,180,180))
		self.screen.blit(lbl, (10, 38))
		self._size_rects = {}
		bx = 105
		for sz in [3, 4, 5]:
			col = self.LIGHT_BLUE if self.GRID_SIZE == sz else self.GRAY
			r = pygame.Rect(bx, 34, 46, 24)
			pygame.draw.rect(self.screen, col, r, border_radius=4)
			t = self.font_small.render(f"{sz}x{sz}", True, self.WHITE)
			self.screen.blit(t, (bx + 10, 38))
			self._size_rects[sz] = r
			bx += 52

		# Algorithm toggle buttons
		lbl2 = self.font_small.render("Algorithm:", True, (180,180,180))
		self.screen.blit(lbl2, (10, 70))
		self._algo_rects = {}
		ax = 105
		for label, val in [("Minimax", False), ("Negamax", True)]:
			col = self.LIGHT_BLUE if self.use_negamax == val else self.GRAY
			r = pygame.Rect(ax, 66, 80, 24)
			pygame.draw.rect(self.screen, col, r, border_radius=4)
			t = self.font_small.render(label, True, self.WHITE)
			self.screen.blit(t, (ax + 10, 70))
			self._algo_rects[val] = r
			ax += 88

		# Mode buttons
		lbl3 = self.font_small.render("Mode:", True, (180,180,180))
		self.screen.blit(lbl3, (10, 102))
		self._mode_rects = {}
		mx = 105
		for label, m in [("vs AI", "player_vs_ai"), ("vs Human", "player_vs_player")]:
			col = self.LIGHT_BLUE if mode == m else self.GRAY
			r = pygame.Rect(mx, 98, 88, 24)
			pygame.draw.rect(self.screen, col, r, border_radius=4)
			t = self.font_small.render(label, True, self.WHITE)
			self.screen.blit(t, (mx + 10, 102))
			self._mode_rects[m] = r
			mx += 96

		# Reset button
		self._reset_rect = pygame.Rect(self.screen_size[0] - 88, 98, 80, 24)
		pygame.draw.rect(self.screen, self.GREEN, self._reset_rect, border_radius=4)
		rt = self.font_small.render("Reset", True, self.BLACK)
		self.screen.blit(rt, (self.screen_size[0] - 68, 102))

		# Score display
		score_txt = f"Human: {self.human_score}    Computer: {self.computer_score}"
		self.screen.blit(self.font_small.render(score_txt, True, self.ORANGE), (10, 130))

		# Winner / status message
		if self.status_msg:
			self.screen.blit(self.font_large.render(self.status_msg, True, self.YELLOW), (250, 125))

		# Draw box the grid will be within
		top = PANEL_HEIGHT
		pygame.draw.line(self.screen, self.BLACK, (self.OFFSET, top + self.OFFSET), (self.size[0]-self.OFFSET, top + self.OFFSET), self.MARGIN)
		pygame.draw.line(self.screen, self.BLACK, (self.OFFSET, top + self.OFFSET + (self.GRID_SIZE * self.HEIGHT)), (self.size[0]-self.OFFSET, top + self.OFFSET + (self.GRID_SIZE * self.HEIGHT)), self.MARGIN)
		pygame.draw.line(self.screen, self.BLACK, (self.OFFSET, top + self.OFFSET), (self.OFFSET, top + self.OFFSET + (self.GRID_SIZE * self.HEIGHT)), self.MARGIN)
		pygame.draw.line(self.screen, self.BLACK, (self.size[0]-self.OFFSET, top + self.OFFSET), (self.size[0]-self.OFFSET, top + self.OFFSET + (self.GRID_SIZE * self.HEIGHT)), self.MARGIN)

		# Draw the grid
		for x in range(1, self.GRID_SIZE):
			pygame.draw.line(self.screen, self.BLACK, (self.OFFSET, top + self.OFFSET + self.HEIGHT * x), (self.size[0]-self.OFFSET, top + self.OFFSET + self.HEIGHT * x), self.MARGIN)
			pygame.draw.line(self.screen, self.BLACK, (self.OFFSET + self.WIDTH * x, top + self.OFFSET), (self.OFFSET + self.WIDTH * x, top + self.OFFSET + self.GRID_SIZE * self.HEIGHT), self.MARGIN)

		self.change_turn()
		pygame.display.update()


	def change_turn(self):
		if(self.game_state.turn_O):
			pygame.display.set_caption("Tic Tac Toe - O's turn")
		else:
			pygame.display.set_caption("Tic Tac Toe - X's turn")


	def draw_circle(self, x, y):
		"""
		YOUR CODE HERE TO DRAW THE CIRCLE FOR THE NOUGHTS PLAYER
		"""
		# Shifted down by PANEL_HEIGHT so pieces draw in the board area, not the panel
		top = PANEL_HEIGHT
		pygame.draw.circle(self.screen, self.BLUE,
			(int(self.OFFSET + self.WIDTH * x + self.WIDTH / 2),
			 int(top + self.OFFSET + self.HEIGHT * y + self.HEIGHT / 2)),
			int(self.WIDTH / 3), self.MARGIN)


	def draw_cross(self, x, y):
		"""
		YOUR CODE HERE TO DRAW THE CROSS FOR THE CROSS PLAYER AT THE CELL THAT IS SELECTED VIA THE gui
		"""
		# Shifted down by PANEL_HEIGHT so pieces draw in the board area, not the panel
		top = PANEL_HEIGHT
		pygame.draw.line(self.screen, self.RED,
			(self.OFFSET + self.WIDTH * x + self.WIDTH / 4,        top + self.OFFSET + self.HEIGHT * y + self.HEIGHT / 4),
			(self.OFFSET + self.WIDTH * x + (self.HEIGHT * 3 / 4), top + self.OFFSET + self.HEIGHT * y + (self.HEIGHT * 3 / 4)), self.MARGIN)
		pygame.draw.line(self.screen, self.RED,
			(self.OFFSET + self.WIDTH * x + (self.HEIGHT * 3 / 4), top + self.OFFSET + self.HEIGHT * y + self.HEIGHT / 4),
			(self.OFFSET + self.WIDTH * x + self.WIDTH / 4,        top + self.OFFSET + self.HEIGHT * y + (self.HEIGHT * 3 / 4)), self.MARGIN)


	def is_game_over(self):
		"""
		YOUR CODE HERE TO SEE IF THE GAME HAS TERMINATED AFTER MAKING A MOVE. YOU SHOULD USE THE IS_TERMINAL()
		FUNCTION FROM GAMESTATUS_5120.PY FILE (YOU WILL FIRST NEED TO COMPLETE IS_TERMINAL() FUNCTION)
		
		YOUR RETURN VALUE SHOULD BE TRUE OR FALSE TO BE USED IN OTHER PARTS OF THE GAME
		"""
		return self.game_state.is_terminal()


	def move(self, move):
		self.game_state = self.game_state.get_new_state(move)


	def play_ai(self):
		"""
		YOUR CODE HERE TO CALL MINIMAX OR NEGAMAX DEPENDEING ON WHICH ALGORITHM SELECTED FROM THE GUI
		ONCE THE ALGORITHM RETURNS THE BEST MOVE TO BE SELECTED, YOU SHOULD DRAW THE NOUGHT (OR CIRCLE DEPENDING
		ON WHICH SYMBOL YOU SELECTED FOR THE AI PLAYER)
		
		THE RETURN VALUES FROM YOUR MINIMAX/NEGAMAX ALGORITHM SHOULD BE THE SCORE, MOVE WHERE SCORE IS AN INTEGER
		NUMBER AND MOVE IS AN X,Y LOCATION RETURNED BY THE AGENT
		"""

		# Call Minimax or Negamax depending on which algorithm is selected
		if self.use_negamax:
			value, best_move = negamax(self.game_state, 6, -1)
		else:
			value, best_move = minimax(self.game_state, 6, False)  # False = minimising (AI) turn

		if best_move is None:
			return

		# AI always plays O (circle) when human is X, and vice versa
		if self.human_is_X:
			self.draw_circle(best_move[0], best_move[1])
		else:
			self.draw_cross(best_move[0], best_move[1])

		self.move(best_move)

		self.change_turn()
		pygame.display.update()

		
		terminal = self.game_state.is_terminal()

		""" USE self.game_state.get_scores(terminal) HERE TO COMPUTE AND DISPLAY THE FINAL SCORES """
		score = self.game_state.get_scores(terminal)
		return score


	def game_reset(self):
		"""
		YOUR CODE HERE TO RESET THE BOARD TO VALUE 0 FOR ALL CELLS AND CREATE A NEW GAME STATE WITH NEWLY INITIALIZED
		BOARD STATE
		"""
		self.status_msg = ""
		self.game_over = False

		# Fill game_state with board state filled with 0
		board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
		self.game_state = GameStatus(board, False)

		self._recalc_dims()
		self.draw_game()
		pygame.display.update()


	def _handle_panel_click(self, pos):
		"""Check if any panel button was clicked and act on it. Returns True if handled."""

		# Board size buttons
		for sz, r in self._size_rects.items():
			if r.collidepoint(pos):
				self.GRID_SIZE = sz
				self.human_score = 0
				self.computer_score = 0
				self.game_reset()
				return True

		# Algorithm buttons
		for val, r in self._algo_rects.items():
			if r.collidepoint(pos):
				self.use_negamax = val
				self.draw_game()
				return True

		#mode buttons
		global mode
		for m, r in self._mode_rects.items():
			if r.collidepoint(pos):
				mode = m
				self.game_reset()
				return True

		# Reset button
		if self._reset_rect.collidepoint(pos):
			self.game_reset()
			return True

		return False


	def play_game(self, mode="player_vs_ai"):
		done = False
		self.game_over = False
		clock = pygame.time.Clock()

		while not done:
			mode = globals()["mode"]
			for event in pygame.event.get():  # User did something
				"""
				YOUR CODE HERE TO CHECK IF THE USER CLICKED ON A GRID ITEM. EXIT THE GAME IF THE USER CLICKED EXIT
				"""

				"""
				YOUR CODE HERE TO HANDLE THE SITUATION IF THE GAME IS OVER. IF THE GAME IS OVER THEN DISPLAY THE SCORE,
				THE WINNER, AND POSSIBLY WAIT FOR THE USER TO CLEAR THE BOARD AND START THE GAME AGAIN (OR CLICK EXIT)
				"""

				"""
				YOUR CODE HERE TO NOW CHECK WHAT TO DO IF THE GAME IS NOT OVER AND THE USER SELECTED A NON EMPTY CELL
				IF CLICKED A NON EMPTY CELL, THEN GET THE X,Y POSITION, SET ITS VALUE TO 1 (SELECTED BY HUMAN PLAYER),
				DRAW CROSS (OR NOUGHT DEPENDING ON WHICH SYMBOL YOU CHOSE FOR YOURSELF FROM THE gui) AND CALL YOUR 
				PLAY_AI FUNCTION TO LET THE AGENT PLAY AGAINST YOU
				"""

				if event.type == pygame.QUIT:
					done = True

				if event.type == pygame.MOUSEBUTTONUP:
					# Get the position
					mouse_pos = pygame.mouse.get_pos()

					# If click is in the panel area, handle button clicks
					if mouse_pos[1] < PANEL_HEIGHT:
						self._handle_panel_click(mouse_pos)
						continue
					
					if self.game_over:
						continue

					# Change the x/y screen coordinates to grid coordinates
					# Subtract PANEL_HEIGHT from y so grid coords are relative to the board
					adjusted_y = mouse_pos[1] - PANEL_HEIGHT
					if self.OFFSET < mouse_pos[0] <= self.size[0] - self.OFFSET and self.OFFSET < adjusted_y <= self.size[1] - self.OFFSET:
						grid_x = int((mouse_pos[0] - self.OFFSET) // self.WIDTH)
						grid_y = int((adjusted_y   - self.OFFSET) // self.HEIGHT)
						coordinates = [grid_x, grid_y]

						# Checks if the grid is empty and if so fills it in with appropriate symbol and makes the move
						if self.game_state.board_state[grid_y][grid_x] == 0:
							if mode == "player_vs_player":
								if self.game_state.turn_O == True:
									self.draw_circle(grid_x, grid_y)
								else:
									self.draw_cross(grid_x, grid_y)

								self.move(coordinates)

								self.game_over = self.is_game_over()

								self.change_turn()

							elif mode == "player_vs_ai":
								# Draw human symbol based on their choice
								if self.human_is_X:
									self.draw_cross(grid_x, grid_y)
								else:
									self.draw_circle(grid_x, grid_y)

								self.move(coordinates)
								self.change_turn()

								self.game_over = self.is_game_over()

								pygame.display.update()

								if not self.game_over:
									self.play_ai()

									self.game_over = self.is_game_over()
									
						# Show score and winner when game ends
						if self.game_over:
							terminal = True
							score = self.game_state.get_scores(terminal)
							if score > 0:
								self.status_msg = f"Human wins! ({score})"
								self.human_score += 1
							elif score < 0:
								self.status_msg = f"Computer wins! ({score})"
								self.computer_score += 1
							else:
								self.status_msg = "Draw!"
							self.draw_game()

			# Check if the game is human vs human or human vs AI player from the GUI. 
			# If it is human vs human then your opponent should have the value of the selected cell set to -1
			# Then draw the symbol for your opponent in the selected cell
			# Within this code portion, continue checking if the game has ended by using is_terminal function

			# Update the screen with what was drawn.
			pygame.display.update()

		pygame.quit()

tictactoegame = RandomBoardTicTacToe()
"""
YOUR CODE HERE TO SELECT THE OPTIONS VIA THE GUI CALLED FROM THE ABOVE LINE
AFTER THE ABOVE LINE, THE USER SHOULD SELECT THE OPTIONS AND START THE GAME. 
YOUR FUNCTION PLAY_GAME SHOULD THEN BE CALLED WITH THE RIGHT OPTIONS AS SOON
AS THE USER STARTS THE GAME
"""

# Show the main menu first, get the chosen mode, then start the game
mode = tictactoegame.show_main_menu()
tictactoegame.game_reset()
tictactoegame.play_game(mode)
