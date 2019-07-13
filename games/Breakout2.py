import pygame,sys
from random import randint
pygame.init()

class Game:

	def __init__(self,width = 800,height = 600):
		pygame.display.set_caption("Breakout Version 2")
		self.screen = pygame.display.set_mode((width,height))
		self.clock,self.FPS,self.total_frames = pygame.time.Clock(),60,0
		self.playerRects = {
			(-6,-2): pygame.Rect(int(width / 2 - 30),height - 10,10,10),
			(-4,-4): pygame.Rect(int(width / 2 - 20),height - 10,10,10),
			(-2,-6): pygame.Rect(int(width / 2 - 10),height - 10,10,10),
			(2,-6): pygame.Rect(int(width / 2),height - 10,10,10),
			(4,-4): pygame.Rect(int(width / 2 + 10),height - 10,10,10),
			(6,-2): pygame.Rect(int(width / 2 + 20),height - 10,10,10),
		}
		self.ball = {
			'rect': pygame.Rect(int(width / 2 - 4),int(height / 2 - 4),8,8),
			'vel': [1,3]
		}
		self.blocks = [
			pygame.Rect(x+2,y+2,26,6) for x in range(25,width-25,30) for y in range(25,int(height/2-25),10)
		]
		self.res = randint(1,7)
		self.score = 0
		self.blocksHit = 0

	def updatePlayer(self):
		left = self.playerRects[(-6,-2)].left
		right = self.playerRects[(6,-2)].right
		if left <= 0:	self.movePlayer(-left)
		if right >= self.screen.get_width():	self.movePlayer((right - 10) - self.screen.get_width())

	def updateBall(self):
		self.ball['rect'].x += self.ball['vel'][0]
		self.ball['rect'].y += self.ball['vel'][1]
		rect = self.ball['rect']
		if rect.top <= 0:
			self.ball['vel'][1] *= -1
		if rect.bottom > self.screen.get_height():
			Game().run()
		if rect.left <= 0 or rect.right >= self.screen.get_width():
			self.ball['vel'][0] *= -1
		for vel, pRect in self.playerRects.items():
			if rect.colliderect(pRect):
				self.ball['vel'] = list(vel)
		for block in self.blocks:
			if block.colliderect(self.ball['rect']):
				self.blocksHit += 1
				self.score += 1
				if self.blocksHit == self.res:
					self.blocksHit = 0
					self.res = randint(1,7)
					self.ball['vel'][1] *= -1
				self.blocks.remove(block)
				continue

	def movePlayer(self,amount):
		for pRect in self.playerRects:
			self.playerRects[pRect].x += amount

	def run(self):
		while 1:
			self.total_frames += 1
			self.clock.tick(self.FPS)
			self.screen.fill((0,42,0))
			self.updatePlayer()
			self.updateBall()
			for pRect in self.playerRects:	self.screen.fill((255,255,255),self.playerRects[pRect])
			for block in self.blocks:	self.screen.fill((255,255,255),block)
			self.screen.fill((255,255,255),self.ball['rect'])
			self.screen.blit(pygame.font.SysFont(None,50).render(str(self.score),True,(0,0,0)),\
			(int(self.screen.get_width() / 2 - 25),450))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)

			key = pygame.key.get_pressed()
			if any([key[pygame.K_a],key[pygame.K_LEFT]]):	self.movePlayer(-5)
			if any([key[pygame.K_d],key[pygame.K_RIGHT]]):	self.movePlayer(5)

if __name__ == "__main__":	Game().run()
