import joystick
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import collections

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
j = joystick.Joystick()
y = collections.deque()

def animate(i):
	y.append(j.readRawValues())
	if(len(y) > 100):
		y.popleft()
	x = range(len(y))
	ax1.clear()
	plt.axis([0,100,-2050,2050])
	ax1.plot(x,y)

ani = animation.FuncAnimation(fig, animate, interval=33)
plt.show()
