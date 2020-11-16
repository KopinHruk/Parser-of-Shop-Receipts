from image_processing import tesseract_image, CheckParser, CrankShaft


def parse_check_image(image_path):
    work_string = tesseract_image(image_path)

    b = CheckParser(debug=False)
    products, prices = b.parse(work_string)

    assert len(prices) == len(products)

    man = CrankShaft()
    dc = man(products, prices)

    return dc
