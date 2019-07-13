#!/usr/local/bin//python3
import pygame,sys
from random import randint
from os import system
clear = lambda:	system('clear')
pygame.init()

class Player(list):

	width,height = 10,10

	def __init__(self,x,y):
		super().__init__([pygame.Rect((x,y,self.width,self.height))])
		self.x = x
		self.y = y
		self.x_change = 0
		self.y_change = -self.height
		self.l = 3

	def update(self,Game):
		key = pygame.key.get_pressed()
		if any([key[pygame.K_w],key[pygame.K_UP]]):	self.y_change = -self.height;self.x_change = 0
		if any([key[pygame.K_s],key[pygame.K_DOWN]]):	self.y_change = self.height;self.x_change = 0
		if any([key[pygame.K_a],key[pygame.K_LEFT]]):	self.x_change = -self.height;self.y_change = 0
		if any([key[pygame.K_d],key[pygame.K_RIGHT]]):	self.x_change = self.height;self.y_change = 0
		
		for block in self:
			if block.left < 0 or block.right > Game.screen.get_width() or \
			block.top < 0 or block.bottom > Game.screen.get_height():
				Game.lose()

		if Game.total_frames % 2 == 0:
			self.x += self.x_change
			self.y += self.y_change
			self.append(pygame.Rect((self.x,self.y,self.width,self.height)))
			if len(self) > self.l:
				self.pop(0)

class Game:

	def __init__(self,width = 600,height = 600):
		pygame.display.set_caption("Snake")
		self.screen = pygame.display.set_mode((width,height))
		self.clock,self.FPS,self.total_frames = pygame.time.Clock(),60,0
		self.player = Player(300,300)
		self.apples = []

	def getApple(self):
		self.apples.append(pygame.Rect((randint(0,int(self.screen.get_width() / 10) - 1) * 10,\
		randint(0,int(self.screen.get_height() / 10) - 10) * 10,10,10)))

	def collisions(self):
		for apple in self.apples:
			for block in self.player:
				if apple.colliderect(block):
					self.player.l += 1
					self.apples.remove(apple)
					return

	def render(self,y = 0,msg = "Hello World!",size = 30,color = (0,0,0)):
		font = pygame.font.SysFont(None,size)
		text = font.render(msg,True,color)
		rect = text.get_rect()
		x = int(self.screen.get_width() / 2 - rect.width / 2)
		self.screen.blit(text,(x,y))

	def start(self):
		while 1:
			self.screen.fill((255,255,255))
			self.render(msg = "Snake",size = 50)
			self.render(y = 45,msg = "Play: 1",color = (0,255,0))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
					self.run()

	def lose(self):
		while 1:
			self.screen.fill((255,255,255))
			self.render(msg = "Good Try.",size = 50)
			self.render(y = 45,msg = "Play Again: 1",color = (0,255,0))
			self.render(y = 90,msg = "Quit: 2",color = (0,255,0))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:
						Game().run()
					elif event.key == pygame.K_2:
						sys.exit(0)

	def run(self):
		clear()
		while 1:
			self.total_frames += 1
			self.clock.tick(self.FPS)
			self.screen.fill((255,255,255))
			self.render(msg = "Score: {}".format(self.player.l - 3),size = 50)
			if randint(1,30) == 1 and len(self.apples) < 20:	self.getApple()
			self.player.update(self)
			for block in self.player:
				self.screen.fill((0,255,0),block)
			for apple in self.apples:
				self.screen.fill((255,0,0),apple)
			self.screen.fill((0,130,0),self.player[len(self.player)-1])
			self.collisions()
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)



if __name__ == "__main__":	Game().start()