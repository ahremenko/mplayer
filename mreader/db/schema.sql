drop table if exists trackgenres cascade;
drop table if exists trackartists cascade;
drop table if exists images cascade;
drop table if exists files CASCADE;
drop table if exists tracks cascade;
drop table if exists artists cascade;
drop table if exists albums cascade;
drop table if exists genres cascade;
drop table if exists ratings cascade;
drop table if exists trackstats cascade;

--drop SEQUENCE if exists autoincrement;

--CREATE SEQUENCE autoincrement START 1000;

CREATE TABLE artists (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    constraint artist_name_uk unique (artist_name)
);

CREATE TABLE albums (
    album_id SERIAL PRIMARY KEY,
    album_name VARCHAR(255) NOT NULL,
    release_date DATE,
    constraint album_name_uk unique (album_name)
);

CREATE TABLE genres (
    genre_id SERIAL PRIMARY KEY,
    genre_name VARCHAR(100) NOT NULL,
    constraint genre_name_uk unique (genre_name)
);

CREATE TABLE tracks (
    track_id SERIAL PRIMARY KEY ,
    track_name VARCHAR(255) NOT NULL,
    album_id BIGINT REFERENCES albums(album_id),
    duration float,    -- длительность трека в секундах
    bpm INT,      
    key_signature VARCHAR(50),
    language VARCHAR(50),
    mood VARCHAR(100),
    track_text text,  -- текст трека
    additional_artists jsonb, -- имена исполнителей или соавторов трека
    track_url text,            -- ссылка на файл с треком (в хранилище s3)
    load_date TIMESTAMP NOT null,
    file_id BIGINT    -- ссылка на allfiles.file_id, нужно только для привязки изображения. FK не делаем, т.к. в последствии trackfiles может быть почищена
);

CREATE TABLE trackgenres (
  track_id BIGINT REFERENCES tracks(track_id),
  genre_id BIGINT REFERENCES genres(genre_id),
  PRIMARY KEY (track_id, genre_id)
);

CREATE TABLE trackartists (
  track_id BIGINT REFERENCES tracks(track_id),
  artist_id BIGINT REFERENCES artists(artist_id),
  PRIMARY KEY (track_id, artist_id)
);

CREATE TABLE ratings (
    track_id BIGINT REFERENCES Tracks(track_id),
    user_id VARCHAR NOT NULL,
    rating FLOAT,
    review TEXT,
    PRIMARY KEY (track_id, user_id)
);
 
CREATE TABLE trackstats (
  track_id BIGINT REFERENCES Tracks(track_id),
  play_count INT, -- количество воспроизведений
  popularity NUMERIC --популярность от 0 до 100
);


CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    artist_id BIGINT REFERENCES Artists(artist_id),
    --album_id BIGINT REFERENCES Albums(album_id),
    track_id BIGINT REFERENCES Tracks(track_id),
    load_date TIMESTAMP NOT NULL,
    image_url text   -- ссылка на файл с картинкой (s3,...)
);  


-- таблица для пакетной обработки файлов с диска
create table files    
(  file_id SERIAL PRIMARY KEY,
   file_path VARCHAR(1000),     -- полный путь с именем файла и расширением на файловом хранилище
   load_date TIMESTAMP NOT NULL,
   file_type varchar(10),           -- тип файла - track / image
   file_name VARCHAR(250),          -- имя файл без пути и расширения - для поиска и привязки изображений
   processed_date TIMESTAMP,
   processed_by int,
   constraint file_path_uk unique (file_path)
);

create unique index files_i01 on files(file_path);

create index files_i02 on files(file_name);








         
         