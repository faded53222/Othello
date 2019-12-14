import pygame
import sys
import time
import random
import pickle
GREY=(111,111,111)
WHITE=(255,255,255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = (800,800)
game_size=(8,8)
cube_height=screen_size[0]/game_size[0]
cube_width=screen_size[1]/game_size[1]
chess_vec=[[],[]]
candidate_list=[]
pos_dic={}
chess_count=[0,0]
class one_pos():
	def __init__(self,pos):
		self.pos=pos
		self.occupied=0
		self.neighbors=[0]*8
	def occupy(self,occupied):
		self.occupied=occupied
		chess_vec[occupied-1].append(self.pos)
		ene_occupied=occupied%2+1
		chess_count[occupied-1]+=1
		if self in candidate_list:
			candidate_list.remove(self)
		for i in range(8):
			if self.neighbors[i]==0:
				continue
			if self.neighbors[i].occupied==0:
				if self.neighbors[i] not in candidate_list:
					candidate_list.append(self.neighbors[i])
			if self.neighbors[i].occupied==ene_occupied:
				current_node=self.neighbors[i]
				while 1:
					current_node=current_node.neighbors[i]
					if current_node==0:
						break
					if current_node.occupied==0:
						break
					if current_node.occupied==occupied:
						while 1:
							current_node=current_node.neighbors[(i+4)%8]
							if current_node.occupied==occupied:
								break
							current_node.occupied=occupied
							chess_vec[occupied-1].append(current_node.pos)
							chess_vec[ene_occupied-1].remove(current_node.pos)
							chess_count[occupied-1]+=1
							chess_count[ene_occupied-1]-=1
						break
def draw_lines(screen):
	for i in range(1,game_size[0]):
		pygame.draw.aaline(screen, WHITE,(i*cube_height,0),(i*cube_height,screen_size[1]),5)
	for i in range(1,game_size[1]):
		pygame.draw.aaline(screen, WHITE,(0,i*cube_width),(screen_size[0],i*cube_width),5)
def draw_cubes(screen):
	for each in chess_vec[0]:
		pygame.draw.rect(screen,[0,0,0],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
	for each in chess_vec[1]:
		pygame.draw.rect(screen,[255,255,255],[(each[1])*cube_width,(each[0])*cube_height,cube_width,cube_height],0)
saved_list=[]
def save():
	data=pickle.dumps((candidate_list,pos_dic,chess_count))
	saved_list.append(data)
def load():
	global pos_dic
	global candidate_list
	(candidate_pos_list,pos_dic,chess_count)=pickle.loads(saved_list[-1])
def init():
	for i in range(game_size[0]):
		for j in range(game_size[1]):
			a_pos=one_pos((i,j))
			pos_dic[(i,j)]=a_pos
	for i in range(game_size[0]):
		for j in range(game_size[1]):
			lis=[(i,j+1),(i+1,j+1),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1),(i-1,j),(i-1,j+1)]
			for k in range(len(lis)):
				if lis[k][0]>=0 and lis[k][0]<game_size[0] and lis[k][1]>=0 and lis[k][1]<game_size[1]:
					pos_dic[(i,j)].neighbors[k]=pos_dic[lis[k]]	
def get_av_pos(turn):
	av_pos=[]
	ene_occupied=(turn+1)%2+1
	for each in candidate_list:
		lab=0
		for i in range(8):
			if each.neighbors[i]==0:
				continue
			if each.neighbors[i].occupied==ene_occupied:
				current_node=each.neighbors[i]
				while 1:
					current_node=current_node.neighbors[i]
					if current_node==0:
						break
					if current_node.occupied==0:
						break
					if current_node.occupied==turn+1:
						lab=1
						av_pos.append(each.pos)
						break
				if lab==1:
					break
	return av_pos
if __name__ == "__main__":
	init()
	pygame.init()
	screen = pygame.display.set_mode(screen_size, 0, 32)
	pygame.display.set_caption("gobang")
	FPS=30
	clock = pygame.time.Clock()
	turn=0
	win_lab=0
	first_lab=0
	pos_pos=[[],[]]
	pos_dic[(3,3)].occupy(2)
	pos_dic[(3,4)].occupy(1)
	pos_dic[(4,3)].occupy(1)
	pos_dic[(4,4)].occupy(2)
	pos_pos[0]=get_av_pos(0)
	pos_pos[1]=get_av_pos(1)
	while True:
		clock.tick(FPS)
		if win_lab==0:
			l=0
			if pygame.mouse.get_pressed()[0]:
				first_lab=1
				pos=pygame.mouse.get_pos()
				pos_=(int(pos[1]/cube_height),int(pos[0]/cube_width))				
				if pos_ in pos_pos[turn]:
					l=1
			if l==1:
				if pos_dic[pos_].occupied==0:
					pos_dic[pos_].occupy(turn+1)
					turn=(turn+1)%2
					pos_pos[turn]=get_av_pos(turn)
					if len(pos_pos[turn])==0:
						turn=(turn+1)%2
						pos_pos[turn]=get_av_pos(turn)
						if len(pos_pos[turn])==0:
							win_lab=1
							print(chess_count[0],chess_count[1])
							if chess_count[0]==chess_count[1]:
								print('tie')
							else:
								print('player ',(chess_count[0]<chess_count[1])+1,' win')
		screen.fill(GREY)
		draw_lines(screen)
		draw_cubes(screen)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
