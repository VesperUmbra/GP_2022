import StandardFileProcessGP as Sfp
import jieba
import matplotlib.pyplot as plt
import seaborn as sbn
# import re


class TokenizerGP:
	def __init__(self, text, coding='c', PAD=0):
		self._coding = coding
		self._PAD = PAD
		temp_dict = dict()
		temp_dict['PAD'] = self._PAD
		i = 1
		if coding == 'c':
			temp_text = list(text)
		elif coding == 'w':
			temp_text = jieba.lcut(text)
		for elem in temp_text:
			temp_dict[elem] = i
			i += 1
		self._char_dict = temp_dict

	def tokenize(self, line_text) -> list:
		if self._coding == 'c':
			text = list(line_text)
		elif self._coding == 'w':
			text = jieba.lcut(line_text)
		return text

	def encode(self, list_text) -> list:
		token = list()
		for element in list_text:
			token.append(self._char_dict[element])
		return token

	def trim(self, list_token: list, seq_len: int) -> list:
		length = len(list_token)
		if length < seq_len:
			for i in range(seq_len - length):
				list_token.append(0)
		else:
			list_token = list_token[:seq_len]
		return list_token

	def decode(self, token_list: list) -> str:
		sentence_list = list()
		for elem in token_list:
			for k, v in self._char_dict.items():
				if elem == v:
					sentence_list.append(k)
		return ''.join(sentence_list)

	def encode_all(self, seq_len, seq_data):
		if self._coding == 'c':
			for seq in seq_data:
				print(seq)
				token = self.encode(seq)
				print(token)
				print(self.trim(token, seq_len))
				print(self.decode(self.trim(token, seq_len)))
		elif self._coding == 'w':
			for seq in seq_data:
				seq_cut = Sfp.word_cut_list(seq)
				print(seq_cut)
				token = self.encode(seq_cut)
				print(token)
				print(self.trim(token, seq_len))
				print(self.decode(self.trim(token, seq_len)))


def main():
	"""
	metadata = Sfp.get_text_file(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 5\final_none_duplicate.txt",
		split_flag="\t",
		head_exist=False
	)
	text_data = list()
	for line in metadata:
		line_text = line[1]
		line_text = re.sub(r"http[:.]+\S+", "", line_text)
		# 排除微博文本中的url
		text_data.append(line_text)
	Sfp.output_in_file("weibotext_processed.txt", text_data)
	"""
	# 以上是仅提取了数据集内正文内容并“顺便”排除掉url的预处理代码
	text_data = Sfp.get_text_file(
		r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 5\weibotext_processed.txt",
		split_flag='',
		head_exist=False
	)
	print(text_data[0])
	total_text = ''.join(text_data)
	code_mode = input("输入编码模式(c/w)：").lower()
	while code_mode not in 'cw':
		code_mode = input("错误：输入不合法。\n请重新输入编码模式(c/w)：").lower()
	t = TokenizerGP(total_text, coding=code_mode)
	test_text = text_data[0]
	char_list_test = t.tokenize(test_text)
	print(char_list_test)
	token_test = t.encode(char_list_test)
	print(token_test)

	if code_mode == 'c':
		seq_len = round(len(total_text)/len(text_data))
	elif code_mode == 'w':
		seq_len = round(len(Sfp.word_cut_list(total_text))/len(text_data))
	seq_len = int(seq_len)
	print("seq_len = {}".format(seq_len))

	token_test = t.trim(token_test, seq_len)
	print(token_test)
	print(t.decode(token_test))

	# 以下是分析句长分布的代码
	c_length = []
	w_length = []
	for line in text_data:
		c_length.append(len(line))
		w_length.append(len(jieba.lcut(line)))
	plt.subplot(121)
	sbn.boxplot(c_length)
	plt.title("句长（按字）")
	plt.subplot(122)
	sbn.boxplot(w_length)
	plt.title("句长（按词，jieba分词基准）")
	plt.savefig('句长统计.png')

	t.encode_all(seq_len, text_data)


if __name__ == "__main__":
	main()
