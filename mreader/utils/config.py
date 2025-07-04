import logging
import math
import os
from datetime import datetime


def conf_app(cpu_uses, ignore):
    try:
        cpu = math.ceil(os.cpu_count()*((cpu_uses/100) if cpu_uses <= 100 else 1))
    except:
        cpu = math.ceil(os.cpu_count()*3/4)
    if cpu < 1:
        cpu = 1
    files_ext_ignored = ignore.split(',')
    ignore_list = [(lambda x: "." + x)(x) for x in files_ext_ignored]
    logger = logging.getLogger(__name__)
    logger.info("============  Starting at: %s   ============" % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    logger.info("spu_total: %s  cpu_utilization: %s  cpu will be used: %s  ignores: %s" % (
        str(os.cpu_count()), str(cpu_uses), str(cpu), ignore_list))
    return cpu, ignore_list


def conf_log(log_file="mplayer.log"):
    logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)
    #logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    #logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
