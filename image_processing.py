import re

import cv2
import numpy as np
import pandas as pd
import pytesseract
import requests

from utils import d_print


def tesseract_image(image_path, tes_config='', timeout=2):
    '''
    Scans image of check for text

    :param image_path: path to image to process
    :param tes_config: tesseract config string (raw)
    :param timeout: tesseract's timeout

    :return: raw canvans of scanned text, or None if Timeout Error
    '''

    img_cv = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

    try:
        work_string = pytesseract.image_to_string(img_rgb, lang='rus', config=tes_config, timeout=timeout)
        return work_string

    except RuntimeError as timeout_error:
        print('Timeout Error; Tesseract cannot process image')


class CheckParser:
    '''
    Parses raw text, tries to find products and their prices, using available patterns;
    If the price wasn't found, it returns 0.0 instead;
    If debug=True, all products and prices will be shown;
    '''

    def __init__(self, debug=False):
        # Define regular expressions
        self.clean_re = re.compile(r"[^А-Я0-9 .]+", re.IGNORECASE)
        self.product_select_re = re.compile(r'^[А-Я .]{8,25}(?= [0-9])', re.IGNORECASE | re.MULTILINE)
        self.price_select_re = re.compile(r'\d{1,2}\.\d{1,2}( )?$', re.MULTILINE)

        self.debug = debug

    def parse_pattern1(self, lines):
        last_was_product = False

        # Output lists
        products = []
        prices = []

        for line in lines:

            line = re.sub(self.clean_re, '', line)

            if last_was_product:
                price = re.search(self.price_select_re, line)
                last_was_product = False

                if price is not None:
                    price = price.group().replace(' ', '')
                else:
                    price = '0.0'
                prices.append(price)
                d_print(f'Price: {price}', self.debug)  # Debug print
                d_print('', self.debug)  # Debug print

            else:
                product = re.search(self.product_select_re, line)

                if product is not None:
                    last_was_product = True
                    product = product.group()
                    products.append(product)
                    d_print(product, self.debug)  # Debug print
                else:
                    last_was_product = False

        return products, prices

    def parse_pattern2(self, lines):
        self.product_select_re = re.compile(r'(?<=[0-9] )[А-Я .]{8,35}', re.IGNORECASE | re.MULTILINE)
        self.price_select_re = re.compile(r'\d{1,2}\. ?\d{1,2}(?= |$)', re.MULTILINE)
        return self.parse_pattern1(lines)

    def parse(self, check_string):
        # Split canvas into lines
        lines = check_string.split('\n')

        # TODO - handle unsuccessful seacrh
        parse_results = []
        parse_metric = []
        patterns = [self.parse_pattern1, self.parse_pattern2]

        for pattern in patterns:
            products, prices = pattern(lines)
            parse_results.append((products, prices))

            # Metric = number_of_products * 1/number_of_zeros
            zeros_num = sum(np.array(prices, dtype=float) == 0)
            parse_metric.append(len(prices) * 1 / (zeros_num + 1))

        best_result_idx = np.array(parse_metric).argmax()
        products, prices = parse_results[best_result_idx]
        d_print(f'Selected pattern: {best_result_idx + 1}', self.debug)  # Debug print

        return products, prices


class CrankShaft:
    # TODO - create doc string
    '''

    '''

    def __init__(self, debug=False):
        self.api_url = "https://receiptnlp.tinkoff.ru/api/fns"
        self.data = {
            "user": "магазин",
            "userInn": "777123456",
            "retailPlaceAddress": "Москва, Головинское шоссе, 5А",
            "kktRegId": "1234567",
            "fiscalDocumentNumber": 13124,
            "fiscalSign": 13124,
            "totalSum": 421421,
            "dateTime": "01.01.1970 21:00",
        }
        self.debug = debug

    def __call__(self, products, prices):
        # Adding scanned products name into json
        items = []
        for product in products:
            items.append({"name": product})
        self.data['items'] = items

        # sending post request and saving response as response object
        response = requests.post(self.api_url, json=self.data)

        # TODO - handle status code not 200
        d_print(f'Status code: {response.status_code}', self.debug)  # Debug print
        response = response.json()

        # Creating DataFrame with results
        df = pd.DataFrame()
        full_names = []
        categories = []
        categories_id = []

        for item in response['result']['items']:
            full_names.append(item['look'])
            categories.append(item['category'])
            categories_id.append(item['category_id'])

        df['scanned_name'] = pd.Series(products)
        df['full_name'] = pd.Series(full_names)
        df['category'] = pd.Series(categories)
        df['category_id'] = pd.Series(categories_id)
        df['price'] = pd.Series(prices)

        # Drop trash
        df.drop(index=df[(df['category_id'] == 9900) & (df['price'] == '0.0')].index, inplace=True)

        return df
