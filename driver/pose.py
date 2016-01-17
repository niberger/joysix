import math
import numpy as np
import numpy.linalg
import vector3 as v3
import trigonometry as trig
import quaternion as quat

class Pose:
	def __init__(self, q, t): 
		self.rot = q
		self.trans = t

	def __mul__(self, p):
		if(isinstance(p, Pose)):
			return Pose(self.rot * p.rot, self.rot * p.trans + self.trans)
		else:
			return self.rot * p + self.trans

	def inv(self):
		return Pose(self.rot.inv(), -(self.rot.inv() * self.trans))


def mt(v):
	r = v[0:3]
	t = v[3:6]
	x = np.linalg.norm(r)
	b = trig.cosox2(x)
	c = trig.sinox3(x)
	g = trig.specialFun1(x)
	h = trig.specialFun3(x)
	I = np.identity(3)
	return b*quat.skew(t) + c*(r*t.transpose() + t*r.transpose()) + v3.dot(r,t)*((c - b) * I + g*quat.skew(r) + h*r*r.transpose())

def exp(v):
	r = v[0:3]
	t = v[3:6]
	q = quat.exp(r)
	D = quat.dexp(r)
	return Pose(q, D * t)

def dexp(v):
	r = v[0:3]
	dexpr = quat.dexp(r)
	MT = mt(v)
	return np.bmat([[dexpr,MT],[np.zeros((3,3)),dexpr]])

def log(p):
	q = p.rot
	t = p.trans
	r = quat.log(q)
	D = quat.dlog(r)
	return np.vstack((r, D * t))

def dlog(v):
	r = v[0:3]
	dlogr = quat.dlog(r)
	MT = mt(v)
	return np.bmat([[dlogr, -dlogr*MT*dlogr],[np.zeros((3,3)),dlogr]])
	
