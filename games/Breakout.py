#!/usr/local/bin//python3
import pygame, sys
from pygame.locals import *
from math import cos, sin
from random import randint
pygame.init()

SIZE = (860,680)
screen = pygame.display.set_mode(SIZE,DOUBLEBUF)
pygame.display.set_caption("Breakout (Brick Breaker)")
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont(None, 30)
running = True
MAXBLOCKS = randint(4,7)
count = 0
player = pygame.Rect(SIZE[0] / 2 - 15,SIZE[1] - 8,60,8)
ball = pygame.Rect(SIZE[0] / 2, SIZE[1] / 2, 10, 10)
x_change = 0
ball_speed = 2
score = 0
r = False
x_vel, y_vel = ball_speed, ball_speed
lst = [pygame.Rect(x,y,30,10)
		for x in range(10,SIZE[0]-10,30)
		for y in range(10,250,10)]
BLOCKS_TO_DEMOLISH = len(lst)
losingM = True

def msg(y = 0, message = "Hello World!", size = 30):
	global SIZE, screen
	font = pygame.font.SysFont(None, size)
	txt = font.render(message, True, (255,255,255))
	size = font.size(message)[0]
	xD = int((SIZE[0] - size) / 2)
	screen.blit(txt, (xD, y))

def button(y=0,message=" ",size=30,width=30,height=10,colors=[(255,0,0),(120,0,0)],func=None):
	buttonX = int(SIZE[0] / 2) - int(width / 2)
	mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
	if buttonX <= mouse[0] <= buttonX + width and y <= mouse[1] <= y + height:
		screen.fill(colors[1],(buttonX,y,width,height))
		if click[0]:
			try:
				func()
			except TypeError:
				pass
	else:	screen.fill(colors[0],(buttonX,y,width,height))
	msg(y,message,size)
	
startMenu = True

def play():
	global startMenu
	startMenu = False

def paused():
	while True:
		screen.fill((0,42,0))
		msg(y=5,message="Game Paused",size=70)
		msg(y=95,message="Press any key to continue...",size=30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
			elif event.type == pygame.KEYDOWN:
				return None

while startMenu:
	clock.tick(FPS)
	screen.fill((0,42,0))
	msg(y=5,message="Welcome to Breakout!",size=70)
	button(y=105,message="Play",size = 70,width=200,height=140,colors=[(0,200,0),(0,255,0)],func=play)
	button(y=275,message="Quit",size=70,width=200,height=140,colors=[(0,0,200),(0,0,255)],func=sys.exit)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

def replay():
	global running,MAXBLOCKS,count,player,ball,x_change,ball_speed,\
	score,r,x_vel,y_vel,lst,BLOCKS_TO_DEMOLISH,losingM,b
	running = True
	MAXBLOCKS = randint(4,7)
	count = 0
	player = pygame.Rect(SIZE[0] / 2 - 15,SIZE[1] - 8,60,8)
	ball = pygame.Rect(SIZE[0] / 2, SIZE[1] / 2, 10, 10)
	x_change = 0
	score = 0
	r = False
	x_vel, y_vel = ball_speed, ball_speed
	lst = [pygame.Rect(x,y,30,10)
		for x in range(10,SIZE[0]-10,30)
		for y in range(10,250,10)]
	BLOCKS_TO_DEMOLISH = len(lst)
	losingM = False
	b = False
	return None

def losingMenu():
	while losingM:
		screen.fill((0,42,0))
		msg(y=30,message="You Lose.",size=70)
		button(y=130,message="Play Again",size=30,width=200,height=100,colors=[(0,200,0),(0,255,0)],func=replay)
		button(y=330,message="Quit",size=30,width=200,height=100,colors=[(200,0,0),(255,0,0)],func=sys.exit)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(0)
b = False

def choice1():
	global ball_speed, x_vel, y_vel,b
	ball_speed = 1
	x_vel, y_vel = ball_speed,ball_speed
	b = True

def choice2():	
	global ball_speed, x_vel, y_vel,b
	ball_speed = 2
	x_vel, y_vel = ball_speed,ball_speed
	b = True

def choice3():
	global ball_speed, x_vel, y_vel,b
	ball_speed = 3
	x_vel, y_vel = ball_speed,ball_speed
	b = True

def split(player,ball):
	rects = []
	for x in range(player.left,player.right,ball.width):
		rects.append(pygame.Rect((x,player.y,ball.width,player.height)))
	return rects

while not b:
	screen.fill((0,42,0))
	msg(y=10,message="Choose Your Speed:",size=70)
	msg(y=210,message="Hint: Best speed is 2",size=70)
	button(y=410,message="1",size=30,width=100,height=50,colors=[(0,200,0),(0,255,0)],func=choice1)
	button(y=510,message="2",size=30,width=100,height=50,colors=[(200,0,0),(255,0,0)],func=choice2)
	button(y=610,message="3",size=30,width=100,height=50,colors=[(0,0,200),(0,0,255)],func=choice3)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)

while running:
	velocities = [
	(v[0] * ball_speed,v[1] * ball_speed) for v in [
	(-3,-1),
	(-2,-2),
	(-1,-3),
	(1,-3),
	(2,-2),
	(3,-1)
	]]
	if ball.y > SIZE[1]:
		losingM = True
		losingMenu()
	clock.tick(FPS)
	screen.fill((0,42,0))
	for blc in lst:
		if count == MAXBLOCKS:
			count = 0
			MAXBLOCKS = randint(4,7)
			y_vel = -y_vel
		if (blc.y <= ball.y <= blc.y + blc.height or blc.y <= ball.y + ball.height <= blc.y + blc.height) and \
				(blc.x <= ball.x <= blc.x + blc.width or \
				blc.x <= ball.x + ball.width <= blc.x + blc.width):
					lst.remove(blc)
					count += 1
					score += 1
					continue
		screen.fill((255,255,255), (blc[0]+2,blc[1]+2,blc[2]-4,blc[3]-4))
	player.x += x_change
	if player.x + player.width > SIZE[0]:
		player.x = SIZE[0] - player.width
	if player.x < 0:
		player.x = 0
	ball.x += x_vel
	ball.y += y_vel
	if ball.x + ball.width >= SIZE[0] or ball.x < 0:
		x_vel *= -1
	if ball.y < 0:
		y_vel *= -1
	rects = split(player,ball)
	for v,rect in enumerate(rects):
		if (rect.top <= ball.top <= rect.bottom or rect.top <= ball.bottom <= rect.bottom) and \
		(rect.left <= ball.left <= rect.right or rect.left <= ball.right <= rect.right): 
			x_vel,y_vel = velocities[v]
			break
	size = font.size(str(score))
	x, y = int(SIZE[0] / 2) - int(size[0] / 2), int(SIZE[1] / 2) - int(size[1] / 2)
	screen.blit(font.render(str(score), True, (255,255,255)), (x,y))
	screen.fill((255,255,255), player)
	screen.fill((255,255,255), ball)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a or event.key == pygame.K_LEFT:
				x_change = -9
			elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				x_change = 9
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_a or event.key == pygame.K_LEFT or \
			event.key == pygame.K_d or event.key == pygame.K_RIGHT:
				x_change = 0
