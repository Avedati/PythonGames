#!/usr/local/bin//python3
import pygame,sys
from random import shuffle
pygame.init()

class Game:

	tile_size = 150
	BOARD = [
		'01','02','03','04',
		'05','06','07','08',
		'09','10','11','12',
		'13','14','15','  '
	]
	shuffle(BOARD)

	def __init__(self,width = 600,height = 600):
		pygame.display.set_caption("Fifteen Puzzle")
		self.screen = pygame.display.set_mode((width,height))
		self.clock,self.FPS,self.total_frames = pygame.time.Clock(),60,0
		self.font = pygame.font.SysFont(None,135)
		self.steps_taken = 0
		self.isMouseDown = 0

	def draw(self):
		rects = []
		count = -1
		for y in range(0,self.screen.get_height(),self.tile_size):
			for x in range(0,self.screen.get_width(),self.tile_size):
				count += 1
				self.screen.blit(self.font.render(self.BOARD[count],True,(0,0,0)),(x+25,y+25))
				rects.append(pygame.Rect([x,y,self.tile_size,self.tile_size]))
		return rects

	def swap(self,b):
		if not self.isMouseDown:
			self.steps_taken += 1
		a = self.BOARD.index('  ')
		ab = abs(a - b)
		if ab == 1 and int(a / 4) == int(b / 4):
				self.BOARD[a],self.BOARD[b] = self.BOARD[b],self.BOARD[a]
		if ab == 4:
			self.BOARD[a],self.BOARD[b] = self.BOARD[b],self.BOARD[a]

	def getUserInput(self,rects):
		mouse,click = pygame.mouse.get_pos(),pygame.mouse.get_pressed()
		for v,rect in enumerate(rects):
			if rect.left <= mouse[0] <= rect.right and rect.top <= mouse[1] <= rect.bottom and click[0]:
				return self.swap(v)

	def render(self,y = 0,msg = "",size = 30,color = (0,0,0)):
		font = pygame.font.SysFont(None,size)
		text = font.render(msg,True,color)
		rect = text.get_rect()
		x = int(self.screen.get_width() / 2 - rect.width / 2)
		self.screen.blit(text,(x,y))

	def winningScreen(self):
		while 1:
			self.screen.fill((255,255,255))
			self.render(msg = "You Won!",size = 100)
			self.render(y = 95,msg = "Steps Taken: {}".format(self.steps_taken),size = 60,color = (200,200,0))
			self.render(y = 165,msg = "Time Spent (seconds): {}".format(round(self.total_frames / self.FPS)),size = 60,color = (200,200,0))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

	def isWon(self):
		for a in range(16):
			if self.BOARD[a] == '  ':
				continue
			if int(self.BOARD[a]) != a + 1:
				return False
		return True

	def run(self):
		while 1:
			if self.isWon():
				self.winningScreen()
			self.total_frames += 1
			self.clock.tick(self.FPS)
			self.screen.fill((255,255,255))
			a = self.draw()
			pygame.display.flip()
			self.getUserInput(a)
			self.isMouseDown = pygame.mouse.get_pressed()[0]
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

if __name__ == "__main__":	Game().run()
