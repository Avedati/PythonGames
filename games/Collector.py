#!/usr/local/bin//python3
import pygame,sys
from random import randint
pygame.init()
pygame.mouse.set_visible(False)

class Game:
	
	def __init__(self,width = 800,height = 600):
		pygame.display.set_caption("Collector")
		self.screen = pygame.display.set_mode((width,height))
		self.clock,self.FPS,self.total_frames = pygame.time.Clock(),60,0
		self.player = pygame.Rect(int(width/2-25),height-50,50,50)
		self.lives = 3
		self.obstacles = []
		self.spawn()

	def text_to_screen(self,y = 5,msg = "Hello World",size = 30,color = (255,255,255)):
		font = pygame.font.SysFont(None,size)
		sz = font.size(msg)[0]
		xD = int(self.screen.get_width() / 2 - sz / 2)
		text = font.render(msg,True,color)
		self.screen.blit(text,(xD,y))
	
	def spawn(self):
		self.obstacles.append(pygame.Rect(randint(0,self.screen.get_width() - 50),randint(0,int(self.screen.get_height() / 2 - 50)),50,50))

	def endGame(self):
		while 1:
			self.screen.fill((0,0,0))
			self.text_to_screen(msg = "Game Over.",size = 40,color = (0,255,0))
			self.text_to_screen(y = 55,msg = "Your score: {}".format(self.lives),size = 20)
			self.text_to_screen(y = 105,msg = "Press <p> to play again.",size = 20)
			self.text_to_screen(y = 155,msg = "Press <q> to quit.",size = 20)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						Game().run()
					elif event.key == pygame.K_q:
						sys.exit(0)

	def update(self):
		self.player.x = pygame.mouse.get_pos()[0] - 25
		if self.player.x + self.player.width > self.screen.get_width():
			self.player.x = self.screen.get_width() - self.player.width	
		for o in self.obstacles:
			o.y += 15
			if o.y > self.screen.get_height():
				self.lives -= 1
				self.obstacles.remove(o)
				self.spawn()
				continue
			if (o.x <= self.player.x <= o.x + o.width or o.x <= self.player.x + self.player.width <= o.x + o.width) and\
			(o.y <= self.player.y <= o.y + o.height or o.y <= self.player.y + self.player.height <= o.y + o.height):
				self.lives += 1
				self.obstacles.remove(o)
				self.spawn()
				continue	

	def startGame(self):
		while 1:
			self.screen.fill((0,0,0))
			self.text_to_screen(msg = "Welcome to Collector!",size = 40,color = (0,255,0))
			self.text_to_screen(y = 55,msg = "When you hit a blue square, you gain a life.",size = 18)
			self.text_to_screen(y = 105,msg = "When a blue square goes off the edge, you lose a life.",size = 18)
			self.text_to_screen(y = 155,msg = "The object of the game is to have as many lives as possible after 1 minute.",size = 18)
			self.text_to_screen(y = 205,msg = "Press <p> to play.",size = 18)
			self.text_to_screen(y = 255,msg = "Press <q> to quit.",size = 18)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						return
					elif event.key == pygame.K_q:
						sys.exit(0)

	def run(self):
		self.startGame()
		while 1:
			self.update()
			self.total_frames += 1
			if int(self.total_frames / self.FPS) == 60:
				self.endGame()
			self.clock.tick(self.FPS)
			self.screen.fill((0,0,0))
			self.text_to_screen(msg = "Lives: {}".format(self.lives),size = 40)
			self.screen.fill((0,255,0),self.player)
			for o in self.obstacles:
				self.screen.fill((0,0,255),o)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

if __name__ == "__main__":
	Game().run()
