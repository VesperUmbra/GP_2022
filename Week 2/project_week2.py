import jieba
from wordcloud import WordCloud
import random
from _tkinter import _flatten
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def getstoplist() -> set:
	"""
	从文件中读取并构建停用词表
	:return:停用词表（集合类型）
	"""
	stopdata = open(
		"D:/buaa_czw/2022 Autumn/General Programming 2022/Week 2/stopwords_list.txt",
		"r",
		encoding="utf-8"
	).readlines()
	stoplist = set()
	for line in stopdata:
		line = line.replace("\n", "")
		jieba.add_word(line)
		# 停用词表加入自定义词典中保证正确过滤停用词和统计词频
		stoplist.add(line)
	return stoplist


def getcsv() -> list:
	"""
	读取并返回csv文件中的第一列
	:return: 读取后的csv文件中的第一列
	"""
	csv = open(
		"D:/buaa_czw/2022 Autumn/General Programming 2022/Week 2/danmuku.csv",
		"r",
		encoding="utf-8"
	)
	datals = list()
	for line in csv:
		line = line.replace("\n", "")
		datals.append(line.split(",")[0])
	datals.pop(0)
	return datals


def wordcount(text, stoplist, counts: dict):
	"""
	统计词频。过滤停用词表中的词汇与仅占一个字符的词语
	:param text: 待统计的文本（分词完毕）
	:param stoplist: 停用词表
	:param counts: 统计词频的字典
	:return:
	"""
	for word in text:
		if (word in stoplist) or (len(word) == 1):
			continue
		else:
			counts[word] = counts.get(word, 0) + 1


def sortcount(counts: dict) -> list:
	"""
	对统计出的词频结果进行排序
	:param counts: 统计词频结果
	:return:排序后的词频统计（元组列表）
	"""
	items = list(counts.items())
	items.sort(key=lambda x: x[1], reverse=True)
	return items


def featurecheck(itemlist: list, entrancelimit: int) -> dict:
	"""
	筛选特征词汇。
	:param itemlist: 待筛选的词语与频数的列表（字典也可以，不过还是列表吧，这样跳出比较快一些）
	:param entrancelimit:准入频数作为参数输入.
	:return: 筛选出的特征词及其频数组成的字典
	"""
	feaword = dict()
	for item in itemlist:
		if item[1] >= entrancelimit:
			feaword[item[0]] = item[1]
		else:
			break
		"""
		有序的词频列表限定的快速跳出，
		因为从多到少筛选的话一旦不符合准入，
		其之下的所有元素都不可能再符合准入。
		"""
	return feaword


def vacttext(text, feature, featurenum) -> list:
	"""
	对一行分词完毕的文本进行特征词向量化。
	:param text: 分词完毕的文本
	:param feature: 特征词表
	:param featurenum: 特征词数
	:return: 文本对应的特征词向量
	"""
	vec = list()
	for i in range(featurenum):
		if feature[i] in text:
			vec.append(1)
		else:
			vec.append(0)
	return vec


def culc_euc_distance(vec_a, vec_b) -> float:
	from math import sqrt, pow
	temp = 0.0
	for i in range(len(vec_a)):
		temp += pow((vec_b[i]-vec_a[i]), 2)
	return sqrt(temp)


def makewordcloud(txt, stoplist):
	wc = WordCloud(
		font_path="c/windows/fonts/simkai.ttf",
		width=1920,
		height=1080,
		background_color='white',
		stopwords=stoplist,
		max_words=50,
		collocations=False
	)
	wc.generate(txt)
	wc.to_file("wc.png")


def culidf(tf: dict, text: list) -> dict:
	from math import log
	word_idf = dict()
	word_doc = dict()
	for line in text:
		for word in tf.keys():
			if word in line:
				word_doc[word] = word_doc.get(word, 0) + 1
	for i in tf.keys():
		word_idf[i] = log(len(text)/(word_doc[i]+1))
	return word_idf


def cultfidf(tf: dict, idf: dict) -> dict:
	word_tf_idf = dict()
	for item in tf.keys():
		word_tf_idf[item] = tf[item]*idf[item]
	return word_tf_idf


def w2vtest(txt: str):
	"""
	进行Word2Vec模型训练，并输出测试结果。
	:param txt:分词完毕的文本
	:return:两个Word2Vec文件，一个不可阅读但可再训练，一个可阅读但不可再训练
	"""
	data = open(txt, "rb")
	model = Word2Vec(LineSentence(data), sg=1, window=10, min_count=5, workers=10, sample=1e-3)
	model.save("danmukuw2vtest.Word2Vec")
	model.wv.save_word2vec_format("danmukuw2vtext2.txt", binary=False)


def main():
	stopwordlist = getstoplist()
	metadata = getcsv()
	basicdata = list()
	# ttxt = open("ttxt.txt", "w", encoding="utf-8")
	for item in metadata:
		if len(item) < 5:
			continue  # 过滤过短弹幕
		line = jieba.lcut(item)
		basicdata.append(line)
		# ttxt.writelines(" ".join(line))
		# ttxt.write("\n")
	# ttxt.close()

	for i in range(10):
		print(basicdata[i])
		print(basicdata[-1-i])
	# 显示部分分词结果
	wordcounts = dict()
	for line in basicdata:
		wordcount(line, stopwordlist, wordcounts)
	# 词频统计
	
	sortedcount = sortcount(wordcounts)
	for i in range(15):
		word, count = sortedcount[i]
		print("{0:<10}{1:>6}".format(word, count))
	# 打印排序前十五的词语
	for i in range(15, -1, -1):
		word, count = sortedcount[-1000-i]
		print("{0:<10}{1:>6}".format(word, count))
	# 打印排序1015~1000位的词语
	
	featureworddict = featurecheck(sortedcount, 6000)
	featurewordlist = list(featureworddict.keys())
	print(featurewordlist)
	featurenum = len(featurewordlist)
	# 筛选特征词表（保留具体词频数据）并计算特征词数量
	
	vectorlist = list()
	for item in basicdata:
		vector = vacttext(item, featurewordlist, featurenum)
		vectorlist.append(vector)
	# 弹幕的向量化
	a, b = random.sample(range(len(vectorlist)), 2)
	# 任意抽取两行
	print(basicdata[a])
	print(basicdata[b])
	print(vectorlist[a])
	print(vectorlist[b])
	dis = culc_euc_distance(vectorlist[a], vectorlist[b])
	print(dis)
	# 计算并输出两条弹幕象征的向量的欧氏距离
	
	txt_for_wc = ' '.join(list(_flatten(basicdata)))  # 制作词云文本
	makewordcloud(txt_for_wc, stopwordlist)
	# 输出词云
	
	wordidfcount = culidf(wordcounts, metadata)
	wordtfidfcount = cultfidf(wordcounts, wordidfcount)
	tfidflist = sortcount(wordtfidfcount)
	tfidf_featurelist = featurecheck(tfidflist, 30000)
	tfidf_feautreword = tfidf_featurelist.keys()
	print(tfidf_feautreword)


if __name__ == "__main__":
	w2vtest("ttxt.txt")
	main()
