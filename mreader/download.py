from mreader.storage.db_func import get_song_url
from mreader.db.db import get_sync_engine
from mreader.storage.mio import get_sync_storage
import logging
import json

logger = logging.getLogger(__name__)


def run():
    engine = get_sync_engine()
    mio = get_sync_storage()
    song_id = 20
    song_url, image_url = get_song_url(engine=engine, song_id=song_id)
    if song_url != '':
        # TODO: remove next line!!
        song_url = song_url.replace("'", '"')
        print('Start downloading track... ', song_url)
        params = json.loads(song_url)
        mio.fget_object(**params, file_path='/home/alex/track_downloaded_.mp3')
        print('Track downloaded!')
    if image_url != '':
        # TODO: remove next line!!
        image_url = image_url.replace("'", '"')
        print('Start downloading image... ', image_url)
        params = json.loads(image_url)
        mio.fget_object(**params, file_path='/home/alex/picture_downloaded.jpeg')
        print('Image downloaded!')


if __name__ == '__main__':
    run()
