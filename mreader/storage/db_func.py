from app.models import Song
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_song_url(engine, song_id):
    song_url = ''
    image_url = ''
    with Session(engine) as session:
        song = session.scalars(select(Song).filter(Song.id == song_id)).one_or_none()
        if song is not None:
            song_url = song.file_path
            image_url = song.picture_path
    return song_url, image_url
