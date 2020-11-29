from image_processing.image_processing import tesseract_image, CheckParser, CrankShaft


# TODO rebuild parse_check_image function
from spell_processor.spell_processor import SpellProcessor


def parse_check_image(image_path, correction=1):
    """

    Parameters
    ----------
    correction : int
        0 - correction is off, very fast, many mistakes in names;
        1 - normal correction, slower, few errors;
        2 - correction with big dictionary, error rate is the same, as in normal mode, but dictionaries saturate faster;
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

    if correction == 1:
        spell = SpellProcessor('dictionaries/ru_50k.txt')
        products = spell.correct(products)
    elif correction == 2:
        spell = SpellProcessor('dictionaries/ru_full.txt')
        products = spell.correct(products)

    # TODO handle errors
    # assert len(prices) == len(products)

    distiller_object = CrankShaft()
    data_class = distiller_object(products, prices)

    return data_class
