import random
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
			_, _, player, opponents, goal = game.start()
			prev_observation = self.generate_observation(player, opponents, goal)
			prev_goal_distance = self.get_goal_distance(player, goal)
			for _ in range(self.goal_steps):
				action = randint(0,3)
				result, _, player, opponents, _ = game.step(action)
				if result == 0:
					training_data.append([[action, prev_observation], -1])
					break
				elif result == 1:
					training_data.append([[action, prev_observation], 1])
					break
				else:
					goal_distance = self.get_goal_distance(player, goal)
					if goal_distance < prev_goal_distance:
						training_data.append([[action, prev_observation], 1])
					else:
						training_data.append([[action, prev_observation], 0])
					prev_observation = self.generate_observation(player, opponents, goal)
					prev_goal_distance = goal_distance
		print(len(training_data))
		return training_data
		
	def generate_observation(self, player, opponents, goal):
		barrier_up = self.is_direction_block(player, opponents, self.vectors_and_keys[0][0])
		barrier_down = self.is_direction_block(player, opponents, self.vectors_and_keys[1][0])
		barrier_left = self.is_direction_block(player, opponents, self.vectors_and_keys[2][0])
		barrier_right = self.is_direction_block(player, opponents, self.vectors_and_keys[3][0])
		goal_angle = self.get_goal_angle(player, goal)
		return [int(barrier_up), int(barrier_down), int(barrier_left), int(barrier_right), goal_angle]
		
	def is_direction_block(self, player, opponents, direction):
		point = [player[0] + direction[0], player[1] + direction[1]]
		return point in opponents or point[0] == 0 or point[1] == 0 or point[0] == 21 or point[1] == 21
		
	def get_goal_angle(self, player, goal):
		if player[0] < goal[0][0]:
			return -1
		if player[0] > goal[3][0]:
			return 1
		else:
			return 0
	
	def get_goal_distance(self, player, goal):
		x_distance = 0
		if player[0] < goal[0][0]:
			x_distance = goal[0][0] - player[0]
		elif player[0] > goal[3][0]:
			x_distance = player[0] - goal[3][0]
		return (20 - player[1] + x_distance)
		
	def model(self):
		return []
		
	def train_model(self, training_data, model):
		return []
		
	def test_model(self, model):
		for _ in range(self.test_games):
			game_memory = []
			game = Game()
			_, _, player, opponents, goal = game.start()
			prev_observation = self.generate_observation(player, opponents, goal)
			for _ in range(self.goal_steps):
				predictions = self.fake_predictions()
				
		
	def train(self):
		training_data = self.initial_population()
		nn_model = self.model()
		nn_model = self.train_model(training_data, nn_model)
		self.test_model(nn_model)
		
	def fake_predictions(self):
		predictions = []
		predictions.append(random.uniform(0.0, 1.0))
		predictions.append(random.uniform(0.0, 1.0 - predictions[0]))
		predictions.append(random.uniform(0.0, 1.0 - predictions[0] - predictions[1]))
		predictions.append(1.0 - predictions[0] - predictions[1] - predictions[2])
		random.shuffle(predictions)
		return predictions
		
	def test(self):
		training_data = self.initial_population()
		i = 0
		for t in training_data:
			if t[1] == 1 and i < 20:
				print(t)
				i+=1
		
if __name__ == "__main__":
	GameNN().test()
