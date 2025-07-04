from pathlib import Path
from PIL import Image
from tinytag import TinyTag
import logging


logger = logging.getLogger(__name__)


def collect_files(path, ignore_list):
    cnt_skipped = 0
    tracks = []
    images = []
    files = list(Path('.' + path).glob('**/*'))
    for file in files:
        if file.is_file():
            file_path = file.as_posix()
            if file.suffix not in ignore_list:
                if TinyTag.is_supported(file):
                    tracks.append(file_path)
                else:
                    try:
                        im = Image.open(file)
                    except (IOError, SyntaxError):
                        logger.info("File %s is not track, is not image. Skipped.", file.resolve().as_posix())
                        cnt_skipped = cnt_skipped + 1
                    else:
                        images.append(file_path)
            else:
                logger.info("File %s will be ignored due settings [ignore_files]", file.resolve().as_posix())
                cnt_skipped = cnt_skipped + 1
    if cnt_skipped > 0:
        logger.info('Skipped: %s', str(cnt_skipped))
    return tracks, images
