import get_api                      # File with secret API key
import os
import ast
import time
from pyechonest import catalog
from random import randrange

''' These files are used to download the data.  A second file called
get_api.py contains the API key and is not included in the github files
get_apy.py contains:

  from pyechonest import config
  config.ECHO_NEST_API_KEY='YOUR API KEY'

To download data in python 3 repl type:
import data_downloads as D
D.download_user_playlist(sample_start=0, sample_end = 10000)

Where sample_start is the first user in the list, and sample_end is the last.'''

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
  return c

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
