class PwdInfo:
	def __init__(self):
		self.platform = ""
		self.username = ""
		self.password = ""

	def writeinfo(self, pf: str, un: str, pw: str, infolist: list):
		self.platform = pf
		self.username = un
		self.password = pw
		# self.platform.encode('utf-8')
		# self.username.encode('utf-8')
		# self.password.encode('utf-8')
		infolist.append(self)
		print("Data create is completed successfully.")

	def readinfo(self):
		if self:
			pf = self.platform
			un = self.username
			pw = self.password
			# pf.decode('utf-8')
			# un.decode('utf-8')
			# pw.decode('utf-8')
			# return pf, un, pw
			print(pf, un, pw)
		else:
			print("Data is not exist. Please check and input correct index of data.")

	def changeinfo(self, column: int, newinfo: str):
		# new_info.encode('utf-8')
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


def main():
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
	main()

'''
2022/9/3: 实现了密码class的基本定义以及明文存储读取和修改的机制。
'''