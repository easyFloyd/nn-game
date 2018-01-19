import random
import numpy as np
from game import Game
from random import randint
from statistics import mean
import tflearn
import math
from tflearn.layers.core import input_data, fully_connected
from tflearn.layers.estimator import regression

class GameNN:
	def __init__(self, initial_games = 2000, test_games = 100, goal_steps = 100, lr = 1e-2, filename = 'game_nn.tflearn'):
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
					training_data.append([np.append([action], prev_observation), -1])
					break
				elif result == 1:
					training_data.append([np.append([action], prev_observation), 1])
					break
				else:
					goal_distance = self.get_goal_distance(player, goal)
					if goal_distance < prev_goal_distance:
						training_data.append([np.append([action], prev_observation), 1])
					else:
						training_data.append([np.append([action], prev_observation), 0])
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
		network = input_data(shape=[None, 6, 1], name='input')
		network = fully_connected(network, 36, activation='relu')
		network = fully_connected(network, 1, activation='linear')
		network = regression(network, optimizer='adam', learning_rate=self.lr, loss='mean_square', name='target')
		model = tflearn.DNN(network, tensorboard_dir='log', tensorboard_verbose=0)
		return model
		
	def train_model(self, training_data, model):
		X = np.array([i[0] for i in training_data]).reshape(-1, 6, 1)
		y = np.array([i[1] for i in training_data]).reshape(-1, 1)
		model.fit(X,y, n_epoch = 3, shuffle = True, run_id = self.filename)
		model.save(self.filename)
		return model
		
	def test_model(self, model):
		games = []
		steps_arr = []
		goal_count = 0
		fail_count = 0
		for _ in range(self.test_games):
			game_memory = []
			game = Game()
			_, stepcount, player, opponents, goal = game.start()
			prev_observation = self.generate_observation(player, opponents, goal)
			for _ in range(self.goal_steps):
				# predictions = self.fake_predictions()
				predictions = []
				for action in range(0,4):
					predictions.append(model.predict(np.append([action], prev_observation).reshape(-1, 6, 1)))
				action = np.argmax(predictions)
				prev_player, prev_opponents = self.get_prev_players(player, opponents)
				game_memory.append([stepcount, prev_player, prev_opponents, prev_observation, action])
				result, stepcount, player, opponents, _ = game.step(action)
				if result != -1:
					if result == 1: 
						goal_count += 1
					else:
						fail_count += 1
					steps_arr.append(stepcount)
					games.append([result, stepcount, game_memory])
					break
				else:
					prev_observation = self.generate_observation(player, opponents, goal)
		print("Goal: ", goal_count)
		print("Fail: ", fail_count)
		print("Average steps: ", mean(steps_arr))
		maxstep = np.argmax(np.array(g[1] for g in games))
		game_memory = games[maxstep][2]
		print("Result: ", games[maxstep][0])
		for m in game_memory:
			print("Step: ", m[0])
			print(" - Player: ", m[1])
			print(" - Opponents: ", ' '.join(map(str,m[2])))
			print(" - Observations: ", m[3])
			print(" - Predicted action: ", m[4])
					
	def train(self):
		print("Initialize training_data ...")
		training_data = self.initial_population()
		print("Initialize model ...")
		nn_model = self.model()
		print("Start training...")
		nn_model = self.train_model(training_data, nn_model)
		print("Start testing ...")
		self.test_model(nn_model)
		
	def get_prev_players(self, player, opponents):
		prev_player = np.copy(np.array(player))
		prev_opponents = np.copy(np.array(opponents))
		return prev_player, prev_opponents
	
	def fake_predictions(self):
		predictions = []
		predictions.append(random.uniform(0.0, 1.0))
		predictions.append(random.uniform(0.0, 1.0 - predictions[0]))
		predictions.append(random.uniform(0.0, 1.0 - predictions[0] - predictions[1]))
		predictions.append(1.0 - predictions[0] - predictions[1] - predictions[2])
		random.shuffle(predictions)
		return predictions
		
	def test(self):
		for i in range(0,3):
			print(i)
		# observation = np.array([int(False), int(False), int(True), 2])
		# action = randint(0,2) - 1
		# orig = np.append([action], observation)
		# print(orig)
		# reshaped = orig.reshape(5,1)
		# print(reshaped)
		# training_data = self.initial_population()
		# i = 0
		# for t in training_data:
			# if t[1] == 1 and i < 20:
				# print(t)
				# i+=1
		
if __name__ == "__main__":
	GameNN().train()
