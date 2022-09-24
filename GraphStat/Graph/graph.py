"""
MODULE GRAPH
利用networkx模块生成网络信息，并实现序列化输出和读取。
"""
import networkx as nx
import pickle


def init_graph(node_dict: dict, edge_list: list):
	"""
	根据输入的节点信息和边信息，构筑网络图数据。

	:param node_dict:节点信息（字典存储）
	:param edge_list: 边信息（列表存储）
	:return: 图对象
	"""
	network_graph = nx.Graph()
	network_graph.add_nodes_from(node_dict.keys())
	for node_id in network_graph.nodes:
		node_attr = node_dict[node_id]
		for attr in node_attr.keys():
			network_graph.nodes[node_id][attr] = node_attr[attr]
	network_graph.add_edges_from(edge_list)
	return network_graph


def save_graph(graph_info: nx.Graph, file_name: str):
	"""
	将图对象序列化输出到指定文件。

	:param graph_info:图对象
	:param file_name: 文件名及目录
	:return: 输出完毕的文件
	"""
	f = open(file_name, 'wb')
	pickle.dump(graph_info, f, 0)
	f.close()


def load_graph(graph_file: str):
	"""
	从指定的序列化文件中读取图对象

	:param graph_file: 存储图对象的序列化文件
	:return: 读取完毕的图对象
	"""
	file = open(graph_file, 'rb')
	return pickle.load(file)
