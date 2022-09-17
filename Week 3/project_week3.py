import jieba
import re
import datetime
import matplotlib.pyplot as plt
from pyecharts import options
from pyecharts.charts import Geo
from pyecharts.globals import GeoType


def get_wordlist(txt):
	"""
	从指定的词表文件中获取单词并组合为set。

	:param txt: 待获取单词的词表文件目录
	:return: 组合完毕的set
	"""
	file = open(
		txt,
		"r",
		encoding="utf-8"
	)
	wordlist_data = file.readlines()
	wordlist_set = set()
	for line in wordlist_data:
		line = line.replace("\n", "")
		wordlist_set.add(line)
		jieba.add_word(line)
	file.close()
	return wordlist_set


def format_axis(ax: str):
	"""
	对微博数据的位置信息进行处理，将原本为字符的坐标信息转换为纯数字信息。

	:param ax:待处理的位置信息（纯文本）
	:return: 处理完毕的位置信息（float列表）
	"""
	axis_meta = ax[1:-1]
	axis_stri = axis_meta.split(",")
	axis_list = list()
	for num in axis_stri:
		axis_list.append(float(num))
	return axis_list


def format_datetime(dt: str):
	"""
	对数据中的时间进行整理并格式化为DateTime结构形式。

	:param dt: 输入的微博信息中的时间信息
	:return: 格式化后的时间信息（Datetime）
	"""
	month_list = [
		"Jan", "Feb", "Mar", "Apr", "May", "Jun",
		"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
	]
	dt_list = dt.split(" ")
	t = dt_list[-3]
	t_list = t.split(":")
	year = int(dt_list[-1])
	month = month_list.index(dt_list[1]) + 1
	day = int(dt_list[2])
	hour = int(t_list[0])
	minute = int(t_list[1])
	second = int(t_list[2])
	dt = datetime.datetime(
		year=year, month=month, day=day,
		hour=hour, minute=minute, second=second
	)
	return dt


def clean_text(text: str) -> str:
	"""
	对微博文本进行清洗降噪（主要清洗内容：url、用户名、“我在这里”一类无意义噪声）。

	:param text: 待清洗文本（仅文本）
	:return: 清洗完毕的文本
	"""
	text1 = re.sub(r"http[:.]+\S+", "", text)
	# 清洗URL
	text2 = re.sub(r"我在:", "", text1)
	text3 = re.sub(r"我在这里:", "", text2)
	# 清洗“我在这里”
	text4 = re.sub(r"\[\S+\]", "", text3)
	# 清洗表情符号
	text5 = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", "", text4)
	# 清洗回复或@及其中用户名
	final_text = re.sub(r"\s+", "", text5)
	# 清洗多余空格
	return final_text


def get_weibo(txt, stopword):
	"""
	从微博数据集中获取（一定量的）微博内容、清洗文本并分词。
	同时处理位置和时间信息。

	:param txt: 待处理的微博数据集文件目录
	:param stopword: 停用词表
	:return: 处理完毕的微博内容（嵌套列表）
	"""
	file = open(
		txt,
		"r",
		encoding="utf-8"
	)
	weibo_metadata = file.readlines()
	weibo_metadata.pop(0)
	weibo_ana = list()
	# i = 0
	for line in weibo_metadata:
		# i += 1
		line = line.replace("\n", "")
		line_temp = list(line.split('\t'))

		axis_temp = line_temp[0]
		line_temp[0] = format_axis(axis_temp)

		text_temp = clean_text(line_temp[1])
		text_temp = jieba.lcut(text_temp)
		str_temp = list()
		for word in text_temp:
			if word not in stopword:
				str_temp.append(word)
		line_temp[1] = str_temp

		dt_temp = line_temp[3]
		if len(dt_temp) != 0:
			line_temp[3] = format_datetime(dt_temp)

		weibo_ana.append(line_temp)
		# if i == 50:
		#	break
	file.close()
	return weibo_ana


def emotion_test(emotion_list):
	"""
	情绪测试（的入口函数），此部分仅读取并构建情绪词汇列表。
	采用闭包函数的方式处理。

	:return: 情绪分析的实际操作函数
	"""
	emotion_dict = dict()
	emotion = ["Anger", "Disgust", "Fear", "Joy", "Sadness"]
	for i in range(5):
		for word in emotion_list[i]:
			emotion_dict[word] = emotion[i]

	def emotion_check(text_info):
		"""
		情绪分析的实际执行函数。

		:param text: 待情绪分析的文本（已降噪并分词完毕）
		:return: 情绪分析的文本结果
		"""
		nonlocal emotion_dict
		for line in text_info:
			emotion_number = {
				"Anger"  : 0,
				"Disgust": 0,
				"Fear"   : 0,
				"Joy"    : 0,
				"Sadness": 0
			}
			sentence = line[1]
			for word_to_check in sentence:
				if word_to_check in emotion_dict.keys():
					emotion_number[emotion_dict[word_to_check]] += 1
			emo_sorted = sorted(emotion_number.items(), key=lambda x: x[1], reverse=True)
			if emo_sorted[0][1] == emo_sorted[4][1]:
				line[2] = "Not Emotional"
			else:
				line[2] = emo_sorted[0][0]
		return text_info

	return emotion_check


def time_check(weibo_info, emotion, *, mode):
	"""
	对微博文本数据进行时间维度的情绪分析，输出指定的时间维度上的指定情绪的发生频数。
	以字典形式输出为可视化处理做准备。

	:param weibo_info:微博数据（全部数据）
	:param emotion: 指定的情绪（文本字符）
	:param mode: 指定的时间维度（文本字符）
	:return: 时间维度上情绪频数的映射（字典）
	"""
	if mode.lower() == "w":
		weekday_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
		week_dict = dict().fromkeys(weekday_list, 0)
		for info in weibo_info:
			if info[2] != emotion:
				continue
			dt_info = info[3]
			if dt_info != "":
				weekday = weekday_list[dt_info.weekday()]
				week_dict[weekday] += 1
		return week_dict

	elif mode.lower() == "m":
		month_list = [
			"Jan", "Feb", "Mar", "Apr", "May", "Jun",
			"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
		]
		month_dict = dict().fromkeys(month_list, 0)
		for info in weibo_info:
			if info[2] != emotion:
				continue
			dt_info = info[3]
			if dt_info != "":
				month = month_list[dt_info.month - 1]
				month_dict[month] += 1
		return month_dict

	elif mode.lower() == "h":
		hour = list(range(24))
		hour_dict = dict().fromkeys(hour, 0)
		for info in weibo_info:
			if info[2] != emotion:
				continue
			dt_info = info[3]
			if dt_info != "":
				hour_dict[dt_info.hour] += 1
		return hour_dict


def culc_distance(point_a, point_b) -> float:
	from math import sqrt
	delta_x = point_a[0] - point_b[0]
	delta_y = point_a[1] - point_b[1]
	return sqrt(delta_x**2+delta_y**2)


def geometrical_check(weibo_info, max_range: float, center=[39.909604, 116.397228]):
	"""
	对微博数据进行地理空间的情绪分析，默认以天安门为中心点。
	并将结果使用饼图输出。

	:param weibo_info: 微博数据（全部数据）
	:param max_range: 容许的最大距离（经纬度标记）
	:param center: 中心点（默认为天安门广场）
	:return: 范围内，各个情绪的频数
	"""
	emo_list = ["Anger", "Fear", "Joy", "Sadness", "Disgust", "Not Emotional"]
	emo_dict = dict().fromkeys(emo_list, 0)
	for line in weibo_info:
		axis_info = line[0]
		if type(axis_info[0]) != type(1.0):
			continue
		# 排除格式不正确的数据（在后台检查变量中有发现）
		distance = culc_distance(axis_info, center)
		if distance > max_range:
			continue
		emo_dict[line[2]] += 1

	plt.figure(figsize=(10,10))
	plt.pie(
		x=emo_dict.values(),
		explode=(0,0,0,0,0,0),
		labels=emo_list,
		colors=['red', 'blue', 'pink', 'green', 'yellow', 'gray'],
		autopct="%3.2f%%",
		shadow=False,
		startangle=90,
		pctdistance=1
	)
	plt.axis("equal")
	plt.savefig("geopie_{}.png".format(max_range))

	return emo_dict


def mapping_check(weibo_info: list):
	"""
	调用pyecharts中geo模块的北京地图，利用位置信息在地图数据上标注各种情绪的发送点。

	:param weibo_info:微博信息（包含位置信息）
	:return: 标注完毕的北京略图（以.html文件的格式直接输出）
	"""
	i = 0
	g = Geo().add_schema(maptype="北京")
	for line in weibo_info:
		if type(line[0][0]) != type(1.0):
			continue
		i += 1
		g.add_coordinate(
			name='',
			longitude=line[0][1],
			latitude=line[0][0]
		)
		g.add(
			series_name=line[2],
			data_pair=[('',line[2])],
			symbol_size=5
		)
		g.set_series_opts(label_opts=options.LabelOpts(is_show=False))
		if i == 10000: break
	g.set_global_opts(title_opts=options.TitleOpts(title="地图情绪标记"))
	g.render("mapping.html")


def plotting_by_timedata(time_check_data: dict, *, emotion, freq, mode: str):
	"""
	将时间分析的结果可视化输出到文件，可以指定图形。

	:param time_check_data: 时间分析情绪的结果
	:param emotion: 分析的情绪，用于制图表题目
	:param freq: 分析的时间维度，用于制图表题目
	:param mode: 图表类型
	:return: 完成图表（输出到文件）
	"""
	x_axis = list(time_check_data.keys())
	y_axis = list(time_check_data.values())
	plt.figure(figsize=(15,10))
	plt.xlabel("Time")
	plt.ylabel("Number")
	plt.title("{0} by {1}".format(emotion, freq))
	if mode.lower() == 'p':
		plt.plot(x_axis, y_axis, color='red', lw=1, ls='-', marker='.',alpha=0.5)
	elif mode.lower() =='b':
		plt.bar(x_axis, y_axis, color='red')
	for i in range(len(y_axis)):
		plt.text(x_axis[i], y_axis[i]+0.5, y_axis[i], va='center')
	plt.savefig('{0}_{1}_putout_{2}.png'.format(emotion,freq,mode))
	return


def main():
	stop_word_list = get_wordlist(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 2\stopwords_list.txt"
	)
	anger_emo = get_wordlist(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 3\emotion_lexicon\anger.txt"
	)
	disgust_emo = get_wordlist(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 3\emotion_lexicon\disgust.txt"
	)
	fear_emo = get_wordlist(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 3\emotion_lexicon\fear.txt"
	)
	joy_emo = get_wordlist(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 3\emotion_lexicon\joy.txt"
	)
	sadness_emo = get_wordlist(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 3\emotion_lexicon\sadness.txt"
	)
	emo_set = list((anger_emo, disgust_emo, fear_emo, joy_emo, sadness_emo))
	print("Wordlist load complete")

	weibo_data = get_weibo(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 3\weibo.txt",
		stop_word_list
	)
	print("Weibo data load complete")

	weibo_data_after_test = emotion_test(emo_set)(weibo_data)
	print("Emotion analysis complete")
	'''
	tc_1 = time_check(weibo_data_after_test, "Joy", mode='h')
	print(tc_1)
	plotting_by_timedata(tc_1, emotion="Joy", freq='h', mode='p')
	plotting_by_timedata(tc_1, emotion="Joy", freq='h', mode='b')

	tc_2 = time_check(weibo_data_after_test, "Sadness", mode='W')
	print(tc_2)
	plotting_by_timedata(tc_2, emotion="Sadness", freq='w', mode='p')
	plotting_by_timedata(tc_2, emotion="Sadness", freq='w', mode='b')

	tc_3 = time_check(weibo_data_after_test, "Anger", mode='m')
	print(tc_3)
	plotting_by_timedata(tc_3, emotion="Anger", freq='m', mode='p')
	plotting_by_timedata(tc_3, emotion="Anger", freq='m', mode='b')

	print(geometrical_check(weibo_data_after_test, max_range=0.1))
	print(geometrical_check(weibo_data_after_test, max_range=0.5))
	'''
	mapping_check(weibo_data_after_test)


if __name__ == "__main__":
	main()
