class PwdInfo:
	def __init__(self):
		'''
		初始化一个“密码数据”类对象，三条数据属性均为字符串变量（考虑加密）
		'''
		self.platform = ""
		self.username = ""
		self.password = ""

	def writeinfo(self, pf: str, un: str, pw: str, infolist: list):
		'''
		保存一个密码数据到新的对象实例中，加密（待实装）并加入数据列表
		函数中的self是一个存储临时数据用的实例数据结构
		:param pf: 对应密码数据的"platform"
		:param un: 对应"username"
		:param pw: 对应"password"
		:param infolist: 需要存入的数据列表
		:return: 隐式地返回可供查询的数据列表
		'''
		# pf.enccode('utf-8')
		# un.enccode('utf-8')
		# pw.enccode('utf-8')
		# 数据的加密操作
		self.platform = pf
		self.username = un
		self.password = pw
		infolist.append(self)
		print("Data create is completed successfully.")

	def readinfo(self):
		'''
		读取并输出一个指定实例中的密码数据（目前是直接读取密码簿，后续考虑先导入中转实例再输出）
		后续实装接入加密解密组件
		还需要考虑接入GUI后在GUI中的输出
		:return: 各个对应platform, username and password的参数
		'''
		if self:
			pf = self.platform
			un = self.username
			pw = self.password
			# pf.deccode('utf-8')
			# un.deccode('utf-8')
			# pw.deccode('utf-8')
			# return pf, un, pw # 接入GUI之后，返回三条数据，将三条数据分别输出在窗体中
			print(pf, un, pw)
		else:
			print("Data is not exist. Please check and input correct index of data.")

	def changeinfo(self, column: int, newinfo: str):
		'''
		更改一个实例中的指定数据
		备注：也许可以集成到writeinfo的方法里面，通过指定默认参数的方式实现部分数据的更改和写入
		但也许需要别的空白实例封装默认信息，还要解决可能发生的数据丢失问题
		目前采用的直接写入密码簿数据的保密性较差，也不好对应后续接入数据库之后数据读写的可用性(?)
		:param column: 指定实例中需要更改的数据类型(1 -> platform, 2 -> username, 3 -> password)
		:param newinfo: 需要替换上去的数据(字符串类型)
		:return:隐式地返回修改后的数据或错误信息
		'''
		# new_info.enccode('utf-8')
		if column == 1:
			self.platform = newinfo
		elif column == 2:
			self.username = newinfo
		elif column == 3:
			self.password = newinfo
		else:
			print("Invalid column order. Please check and input correct order.")
			return -1

		print("Data is changed successfully.")


def pwtest():
	pwdnote = list()
	defpwd = PwdInfo()
	defpwd.writeinfo('pycharm', 'czw', 'buaaczw', pwdnote)
	defpwd.readinfo()
	pwdnote[-1].readinfo()

	inputpwd = PwdInfo()
	inputpf = input()
	inputun = input()
	inputpw = input()
	inputpwd.writeinfo(inputpf, inputun, inputpw, pwdnote)
	inputpwd.readinfo()
	pwdnote[-1].readinfo()

	info_to_change = int(input())-1
	col_to_change = int(input())
	new_info = input()
	pwdnote[info_to_change].readinfo()
	while pwdnote[info_to_change].changeinfo(col_to_change, new_info) == -1:
		col_to_change = int(input())
	pwdnote[info_to_change].readinfo()


if __name__ == '__main__':
	pwtest()

'''
2022/9/3: 实现了密码class的基本定义以及明文存储读取和修改的机制。
'''