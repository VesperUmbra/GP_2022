import functools
import os
from tqdm import tqdm
from memory_profiler import profile
from line_profiler import LineProfiler
import pysnooper
import pickle
from random import random
import pygame
import time


def path_check(path):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if os.path.exists(path):
				print("存在该路径，正常访问...", end='\n')
			else:
				print("不存在该路径，尝试创建...", end='\n')
				os.mkdir(path)
			return func(*args, **kwargs)
		return wrapper
	return decorator


def pathcheck_main():
	path1 = r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8'
	path2 = r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\path_test'

	@path_check(path1)
	def printf(str_):
		print(str_)
	printf(path1)

	@path_check(path2)
	def printf(str_):
		print(str_)
	printf(path2)


class MusicNotice:
	def __init__(self, func):
		self._func = func
		self._bgmdict = {
			1: '01 名もなき悪夢の果て -Short ver.-.mp3',
			2: '02 死と戯れの領域.mp3',
			3: '03 Tharbad Night.mp3',
			4: '04 曇り空の向こう側.mp3',
			5: '05 Unmitigated Evil.mp3',
			6: '06 Rise of the GRENDEL.mp3',
			7: '07 ようこそモンマルトへ.mp3',
			8: '08 黎き狭間の中で.mp3'
		}
		self._typelist = [
			float, int, tuple, list, dict, str, complex, set
		]

	def __call__(self, *args, **kwargs):
		return_value = self._func(*args, **kwargs)
		if len(return_value) == 1:
			check_value = list(return_value)
		else:
			check_value = return_value
		for item in check_value:
			for type_name in self._typelist:
				if isinstance(item, type_name):
					bgm_name = self._bgmdict[self._typelist.index(type_name) + 1]
					pygame.init()
					pygame.mixer.init()
					pygame.mixer.music.load(
						rf"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\BGM_set\{bgm_name}"
					)
					pygame.mixer.music.set_volume(0.1)
					pygame.mixer.music.play()
					time.sleep(10)
					pygame.mixer.music.stop()
					pygame.mixer.music.unload()
					break
		return return_value


def musicnotice_main():
	@MusicNotice
	def nothing_process():
		return 0.1, 1, (2, 3), [4], {5: 6}, '7', 8j, {9, 10}
		# 返回多个不同类型的值
	print(nothing_process())


class Logging:
	def __init__(self, logfile):
		self._logfile = logfile

	def __call__(self, func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			info = 'Process: Calling ' + func.__name__
			with open(self._logfile, 'a') as file:
				file.write(info + '\n')
			return func(*args, **kwargs)
		return wrapper


def logging_main():
	@Logging(r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\path_test\test.log')
	def what_happen(a_int):
		print(a_int)
	for i in range(50):
		what_happen(i)


class Processing:
	def __init__(self):
		self._list = list()

	@pysnooper.snoop(r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\path_test\process_log.log")
	@profile
	def simulator_makehugelist(self):
		for i in tqdm(range(300000)):
			self._list.append(random())

	def simulator_travelhugelist(self):
		for i in tqdm(self._list):
			pass

	@pysnooper.snoop(r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\path_test\process_log.log")
	def simulator_savehugelist(
			self,
			path=r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\path_test\process_test.txt'
	):
		with open(path, 'wb') as file:
			pickle.dump(self._list, file, 0)


@pysnooper.snoop(r"D:\buaa_czw\2022 Autumn\General Programming 2022\Week 8\path_test\process_log.log")
def processing_main():
	p = Processing()
	p.simulator_makehugelist()

	lp = LineProfiler()
	lp_wrapper = lp(p.simulator_travelhugelist)
	lp_wrapper()
	lp.print_stats()

	p.simulator_savehugelist()


if __name__ == "__main__":
	pathcheck_main()
	musicnotice_main()
	logging_main()
	processing_main()
