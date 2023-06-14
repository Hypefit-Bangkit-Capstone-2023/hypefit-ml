import os

storage_base_url = os.environ.get("STORAGE_BASE_URL")


def get_image_url(key):
  return f'{storage_base_url}/{key}'
