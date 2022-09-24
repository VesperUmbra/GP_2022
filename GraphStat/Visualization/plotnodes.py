from GraphStat.Graph import stat
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sbn
import pandas


def plt_attr_distribution(graph: nx.Graph, *, mode: str, attr_name: str):
	"""
	根据图对象、指定的模式和指定的属性名，绘制某个属性的分布图。
	:param graph: 图对象
	:param mode: 绘图模式
	:param attr_name: 属性名称
	:return: 指定的属性的分布图
	"""
	mode = mode.lower()
	sbn.set(style='darkgrid')
	attr_dis = stat.cal_attr_distribution(graph, attr_name=attr_name)
	dataset = pandas.DataFrame(
		data=list(attr_dis.items()),
		columns=[f"{attr_name.upper()}", f"F_{attr_name.upper()}"]
	)
	plt.figure(figsize=(20, 20))
	if mode == 'b':
		sbn.barplot(
			x=f'{attr_name.upper()}', y=f'F_{attr_name.upper()}',
			data=dataset
		)
	elif mode == 's':
		sbn.scatterplot(
			x=f'{attr_name.upper()}', y=f'F_{attr_name.upper()}',
			data=dataset
		)
	plt.title(f"{attr_name.upper()} DISTRIBUTION")
	plt.savefig(f"{attr_name}_distribution_{mode}.png")
