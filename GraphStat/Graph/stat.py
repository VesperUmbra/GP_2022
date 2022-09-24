"""
MODULE STAT
处理图对象中的统计问题。
"""
import networkx as nx


def get_node_number(graph: nx.Graph):
	"""
	输出图对象中的节点数量。
	:param graph: 图对象
	:return: 图对象中的节点数量（整数）
	"""
	return len(graph.nodes)


def get_edge_number(graph: nx.Graph):
	"""
	输出图对象中的边数。
	:param graph: 图对象
	:return: 图对象中边的数量（整数）
	"""
	return len(graph.edges)


def cal_average_degree(graph: nx.Graph):
	"""
	计算图对象中的各个节点的平均度。
	:param graph: 图对象
	:return: 图对象中节点的平均度。
	"""
	graph_degree = dict(graph.degree).values()
	return sum(graph_degree)/len(graph_degree)


def cal_degree_distribution(graph: nx.Graph) -> dict:
	"""
	计算图对象中节点的度的分布（字典形式）
	:param graph: 图对象
	:return: 图对象中节点的度的分布（字典）
	"""
	graph_degree = dict(graph.degree)
	degree_distribution = dict()
	for node, degree in graph_degree.items():
		degree_distribution[degree] = degree_distribution.get(degree, 0) + 1
	for key in degree_distribution.keys():
		degree_distribution[key] = degree_distribution[key]/len(graph.nodes)
	return degree_distribution


def cal_attr_distribution(graph: nx.Graph, *, attr_name: str) -> dict:
	"""
	计算图对象中指定属性的分布。
	:param graph: 图对象
	:param attr_name: 指定属性名
	:return: 属性的分布（字典）
	"""
	graph_node = graph.nodes
	attr_distribution = dict()
	for node_id in graph_node:
		attr = graph_node[node_id][attr_name]
		attr_distribution[attr] = attr_distribution.get(attr, 0) + 1
	for key in attr_distribution.keys():
		attr_distribution[key] = attr_distribution[key]/len(graph_node)
	return attr_distribution
