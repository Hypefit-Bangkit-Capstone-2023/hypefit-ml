import cv2
import os
import numpy as np
from sklearn.cluster import KMeans
import requests
import colorsys


def load_image(image_path):
  image = None

  if image_path.startswith('http'):
    response = requests.get(image_path)
    np_image = np.frombuffer(response.content, np.uint8)
    image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
  else:
    _, ext = os.path.splitext(image_path)
    if ext != '.jpg':
      raise Exception("Only jpg files are supported")
    image = cv2.imread(image_path)

  return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def resize_image(image, max_height=400):
  height, width, _ = image.shape
  if height > max_height:
    ratio = max_height / height
    image = cv2.resize(image, (int(width * ratio), max_height))
  return image


def get_dominant_colors(img_path):
  image = load_image(img_path)
  image = resize_image(image)
  pixels = image.reshape(-1, 3)

  cluster_len = 5
  k_means = KMeans(n_clusters=cluster_len, n_init=10)
  k_means.fit(pixels)

  _, pixels_color_wise = np.unique(k_means.labels_, return_counts=True)
  percentages = pixels_color_wise / pixels.shape[0]
  colors = np.asarray(k_means.cluster_centers_, dtype='uint8')

  colors_with_percentage = np.empty((cluster_len, 2), dtype=object)
  for i in range(cluster_len):
    colors_with_percentage[i] = [colors[i], percentages[i]]

  sorted_indices = np.argsort(-colors_with_percentage[:, 1])
  colors_with_percentage_sorted = colors_with_percentage[sorted_indices]

  return colors_with_percentage_sorted


def rgb_to_hsv(rgb):
  rgb = rgb / 255
  h, s, v = colorsys.rgb_to_hsv(*rgb)
  return h * 360, s * 100, v * 100
