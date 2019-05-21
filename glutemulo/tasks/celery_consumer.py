# -*- coding: utf-8 -*-
from datetime import timedelta
import functools
import math

from celery import Celery
from celery.signals import setup_logging

from ..config import cfg
from ..logger import log
from ..model import Observations, Observation
from ..redisqueue import Queue
from ..backend import copy
from ..consumer import Consumer


def do_import(obs):
    total = len(obs)
    if not total:
        return 0
    log.info(f"Copying '{total}' observations")
    return copy(cfg.DATASET, [obs[0]._fields] + obs)

def import_from_topic(topic):
    consumer = Consumer()
    for data in queue.consume():
        try:
            obs.append(Observation(*data))
        except Exception as e:
            log.exception(e)
    log.debug(f'Importing {len(obs)} observations from queue {queue.name}')
    return do_import(obs)


