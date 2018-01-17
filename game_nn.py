from game import Game
from random import randint

class GameNN:
	def __init__(self, initial_games = 100, test_games = 100, goal_steps = 100, lr = 1e-2, filename = 'game_nn.tflearn'):
		self.initial_games = initial_games
		self.test_games = test_games
		self.goal_steps = goal_steps
		self.lr = lr
		self.filename = filename
		self.vectors_and_keys = [
			[[0, 1], 0],
			[[0, -1], 1],
			[[-1, 0], 2],
			[[1, 0], 3]
			]
			
	def initial_population(self):
		training_data = []
		for _ in range(self.initial_games):
			game = Game()
			_, _, player, _ = game.start()
			prev_observation = self.generate_observation(player)
			for _ in range(self.goal_steps):
				action = randint(0,3)
				result, _, player, _ = game.step(action)
				if result == 0:
					training_data.append([[action, prev_observation], 0])
					break
				elif result == 1:
					training_data.append([[action, prev_observation], 1])
					break
				else:
					training_data.append([[action, prev_observation], 1])
					prev_observation = self.generate_observation(player)
		print(len(training_data))
		return training_data
		
	def generate_observation(self, player):
		barrier_up = self.is_direction_block(player, self.vectors_and_keys[0][0])
		barrier_down = self.is_direction_block(player, self.vectors_and_keys[1][0])
		barrier_left = self.is_direction_block(player, self.vectors_and_keys[2][0])
		barrier_right = self.is_direction_block(player, self.vectors_and_keys[3][0])
		return [barrier_up, barrier_down, barrier_left, barrier_right]
		
	def is_direction_block(self, player, direction):
		point = [player[0] + direction[0], player[1] + direction[1]]
		return point[0] == 0 or point[1] == 0 or point[0] == 21 or point[1] == 21
		
	def train(self):
		training_data = self.initial_population()
		for t in training_data:
			if t[1] == 0: print(t)
		
if __name__ == "__main__":
	GameNN().train()
