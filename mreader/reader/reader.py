import logging
import asyncio
#from codetiming import Timer
from mreader.reader.db_func import store_file
from mreader.reader.filetype import FileType

logger = logging.getLogger(__name__)


async def read_files(engine, storage, tracks, images, cpus, prefix, bar):
    tracks_queue = asyncio.Queue()
    images_queue = asyncio.Queue()

    for file in tracks:
        await tracks_queue.put(file)
    for file in images:
        await images_queue.put(file)
    #with Timer(text="\nTotal elapsed time: {:.1f}"):
    tasks = []
    for i in range(1, cpus+1):
        task = asyncio.create_task(process_file(job_no=i, work_queue=tracks_queue, engine=engine,
                                                storage=storage, file_type=FileType.song, bar=bar, prefix=prefix))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=False)
    for i in range(1, cpus+1):
        task = asyncio.create_task(process_file(job_no=i, work_queue=images_queue, engine=engine,
                                                storage=storage, file_type=FileType.image, bar=bar))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=False)


async def process_file(job_no, work_queue, engine, storage, file_type, bar, prefix=None):
    while not work_queue.empty():
        file_path = await work_queue.get()
        await store_file(job_no, engine, storage, file_path, file_type, prefix=prefix)
        bar.update()





