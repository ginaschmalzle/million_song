import get_api                      # File with secret API key
import os
import ast
import time
from pyechonest import catalog
from random import randrange

# Goals:
# 1. Read in a random person's playlist
# 2. Read in a bunch of people's playlists
# 3. For each person list the artist and song that they play the most
# 4. See who else listens to that artist and song.  Recommend and artist/song that they listen to that is not already on the person's play list.

def get_users(file='taste_profile_usercat_120k.txt'):
  ''' Creates a list of users.  This list will be used to extract information about
  their listening habits through an API key.'''
  my_list = []
  try:
    with open(os.path.join('../DATA/'+file), 'r') as f:
        contents = f.read()
  except Exception as e:
          print('Error {}\n    in file {}'.format(e, file))
  list_of_lines = [line.split('\t') for line in contents.split('\n')[1:]]
  for i in range(0, len(list_of_lines)-2):
    my_list.append(list_of_lines[i][0].split())
  return my_list

def get_user_dictionary(user_id, save_to_file = 'yes'):
  ''' Retrieves single user dictionary that contains the songs they listened to'''
  cat = catalog.Catalog(user_id)
  c = cat.get_item_dicts()
  if save_to_file == 'yes':
    filename = str(user_id)+'.dict'
    try:
      with open(os.path.join('../DATA/DOWNLOADS/'+filename), 'w') as f:
          f.write(str(c))
    except Exception as e:
            print('Error {}\n    in file {}'.format(e, file))
  #return c

def download_user_playlist(sample_start=9724, sample_end = 10000):
  ''' Downloads user play lists from sample_start to sample_end and puts
  them into the DOWNLOADS directory. function pauses every 60 downloads
  since API access is restricted '''
  users = get_users()
  max_sample = 60
  for i in range (sample_start, sample_end):
    get_user_dictionary(users[i][3], save_to_file = 'yes')
    if (i % max_sample == 0 and i != 0):
      print i
      time.sleep(120)



###########################################################
def retrieve_sample_playlist(num_of_samples = 100, print_to_file = 'no'):
  ''' Creates a large dictionary that includes sample playlists from num_of_samples users.
  API access is limited to only 100 hits per minute.  If num_of_samples is greater than 120
  a 60 second sleep time is imposed. If you want to keep the output in a file use print_to_file =
  yes, otherwise no'''
  users_dict = {}
  users = get_users()
  max_sample = 101
  for x in range (1, num_of_samples):
    i = randrange(len(users)-1)
    print x, i
    users_dict[users[i][3]] = get_user_dictionary(users[i][3])
    if x % max_sample == 0:
      time.sleep(60)
  if print_to_file == 'yes':
    f = open('users_playlist.dict', 'w')
    f.write(str(users_dict))
  return users_dict
