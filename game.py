from random import randint

class Game:
	def __init__(self, board_width = 20, board_height = 20, opponents_number = 3, gui = False):
		self.gui = gui
		self.opponents_number = opponents_number
		self.board = {'width': board_width, 'height': board_height}
		self.result = -1 #-1: ingame, 0: lost, 1: win
		
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
		if self.result != -1: self.end_game()
		self.stepcount += 1
		self.move(self.player, direction)
		self.check_result()
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
		orig = list(opponent)
		self.move(opponent, randint(0,3))
		if (opponent == self.player or
			opponent[0] == 0 or
			opponent[0] == self.board["width"] + 1 or
			opponent[1] == 0 or
			opponent[1] == self.board["height"] + 1):
			opponent[0] = orig[0]
			opponent[1] = orig[1]
	
	def end_game(self):
		raise Exception("Game over")
	
	def get_status(self):
		return self.result, self.stepcount, self.player, self.opponents, self.goal
	
if __name__ == "__main__":
	game = Game()
	print(game.start())
	for _ in range(20):
		print(game.step(randint(0,3)))
