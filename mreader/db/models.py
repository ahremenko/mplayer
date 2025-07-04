from sqlalchemy import Sequence, func, ForeignKey, Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


#seq = Sequence('autoincrement')


class Base(DeclarativeBase):
    pass


class TrackFile(Base):
    __tablename__ = 'files'
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(1000), unique=True)
    load_date = Column(Date, server_default=func.now())
    file_type = Column(String(10))
    file_name = Column(String(250))
    processed_date = Column(Date)
    processed_by = Column(Integer)


class Image(Base):
    __tablename__ = 'images'
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    track_id = Column(Integer, ForeignKey('tracks.track_id'))
    image_url = Column(String)
    load_date = Column(Date, server_default=func.now())


class TrackGenre(Base):
    __tablename__ = 'trackgenres'
    track_id = Column(Integer, ForeignKey('tracks.track_id'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)
    track = relationship('Track', back_populates='trackgenres')
    genre = relationship('Genre', back_populates='trackgenres')


class TrackArtist(Base):
    __tablename__ = 'trackartists'
    track_id = Column(Integer, ForeignKey('tracks.track_id'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), primary_key=True)
    track = relationship('Track', back_populates='trackartists')
    artist = relationship('Artist', back_populates='trackartists')


class Genre(Base):
    __tablename__ = 'genres'
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    genre_name = Column(String(100), unique=True)
    trackgenres = relationship(TrackGenre, back_populates='genre')


class Artist(Base):
    __tablename__ = 'artists'
    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_name = Column(String(255), unique=True)
    trackartists = relationship(TrackArtist, back_populates='artist')
    images = relationship(Image, backref='artist')


class Album(Base):
    __tablename__ = 'albums'
    album_id = Column(Integer, primary_key=True, autoincrement=True)
    album_name = Column(String(255), unique=True)
    release_date = Column(Date)
    tracks = relationship('Track', backref='album')


class Track(Base):
    __tablename__ = 'tracks'
    track_id = Column(Integer, primary_key=True, autoincrement=True)
    track_name = Column(String(255))
    album_id = Column(Integer, ForeignKey('albums.album_id'))
    duration = Column(Float)
    bpm = Column(Integer)
    track_url = Column(String)
    load_date = Column(Date, server_default=func.now())
    file_id = Column(Integer)
    trackgenres = relationship(TrackGenre, back_populates='track')
    trackartists = relationship(TrackArtist, back_populates='track')
    images = relationship(Image, backref='track')
