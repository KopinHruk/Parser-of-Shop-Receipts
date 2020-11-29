import os

from tqdm import tqdm

from image_processing.image_processing import tesseract_image, CheckParser
from spell_processor.spell_processor import SpellProcessor

images_dir = 'dict_fill_images/'
images = [images_dir + f for f in os.listdir(images_dir) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]

for image in tqdm(images):
    work_string = tesseract_image(image)

    raw_parser_object = CheckParser(debug=False)
    products, prices = raw_parser_object.parse(work_string)

    spell = SpellProcessor('dictionaries/ru_full.txt')
    products = spell.correct(products)