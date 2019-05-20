
"""
Logging module
"""

import logging
from .config import cfg

def init():
    """
    Initialize logger
    """
    logfmt = '[%(levelname)s][%(asctime)s][%(filename)s %(lineno)d] - %(message)s - '
    dtfmt = '%Y-%m-%d %I:%M:%S'
    level = logging.getLevelName(cfg['LOG_LEVEL'])
    logging.basicConfig(level=level, format=logfmt, datefmt=dtfmt)

init()

log = logging.getLogger()
log.info('LOG started with level %s', cfg['LOG_LEVEL'])
