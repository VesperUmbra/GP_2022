import pandas
import StandardFileProcessGP as Sfp
from GraphStat.Graph import graph, node, stat
from GraphStat.Visualization import plotgraph, plotnodes


def main():
	"""
	node_metadata = pandas.read_csv(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 4\twitch_gamers\large_twitch_features.csv"
	)
	edge_metadata = Sfp.csv_to_number_list(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 4\twitch_gamers\large_twitch_edges.csv"
	)
	# Sfp是我个人综合的用于作业数据文件的统合处理的函数模块
	nodes = node.Node(node_metadata)
	graph_test = graph.init_graph(nodes.node_data, edge_metadata)
	graph.save_graph(graph_test, 'test_graph.txt')
	"""
	# 至此为读取数据，生成图像并序列化输出到文件中的一次性代码。
	# 后续将直接从序列化文件中读取图对象进行各项方法的测试。
	# 毕竟这样子真的很方便也很快捷（抹泪
	graph_data = graph.load_graph('test_graph.txt')

	print(stat.get_node_number(graph_data))
	print(stat.get_edge_number(graph_data))
	print(stat.cal_average_degree(graph_data))
	deg_dis = stat.cal_degree_distribution(graph_data)
	reg_dis = stat.cal_attr_distribution(graph_data, attr_name='language')
	# 示例，计算“语言”属性的分布。
	
	plotgraph.plt_degree_distribution(graph_data, mode='b')
	plotgraph.plt_degree_distribution(graph_data, mode='s')
	plotnodes.plt_attr_distribution(graph_data, mode='b', attr_name='language')
	plotnodes.plt_attr_distribution(graph_data, mode='s', attr_name='language')

	plotgraph.plot_ego(graph_data, 0)


if __name__ == "__main__":
	main()
