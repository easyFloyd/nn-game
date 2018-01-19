from random import randint

class Game:
	def __init__(self, board_width = 20, board_height = 20, opponents_number = 3, gui = False, hard = False):
		self.gui = gui
		self.hard = hard
		self.opponents_number = opponents_number
		self.board = {'width': board_width, 'height': board_height}
		self.result = -1 #-1: ingame, 0: lost, 1: win
		self.vectors_and_keys = [
			[[0, 1], 0],
			[[0, -1], 1],
			[[-1, 0], 2],
			[[1, 0], 3]
			]
		
	def start(self):
		self.stepcount = 0
		self.init_player()
		self.init_opponents()
		self.init_goal()
		return self.get_status()
		
	def init_player(self):
		x = randint(1, self.board["width"] - 1)
		y = 1
		self.player = [x,y]
		
	def init_opponents(self):
		self.opponents = []
		for _ in range(self.opponents_number):
			opponent = []
			while opponent == []:
				opponent = [randint(1, self.board["width"]), randint(1, self.board["height"])]
				if opponent in self.opponents or opponent == self.player: opponent = []
			self.opponents.insert(0, opponent)
	
	def init_goal(self):
		self.goal = []
		halfboard = int(self.board["width"] / 2)
		self.goal.append([halfboard - 1, self.board["height"]])
		self.goal.append([halfboard, self.board["height"]])
		self.goal.append([halfboard + 1, self.board["height"]])
		self.goal.append([halfboard + 2, self.board["height"]])
		if self.board["width"] % 2 != 0:
			self.goal.append([halfboard + 3, self.board["height"]])
			
	def step(self, direction):
		# 0 - UP
		# 1 - DOWN
		# 2 - LEFT
		# 3 - RIGHT
		self.stepcount += 1
		self.move(self.player, direction)
		self.check_result()
		if self.result != -1: self.end_game()
		for opponent in self.opponents:
			self.move_opponent(opponent)
		return self.get_status()
	
	def move(self, player, direction):
		if direction == 0:
			#print("Move UP")
			player[1] += 1
		if direction == 1:
			#print("Move DOWN")
			player[1] -= 1
		if direction == 2:
			#print("Move LEFT")
			player[0] -= 1
		if direction == 3:
			#print("Move RIGHT")
			player[0] += 1
	
	def check_result(self):
		if (self.player in self.opponents or
			self.player[0] == 0 or
			self.player[0] == self.board["width"] + 1 or
			self.player[1] == 0 or
			self.player[1] == self.board["height"] + 1):
			self.result = 0
		if (self.result == -1 and self.player in self.goal):
			self.result = 1
	
	def move_opponent(self, opponent):
		direction = self.get_opponent_direction(opponent)
		if direction != -1: self.move(opponent, direction)
		
	def get_opponent_direction(self, opponent):
		if self.hard:
			horizontal, vertical = self.get_opponent_move_vector_hard(opponent)
		else:
			horizontal, vertical = self.get_opponent_move_vector_easy()
		
		if horizontal == 1 and self.is_valid_opponent_move([0,horizontal], opponent):
			return self.get_direction_by_vector([0,horizontal])
		if randint(0,1) == 0:
			if vertical != 0 and self.is_valid_opponent_move([vertical,0], opponent):
				return self.get_direction_by_vector([vertical,0])
			if horizontal == -1 and self.is_valid_opponent_move([0,horizontal], opponent):
				return self.get_direction_by_vector([0,horizontal])
		else:
			if horizontal == -1 and self.is_valid_opponent_move([0,horizontal], opponent):
				return self.get_direction_by_vector([0,horizontal])
			if vertical != 0 and self.is_valid_opponent_move([vertical,0], opponent):
				return self.get_direction_by_vector([vertical,0])
		return -1
		
	def get_opponent_move_vector_hard(self, opponent):
		orig_point = [opponent[0], opponent[1]]
		target = [self.player[0], self.player[1] + 1]
		vertical = 0 # -1: Right, +1: Left
		horizontal = 0 # -1: Down, +1: Up
		if orig_point[0] < target[0]:
			vertical = 1
		elif orig_point[0] > target[0]:
			vertical = -1
		if orig_point[1] < target[1]:
			horizontal = 1
		elif orig_point[1] > target[1]:
			horizontal = -1
		return horizontal, vertical
		
	def get_opponent_move_vector_easy(self):
		return randint(-1,1), randint(-1,1)
		
		
	def is_valid_opponent_move(self, vector, orig_point):
		result = [orig_point[0] + vector[0], orig_point[1] + vector[1]]
		if (result == self.player or
			result in self.opponents or
			result[0] == 0 or
			result[0] == self.board["width"] + 1 or
			result[1] == 0 or
			result[1] == self.board["height"] + 1):
			return False
		else:
			return True
	
	def get_direction_by_vector(self, vector):
		for v in self.vectors_and_keys:
			if v[0] == vector: return v[1]
	
	def end_game(self):
		msg = ""
		if self.result == 1:
			msg = "GOAL"
		else:
			msg = "FAIL"
		raise Exception(msg)
	
	def get_status(self):
		return self.result, self.stepcount, self.player, self.opponents, self.goal
	
if __name__ == "__main__":
	game = Game(hard = True)
	result, stepcount, player, opponents, goal = game.start()
	print("----------------")
	print("START")
	print(" - Player: ", player)
	print(" - Opponents: ", opponents)
	print(" - Goal: ", goal)
	for _ in range(25):
		direction = 0 #randint(0,3)
		print("----------------")
		print("Next move: ", direction)
		result, stepcount, player, opponents, _ = game.step(direction)
		print("Step: ", stepcount)
		print(" - Result: ", result)
		print(" - Player: ", player)
		print(" - Opponents: ", opponents)
	
