from . import carto
from . import postgres
from . import bigquery
from ..config import cfg
from ..logger import log


if cfg.BACKEND.lower() == 'logger':
    log.info('Using logger backend')
    copy = lambda args, kwargs: log.debug(f'copy({args}, {kwargs})')
    init = lambda args, kwargs: log.debug(f'init({args}, {kwargs})')
elif cfg.BACKEND.lower() == 'postgres':
    log.info('Using postgres backend')
    copy = postgres.copy
    init = postgres.init
else:
    log.info('Using Carto backend')
    copy = carto.copy
    init = carto.init

