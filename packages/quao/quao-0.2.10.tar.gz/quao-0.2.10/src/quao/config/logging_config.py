"""
    QuaO Project logging_config.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
# import logging

from loguru import logger

logger.add( format="{level} : {time} : {message}: {process}",  level='DEBUG')

# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
