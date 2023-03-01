from shapely import Point, LineString
import matplotlib.pyplot as plt

line = LineString([(-10, 0), (-5, 0), (0, 0), (5, 0), (10, 0)])

vel = 0.2
p = []

for t in range(100):
    p.append(vel*t)

trajectory = []

for i in range(len(p)):
    trajectory.append(line.interpolate(p[i]))

xs = [point.x for point in trajectory]
ys = [point.y for point in trajectory]
plt.scatter(xs, ys)
plt.show()
