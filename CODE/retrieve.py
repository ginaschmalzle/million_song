import sqlite3
import os

''' These are codes to retrieve data from the sqlite3 music database'''

def tuple2list(retrieved_data):
  ''' Convert sqlite3 tuple format to list of lists.'''
  user_list = []
  for item in retrieved_data:
    id_num = item[0]
    user = item[1].encode('utf8')
    selection_number = item[2]
    artist_id = item[3].encode('utf8')
    artist_name = item[4].encode('utf8')
    date_added = item[5].encode('utf8')
    foreign_id = item[6].encode('utf8')
    last_modified = item[7].encode('utf8')
    play_count = item[8]
    song_id = item[9].encode('utf8')
    song_name = item[10].encode('utf8')
    if play_count != 9999:
      user_list.append([id_num, user, selection_number, artist_id,
      artist_name, date_added, foreign_id, last_modified, play_count,
      song_id, song_name])
  return user_list

def tuple2listtable(retrieved_data):
  ''' Convert sqlite3 tuple format to list of lists.'''
  user_list = []
  for item in retrieved_data:
    user = item[0].encode('utf8')
    selection_number = item[1]
    song_name = item[2].encode('utf8')
    artist_name = item[3].encode('utf8')
    play_count = item[4]
    if play_count != 9999:
      user_list.append([user, selection_number, song_name, artist_name, play_count])
  return user_list

def artisttuple2list(retrieved_data):
  ''' Convert sqlite3 tuple format to list of lists.'''
  artist_list = []
  for item in retrieved_data:
    artist_list.append(item[0].encode('utf8'))
  return artist_list

def artistsongtuple2list(retrieved_data):
  ''' Convert sqlite3 tuple format to list of lists.'''
  artistsong_list = []
  for item in retrieved_data:
    artist_name = item[0].encode('utf8')
    song_name = item[1].encode('utf8')
    if song_name != 'NA':
       artistsong_list.append([artist_name, song_name])
  return artistsong_list

def retrieve_users_info_from_song(song='Half Of My Heart', artist = 'John Mayer',
            db='music_user.db', type='list_of_lists'):
  """Give me a song and an artist, and I will retrieve users and their info that listened
  to that song"""
  retrieved_data = ()
  user_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT * FROM users WHERE artist_name=? AND song_name=?''',
          (artist, song))
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  user_list = tuple2list(retrieved_data)
  return user_list


def retrieve_users_info_from_artist(artist = 'John Mayer',
            db='music_user.db', type='list_of_lists'):
  """Give me a song and an artist, and I will retrieve users and their info that listened
  to that song"""
  retrieved_data = ()
  user_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT * FROM users WHERE artist_name=?''',
          (artist,))
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  user_list = tuple2list(retrieved_data)
  return user_list

def retrieve_songs_from_user(user='CAMYCVW1332EAAD07A',
            db='music_user.db', type='list_of_lists'):
  """Give me a user and I will retrieve their song list"""
  retrieved_data = ()
  user_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT * FROM users WHERE user=?''',
          (user,))
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  user_list = tuple2list(retrieved_data)
  return user_list

def retrieve_list_of_artists (db='music_user.db'):
  """Retrieve all artists from database"""
  retrieved_data = ()
  artist_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT artist_name FROM users''')
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  artists = artisttuple2list(retrieved_data)
  artists.sort()
  prev_item = 'test';
  for item in artists:
    if item != prev_item:
      artist_list.append(item)
      prev_item = item
    else:
      continue
  return artist_list

def retrieve_list_of_artists_and_songs (db='music_user.db'):
  """Retrieve all artists from database"""
  retrieved_data = ()
  artist_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT artist_name, song_name FROM users''')
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  artists = artistsongtuple2list(retrieved_data)
  artists.sort()
  prev_item = 'test';
  for item in artists:
    if item != prev_item:
      artist_list.append(item)
      prev_item = item
    else:
      continue
  return artist_list

def retrieve_list_of_users (db='music_user.db'):
  """Retrieve all users from database"""
  retrieved_data = ()
  users_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT user FROM users''')
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  users = artisttuple2list(retrieved_data)
  users.sort()
  prev_item = 'test';
  for item in users:
    if item != prev_item:
      users_list.append(item)
      prev_item = item
    else:
      continue
  return users_list

def retrieve_list_of_songs_by_artist (artist = 'John Mayer', db='music_user.db',):
  """Retrieve all songs from artist in database"""
  retrieved_data = ()
  artist_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT song_name FROM users WHERE artist_name = ?''',
          (artist,))
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  artists = artisttuple2list(retrieved_data)
  artists.sort()
  artist_list = [];
  prev_item = 'test';
  for item in artists:
    if item != prev_item and item != 'NA':
      artist_list.append(item)
      prev_item = item
    else:
      continue
  return artist_list

def db2table (db='music_user.db',):
  """Retrieve all songs from artist in database"""
  retrieved_data = ()
  artist_list = []
  connection = sqlite3.connect(os.path.join('../DATA/DB/', db))
  with connection:
      cursor = connection.cursor()
      try:
        cursor_output = cursor.execute(
          '''SELECT user, selection_number, song_name, artist_name, play_count FROM users''')
      except Exception as e:
        # What exceptions may we encounter here?
        print(e)
  retrieved_data = cursor_output.fetchall()
  table = tuple2listtable(retrieved_data)
  f = open('music.dat', 'w')
  f.write("User, selection#, Song, artist, play_count\n")
  for i in range(0,len(table)):
    f.write(str(table[i][0])+', '+str(table[i][1])+', \''+str(table[i][2])+'\', \''+str(table[i][3])+'\', '+str(table[i][4])+'\n')
