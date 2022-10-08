from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import os
from glob import glob


# 基类的实现
class FilterGP:
	def __init__(self, image_data: Image.Image, image_param):
		self._image_data = image_data
		self._image_param = image_param

	def filter(self):
		pass


# 子类：边缘提取
class EdgeFilterGP(FilterGP):
	def __init__(self, image_data, image_param):
		super().__init__(image_data, image_param)

	def filter(self):
		return self._image_data.filter(ImageFilter.FIND_EDGES)


# 子类：锐化
class SharpenFilterGP(FilterGP):
	def __init__(self, image_data, image_param):
		super().__init__(image_data, image_param)

	def filter(self):
		return self._image_data.filter(ImageFilter.SHARPEN)


# 子类：模糊
class BlurFilterGP(FilterGP):
	def __init__(self, image_data, image_param):
		super().__init__(image_data, image_param)

	def filter(self):
		return self._image_data.filter(ImageFilter.BLUR)


# 子类：大小调整
class ResizeFilterGP(FilterGP):
	def __init__(self, image_data, image_param):
		super().__init__(image_data, image_param)

	def filter(self):
		return self._image_data.resize((self._image_param[0], self._image_param[1]))


# 图片批处理类
class ImageShopGP:
	def __init__(self, image_type: str, image_path: str):
		self._type = image_type
		self._path = image_path
		self._lis = list()
		self._process_lis = list()

	def load_images(self):
		self._lis = glob(os.path.join(self._path, '*.'+self._type))

	def __batch_ps(self, Filter_obj):
		return Filter_obj.filter()

	def batch_ps(self, process_type: tuple, *args: [tuple]):
		self.load_images()
		for item in self._lis:
			self._process_lis.append(Image.open(item, mode='r'))

		if process_type[0] == 'Edge':
			for item in range(len(self._process_lis)):
				e = EdgeFilterGP(self._process_lis[item], process_type[1])
				self._process_lis[item] = self.__batch_ps(e)
		elif process_type[0] == 'Sharpen':
			for item in range(len(self._process_lis)):
				s = SharpenFilterGP(self._process_lis[item], process_type[1])
				self._process_lis[item] = self.__batch_ps(s)
		elif process_type[0] == 'Blur':
			for item in range(len(self._process_lis)):
				b = BlurFilterGP(self._process_lis[item], process_type[1])
				self._process_lis[item] = self.__batch_ps(b)
		elif process_type[0] == 'Resize':
			for item in range(len(self._process_lis)):
				r = ResizeFilterGP(self._process_lis[item], process_type[1])
				self._process_lis[item] = self.__batch_ps(r)

		if len(args) > 0:
			for arg in args:
				if arg[0] == 'Edge':
					for item in range(len(self._process_lis)):
						e = EdgeFilterGP(self._process_lis[item], arg[1])
						self._process_lis[item] = self.__batch_ps(e)
				elif arg[0] == 'Sharpen':
					for item in range(len(self._process_lis)):
						s = SharpenFilterGP(self._process_lis[item], arg[1])
						self._process_lis[item] = self.__batch_ps(s)
				elif arg[0] == 'Blur':
					for item in range(len(self._process_lis)):
						b = BlurFilterGP(self._process_lis[item], arg[1])
						self._process_lis[item] = self.__batch_ps(b)
				elif arg[0] == 'Resize':
					for item in range(len(self._process_lis)):
						r = ResizeFilterGP(self._process_lis[item], arg[1])
						self._process_lis[item] = self.__batch_ps(r)

	def display(self, row=3, column=3, max_images=81):
		if len(self._process_lis) > max_images:
			display_lis = self._process_lis[:max_images]
		else:
			display_lis = self._process_lis
		size = row*column
		for i in range(0, len(display_lis), size):
			plt.figure(figsize=(10, 10))
			for pos in range(1, size+1):
				if i+pos-1 < len(display_lis):
					image_data = display_lis[i+pos-1]
					plt.subplot(row, column, pos)
					plt.imshow(image_data)
				else:
					continue
			plt.savefig(f"display_{i}_{i+size}.png")

	def save(self, save_path):
		for image in self._process_lis:
			index = self._process_lis.index(image)
			image.save(save_path+f"_{index+1}."+self._type)


class TestImageShopGP(ImageShopGP):
	def __init__(self, t7pe, path):
		super().__init__(t7pe, path)

	def batch(self, proc: tuple, *args: [tuple]):
		super().batch_ps(proc, *args)

	def save(self, save_path):
		super().save(save_path)

	def display(self):
		super().display()


def main():
	image_path = r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 6\model_imgs'
	image_type = r'jpg'
	save_path = r'D:\buaa_czw\2022 Autumn\General Programming 2022\Week 6\output_imgs\\'
	proc_type = input("输入操作类型(Edge/Sharpen/Blur/Resize):")
	param = None
	if proc_type == 'Resize':
		param = eval(input("输入重组的尺寸(元组)"))

	test = TestImageShopGP(image_type, image_path)
	test.batch((proc_type, param))
	test.display()
	test.save(save_path)


if __name__ == '__main__':
	main()
