from PIL import Image
from os import listdir
import numpy as np


def get_images_from_directory(path):
	img_paths = listdir(path)
	res = []
	for img_name in img_paths:
		res.append(Image.open(path + "/" + img_name))
	return res


def get_str_to_print(img1, img2):
	str1 = img1.filename.split("/")
	str2 = img2.filename.split("/")
	return str1[len(str1) - 1] + " " + str2[len(str2) - 1]


def check_duplicates(arr: list, s: str):
	for i in arr:
		img1 = i.split(" ")[0]
		img2 = i.split(" ")[1]
		if s.find(img1) >= 0 and s.find(img2) >= 0:
			return False
	return True


def print_arr(arr: list):
	for i in arr:
		print(i)


def resize_images(imgs: list):
	res = []
	for img in imgs:
		img1 = img.resize((500, 500)).convert("L")
		img1.filename = img.filename
		res.append(img1)
	return res


def mse(img1, img2):
	img1_array = np.asarray(img1.getdata())
	img2_array = np.asarray(img2.getdata())
	err = np.sum((img1_array.astype("float") - img2_array.astype("float")) ** 2)
	err /= float(img1_array.size)
	return err


def mse_method(imgs: list):
	result = []
	for img1 in imgs:
		for img2 in imgs:
			if img1.filename == img2.filename: continue
			err = mse(img1, img2)
			if err < 1000:
				print_str = get_str_to_print(img1, img2)
				if check_duplicates(result, print_str):
					result.append(print_str)
	print_arr(result)


dir_name = "dev_dataset"
images = get_images_from_directory(dir_name)
images = resize_images(images)
mse_method(images)
