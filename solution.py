from PIL import Image
from os import listdir
import numpy as np
import sys


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


def resize_images(imgs: list):
	res = []
	for img in imgs:
		img1 = img.resize((250, 250)).convert("L")
		img1.filename = img.filename
		res.append(img1)
	return res


def avg(img):
	return np.mean(np.asarray(img.getdata()))


def var(img, average):
	img_np = np.asarray(img.getdata())
	res = 0
	for pixel in img_np:
		r = pixel
		res += pow(abs(r - average), 2)
	return res


def cov(img1, img2, avg1, avg2):
	img1_np = np.asarray(img1.getdata())
	img2_np = np.asarray(img2.getdata())
	result = 0
	for i in range(img1.width * img1.height):
		r1 = img1_np[i]
		r2 = img2_np[i]
		result += (r1-avg1) * (r2-avg2)
	return result


def ssim(img1, img2):
	l_coef = 255
	k1 = 0.01
	k2 = 0.03
	u1 = avg(img1)
	u2 = avg(img2)
	o1 = var(img1, u1)
	o2 = var(img2, u2)
	images_cov = cov(img1, img2, u1, u2)
	c1 = l_coef * k1
	c2 = l_coef * k2
	ssim_numerator = (2 * u1 * u2 + c1) * (2 * images_cov + c2)
	ssim_denominator = ((u1 * u1) + (u2 * u2) + c1) * (o1 + o2 + c2)
	return ssim_numerator / ssim_denominator


def ssim_method(imgs):
	result = []
	for i in range(len(imgs)):
		img1 = imgs[i]
		for j in range(i + 1, len(imgs)):
			img2 = imgs[j]
			err = ssim(img1, img2)
			if err > 0.43:
				print_str = get_str_to_print(img1, img2)
				if check_duplicates(result, print_str):
					result.append(print_str)
					print(print_str)


dir_name = sys.argv[2]
images = get_images_from_directory(dir_name)
images = resize_images(images)
ssim_method(images)
