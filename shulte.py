from random import shuffle
from tkinter import Tk, Canvas


block_size = 150
font = ('Sans Serif', -74)


def main():
	numbers = [i for i in range(1, 26)]
	shuffle(numbers)

	root = Tk()
	root.title('Shulte Table')

	c = Canvas(root, width=block_size*5+3, height=block_size*5+3, bg='#d0daeb')
	c.grid()

	x = 3
	y = 3
	for index, i in enumerate(numbers):
		if index != 0 and index % 5 == 0:
			x = 3
			y = y + block_size
		c.create_rectangle(x, y, x+block_size, y+block_size, fill='#ffffff', tags='0')
		c.create_text((x+(block_size/2), y+(block_size/2)), text=str(i), font=font)
		x = x + block_size

	root.mainloop()


if __name__ == '__main__':
	main()