import random
import time
import os
import keyboard


MAP_LENGTH = 22
MAP_HEIGHT = 20
PLAYER1 = 0
PLAYER2 = 0


class Wall:
	def __init__(self, x, y, sprite):
		self.x = x
		self.y = y
		self.sprite = sprite
	def __str__(self):
		return self.sprite


class GameScreen:
	def __init__(self, player1, player2, ball):
		global MAP_LENGTH
		global MAP_HEIGHT
		self.map_lenght = MAP_LENGTH
		self.map_height = MAP_HEIGHT
		self.coordinates = [[' '] * self.map_lenght for i in range(self.map_height)]
		self.player1 = player1
		self.player2 = player2
		self.ball = ball

	def place_players(self):
		board_center = int((self.map_lenght - 3) / 2)

		for index, part in enumerate(self.player1.platform):
			part.x = board_center + index
			part.y = self.map_height - 4
			part.x_prev = board_center + index

		for index, part in enumerate(self.player2.platform): 
			part.x = board_center + index
			part.y = 3
			part.x_prev = board_center + index

	def create_map(self):
		for row in range(self.map_height):
			for elem in range(self.map_lenght):
				if elem == 0 or elem == self.map_lenght-1:
					self.coordinates[row][elem] = Wall(elem, row, '|')

	def render(self):
		#ball
		self.coordinates[self.ball.y_prev][self.ball.x_prev] = ' '
		self.coordinates[self.ball.y][self.ball.x] = self.ball

		#platform
		# for part in self.player1.platform:
		# 	self.coordinates[part.y][part.x_prev] = ' '
		# for part in self.player2.platform:
		# 	self.coordinates[part.y][part.x_prev] = ' '
		self.coordinates[self.player1.platform[0].y][self.player1.last_x] = ' '
		self.coordinates[self.player2.platform[0].y][self.player2.last_x] = ' '

		for part in self.player1.platform:
			self.coordinates[part.y][part.x] = part
		for part in self.player2.platform:
			self.coordinates[part.y][part.x] = part

		#render
		for row in self.coordinates:
			for elem in row:
				print(elem, end='')
			print()

	def clear(self):
		os.system('cls' if os.name == 'nt' else 'clear')


class Player:
	def __init__(self, length):
		self.platform = [PlatformPart() for i in range(length)]
		self.last_x = 1

	def move(self, direction, game_map):
		global MAP_LENGTH
		if direction == 'right' and self.platform[-1].x < MAP_LENGTH - 2:
			self.last_x = self.platform[0].x
			#game_map.coordinates[self.platform[0].y][self.platform[-1].x] = ' '
			for p in self.platform:
				p.x_prev = p.x
				p.x = p.x + 1
		if direction == 'left' and self.platform[-1].x > len(self.platform):
			self.last_x = self.platform[-1].x
			#game_map.coordinates[self.platform[0].y][self.platform[0].x] = ' '
			for p in self.platform:
				p.x_prev = p.x
				p.x = p.x - 1


class PlatformPart:
	def __init__(self):
		self.sprite = 'X'
		self.x = 0
		self.y = 0
		self.x_prev = 0

	def __str__(self):
		return self.sprite


class Ball:
	def __init__(self):
		global MAP_LENGTH
		global MAP_HEIGHT
		self.sprite = 'o'
		self.x = int(MAP_LENGTH/2)
		self.y = int(MAP_HEIGHT/2)
		self.x_prev = int(MAP_LENGTH/2)
		self.y_prev = int(MAP_HEIGHT/2)
		self.next_block = ''
		self.directions = {
			'up': (0, -1), 'down': (0, 1),
			'right-up': (1, -1), 'right-down': (1, 1),
			'left-up': (-1, -1), 'left-down': (-1, 1)
		}
		self.direction = self.directions['down']

	def move(self, game_map):
		self.x_prev = self.x
		self.y_prev = self.y
		self.x = self.x + self.direction[0]
		self.y = self.y + self.direction[1]
		self.next_block = game_map.coordinates[self.y + self.direction[1]][self.x + self.direction[0]]
		self.check_blocks(game_map)

	def check_blocks(self, game_map):
		global MAP_LENGTH
		global MAP_HEIGHT
		block_type = type(self.next_block)

		if block_type is PlatformPart and self.y > MAP_HEIGHT/2:
			p = game_map.player1.platform.index(self.next_block) + 1
			length = len(game_map.player1.platform)
			delta = (length-1)/2 + 1
			if p == delta:
				self.direction = self.directions['up']
			elif p < delta:
				self.direction = self.directions['left-up']
			elif p > delta:
				self.direction = self.directions['right-up']

		elif block_type is PlatformPart and self.y < MAP_HEIGHT/2:
			p = game_map.player2.platform.index(self.next_block) + 1
			length = len(game_map.player2.platform)
			delta = (length-1)/2 + 1
			if p == delta:
				self.direction = self.directions['down']
			elif p < delta:
				self.direction = self.directions['left-down']
			elif p > delta:
				self.direction = self.directions['right-down']

		elif block_type is Wall:
			if self.direction == self.directions['left-up']:
				self.direction = self.directions['right-up']

			elif self.direction == self.directions['right-up']:
				self.direction = self.directions['left-up']

			elif self.direction == self.directions['right-down']:
				self.direction = self.directions['left-down']

			elif self.direction == self.directions['left-down']:
				self.direction = self.directions['right-down']

		elif self.y == 0:
			self.goal(2)
		elif self.y == MAP_HEIGHT-2:
			self.goal(1)

	def goal(self, side):
		global MAP_HEIGHT
		global MAP_LENGTH
		global PLAYER1
		global PLAYER2

		print(' '*int((MAP_LENGTH-5)/2) + 'GOAL!')

		self.x = int(MAP_LENGTH/2)
		self.y = int(MAP_HEIGHT/2)
		self.next_block = ''

		if side == 1:
			self.direction = self.directions['down']
			PLAYER2 = PLAYER2 + 1
		else:
			self.direction = self.directions['up']
			PLAYER1 = PLAYER1 + 1

		time.sleep(1)

	def __str__(self):
		return self.sprite


def main():
	global PLAYER1
	global PLAYER2
	global MAP_LENGTH
	player1 = Player(5)
	player2 = Player(5)
	ball = Ball()
	game_map = GameScreen(player1, player2, ball)
	game_map.place_players()
	game_map.create_map()

	while True:

		game_map.clear()
		game_map.render()

		if keyboard.is_pressed('d'):
			game_map.player1.move('right', game_map)
		if keyboard.is_pressed('a'):
			game_map.player1.move('left', game_map)

		if game_map.player2.platform[0].x < game_map.ball.x:
			game_map.player2.move('right', game_map)
		elif game_map.player2.platform[-1].x > game_map.ball.x:
			game_map.player2.move('left', game_map)		

		game_map.ball.move(game_map)	

		padding = int((MAP_LENGTH-5)/2)
		print(' '*padding + 'SCORE\n' + ' '*(padding-3) + 'player 1: ' + str(PLAYER1) + '\n' + ' '*(padding-3) + 'player 2: ' + str(PLAYER2)) #score print

		time.sleep(0.1)


if __name__ == '__main__':
	main()