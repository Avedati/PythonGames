#!/usr/local/bin//python3
import pygame,sys;pygame.init()
class Game:
	def __init__(self,width = 600,height = 750):
		pygame.display.set_caption("Speed")
		self.screen = pygame.display.set_mode((width,height));self.clock,self.FPS,self.total_frames = pygame.time.Clock(),60,0
		self.player = pygame.Rect(int(width / 2) - 5,height-10,10,10);self.spikes = pygame.Rect((width - 50,0,50,height));self.exit = pygame.Rect(int(width / 2) - 25,0,50,50)
	def drawSpikes(self):
		if self.screen.get_height() % 50 != 0:	return
		self.screen.fill((120,120,120),(self.screen.get_width() - 1,0,1,self.screen.get_height()))
		for y in range(0,self.screen.get_height(),50):	pygame.draw.polygon(self.screen,(120,120,120),[(self.spikes.x+50,y),(self.spikes.x,y+25),(self.spikes.x+50,y+50)])
	def updateSpikes(self):
		if self.total_frames % 3 == 0:	self.spikes.x -= 1
		if self.spikes.colliderect(self.player):	Game().run()
	def textObjects(self,y,text,size,color):
		text = pygame.font.SysFont(None,size).render(text,True,color);return text,text.get_rect()
	def render(self,y = 5,text = " ",size = 30,color = (0,0,0)):
		text,rect = self.textObjects(y,text,size,color);x = int(self.screen.get_width() / 2 - rect.width / 2)
		self.screen.blit(text,(x,y))
	def win(self):
		while 1:
			self.clock.tick(self.FPS);self.screen.fill((255,255,255))
			self.render(text = "You Win!",size = 50);self.render(y = 65,text = "Play again: 1",color = (0,255,0));self.render(y = 130,text = "Quit: 2",color = (0,255,0))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:	sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_1:	Game().run()
					elif event.key == pygame.K_2:	sys.exit(0)
	def run(self):
		w = s = False
		while 1:
			if self.total_frames % 3 == 0:	w = s = False
			self.total_frames += 1;self.clock.tick(self.FPS)
			# Drawing #
			self.screen.fill((255,255,255));self.screen.fill((0,255,0),self.player);self.screen.fill((0,0,255),self.exit)
			self.updateSpikes();self.drawSpikes()
			if self.exit.colliderect(self.player):	self.win()
			pygame.display.flip()
			# Keyboard Input #
			for event in pygame.event.get():
				if event.type == pygame.QUIT:	sys.exit(0)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:	w = True
					elif event.key == pygame.K_s:	s = True
			if w and s:	self.player.y -= self.player.height
if __name__ == "__main__":	Game().run()