from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
	terminal = game_state.is_terminal()
	if (depth==0) or (terminal):
		newScores = game_state.get_scores(terminal)
		return newScores, None
	
	if maximizingPlayer:
		value = float('-inf')
		for move in game_state.get_moves():
			# Simulate Move
			game_state.board_state[move[1]][move[0]] = 1

			# Recursive call ot minimax and passing value up from its children
			v2, a2 = minimax(game_state, depth - 1, False, alpha, beta)
			if v2 > value:
				value = v2
				best_move = move

						
			# Undo simulated move
			game_state.board_state[move[1]][move[0]] = 0
			
			# A-b Pruning
			if value >= beta:
				break
			alpha = max(alpha, value)

		return value, best_move
	else:
		value = float('inf')
		for move in game_state.get_moves():
			# Simulate Move
			game_state.board_state[move[1]][move[0]] = -1

			v2, a2 = minimax(game_state, depth - 1, True, alpha, beta)
			if v2 < value:
				value = v2
				best_move = move

			# Undo simulated move
			game_state.board_state[move[1]][move[0]] = 0


			# A-b Pruning
			if value <= alpha:
				break
			beta = min(beta, value)


		return value, best_move

	
	"""
	YOUR CODE HERE TO FIRST CHECK WHICH PLAYER HAS CALLED THIS FUNCTION (MAXIMIZING OR MINIMIZING PLAYER)
	YOU SHOULD THEN IMPLEMENT MINIMAX WITH ALPHA-BETA PRUNING AND RETURN THE FOLLOWING TWO ITEMS
	1. VALUE
	2. BEST_MOVE
	
	THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
	"""
		  
	

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
	terminal = game_status.is_terminal()
	if (depth==0) or (terminal):
		scores = game_status.get_negamax_scores(terminal)
		return turn_multiplier * scores, None
		
	value = float("-inf")
	best_move = None
	
	for move in game_status.get_moves():
		#stimulate move
		game_status.board_state[move[1]][move[0]] = turn_multiplier
		#recursive call 
		v2, a2 = negamax(game_status, depth -1, -turn_multiplier, -beta, -alpha)
		#flip returned value
		v2 = -v2
		if v2 > value:
			value = v2 
			best_move = move
		#undo simulated move
		game_status.board_state[move[1]][move[0]] = 0
		#alph beta pruning 
		if value >= beta:
			break
		alpha = max(alpha, value)	
	#return value, best_move
	return value, best_move	
			
			
			

	"""
	YOUR CODE HERE TO CALL NEGAMAX FUNCTION. REMEMBER THE RETURN OF THE NEGAMAX SHOULD BE THE OPPOSITE OF THE CALLING
	PLAYER WHICH CAN BE DONE USING -NEGAMAX(). THE REST OF YOUR CODE SHOULD BE THE SAME AS MINIMAX FUNCTION.
	YOU ALSO DO NOT NEED TO TRACK WHICH PLAYER HAS CALLED THE FUNCTION AND SHOULD NOT CHECK IF THE CURRENT MOVE
	IS FOR MINIMAX PLAYER OR NEGAMAX PLAYER
	RETURN THE FOLLOWING TWO ITEMS
	1. VALUE
	2. BEST_MOVE
	
	THE LINE TO RETURN THESE TWO IS COMMENTED BELOW WHICH YOU CAN USE
	
	"""
