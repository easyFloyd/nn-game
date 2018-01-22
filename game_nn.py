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
	def __init__(self, initial_games = 10000, test_games = 100, goal_steps = 100, lr = 1e-2, filename = 'game_nn.tflearn'):
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
			
	def init_training_data(self):
		training_data = []
		for _ in range(self.initial_games):
			game = Game(opponents_number = 60)
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
			game = Game(opponents_number = 60)
			_, stepcount, player, opponents, goal = game.start()
			prev_observation = self.generate_observation(player, opponents, goal)
			for _ in range(self.goal_steps):
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
		for g in games:
			if g[0] == 0:
				game_memory = g[2][-1]
				print(" - Player: ", game_memory[1])
				print(" - Observations: ", game_memory[3])
				print(" - Predicted action: ", game_memory[4])
				
	def get_prev_players(self, player, opponents):
		prev_player = np.copy(np.array(player))
		prev_opponents = np.copy(np.array(opponents))
		return prev_player, prev_opponents
					
	def visualise_game(self, model):
		game = Game(opponents_number = 60, gui = True, hard = False)
		_, stepcount, player, opponents, goal = game.start()
		prev_observation = self.generate_observation(player, opponents, goal)
		for _ in range(self.goal_steps):
			predictions = []
			for action in range(0,4):
				predictions.append(model.predict(np.append([action], prev_observation).reshape(-1, 6, 1)))
			action = np.argmax(predictions)
			result, stepcount, player, opponents, _ = game.step(action)
			if result != -1:
				break
			else:
				prev_observation = self.generate_observation(player, opponents, goal)
					
	def train(self):
		print("Initialize training_data ...")
		training_data = self.init_training_data()
		print("Initialize model ...")
		nn_model = self.model()
		print("Start training...")
		nn_model = self.train_model(training_data, nn_model)
		print("Start testing ...")
		self.test_model(nn_model)
		
	def visualise(self):
		nn_model = self.model()
		nn_model.load(self.filename)
		self.visualise_game(nn_model)
		
		
	def test(self):
		nn_model = self.model()
		nn_model.load(self.filename)
		self.test_model(nn_model)
		
if __name__ == "__main__":
	GameNN().test()
