import os
import sys
import logging
from configs import Parameters
from blur_detector.blur_detector import detect_blur_spot

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Loading packages ...")


def main(image_path):
    detect_blur_spot(image_path, 350)


if __name__ == "__main__":
    image_path = "/home/ktp_user/Documents/Github_repo/image_quality_assessment/datasets/blurry/img_10.png"
    main(image_path)

