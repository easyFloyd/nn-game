import sys
from game_nn import GameNN

class Program:
	def train(self):
		GameNN().train()
		
	def test(self):
		GameNN().test()
		
	def visualise(self):
		GameNN().visualise()
		
if __name__ == "__main__":
	method = sys.argv[1]
	p = Program()
	if method == "test":
		p.test()
	elif method == "train":
		p.train()
	elif method == "visualise":
		p.visualise()
	else:
		print("Pleasy try the following commands:")
		print("- python main.py train (to train the neural network)")
		print("- python main.py test (to test the neural network)")
		print("- python main.py visualise (to visualise one game)")
