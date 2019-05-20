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
		img1 = img.resize((500, 500))
		img1.filename = img.filename
		res.append(img1)
	return res


def avg(img):
	return np.mean(np.asarray(img.getdata()))


def var(img, average):
	img_np = np.asarray(img.getdata())
	res = 0
	for pixel in img_np:
		r = pixel[0]
		g = pixel[1]
		b = pixel[2]
		res += pow(abs(1 * r - average), 2)
		res += pow(abs(1 * g - average), 2)
		res += pow(abs(1 * b - average), 2)
	return res


def cov(img1, img2, avg1, avg2):
	img1_np = np.asarray(img1.getdata())
	img2_np = np.asarray(img2.getdata())
	result = 0
	for i in range(img1.width * img1.height):
		r1 = img1_np[i][0]
		g1 = img1_np[i][1]
		b1 = img1_np[i][2]

		r2 = img2_np[i][0]
		g2 = img2_np[i][1]
		b2 = img2_np[i][2]

		result += (b1-avg1) * (b2-avg2) + (g1-avg1) * (g2-avg2) + (r1-avg2) * (r2-avg2) ##migth be not "r1-avg2", but "r1-avg1"

	return result


def ssim(img1, img2):
	l = pow(2, 24) - 1
	k1 = 0.01
	k2 = 0.03
	u1 = avg(img1)
	u2 = avg(img2)
	o1 = var(img1, u1)
	o2 = var(img2, u2)
	images_cov = cov(img1, img2, u1, u2)
	c1 = l * k1
	c2 = l * k2
	ssim_numerator = (2 * u1 * u2 + c1) * (2 * images_cov + c2)
	ssim_denominator = ((u1 * u1) + (u2 * u2) + c1) * (o1 + o2 + c2)
	return ssim_numerator / ssim_denominator

#6 - 0.65 4-0.44
#TODO: check cov difference
#TODO: check if there are any images with similarity > 0.44, which are not actualy similar
def ssim_method(imgs):
	result = []
	for img1 in imgs:
		for img2 in imgs:
			if img1.filename == img2.filename: continue
			err = ssim(img1, img2)
			if err > 0.85:
				print_str = get_str_to_print(img1, img2)
				if check_duplicates(result, print_str):
					result.append(print_str)
	print_arr(result)

dir_name = "dev_dataset"
images = get_images_from_directory(dir_name)
images = resize_images(images)
ssim_method(images)

