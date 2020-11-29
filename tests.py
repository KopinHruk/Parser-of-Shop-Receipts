import os
from tqdm import tqdm
from check_parser import parse_check_image

images_dir = 'dict_fill_images/'
images = [images_dir + f for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]

for image in tqdm(images):
    b = parse_check_image(image, 1)