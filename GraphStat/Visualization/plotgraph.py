import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sbn
from GraphStat.Graph import stat
import pandas


def plot_ego(graph: nx.Graph, node_id):
	"""
	根据图对象，绘制给定节点的邻接网络图。
	:param graph: 图对象
	:param node_id: 需绘制的节点编号
	:return: 邻接网络图（星型）
	"""
	adj_nodes = list(graph.adj[node_id].keys())
	plt_g = nx.Graph()
	plt_g.add_node(node_id)
	plt_g.add_nodes_from(adj_nodes)
	for adj_node in adj_nodes:
		plt_g.add_edge(node_id, adj_node)
	plt.figure(figsize=(20, 20))
	nx.draw(plt_g, nx.spring_layout(plt_g), with_labels=True, node_size=1000)
	plt.title(f"ADJ_Node_{node_id}")
	plt.savefig(f"PlotGraph_Node_{node_id}.png")


def plt_degree_distribution(graph: nx.Graph, *, mode: str):
	"""
	根据图对象，利用seaborn包绘制指定的度分布图。
	:param graph: 图对象
	:param mode: 绘图模式
	:return: 绘制的指定分布图
	"""
	mode = mode.lower()
	sbn.set(style='darkgrid')
	degre_dis = stat.cal_degree_distribution(graph)
	dataset = pandas.DataFrame(
		data=list(degre_dis.items()),
		columns=["DEGREE", "F_DEGREE"]
	)
	plt.figure(figsize=(20, 20))
	if mode == 'b':
		sbn.barplot(
			x="DEGREE", y="F_DEGREE",
			data=dataset
		)
	elif mode == 's':
		sbn.scatterplot(
			x="DEGREE", y="F_DEGREE",
			data=dataset
		)
	plt.title("DEGREE DISTRIBUTION")
	plt.savefig(f"degree_distribution_{mode}.png")
