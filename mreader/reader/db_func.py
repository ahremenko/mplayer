from app.models import Genre, Album, Artist, Song, TrackFile
from sqlalchemy import func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import logging
from tinytag import TinyTag
from pathlib import PurePath
from mreader.storage.storage import save_file_to_s3
from mreader.reader.filetype import FileType

logger = logging.getLogger(__name__)


async def store_file(job_no, engine, storage, file_path, file_type, prefix):
    file_id = await get_file_id(engine, file_path)
    result = 'SKIPPED (already exists!)'
    if file_id is None:
        async with AsyncSession(engine) as session:
            async with session.begin():
                file = TrackFile(file_path=file_path, load_date=func.now(),
                                 file_type=str(file_type), processed_by=job_no, file_name=PurePath(file_path).stem)
                session.add(file)
                await session.flush()
                file_id = file.file_id
            async with session.begin():
                if file_type == FileType.song:
                    await parse_song(session=session, storage=storage, file_path=file_path, file_id=file_id,
                                     prefix=prefix)
                if file_type == FileType.image:
                    await parse_image(session=session, storage=storage, file_path=file_path, file_id=file_id)

            result = 'Added'
    curr = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    logger.info(f'{job_no} {curr} | Result: {result} file: {file_path} file_id: {file_id}')


# TODO: add mypy - линтер для статической типизации
async def parse_song(session, storage, file_path, file_id, prefix):
    tag = TinyTag.get(file_path)
    genre = await merge_genre(session=session, name=tag.genre)
    album = await merge_album(session=session, name=tag.album)
    artists = await merge_artist(session=session, name=tag.artist)
    file_url = await save_file_to_s3(storage=storage, bucket_name=str(FileType.song), file_path=file_path)
    song_name = tag.title if tag.title is not None else prefix + PurePath(file_path).stem
    year = tag.year
    release_date = datetime.strptime((str(year) + '-01-01'), "%Y-%m-%d") \
        if year is not None and str(year) != "" else None
    song = Song(title=song_name.strip(), duration=timedelta(seconds=tag.duration), bitrate=tag.bitrate,
                year=release_date, album=tag.album, genre=tag.genre, artist=tag.artist, albumartist=tag.albumartist,
                file_id=file_id, file_path=file_url)
    if album is not None:
        song.albums.append(album)
    for artist in artists:
        song.artists.append(artist)
    if genre is not None:
        song.genres.append(genre)
    session.add(song)
    logger.info(f'track: {file_path}  (artist: {tag.artist}, album: {tag.album}, genre: {tag.genre} parsed ')


async def merge_artist(session, name):
    artists = []
    if name == "" or name is None:
        return artists
    elements = name.split('&')
    for elem in elements:
        artist_name = elem.strip()
        if artist_name != "":
            insert_stmt = (insert(Artist).values(name=artist_name)
                           .on_conflict_do_nothing(index_elements=['name']))
            artist = (await session.scalars(insert_stmt)).one_or_none()
            if artist is None:
                artist = (await session.scalars(select(Artist).filter(Artist.name == artist_name))).one_or_none()
            if artist is not None:
                artists.append(artist)
    return artists


async def merge_album(session, name):
    if name == "" or name is None:
        return None
    album_name = name.strip()
    insert_stmt = (insert(Album).values(name=album_name)
                   .on_conflict_do_nothing(index_elements=['name']))
    album = (await session.scalars(insert_stmt)).one_or_none()
    if album is None:
        album = (await session.scalars(select(Album).filter(Album.name == album_name))).one_or_none()
    return album


async def merge_genre(session, name):
    if name == "" or name is None:
        return None
    genre_name = name.strip()
    insert_stmt = (insert(Genre).values(name=genre_name)
                   .on_conflict_do_nothing(index_elements=['name']))
    genre = (await session.scalars(insert_stmt)).one_or_none()
    if genre is None:
        genre = (await session.scalars(select(Genre).filter(Genre.name == genre_name))).one_or_none()
    return genre


async def get_file_id(engine, file_path):
    file_id = None
    async with AsyncSession(engine) as session:
        async with session.begin():
            file = (await session.scalars(select(TrackFile).filter(TrackFile.file_path == file_path))).one_or_none()
            if file is not None:
                file_id = file.file_id
    return file_id


async def parse_image(session, storage, file_path, file_id):
    status = 'skipped'
    file_name = PurePath(file_path).stem
    artist_name = PurePath(file_path).parent.name
    artist = (await session.scalars(select(Artist).filter(Artist.name == artist_name))).one_or_none()
    if artist is None:
        artist_name = PurePath(file_path).parent.parent.name
        artist = (await session.scalars(select(Artist).filter(Artist.name == artist_name))).one_or_none()
    song = (await session.scalars(select(Song).join(TrackFile, Song.file_id == TrackFile.file_id)
                                  .filter(TrackFile.file_name == file_name))).one_or_none()
    if song is not None or artist is not None:
        file_url = await save_file_to_s3(storage=storage, bucket_name=str(FileType.image), file_path=file_path)
        if song is not None:
            await session.execute(update(Song).values(picture_path=file_url).filter(Song.id == song.id))
        if artist is not None:
            await session.execute(update(Artist).values(icon_path=file_url).filter(Artist.id == artist.id))
        await session.execute(update(TrackFile).values(processed_date=func.now()).filter(TrackFile.file_id == file_id))
        status = 'processed'
    logger.info(f'image: {file_path}  file_name: {file_name}  artist: {artist_name}  status: {status}')
