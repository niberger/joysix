import numpy as np
import numpy.linalg

class Solver:

	def __init__(self, f, tol = 1e-4, maxiter = 50):
		self.f = f
		self.tol = tol
		self.maxiter = maxiter

	def solve(self, y_goal, x_hint):
		x = x_hint.copy()
		for i in range(self.maxiter):
			(y, jac) = self.f(x)
			dy = y - y_goal
			dist = np.linalg.norm(dy)
			if(dist < self.tol):
				return x
			dx = np.linalg.solve(jac, dy)
			x = x - dx
		raise StopIteration

