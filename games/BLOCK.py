#!/usr/local/bin//python3
import pygame, sys
from pygame.locals import *
from random import randint
pygame.init()

class Player(pygame.sprite.Sprite):

	def __init__(self,x,y,width,height):
		super().__init__()
		self.image = pygame.Surface((width,height))
		self.image.fill((0,0,0))
		self.rect = pygame.Rect(x,y,width,height)
		self.hp = [50,50]

	def update(self,Game):
		for z in Game.zombies:
			if z.rect.x == self.rect.x and z.rect.y == self.rect.y:
				self.hp[0] -= 1
		if self.hp[0] <= 0:
			Game.lose()
		if self.rect.x + self.rect.width > Game.screen.get_width():
			self.rect.x = Game.screen.get_width() - self.rect.width
		if self.rect.x < 0:
			self.rect.x = 0
		if self.rect.y + self.rect.height > Game.screen.get_height():
			self.rect.y = Game.screen.get_height() - self.rect.height
		if self.rect.y < 0:
			self.rect.y = 0

class Zombie(pygame.sprite.Sprite):

		def __init__(self,x,y,width,height,speed):
			super().__init__()
			self.image = pygame.Surface((width,height))
			self.image.fill((0,255,0))
			self.rect = pygame.Rect(x,y,width,height)
			self.speed = speed

		def update(self,Game):
			r = Game.player.rect
			if self.rect.x == r.x and self.rect.y == r.y:
				pass
			elif randint(1,self.speed) == 1:
				if r.x > self.rect.x:
					self.rect.x += self.rect.width
				if r.x < self.rect.x:
					self.rect.x -= self.rect.width
				if r.y > self.rect.y:
					self.rect.y += self.rect.height
				if r.y < self.rect.y:
					self.rect.y -= self.rect.height

class Game:

	def __init__(self,width=800,height=600):
		self.screen = pygame.display.set_mode((width,height),DOUBLEBUF)
		pygame.display.set_caption("BLOCK")
		self.clock, self.FPS = pygame.time.Clock(), 60
		self.font = pygame.font.SysFont(None,30)
		self.player = Player(400,300,20,20)
		self.score = 0
		self.zombies = []
		self.zombie_speed = 15
		self.draw_list = pygame.sprite.Group()
		self.draw_list.add(self.player)
		for z in self.zombies:	self.draw_list.add(z)

	def text(self,y=0,msg="Hello World.",color=(0,0,0)):
		size = self.font.size(msg)[0]
		xD = int((self.screen.get_width() - size) / 2)
		txt = self.font.render(msg,True,color)
		self.screen.blit(txt,(xD,y))

	def gen_zombies(self):
		for x in range(20):
			self.zombies.append(Zombie(randint(0,int(self.screen.get_width() / 20)) * 20,\
					randint(0,int(self.screen.get_height())) * 20, 20, 20, self.zombie_speed))
		for z in self.zombies:	self.draw_list.add(z)

	def menu(self):
		while True:
			self.screen.fill((255,255,255))
			self.text(y = 5,msg = "Type a number to be your zombie speed",color = (0,255,0))
			self.text(y = 55,msg = "(0 being smallest, 9 being biggest)")
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.unicode in list('0123456789'):
						self.zombie_speed = 15 - int(event.unicode)
						self.gen_zombies()
						return None

	def lose(self):
		while True:
			if len(self.zombies) == 0:
				self.gen_zombies()
			self.screen.fill((255,255,255))
			self.text(y = 5,msg = "You Lose.",color=(0,255,0))
			self.text(y = 115,msg = "Your Score was: {}".format(int(self.score / self.FPS)))
			self.text(y = 215,msg = "Press <SPACE> to quit and <p> to play again")
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						sys.exit(0)
					elif event.key == pygame.K_p:
						Game().run()

	def run(self):
		self.menu()
		while True:
			self.score += 1
			self.clock.tick(self.FPS)
			if len(self.zombies) == 0:
				self.gen_zombies()
			self.screen.fill((255,255,255))
			self.text(y = 5,msg = "HP: ("+str(self.player.hp[0])+", "+str(self.player.hp[1])+")")
			self.player.update(self)
			for z in self.zombies:	z.update(self)
			self.draw_list.draw(self.screen)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_a,pygame.K_LEFT]:
						self.player.rect.x -= self.player.rect.width
					elif event.key in [pygame.K_d,pygame.K_RIGHT]:
						self.player.rect.x += self.player.rect.width
					elif event.key in [pygame.K_w,pygame.K_UP]:
						self.player.rect.y -= self.player.rect.height
					elif event.key in [pygame.K_s,pygame.K_DOWN]:
						self.player.rect.y += self.player.rect.height
if __name__ == "__main__":
	Game().run()
