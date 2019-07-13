import pygame,sys
pygame.init()

class Player:

	def __init__(self,rect):
		self.rect = pygame.Rect(rect)
		self.y = self.rect.y
		self.image = pygame.Surface((rect[2],rect[3]))
		self.image.fill((0,0,0))
		self.jump = False
		self.fall = False
		self.vel = 0

	def draw(self,Game):
		if self.jump:
			self.vel -= 1
			self.rect.y += self.vel
			if self.vel == -15:
				self.jump = False
				self.vel = 0
		elif self.fall:
			self.vel = 5
			self.rect.y += self.vel
			if self.rect.y > self.y:
				self.rect.y = self.y
				self.fall = False
		elif self.rect.y < 0:
			self.fall = True
		elif self.rect.y < self.y:
			self.vel = 1
			self.rect.y += self.vel
		Game.screen.blit(self.image,(self.rect.x,self.rect.y))

class Obstacle:

	def __init__(self,rect):
		self.rect = pygame.Rect(rect)
		self.image = pygame.Surface((rect[2],rect[3]))
		self.image.fill((255,0,0))
	
	def draw(self,Game):
		if self.rect.x == Game.player.rect.x and self.rect.y == Game.player.rect.y:
			Game.lose()
		Game.screen.blit(self.image,(self.rect.x,self.rect.y))

class Aviator:

	def __init__(self,rect):
		self.rect = pygame.Rect(rect)
		self.image = pygame.Surface((rect[2],rect[3]))
		self.image.fill((0,255,0))
		self.bullets = []

	def shoot(self):
		self.bullets.append(pygame.Rect((self.rect.x,self.rect.y + int(self.rect.height / 2) - 5,self.rect.width,10)))

	def draw(self,Game):
		player = Game.player.rect
		for bullet in self.bullets:
			bullet.x -= 5
			if (bullet.left <= player.left <= bullet.right or bullet.left <= player.right <= bullet.right) and \
			(bullet.top <= player.top <= bullet.bottom or bullet.top <= player.bottom <= bullet.bottom):
				Game.lose()
			Game.screen.fill((0,0,255),bullet)
		self.rect.y = Game.player.rect.y
		if Game.total_frames % 30 == 0:
			self.shoot()
		Game.screen.blit(self.image,(self.rect.x,self.rect.y))

class Game:

	def __init__(self,width = 600,height = 600):
		pygame.display.set_caption("Light As A Feather")
		self.SIZE = (width,height)
		self.screen = pygame.display.set_mode((width,height))
		self.clock,self.FPS,self.total_frames = pygame.time.Clock(),60,0
		self.player = Player((125,575,25,25))
		self.aviator = Aviator((425,575,25,25))
		self.obstacles = []

	def textObjects(self,y,msg,size):
		font = pygame.font.Font(None,int(size))
		sz = font.size(msg)
		return font,sz,int(self.screen.get_width() / 2 - sz[0] / 2)

	def render(self,y = 5,msg = "Hello World!",size = 30,color = (0,0,0)):
		font,size,x = self.textObjects(y,msg,size)
		self.screen.blit(font.render(msg,True,color),(x,y))

	def button(self,y = 5,msg = "Hello World!",size = 30,colors = [(0,200,0),(0,255,0)],func = None):
		font,sz,x = self.textObjects(y,msg,size)
		mouse,click = pygame.mouse.get_pos(),pygame.mouse.get_pressed()
		rect = pygame.Rect((x,y,sz[0],sz[1]))
		if rect.left <= mouse[0] <= rect.right and rect.top <= mouse[1] <= rect.bottom:
			self.render(y,msg,size,colors[1])
			if any(click):
				try:
					func()
				except TypeError:
					pass
		else:
			self.render(y,msg,size,colors[0])

	def playAgain(self):
		Game().start()

	def start(self):
		while 1:
			self.screen.fill((255,255,255))
			self.render(msg = "Light As A Feather.",size = 50)
			self.button(y = 45,msg = "Play",func = self.run)
			self.button(y = 90,msg = "Rules",func = self.rules)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						self.run()
					elif event.key == pygame.K_r:
						self.rules()

	def rules(self):
		while 1:
			self.screen.fill((255,255,255))
			self.render(msg = "Rules",size = 50)
			self.render(y = 45,msg = "Press <w>,<UP ARROW>,or <SPACE> to jump.",size = 20)
			self.render(y = 90,msg = "Avoid the red pixels and blue bullets.",size = 20)
			self.render(y = 135,msg ="When you hit the top of the screen, you fall rapidly.",size = 20)
			self.render(y = 180,msg = "When you hit the ground, you negate this effect.",size = 20)
			self.render(y = 225,msg = "Press <a>,<LEFT ARROW>,<d>,and <RIGHT ARROW> to go left and right.",size = 20)
			self.button(y = 270,msg = "Play",func = self.run)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						self.run()

	def lose(self):
		while 1:
			self.screen.fill((255,255,255))
			self.render(msg = "Good Try.",size = 50)
			self.render(y = 45,msg = "Your Score: {}".format(int(self.total_frames / self.FPS)))
			self.button(y = 90,msg = "Play Again",func = self.playAgain)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						Game().run()

	def spawn(self):
		self.obstacles.append(Obstacle((425,575,25,25)))

	def run(self):
		while 1:
			key = pygame.key.get_pressed()
			if any([key[pygame.K_a],key[pygame.K_LEFT]]):	self.player.rect.x -= 3
			if any([key[pygame.K_d],key[pygame.K_RIGHT]]):	self.player.rect.x += 3
			self.total_frames += 1
			if self.total_frames % 36 == 0:
				self.spawn()
			self.clock.tick(self.FPS)
			self.screen.fill((255,255,255))
			self.render(msg = "Score: {}".format(int(self.total_frames / self.FPS)))
			self.player.draw(self)
			self.aviator.draw(self)
			for obstacle in self.obstacles:
				obstacle.rect.x -= 5
				obstacle.draw(self)
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key in [pygame.K_w,pygame.K_UP,pygame.K_SPACE]:
						self.player.jump = True

if __name__ == "__main__":
	Game().start()