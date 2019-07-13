#!/usr/local/bin//python3
import pygame,sys
from random import randint
pygame.init()

class Bullet(pygame.sprite.Sprite):

	List = pygame.sprite.Group()
	width,height = 14,4

	def __init__(self,x,y):
		super().__init__()
		x += 2
		y += 6
		self.image = pygame.Surface((self.width,self.height))
		self.image.fill((255,255,255))
		self.rect = pygame.Rect((x,y,self.width,self.height))
		self.List.add(self)

	@staticmethod
	def add(lst,width,height):
		lst.append(Bullet(0,randint(0,int(height / Bullet.height)) * Bullet.height))

	@staticmethod
	def moveAll(lst,amount,width):
		for bullet in lst:
			bullet.rect.x += amount
			if bullet.rect.x >= width:
				lst.remove(bullet)


class Game:

	def __init__(self,width = 800,height = 800):
		Bullet.List = pygame.sprite.Group()
		pygame.display.set_caption("Make It Rain")
		self.screen = pygame.display.set_mode((width,height))
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.total_frames = 0
		self.bullets = []
		self.player = pygame.Rect((width - 8,int(height / 2) - 4,8,8))
		self.lives = 3
		self.x_change = 0
		self.y_change = 0
		self.x_plus = 0
		self.y_plus = 0

	def checkCollision(self):
		for b in self.bullets:
			if (self.player.left <= b.rect.left <= self.player.right or self.player.left <= b.rect.right <= self.player.right) and \
			(self.player.top <= b.rect.top <= self.player.bottom or self.player.top <= b.rect.bottom <= self.player.bottom):
				self.lives -= 1
				self.bullets.remove(b)
				Bullet.List.remove(b)
				break

	def text_objects(self,y,msg,size):
		font = pygame.font.Font(None,size)
		size = font.size(msg)[0]
		x = int(self.screen.get_width() / 2 - size / 2)
		return pygame.Rect(x,y,font.size(msg)[0],font.size(msg)[1])

	def text_to_screen(self,y = 5,msg = "Hello World!",size = 30,color = (255,255,255)):
		textRect = self.text_objects(y,msg,size)
		font = pygame.font.Font(None,size)
		self.screen.blit(font.render(msg,True,color),(textRect.x,textRect.y))

	def button(self,y = 5,msg = "Hello World",size = 30,colors = [(0,200,0),(0,255,0)],func = None):
		textRect = self.text_objects(y,msg,size)
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		j = False
		if textRect.left <= mouse[0] <= textRect.right and textRect.top <= mouse[1] <= textRect.bottom:
			colorIndex = 1
			if click[0]:
				func()
		else:
			colorIndex = 0
		font = pygame.font.Font(None,size)
		self.screen.blit(font.render(msg,True,colors[colorIndex]),(textRect.x,textRect.y))

	def newGame(self):
		Game().run()

	def lose(self):
		while 1:
			self.screen.fill((0,0,0))
			self.text_to_screen(msg = "Good Try.",size = 50)
			self.text_to_screen(y = 95,msg = "Your Score: {}".format(self.total_frames),size = 30)
			self.button(y = 190,msg = "Press <p> to play again.",func = self.newGame)
			self.button(y = 285,msg = "Press <q> to quit.",func = sys.exit)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						Game().run()
					elif event.key == pygame.K_q:
						sys.exit(0)

	def start(self):
		while 1:
			self.screen.fill((0,0,0))
			self.text_to_screen(msg = "Welcome to \"Make it rain!\".",size = 40)
			self.text_to_screen(y = 95,msg = "Just avoid the bullets and you\'ll be fine.",size = 25)
			self.text_to_screen(y = 195,msg = "Use the <w> key, the <s> key and the mouse to control your pixel",size = 25)
			self.button(y = 285,msg = "Press <p> to play.",func = self.newGame)
			self.button(y = 375,msg = "Press <q> to quit.",func = sys.exit)
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
		while 1:
			if self.lives <= 0:
				self.lose()
			if self.player.y <= 0:
				self.y_plus = 0
				self.y_change = 0
			if self.player.y >= self.screen.get_height():
				self.y_plus = 0
				self.y_change = 0
			if self.player.x <= 0:
				self.x_plus = 0
				self.x_change = 0
			if self.player.x >= self.screen.get_width():
				self.x_plus = 0
				self.x_change = 0
			self.x_change += self.x_plus
			self.y_change += self.y_plus
			self.total_frames += 1
			self.clock.tick(self.FPS)
			self.screen.fill((0,0,0))
			self.text_to_screen(y = 15,msg = "Lives: {}".format(self.lives))
			self.player.x = pygame.mouse.get_pos()[0] - int(self.player.width / 2) + self.x_change
			self.player.y = pygame.mouse.get_pos()[1] - int(self.player.height / 2) + self.y_change
			self.checkCollision()
			self.screen.fill((0,255,0),self.player)
			Bullet.List.draw(self.screen)
			if self.total_frames % 3 == 0:
				Bullet.add(self.bullets,self.screen.get_width(),self.screen.get_height())
				Bullet.moveAll(self.bullets,Bullet.width - self.lives,self.screen.get_width())
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_a,pygame.K_LEFT]:
						self.x_plus = -5
					elif event.key in [pygame.K_d,pygame.K_RIGHT]:
						self.x_plus = 5
					elif event.key in [pygame.K_w,pygame.K_UP]:
						self.y_plus = -5
					elif event.key in [pygame.K_s,pygame.K_DOWN]:
						self.y_plus = 5
				elif event.type == pygame.KEYUP:
					if event.key in [pygame.K_a,pygame.K_d,pygame.K_LEFT,pygame.K_RIGHT]:
						self.x_plus = 0
					elif event.key in [pygame.K_w,pygame.K_s,pygame.K_UP,pygame.K_DOWN]:
						self.y_plus = 0

if __name__ == "__main__":
	g = Game()
	g.start()
	g.run()
