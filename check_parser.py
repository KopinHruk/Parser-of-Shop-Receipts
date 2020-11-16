from image_processing.image_processing import tesseract_image, CheckParser, CrankShaft


# TODO rebuild parse_check_image function
def parse_check_image(image_path):
    """

    Parameters
    ----------
    image_path : str
        Path to image to process

    Returns
    -------
    ParsedProductsList()
        Data Object that contains products and their attributes
    """

    work_string = tesseract_image(image_path)

    raw_parser_object = CheckParser(debug=False)
    products, prices = raw_parser_object.parse(work_string)

    # TODO handle errors
    # assert len(prices) == len(products)

    distiller_object = CrankShaft()
    data_class = distiller_object(products, prices)

    return data_class
