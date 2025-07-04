import click
import asyncio
import logging
from mreader.reader.collector import collect_files
from mreader.reader.reader import read_files
from mreader.utils.config import conf_log, conf_app
from mreader.db.db import get_engine, get_engine_string
from mreader.storage.mio import get_storage
from tqdm import tqdm

logger = logging.getLogger(__name__)


# to run me use: python3 -m mreader
@click.command()
@click.option('--path', default='/data', help='The root directory with media library for Meta-data')
@click.option('--cpu', default=75, help='CPU usage in percents')
@click.option('--log', default='mplayer.log', help='Log filename')
@click.option('--prefix', default='**_', help='prefix for empty title, e.g.: NA_')
@click.option('--ignore', default='docx,doc,pdf', help='file extensions for ignore, e.g.: docx,pdf,xlsx')
def run(path, cpu, log, prefix, ignore):
    conf_log(log)
    cpus, ignore_list = conf_app(abs(cpu), ignore)
    engine = get_engine()
    if engine is None:
        raise "Database connection error. Check ENVIRONMENT VARIABLES."
    mio = get_storage()
    if mio is None:
        raise "Minio/s3 connection error. Check ENVIRONMENT VARIABLES."
    print(f'==== mReader v.0.2  DB: {get_engine_string()}  path: {path}  CPUs: {cpus}  ignore list: {ignore_list} ====')
    tracks, images = collect_files(path=path, ignore_list=ignore_list)
    bar = tqdm(total=len(tracks)+len(images))
    asyncio.run(read_files(engine=engine, storage=mio, tracks=tracks, images=images, cpus=cpus, prefix=prefix, bar=bar))


if __name__ == '__main__':
    run()

