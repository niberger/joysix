import pygame, math, time
import joystick, solver, pose, vector3
from operator import itemgetter
from vector3 import col as col
import numpy as np

class Simulation:
	def __init__(self, win_width = 640, win_height = 480):
		pygame.init()
		self.screen = pygame.display.set_mode((win_width, win_height))
		pygame.display.set_caption("JoySix Cube Demo")
		self.clock = pygame.time.Clock()
		self.vertices = [
			[-1,1,-1],
			[1,1,-1],
			[1,-1,-1],
			[-1,-1,-1],
			[-1,1,1],
			[1,1,1],
			[1,-1,1],
			[-1,-1,1]
		]
		# Define the vertices that compose each of the 6 faces. These numbers are
		# indices to the vertices list defined above.
		self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
		# Define colors for each face
		self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]
		self.angle = 0
		self.joystick = joystick.Joystick()

	
	def run(self):

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			#40 fps max
			time_passed = self.clock.tick(40)

			self.screen.fill((0,32,0))
		
			#events from joystick
			P = pose.exp(col([-math.pi / 2,0,0,0,0,0])) * self.joystick.getPose()

			# It will hold transformed vertices.
			t = []
			
			for v in self.vertices:
				v_c = col(v)
				p = 0.01 * (P * (100 * v_c))				
				# Transform the point from 3D to 2D
				factor = 256 / (4 + p[2,0])
				x = p[0,0] * factor + self.screen.get_width() / 2
				y = -p[1,0] * factor + self.screen.get_height() / 2
				z = p[2,0]
				# Put the point in the list of transformed vertices
				t.append([x,y,z])

			# Calculate the average Z values of each face.
			avg_z = []
			i = 0
			for f in self.faces:
				z = (t[f[0]][2] + t[f[1]][2] + t[f[2]][2] + t[f[3]][2]) / 4.0
				avg_z.append([i,z])
				i = i + 1

			# Draw the faces using the Painter's algorithm:
			# Distant faces are drawn before the closer ones.
			for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
				face_index = tmp[0]
				f = self.faces[face_index]
				pointlist = [(t[f[0]][0], t[f[0]][1]), (t[f[1]][0], t[f[1]][1]),
							 (t[f[1]][0], t[f[1]][1]), (t[f[2]][0], t[f[2]][1]),
							 (t[f[2]][0], t[f[2]][1]), (t[f[3]][0], t[f[3]][1]),
							 (t[f[3]][0], t[f[3]][1]), (t[f[0]][0], t[f[0]][1])]
				pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)

				
			self.angle += 1
			
			pygame.display.flip()


if __name__ == '__main__':
	s = Simulation()
	s.run()
