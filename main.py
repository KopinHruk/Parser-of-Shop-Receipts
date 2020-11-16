import argparse

from image_processing import tesseract_image, CheckParser, CrankShaft


def get_parser():
    """
    Creates parser using argparse module
    :return: args from CLI
    """

    parser = argparse.ArgumentParser(description='Check parser')

    parser.add_argument('image_path', type=str, help='Path to image to process')

    args = parser.parse_args()

    return args


def main():
    args = get_parser()

    work_string = tesseract_image(args.image_path)

    b = CheckParser(True)
    products, prices = b.parse(work_string)

    assert len(prices) == len(products)

    man = CrankShaft()
    df = man(products, prices)
    print(df)


if __name__ == '__main__':
    main()
