"""
该文件存储2022年秋季，现代程序设计技术课程中，
作业使用的通用文件处理函数，以备后续复用。
封装jieba库。
made by CZW(Rui Xue).
Version 1: 21 Sep. 2022.
"""
import jieba
import pandas


def get_word_set(txt_name: str) -> set:
	"""
	从指定的词表文件中获取单词并组合为set。

	:param txt_name: 待获取单词的词表文件目录
	:return: 组合完毕的set
	"""
	file = open(
		txt_name,
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


def get_text_file(file_name: str, split_flag: str, head_exist: bool) -> list:
	"""
	标准化读取文件，并根据指定的分隔符划分文件各行的信息，最终统合为列表输出。
	文件内容的后续处理留待具体作业内容具体设定。

	:param file_name:待读取的文件路径（完整）。
	:param split_flag:文件行内数据的分隔符。
	:param head_exist:标记是否存在文件头
	:return: 统合完毕的文件列表。
	"""
	file = open(
		file_name,
		"r",
		encoding="utf-8"
	)
	file_data = file.readlines()
	if head_exist:
		file_data = file_data[1:]
	file_out = list()
	for line in file_data:
		line = line.replace("\n", "")
		if split_flag != '':
			line = list(line.split(split_flag))
		file_out.append(line)
	file.close()
	return file_out


def word_cut_list(text: str) -> list:
	"""
	对文本进行分词，输出分词结果。
	分词结果的后续处理留待具体项目具体应用。

	:param text: 待分词文本 （字符串）
	:return: 分词结果（列表形式）
	"""
	return jieba.lcut(text)


def output_in_file(filename: str, file_data):
	file = open(
		filename,
		"w",
		encoding='utf-8'
	)
	for item in file_data:
		file.write(item)
		file.write("\n")
	file.close()


def csv_to_number_list(csv_file: str) -> list:
	csv_data = pandas.read_csv(
		csv_file
	)
	file_list = list()
	for i in range(len(csv_data)):
		line = csv_data.loc[i]
		file_list.append([line[0], line[1]])
	return file_list
