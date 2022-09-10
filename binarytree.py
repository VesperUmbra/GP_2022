class BinaryPtr:
	def __init__(self):
		'''
		初始化一个二叉树节点。左右子树设置为非实例化的None防止过度递归内存溢出
		'''
		self.data = None
		self.left = None
		self.right = None

	def createaleaf(self, tempdata):
		'''
		构造一个非空二叉树节点，并初始化空白的左右子树方便后续插入元素。
		（原则上作为插入元素的子函数，不单独运用）
		:param tempdata: 需要插入二叉树的元素
		:return: 一个指定位置的二叉树节点
		'''
		self.data = tempdata
		self.left = BinaryPtr()
		self.right = BinaryPtr()

	def showaleafdata(self):
		'''
		展示一个二叉树节点存储的元素（不是内存地址）
		:return:
		'''
		print(self.data, end=' ')

	def pluginleafbybst(self, item):
		'''
		以二叉排序树规则插入二叉树元素。
		:param item: 待插入的元素
		:return: 按照二叉排序树规则构造的二叉树（由于递归调用，最终返回的是根节点）
		'''
		if self.data == None:
			self.createaleaf(item)
		elif item < self.data:
			self.left.pluginleafbybst(item)
		else:
			self.right.pluginleafbybst(item)

	def searchinbst(self, itemtosearch):
		'''
		以二叉排序树的规则查找指定的元素。
		:param itemtosearch: 待查找的元素
		:return: 查询结果（存在则返回对应节点的内存地址，否则返回错误信息）
		'''
		if self.data != None:
			if self.data == itemtosearch:
				print("Find item:", end=' ')
				self.showaleafdata()
				print('in position: ',self)
				return
			elif itemtosearch < self.data:
				self.left.searchinbst(itemtosearch)
			else:
				self.right.searchinbst(itemtosearch)
		else:
			print("Error: No such item")
			return -1

	def preorder(self):
		'''
		二叉树的前序遍历
		:return:
		'''
		if self.data != None:
			self.showaleafdata()
			self.left.preorder()
			self.right.preorder()

	def inorder(self):
		'''
		二叉树的中序遍历
		:return:
		'''
		if self.data != None:
			self.left.inorder()
			self.showaleafdata()
			self.right.inorder()

	def postorder(self):
		'''
		二叉树的后序遍历
		:return:
		'''
		if self.data != None:
			self.left.postorder()
			self.right.postorder()
			self.showaleafdata()

	def destroybt(self):
		if self.data != None:
			self.left.destroybt()
			self.right.destroybt()
			self.__init__()


def test():
	testlist = [10, 5, 2, 12, 20, 19, 17, 5]
	examlist = list(range(10))
	print(testlist)
	print(examlist)
	testtree = BinaryPtr()
	for item in testlist:
		testtree.pluginleafbybst(item)
	testtree.preorder()
	print('')
	testtree.inorder()
	print('')
	testtree.postorder()
	print('')
	testtree.searchinbst(6)
	testtree.searchinbst(5)
	testtree.destroybt()
	examtree = BinaryPtr()
	for item in examlist:
		examtree.pluginleafbybst(item)
	examtree.preorder()
	print('')
	examtree.inorder()
	print('')
	examtree.postorder()
	print('')
	examtree.searchinbst(12)
	examtree.searchinbst(5)
	examtree.destroybt()

if __name__ == '__main__':
	test()