# ! /usr/bin/env python3

import numpy as np 
import matplotlib.pyplot as plt
from shapely import Point, LineString
import dubins

def get_dubins(start, end, theta0, theta1, step_size = 0.5):
	q0 = (start[0], start[1], theta0)
	q1 = (end[0], end[1], theta1)

	turning_radius = 1.55
	path = dubins.shortest_path(q0, q1, turning_radius)
	
	configurations, _ = path.sample_many(step_size)

	x, y, yaw = np.array([]), np.array([]), np.array([])
	for i in range(len(configurations)):
		x = np.append(x, configurations[i][0])
		y = np.append(y, configurations[i][1])
		if np.pi <= configurations[i][2] <= 2*np.pi:
			yaw = np.append(yaw, 2*np.pi-configurations[i][2])
		else:
			yaw = np.append(yaw, configurations[i][2])
	
	return x, y, yaw

def get_straight_dubins(start, end, theta0, theta1, step_size = 1):
	q0 = (start[0], start[1], theta0)
	q1 = (end[0], end[1], theta1)

	turning_radius = 0.0001

	path = dubins.shortest_path(q0, q1, turning_radius)
	configurations, _ = path.sample_many(step_size)

	x, y, yaw = np.array([]), np.array([]), np.array([])
	for i in range(len(configurations)):
		x = np.append(x, configurations[i][0])
		y = np.append(y, configurations[i][1])
		if np.pi <= configurations[i][2] <= 2*np.pi:
			yaw = np.append(yaw, 2*np.pi-configurations[i][2])
		else:
			yaw = np.append(yaw, configurations[i][2])

	return x, y, yaw


def arr_to_point(x, y):
	point_arr = []
	for i in range(len(x)):
		point_arr.append(Point(x[i], y[i], 0))
	return point_arr

def point_to_arr(lane):
	arr_x, arr_y = [], []
	for i in range(len(lane[0])):
		arr_x.append(lane[0][i].x)
		arr_y.append(lane[0][i].y)
	return arr_x, arr_y

x1, y1, _ = get_straight_dubins([10, -0.9], [2.5, -0.9], np.pi, np.pi)
x2, y2, _ = get_dubins([2.5, -0.9], [0.9, -2.5], np.pi, -np.pi/2)
x3, y3, _ = get_straight_dubins([0.9, -2.5], [0.9, -10], -np.pi/2, -np.pi/2)
x, y = np.hstack((x1, x2, x3)), np.hstack((y1, y2, y3))
points = arr_to_point(x, y)

line = LineString(points)

vel = 0.7
p = []

for t in range(240):
    p.append(vel*t*0.05)

print(p[-1])
print(line.length)

trajectory = []

for i in range(len(p)):
    trajectory.append(line.interpolate(p[i]))

xs = [point.x for point in trajectory]
ys = [point.y for point in trajectory]
plt.scatter(xs, ys)
plt.show()
