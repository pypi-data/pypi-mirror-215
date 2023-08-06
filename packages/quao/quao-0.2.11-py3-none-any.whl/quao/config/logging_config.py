"""
    QuaO Project logging_config.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import sys

# import logging

from loguru import logger

logger.add(sink=sys.stderr, format="{level} : {time} : {message}: {process}",  level='DEBUG')

# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
