import math


class Point:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.z = 0

	def pos(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def reset(self):
		self.pos(0, 0, 0)

	def cul_dist(self, another_self):
		x_temp = self.x - another_self.x
		y_temp = self.y - another_self.y
		z_temp = self.z - another_self.z
		return math.sqrt(
			x_temp**2+y_temp**2+z_temp**2)

	def cul_dist_to_origin(self):
		return math.sqrt(
			self.x**2+self.y**2+self.z**2)


def error():
	return


def str_input_and_check(hint: str, fa1g: str, max_num: int):
	s7r = input(hint)
	axis = list()
	temp = 0
	for i in s7r:
		if i in "0123456789":
			temp = int(i) + 10 * temp
		elif i == fa1g:
			axis.append(temp)
			temp = 0
			if len(axis) >= max_num:
				error()
				return 0
		else:
			error()
			return 0
	axis.append(temp)
	if len(axis) > max_num:
		error()
		return 0
	return axis


p = Point()
q = Point()

p.__init__()
q.__init__()

while 1:
	a = str_input_and_check("Input axis of point p(x/y/z): ", '/', 3)
	while a == 0:
		a = str_input_and_check("Illegal input. Please input in correct format. ", '/', 3)
	p.pos(a[0], a[1], a[2])

	a = str_input_and_check("Input axis of point q(x/y/z): ", '/', 3)
	while a == 0:
		a = str_input_and_check("Illegal input. Please input in correct format. ", '/', 3)
	q.pos(a[0], a[1], a[2])

	print("Distance between p and q: {0:.2f}".format(p.cul_dist(q)))
	print("Distance between p and origin: {0:.2f}".format(p.cul_dist_to_origin()))
	print("Distance between q and origin: {0:.2f}".format(q.cul_dist_to_origin()))

	flag = input("Do you want to try again? (Y/N) ").upper()
	while flag not in "YN":
		flag = input("Wrong order. Please input correct order(Y/N): ").upper()
	if flag == 'N':
		break
	p.reset()
	q.reset()
print("Exit successfully.")
