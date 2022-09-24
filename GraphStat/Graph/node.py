"""
MODULE Node:
执行"Node"类的生成和查询等相关操作。
"""
import pandas


class Node:
	def __init__(self, node_info: pandas.DataFrame):
		"""
		初始化Node类变量，传入读取了csv文件后的DataFrame变量，
		生成存储节点信息的字典。

		:param node_info:读取csv文件后得到的DataFrame。
		"""
		total_node = dict()
		for i in range(len(node_info)):
			node_attr = dict()
			node = node_info.loc[i]
			node_id = node['numeric_id']
			for attr in node.keys():
				if attr == 'numeric_id':
					continue
				node_attr[attr] = node[attr]
			total_node[node_id] = node_attr
		self.node_data = total_node

	def get_attr(self, *, node_id, attr_name):
		"""
		根据输入的节点id与指定的属性名称，查询指定节点的指定属性。

		:param node_id:需查询的节点ID
		:param attr_name: 需查询的属性名称。
		:return: 指定条目的指定属性字段。
		"""
		node_info = self.node_data[node_id]
		return node_info[attr_name]

	def print_node(self, node_id):
		"""
		根据输入的指定id，输出节点的全部信息。

		:param node_id:待查节点ID
		:return: 在终端屏幕上输出各项属性的名称和字段
		"""
		node_info = self.node_data[node_id]
		for attr, para in node_info.items():
			print(f"{attr:>15}: {para:<15}")
