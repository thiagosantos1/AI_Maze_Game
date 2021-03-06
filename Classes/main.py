# Copyright by Thiago Santos
# All rights reserved

# Please, read the file Read_Me to undestand better about the game and solution

# Referece Websites

# Main class 
# Use to control the logic of the game
import pygame
from time import sleep
from maze import *
from tiles import *
from character import *
from survivor import *
from interaction import interaction
from bonus import *
import random
import sys
from monster import *
import DisplayText  # class to display any text on screen

sys.setrecursionlimit(sys.getrecursionlimit() *4) # the default value is not enough if you wanna a maze of size >50


pygame.init()

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [153, 153, 153]
BEGE = [222,184,135]
GREEN = [0,255,0]
RED = [255,0,0]
PINK = [255,105,180]
DARK_PINK = [255,20,147]
BLUE = [  0,   0, 255]
BROWN = [165,42,42]
PURPLE = [160,32,240]
DARK_GRAY = [49,79,79]
SKY_BLUE = [0,191,255]
TURQUOISE = [64,224,208]
GREN_YELLOW = [173,255,47]
YELLOW = [255,255,0]
GOLD = [255,215,0]
ORANGE = [255,165,0]
DARK_ORANGE = [255,140,0]
ORCHILD = [218,112,214]

list_colors = ( (BLACK),(WHITE),(GRAY),(BEGE),(GREEN),(RED),(PINK),(DARK_PINK),(BLUE),(BROWN),(PURPLE) 
				,(DARK_GRAY) ,(SKY_BLUE) ,(TURQUOISE) ,(GREN_YELLOW) ,(YELLOW) ,(GOLD) ,(ORANGE) 
				,(DARK_ORANGE) ,(ORCHILD) )

WIDTH = 1200
HEIGHT = 700

mazeColor = random.randrange(0,len(list_colors))
backgroundColor = mazeColor
while backgroundColor == mazeColor:
	backgroundColor = random.randrange(0,len(list_colors))


mazeSize = 0
game_mode = "AI" # player is gonna choose to play or put PC to play
while(mazeSize <10):
	mazeSize = int(input("Please, enter the size of the Maze(it's N*N) >=10: "))

tileWidth = WIDTH // mazeSize

# make sure is divisble by 2. make easir to control how to move
while(tileWidth %2 !=0):
	tileWidth+=1

if tileWidth * mazeSize > WIDTH:
	tileWidth -=1
	while(tileWidth %2 !=0):
		tileWidth-=1

tileHeight = HEIGHT // mazeSize

while tileHeight %2 !=0:
	tileHeight+=1

if tileHeight * mazeSize > HEIGHT:
	tileHeight-=1
	while(tileHeight %2 !=0):
		tileHeight-=1


WIDTH = tileWidth * mazeSize
HEIGHT = tileHeight * mazeSize


screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Maze")
pygame.mouse.set_visible(False)

maze = Maze(mazeSize,WIDTH,HEIGHT)

mode = input("\nDo you wanna to play as the robot(Y/N) ? - No means AI will play as both mode\nChoise: ").upper()
if mode == 'Y' or mode =="YES":
	game_mode = "player"
#survivor = Survivor(1,"BFS") # each tile you wish the survivor to start at
survivor = Survivor(1,"A_Star",game_mode) # each tile you wish the survivor to start at
# create all monster
# can make it better and do random, later
monster_per_block = 10 # 1 monster for each 10 squares - Maximum is 6 monsters
qtd_monsters = mazeSize - monster_per_block
Monster( mazeSize , 'BFS') # must have at least one
if qtd_monsters >= monster_per_block:
	Monster( (mazeSize * mazeSize), 'DFS')
	qtd_monsters = qtd_monsters - monster_per_block

if qtd_monsters >= monster_per_block:
	Monster( ((mazeSize//2) * (mazeSize//2) ), 'DFS')
	qtd_monsters = qtd_monsters - monster_per_block

if qtd_monsters >= monster_per_block:
	Monster( ((mazeSize * mazeSize) -mazeSize +1) , 'DFS')
	qtd_monsters = qtd_monsters - monster_per_block

if qtd_monsters >= monster_per_block:
	Monster( ((mazeSize * (mazeSize//2)) -(mazeSize -1)) , 'DFS')
	qtd_monsters = qtd_monsters - monster_per_block

if qtd_monsters >= monster_per_block:
	Monster( ((mazeSize * (mazeSize//2)) -(mazeSize//2)) , 'DFS')




# Used to manage how fast the screen updates
clock = pygame.time.Clock()
FPS = 35 # if we increase this number, the speed of character will be lower
total_frames = 0

# Loop until the user clicks the close button.
done = False


while not done:

	milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
	clock_elapsed_seconds = milliseconds / 10000.0 # seconds passed since last frame (float)

	if total_frames ==0:
		pygame.mixer.music.load('../Sound_Effects/welcome/welcome.wav')
		# play the background game music
		pygame.mixer.music.play(-1) # -1 put to loop the music forever

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			done = True

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				mazeColor = random.randrange(0,len(list_colors))
				backgroundColor = mazeColor
				while backgroundColor == mazeColor:
					backgroundColor = random.randrange(0,len(list_colors))
			# generate a new maze
			if event.key == pygame.K_g:
				maze.resetMaze()
				maze = Maze(mazeSize,WIDTH,HEIGHT)
				Maze.resetTiles()
				survivor.resetPath()
				for monster in Monster.List_Monster:
					monster.reset_all_path()
	if survivor.gameMode != "AI" and survivor.isAlive:
		if len(Bonus.list_bonus)>0 :
			interaction(screen, survivor)
			

    # --- Game logic should go here

    # interaction method from Interaction class. It control all events from the game
    # player can play as the robot if use this line
	#interaction(screen, survivor)
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
	screen.fill(list_colors[backgroundColor])
 	
    # --- Drawing code should go here
	maze.draw_maze(screen,list_colors[mazeColor])

	if survivor.isAlive:
		# move to the new direction, and also draw the player in the screen
		survivor.update(screen,clock_elapsed_seconds)

		#Monster.spawn(survivor,total_frames, FPS)
		# move to the new direction, and also draw the monsters in the screen
		for monster in Monster.List_Monster:
			monster.update(screen,clock_elapsed_seconds, survivor)

		Bonus.spawn(total_frames, FPS,survivor)

		Bonus.update(screen,survivor)
	# display the healthy of the player in the screen
	DisplayText.text_to_screen(screen, 'Health: {0}'.format(survivor.health), WIDTH//2 - tileWidth*4,0,16, BLACK)

    # display the player score
	DisplayText.text_to_screen(screen, 'Score: {0}'.format(survivor.score), WIDTH//2+tileWidth,0,16, BLACK)
 		
	if not survivor.isAlive:
		# display the player score
		DisplayText.text_to_screen(screen, 'GAME OVER!!! Final Score:  {0}'.format(survivor.score), tileWidth,HEIGHT//3,HEIGHT//12, BLACK)
 	# update the total of frames
	total_frames+=1
    # --- Go ahead and update the screen with what we've drawn.
	pygame.display.flip()


	clock.tick(FPS)

pygame.quit()





