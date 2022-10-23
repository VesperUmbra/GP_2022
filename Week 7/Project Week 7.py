import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sbn
from sklearn.decomposition import PCA


class DataCheckGP:
	def __init__(self, DataPath, Distinct):
		self._Distinct = Distinct
		df_dict = dict()
		for region in Distinct:
			region_data = pd.read_csv(DataPath+f"PRSA_Data_{region}_20130301-20170228.csv")
			region_data = pd.concat([region_data, pd.DataFrame(columns=['datetime'])], sort=False)
			for i in range(0, len(region_data)):
				line = region_data.loc[i]
				date_t = dt.datetime(
					year=int(line['year']), month=int(line['month']),
					day=int(line['day']), hour=int(line['hour'])
				)
				region_data.loc[i, 'datetime'] = date_t
				# 格式化时间变量，便于统计
			df_dict[region] = region_data
		self._Dict = df_dict

	def time_anal(self, region_to_anal, type_of_poll, start_time, end_time):
		metadata_to_anal = self._Dict[region_to_anal]
		data_to_anal = metadata_to_anal[
			(metadata_to_anal['datetime'] >= start_time) & (metadata_to_anal['datetime'] <= end_time)
		][['datetime', type_of_poll]]
		return data_to_anal

	def area_anal(self, type_of_poll, DateTime):
		total_data = pd.DataFrame(columns=['station', type_of_poll])
		for region in self._Distinct:
			region_metadata = self._Dict[region]
			region_data = region_metadata[region_metadata['datetime'] == DateTime][['station', type_of_poll]]
			total_data = pd.concat([total_data, region_data], ignore_index=True)
		return total_data

	def Dict(self):
		return self._Dict


class VisualGP:
	def __init__(self, stat_data: pd.DataFrame, *args):
		"""
		初始化，传入统计数据和必要参数
		:param stat_data: 统计数据，经过上方的类清理过的
		:param args: 统计参数
		"""
		self._stat_data = stat_data
		self._param = args

	def timedata_to_line(self):
		plt.figure(figsize=(10, 10))
		sbn.lineplot(data=self._stat_data, x='datetime', y=self._param[0])
		plt.title(f"{self._param[0]}_in_{self._param[1]}")
		plt.savefig(f"{self._param[0]}_in_{self._param[1]}.png")

	def areadata_to_pie(self):
		plt.figure(figsize=(10, 10))
		plt.pie(
			x=self._stat_data.loc[:, self._param[0]], colors=sbn.color_palette('bright'),
			labels=self._stat_data.loc[:, 'station'], autopct='%0.0f%%'
		)
		plt.title(f"{self._param[0]} in Beijing")
		plt.savefig(f"{self._param[0]} in Beijing.png")


class NotNumErrorGP(ValueError):
	def __init__(self, lineindex, region, year, month, day, hour, pollutant):
		super(NotNumErrorGP, self).__init__()
		self._lindex = lineindex
		self._region = region
		self._year = year
		self._month = month
		self._day = day
		self._hour = hour
		self._pollutant = pollutant
		self.message = f"""data {self._region} have NotNumError, \
in time {self._year}/{self._month}/{self._day} {self._hour}:00 (line {self._lindex}), \
at column {self._pollutant}."""


class AdvanceAnalGP:
	def __init__(self, DataPath, distinct):
		self._Dp = DataPath
		self._Dist = distinct
		print(f"地区{self._Dist}，数据读取中...", end='\n')
		total_dataframe = pd.read_csv(DataPath+f"PRSA_Data_{distinct}_20130301-20170228.csv")
		total_dataframe = total_dataframe.drop(columns=['No', 'year', 'month', 'day', 'hour', 'wd', 'station'])
		# 排除与主成分分析等无关的时间、编号和字符变量。
		self._Df = total_dataframe
		print("数据读取完毕", end='\n')

	def data_pca(self, division=2):
		pca = PCA(n_components=division)
		print("开始PCA分析...", end='\n')
		pca.fit(self._Df)
		print(pca.explained_variance_ratio_)
		pca_result = pd.DataFrame(data=pca.transform(self._Df), columns=['X1', 'X2'])
		print("结束PCA分析，开始绘图...", end='\n')
		plt.figure(figsize=(10, 10))
		sbn.scatterplot(x='X1', y='X2', data=pca_result)
		plt.savefig(self._Dp + f"PCA_result_{self._Dist}.jpg")
		# 查看主成分的方差占比

	def data_heatmap(self):
		plt.figure(figsize=(10, 10))
		df_corr = self._Df.corr()
		sbn.heatmap(df_corr, annot=True, cmap='Reds', vmin=-1, vmax=1, fmt='.2f')
		plt.savefig(self._Dp + f"heatmap_{self._Dist}.png")


def basicmain():
	distinct = [
		"Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
		"Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
	]
	da = DataCheckGP(
		r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 7\PRSA_Data_AfterProcess\\',
		distinct
	)
	# area_to_check = input("请输入需要统计的地区：")
	# poll_to_check = input("请输入需要统计的污染物：")
	# s_t = list(map(int, input("请输入起始时间(yyyy-mm-dd-hh)：").split('-')))
	# s_dt = dt.datetime(year=s_t[0], month=s_t[1], day=s_t[2], hour=s_t[3])
	# e_t = list(map(int, input("请输入结束时间(yyyy-mm-dd-hh)：").split('-')))
	# e_dt = dt.datetime(year=e_t[0], month=e_t[1], day=e_t[2], hour=e_t[3])
	area_to_check = 'Aotizhongxin'
	poll_to_check = 'PM10'
	s_dt = dt.datetime(2016, 1, 1, 0)
	e_dt = dt.datetime(2017, 1, 1, 0)
	atzx_PM25_timedata = da.time_anal(area_to_check, poll_to_check, s_dt, e_dt)
	atzx_PM25_visual = VisualGP(atzx_PM25_timedata, poll_to_check, area_to_check)
	atzx_PM25_visual.timedata_to_line()

	test_dt = dt.datetime(2015, 5, 1, 9)
	PM10_15519_areadata = da.area_anal('PM10', test_dt)
	PM10_15519_visual = VisualGP(PM10_15519_areadata, "PM10")
	PM10_15519_visual.areadata_to_pie()


def checkcsv():
	distinct = [
		"Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
		"Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
	]
	DataPath = r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 7\PRSA_Data_20130301-20170228\\'
	for region in distinct:
		df_to_check = pd.read_csv(DataPath+f"PRSA_Data_{region}_20130301-20170228.csv")
		for i in range(len(df_to_check)):
			line = df_to_check.loc[i]
			a = list(map(int, np.where(line.isnull())[0]))
			try:
				a[0]
				# 用于触发IndexError的钓鱼语句，触发了Error则表明无空缺值，否则存在空缺值
				year = line['year']
				month = line['month']
				day = line['day']
				hour = line['hour']
				raise NotNumErrorGP(i+1, region, year, month, day, hour, tuple(df_to_check.columns.take(a)))
			except IndexError:
				pass
			except NotNumErrorGP as nne:
				print(nne.message)
				print("自动根据整体数据填充空值...", end='\n')
				for col in list(df_to_check.columns.take(a)):
					if col == 'wd':
						value = df_to_check.loc[i-1, col]
						# 字符串类型的风向置空时，直接填充前项
					else:
						value = np.floor(df_to_check[col].mean())
						# 数值类型的数据置空时，填充整体均值
					df_to_check.loc[i, col] = value
		df_to_check.to_csv(
			r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 7\PRSA_Data_AfterProcess\\" +
			f"PRSA_Data_{region}_20130301-20170228.csv"
		)


def relation_check_main():
	distinct = [
		"Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng",
		"Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"
	]
	DataPath = r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 7\PRSA_Data_AfterProcess\\'
	for region in distinct:
		df = AdvanceAnalGP(DataPath, region)
		df.data_pca()
		df.data_heatmap()


if __name__ == '__main__':
	# checkcsv()
	basicmain()
	# relation_check_main()
