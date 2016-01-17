import pose, solver
import quaternion as quat
import vector3
import math, serial
import numpy as np
import numpy.linalg
from vector3 import col, dot

class Joystick:
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyACM0', 9600)

		#geometrical calibration
		self.rs = [40, 40, 40]
		self.ls = [102, 145, 102]
		self.pot_angle = 220/180*math.pi
		angles = [2./3.*math.pi, 0., -2./3.*math.pi]

		#placements of the 3 joysticks
		self.placements = []
		#attach point on the ball
		self.attach_ps = []
		for r,l,a in zip(self.rs, self.ls, angles):
			p_init = pose.exp(col([0, 0, 0, 0, 0, -(r+l)]))
			p_rot = pose.exp(col([0, a, 0, 0, 0, 0]))
			placement = p_rot * p_init
			self.placements.append(placement)
			attach_p = placement * col([0, 0, l])
			self.attach_ps.append(attach_p)

		#last calculated pose in logarithmic coordinates
		self.last_x = col([0, 0, 0, 0, 0, 0])
		#definition of the numerical solver
		f = lambda x: self.getValuesFromPose(pose.exp(x))
		self.solver = solver.Solver(f)

	def getValuesFromPose(self, P):
		'''return the virtual values of the pots corresponding to the pose P'''
		vals = []
		grads = []
		for i, r, l, placement, attach_p in zip(range(3), self.rs, self.ls, self.placements, self.attach_ps):
			#first pot axis
			a = placement.rot * col([1, 0, 0])
			#second pot axis
			b = placement.rot * col([0, 1, 0])
			#string axis
			c = placement.rot * col([0, 0, 1])

			#attach point on the joystick
			p_joystick = P * attach_p
			v = p_joystick - placement.trans
			va = v - dot(v, a)*a
			vb = v - dot(v, b)*b
			#angles of the pots
			alpha = math.atan2(dot(vb, a), dot(vb, c))
			beta = math.atan2(dot(va, b), dot(va, c))
			vals.append(alpha)
			vals.append(beta)
			
			#calculation of the derivatives
			dv = np.bmat([-P.rot.mat() * quat.skew(attach_p), P.rot.mat()])
			dva = (np.eye(3) - a*a.T) * dv
			dvb = (np.eye(3) - b*b.T) * dv
			dalpha = (1/dot(vb,vb)) * (dot(vb,c) * a.T - dot(vb,a) * c.T) * dvb
			dbeta = (1/dot(va,va)) * (dot(va,c) * b.T - dot(va,b) * c.T) * dva
			grads.append(dalpha)
			grads.append(dbeta)
		return (col(vals), np.bmat([[grads]]))
		
	def getNumericalGradient(self, P, h = 1e-5):
		'''just to check the calculations...'''
		grad = []
		for i in range(6):
			dv = [0, 0, 0, 0, 0, 0]
			dv[i] = h
			gi = (1./h) * (self.getValuesFromPose(P * pose.exp(col(dv))) - self.getValuesFromPose(P))
			grad.append(gi)
		return np.bmat(grad)

	def readRawValues(self):
		'''read the values of the potentiometers'''
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.write('g') #g for get
		raw_values = self.ser.readline()
		return raw_values.split()

	def readValues(self):
		'''read the values of the potentiometers'''
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.write('g') #g for get
		raw_values = self.ser.readline()
		coef = self.pot_angle / 4096
		values = col([coef * float(x) for x in raw_values.split()])
		return values

	def getPose(self):
		'''return the pose of the joystick (numerically calculated)'''
		y = self.readValues()
		x = self.solver.solve(y, self.last_x)
		P = pose.exp(x)
		self.last_x = pose.log(P)
		return P

