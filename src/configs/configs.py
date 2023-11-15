import argparse


class Parameters:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument('--image_path', type=str,
                                 help='the path of image')
        self.parser.add_argument('--threshold', type=float, default=100.0,
                                 help='set blurry threshold')

    def parse(self):
        args = self.parser.parse_args()
        return args
