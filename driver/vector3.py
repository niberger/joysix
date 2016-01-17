import numpy as np

def vector3(x, y, z):
	return np.matrix([[x],[y],[z]])

def vector6(a, b, c, x, y, z):
	return np.matrix([[a],[b],[c],[x],[y],[z]])

def col(v):
	col = [[x] for x in v]
	return np.matrix(col)

def dot(u, v):
	return (u.T*v)[0,0]
