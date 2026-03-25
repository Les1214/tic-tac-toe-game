# -*- coding: utf-8 -*-


class GameStatus:


	def __init__(self, board_state, turn_O):

		self.board_state = board_state
		self.turn_O = turn_O
		self.oldScores = 0

		self.winner = ""
	
	def is_terminal(self):
		"""
		YOUR CODE HERE TO CHECK IF ANY CELL IS EMPTY WITH THE VALUE 0. IF THERE IS NO EMPTY
		THEN YOU SHOULD ALSO RETURN THE WINNER OF THE GAME BY CHECKING THE SCORES FOR EACH PLAYER 
      """
		# Grab a len of board for future check
		grid_size = len(self.board_state)
		
		#calculate score
		score = self.get_scores(True)
		#check if the current state of the board is terminal
		if (grid_size == 3 and score != 0) or (not any(0 in row for row in self.board_state)):
			
			#determine winner
			if score > 0 :
				self.winner = "Human"
			elif score < 0 :
				self.winner = "Computer Player"
			else: 
				self.winner = "Draw"
				
			#return terminal state	
			return True 
			
		return False	
		

	def get_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE THE SCORES. MAKE SURE YOU ADD THE SCORE FOR EACH PLAYER BY CHECKING 
        EACH TRIPLET IN THE BOARD IN EACH DIRECTION (HORIZONAL, VERTICAL, AND ANY DIAGONAL DIRECTION)
        
        YOU SHOULD THEN RETURN THE CALCULATED SCORE WHICH CAN BE POSITIVE (HUMAN PLAYER WINS),
        NEGATIVE (AI PLAYER WINS), OR 0 (DRAW)
        
        """  
		#find board size
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		score = 0

		#check for horizontal triplets
		for row in range(rows):
			for col in range(cols - 2):
				total = self.board_state[row][col] + self.board_state[row][col + 1] + self.board_state[row][col + 2]
				if total == 3:
					score += 1
				elif total == -3:
					score -= 1

		#check for vertical triplets
		for row in range(rows - 2):
			for col in range(cols):
				total = self.board_state[row][col] + self.board_state[row + 1][col] + self.board_state[row + 2][col]
				if total == 3:
					score += 1
				elif total == -3:
					score -= 1

		#check for diagonal down right triplets
		for row in range(rows - 2):
			for col in range(cols - 2):
				total = self.board_state[row][col] + self.board_state[row + 1][col + 1] + self.board_state[row + 2][col + 2]
				if total == 3:
					score += 1
				elif total == -3:
					score -= 1

		#check for diagonal down left triplets
		for row in range(rows - 2):
			for col in range(2, cols):
				total = self.board_state[row][col] + self.board_state[row + 1][col - 1] + self.board_state[row + 2][col - 2]
				if total == 3:
					score += 1
				elif total == -3:
					score -= 1
				
		return score

	def get_negamax_scores(self, terminal):
		"""
        YOUR CODE HERE TO CALCULATE NEGAMAX SCORES. THIS FUNCTION SHOULD EXACTLY BE THE SAME OF GET_SCORES UNLESS
        YOU SET THE SCORE FOR NEGAMX TO A VALUE THAT IS NOT AN INCREMENT OF 1 (E.G., YOU CAN DO SCORES = SCORES + 100 
                                                                               FOR HUMAN PLAYER INSTEAD OF 
                                                                               SCORES = SCORES + 1)
        """
		return self.get_scores(terminal)
	    

	def get_moves(self):
		moves = []
		"""
        YOUR CODE HERE TO ADD ALL THE NON EMPTY CELLS TO MOVES VARIABLES AND RETURN IT TO BE USE BY YOUR
        MINIMAX OR NEGAMAX FUNCTIONS
        """
		rows = len(self.board_state)
		cols = len(self.board_state[0])
		for row in range(rows):
			for col in range(cols):
				if self.board_state[row][col] == 0:
					moves.append([col, row])

		return moves


	def get_new_state(self, move):
		new_board_state = self.board_state.copy()
		x, y = move[0], move[1]
		new_board_state[y][x] = -1 if self.turn_O else 1
		return GameStatus(new_board_state, not self.turn_O)
