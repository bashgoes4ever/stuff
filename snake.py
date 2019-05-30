import random
import time
import os
import keyboard


GAME_RUNNING = True
GAME_SPEED = 0.06


class Wall:
	def __init__(self, x, y, sprite):
		self.x = x
		self.y = y
		self.sprite = sprite
	def __str__(self):
		return self.sprite


class Map:
	def __init__(self, map_height, map_lenght):
		self.map_height = map_height
		self.map_lenght = map_lenght
		self.coordinates = []

	def create_map(self):
		self.coordinates = [[' '] * self.map_lenght for i in range(self.map_height)]
		for row in range(self.map_height):
			for elem in range(self.map_lenght):
				if row == 0 or row == self.map_height-1:
					self.coordinates[row][elem] = Wall(elem, row, '-')
				elif  elem == 0 or elem == self.map_lenght-1:
					self.coordinates[row][elem] = Wall(elem, row, '|')


class Food:
	def __init__(self, map):
		self.y = random.randint(1, map.map_height-1)
		self.x = random.randint(1, map.map_lenght-1)
		while map.coordinates[self.y][self.x] != ' ':
			self.y = random.randint(1, map.map_height-1)
			self.x = random.randint(1, map.map_lenght-1)			
		sprites = ['Q', 'q', '@', '&', '*']
		self.sprite = random.choice(sprites)

	def __str__(self):
		return self.sprite


# snake
class SnakeHead:
	def __init__(self, game_map):
		self.points = 0
		self.directions = ['r', 'l', 't', 'b', 'stop']
		self.sprites = ['>', '<', '^', 'v']
		self.y = int(game_map.map_height/2)
		self.x = int(game_map.map_lenght/2)
		self.x_prev = self.x - 1
		self.y_prev = self.y
		self.direction = self.directions[0]
		self.sprite = self.sprites[0]
		self.current_block = game_map.coordinates[int(game_map.map_height/2)][int(game_map.map_lenght/2)+1]
		self.parts_array = [self]

	def snake_move(self, game_map):
		self.x_prev = self.x
		self.y_prev = self.y

		if self.direction == self.directions[0]:
			self.x = self.x + 1
		elif self.direction == self.directions[1]:
			self.x = self.x - 1
		elif self.direction == self.directions[2]:
			self.y = self.y - 1
		elif self.direction == self.directions[3]:
			self.y = self.y + 1

	def eat_food(self):
		self.parts_array.append(SnakePart(self.parts_array[-1].y_prev, self.parts_array[-1].x_prev, self.parts_array))
		self.points = self.points + 1

	def __str__(self):
		return self.sprite


class SnakePart:
	def __init__(self, y, x, parts_array):
		self.y = y
		self.x = x
		self.y_prev = 0
		self.x_prev = 0
		sprites = ['o', 'O', '0', '8']
		self.sprite = random.choice(sprites)
		self.next_part = parts_array[-1]

	def follow(self):
		self.y_prev = self.y
		self.x_prev = self.x
		self.x = self.next_part.x_prev
		self.y = self.next_part.y_prev

	def __str__(self):
		return self.sprite


class Update:
	def __init__(self, game_map, snake):
		self.game_map = game_map
		self.snake = snake
	def render(self):
		for i in self.snake.parts_array:

			self.game_map.coordinates[i.y_prev][i.x_prev] = ' '
			block_type = type(self.game_map.coordinates[i.y][i.x])
			#food
			if block_type == Food and type(i) == SnakeHead: 
				i.eat_food()
				add_food(self.game_map)

			#wall
			if block_type == Wall and type(i) == SnakeHead:
				if i.x == 0:
					i.x = self.game_map.map_lenght - 2

				if i.x == self.game_map.map_lenght - 1:
					i.x = 1

				if i.y == 0:
					i.y = self.game_map.map_height - 2

				if i.y == self.game_map.map_height - 1:
					i.y = 1

			#bite yourself
			if block_type == SnakePart and type(i) == SnakeHead:
				game_over(self.snake, self.game_map)
				break					

			self.game_map.coordinates[i.y][i.x] = i

		for row in self.game_map.coordinates:
			for elem in row:
				print(elem, end='')
			print()

	def clear(self):
		os.system('cls' if os.name == 'nt' else 'clear')


def add_food(game_map):
	food = Food(game_map)
	game_map.coordinates[food.y][food.x] = food


def game_over(snake, game_map):
	for i in snake.parts_array:
		game_map.coordinates[i.y_prev][i.x_prev] = ' '
	snake.parts_array = []

	string1 = 'GAME OVER'
	string2 = 'POINTS: ' + str(snake.points)
	padding_left1 = int((game_map.map_lenght-len(string1))/2)
	padding_left2 = int((game_map.map_lenght-len(string2))/2)
	padding_top = int((game_map.map_height-1)/2)
	for i, char in enumerate(string1):
		game_map.coordinates[padding_top][padding_left1+i] = char
	for i, char in enumerate(string2):
		game_map.coordinates[padding_top+2][padding_left2+i] = char

	global GAME_RUNNING
	GAME_RUNNING = False


def increase_game_speed(k):
	global GAME_SPEED
	GAME_SPEED = GAME_SPEED - GAME_SPEED*(k)


# main
def main():
	game_map = Map(20, 40)
	game_map.create_map()
	snake = SnakeHead(game_map)
	game_update = Update(game_map, snake)
	add_food(game_map)
	start_time = time.time()

	while GAME_RUNNING:
		cur_time = time.time() - start_time
		if cur_time >= 7:
			start_time = time.time()
			increase_game_speed(0.05)

		game_update.clear()
		print(' '*int((game_map.map_lenght-19)/2) + 'SNAKE THE GAME V1.0')
		game_update.render()
		snake.snake_move(game_map)
		for part in snake.parts_array[1:]:
			part.follow()

		if keyboard.is_pressed('w') and snake.direction is not snake.directions[3]:
			snake.direction = snake.directions[2]
			snake.sprite = snake.sprites[2]
		elif keyboard.is_pressed('d') and snake.direction is not snake.directions[1]:
			snake.direction = snake.directions[0]
			snake.sprite = snake.sprites[0]
		elif keyboard.is_pressed('s') and snake.direction is not snake.directions[2]:
			snake.direction = snake.directions[3]
			snake.sprite = snake.sprites[3]
		elif keyboard.is_pressed('a') and snake.direction is not snake.directions[0]:
			snake.direction = snake.directions[1]
			snake.sprite = snake.sprites[1]

		print('POINTS: ' + str(snake.points) + '\nSPEED: ' + str(1-GAME_SPEED*10))


		time.sleep(GAME_SPEED)
	


if __name__ == '__main__':
	main()