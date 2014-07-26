-- *****************
-- 20140723
--
-- Script to populate Million Song project database.
--
-- Run as
--     sqlite3 music_user.db < build_DB/create_music_user_db.sql
--
-- *****************

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    user TEXT,
    selection_number NUMBER,
    artist_id TEXT,
    artist_name TEXT,
    date_added TEXT,
    foreign_id TEXT,
    last_modified TEXT,
    play_count NUMBER,
    song_id TEXT,
    song_name TEXT
);

SELECT * FROM sqlite_master WHERE type='table';
