import os
import sys
import logging
from configs import Parameters

logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Loading packages ...")


def main():
    pass


if __name__ == "__main__":
    args = Parameters().parser()
