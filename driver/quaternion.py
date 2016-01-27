import math
import numpy as np
import numpy.linalg
import trigonometry as trig
from vector3 import col

class Quaternion:
	def __init__(self, w, v):
		self.w = w
		self.v = v

	def x(self):
		return self.v[0,0]
	def y(self):
		return self.v[1,0]
	def z(self):
		return self.v[2,0]

	def __repr__(self):
		return "("+str(self.w)+", "+str(self.x())+", "+str(self.y())+", "+str(self.z())+" )"

	def __mul__(self, q):
		if(isinstance(q, Quaternion)):
			w = self.w * q.w - self.x() * q.x() - self.y() * q.y() - self.z() * q.z()
			x = self.w * q.x() + self.x() * q.w + self.y() * q.z() - self.z() * q.y()
			y = self.w * q.y() + self.y() * q.w + self.z() * q.x() - self.x() * q.z()
			z = self.w * q.z() + self.z() * q.w + self.x() * q.y() - self.y() * q.x()
			return Quaternion(w, col([x, y, z]))
		else:
			return (self * Quaternion(0, q) * self.inv()).im()
			

	def inv(self):
		return Quaternion(self.w, -self.v)

	def im(self):
		return self.v
	
	def yaw(self):
		return math.atan2(2*(self.w*self.z() + self.x()*self.y()), 1 - 2*(self.y()*self.y() + self.z()*self.z()))

	def pitch(self):
		return math.asin(2*(self.w*self.y() - self.z()*self.x()))

	def roll(self):
		return math.atan2(2*(self.w*self.x() + self.z()*self.y()), 1 - 2*(self.y()*self.y() + self.x()*self.x()))

	def mat(self):
		return np.bmat([self * col([1,0,0]), self * col([0,1,0]), self * col([0,0,1])])

def id():
	return Quaternion(1., col([0., 0., 0.]))

def skew(v):
	return np.matrix([[0,-v[2,0],v[1,0]], [v[2,0],0,-v[0,0]], [-v[1,0],v[0,0],0]])

def exp(v):
	hv = 0.5*v
	theta = np.linalg.norm(hv)
	a = trig.sinox(theta)
	b = math.cos(theta)
	return Quaternion(b, a*hv)

def dexp(v):
	x = np.linalg.norm(v)
	a = trig.sinox(x)
	b = trig.cosox2(x)
	c = trig.sinox3(x)
	I = np.identity(3)
	S = skew(v)
	W = v * v.transpose()
	return a*I + b*S + c*W

def log(q):
	im = q.im()
	imn = np.linalg.norm(im)
	n = math.atan2(imn, q.w)
	if(abs(n) < 1e-6):
		return 2*im
	else:
		return 2*(n/imn)*im

def dlog(v):
	x = np.linalg.norm(v)
	y = trig.specialFun4(x)
	z = trig.specialFun2(x)
	I = np.identity(3)
	S = skew(v)
	W = v * v.transpose()
	return y*I - 0.5*S + z*W
	
	
