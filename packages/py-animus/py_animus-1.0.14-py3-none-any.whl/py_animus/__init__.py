"""
    Copyright (c) 2023. All rights reserved. NS Coetzee <nicc777@gmail.com>

    This file is licensed under GPLv3 and a copy of the license should be included in the project (look for the file 
    called LICENSE), or alternatively view the license text at 
    https://raw.githubusercontent.com/nicc777/verbacratis/main/LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt
"""


import traceback
import logging
import logging.handlers
import sys
import os
from datetime import datetime

import yaml
try:    # pragma: no cover
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError: # pragma: no cover
    from yaml import Loader, Dumper


def get_utc_timestamp(with_decimal: bool=False): # pragma: no cover
    epoch = datetime(1970,1,1,0,0,0)
    now = datetime.utcnow()
    timestamp = (now - epoch).total_seconds()
    if with_decimal:
        return timestamp
    return int(timestamp)


def is_debug_set_in_environment()->bool:    # pragma: no cover
    try:
        env_debug = os.getenv('DEBUG', '0').lower()
        if env_debug in ('1','true','t','enabled'):
            return True
    except:
        pass
    return False


def get_logging_stream_handler(
    level=logging.INFO,
    formatter: logging.Formatter=logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
)->logging.StreamHandler:
    try:
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(level)    
        h.setFormatter(formatter)
        return h
    except: # pragma: no cover
        traceback.print_exc()
    return None # pragma: no cover


def get_logger(
    level=logging.INFO,
    log_format: str='%(asctime)s %(levelname)s - %(message)s'
)->logging.Logger:
    if is_debug_set_in_environment() is True:
        level = logging.DEBUG

    logger = logging.getLogger()
    logger.setLevel(level=level)
    logger.handlers = []
    formatter = logging.Formatter(log_format)

    h = get_logging_stream_handler(
        level=level,
        formatter=formatter
    )
    if h is not None:
        logger.addHandler(h)

    logger.debug('Logging init done')
    return logger


def parse_raw_yaml_data(yaml_data: str, logger=get_logger())->dict:
    configuration = dict()
    current_part = 0
    # logger.debug('parse_raw_yaml_data(): RAW DATA: {}'.format(yaml_data))
    try:
        for data in yaml.load_all(yaml_data, Loader=Loader):
            current_part += 1
            configuration['part_{}'.format(current_part)] = data
        # logger.debug('configuration={}'.format(configuration))
    except: # pragma: no cover
        traceback.print_exc()
        raise Exception('Failed to parse configuration')
    return configuration

