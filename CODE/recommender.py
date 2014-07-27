import retrieve as R
import operator
import numpy as np
import matplotlib as plt
import pylab

plt.rcParams['figure.figsize'] = [9,9]
plt.rcParams['figure.dpi'] = 80

''' This contains two recommenders.  The simple_recommender simply considers one
song or artist that you feed it, checks to see who else has your input in the data
base, adds up the number of times other songs are in other people's playlists and
spits out the songs that appear most often.  Past selection history is not considered.
The user_recommender, however, takes into consideration all of a person's past
selections.  It finds all other users that have any of the songs you have in your
database, and counts how many times a particular user shows up.  The user that is
counted the most is most similar to the input user's play list is the one that is
counted the most.  This program takes the top 3 (arbitrary) other users that are
most like the input user and spits out songs that the input user does not have.
Again, it tally's the number of times the songs are in the other user's databases
and ranks them according to how many databases they show up in.

The module operator requires Python 2.7, hence this code needs to be run in that
version of Python.'''

def simple_recommender(song='Yeah!', artist = 'Usher', plot = 'yes'):
  ''' This recommender searches for other people that also downloaded the song,
  then looks at their song lists.  It counts the number of times a song was
  in a other user's song list and ranks them. If you would like to see the top
  10 songs that are in other user song lists that also include the given artist
  and song, use plot = yes.  To run in python repl type:
    import recommender as R
    R.simple_recommender(song = YOUR SONG IN PARENS, artist = YOUR ARTIST IN PARENS)
  Enjoy!'''
  # Collect other people's play lists that have your song and/or artist
  if song == '':
    other_user_info = R.retrieve_users_info_from_artist(artist=artist)
  else:
    other_user_info = R.retrieve_users_info_from_song(song= song, artist=artist)
  other_user_songs = []; count_dict = {}; sorted_count = {}
  # Count the times the songs appear in other people's play lists.
  # Play_count is included in the database, but I found that this number
  # can bias the results.  Hence it is not included in this algorithm.
  for line in other_user_info:
      other_user_songs.append(R.retrieve_songs_from_user(line[1]))
  for i in range(0, len(other_user_songs)):
    for j in range(0, len(other_user_songs [i])):
      uartist = other_user_songs[i][j][4]
      usong = other_user_songs[i][j][10]
      play_count = other_user_songs[i][j][8]
      if ( uartist != artist and usong != song):
        try:
            count_dict[uartist,usong] = count_dict[uartist,usong] + 1
        except KeyError:
            count_dict[uartist,usong] = 1
      else:
        continue
  # Sort values in the dictionary
  sorted_count = sorted(count_dict.iteritems(), key=operator.itemgetter(1))
  # Plot how many times the top 10 songs were counted
  if plot == 'yes':
    counts = []; names = []
    for i in range(0, len(sorted_count)):
      if (sorted_count[i][1] > 5):
        counts.append(sorted_count[i][1])
        names.append(sorted_count[i][0])
    counts = counts[10:]
    names = names[10:]
    nloc = np.array(range(len(names))) +0.5
    width = 0.2
    f = pylab.subplot(211)
    f.bar(nloc, counts, width = width)
    f.set_xticks(nloc)
    f.set_xticklabels(names, rotation = 90, ha='center')
    f.set_ylabel('Counts')
    f.set_title('Top 10 other songs in users song lists that include \''+song+'\' by '+artist)
    pylab.savefig('top10.jpg')
    pylab.show()
  # Return the sorted count of songs/artists
  return sorted_count

def print_recs(sorted_count):
  ''' Prints the recommendations from the recommender'''
  for i in range (1,4):
    print (str(i)+'. '+ str(sorted_count[len(sorted_count)-i][0][1])+' by ' +str(sorted_count[len(sorted_count)-i][0][0]))

def run_simple_recommender():
  ''' The function runs the simple_recommender via command line.  In python repl,
  simply type:
    import recommender as R
    R.run_simple_recommender()
  and follow the directions. This function does not plot top 10 songs. '''
  print ("Welcome to the Recommender, the one stop for music recommendations!")
  artist = raw_input("Please enter an artist (be mindful of Caps!): ")
  song_list = R.retrieve_list_of_songs_by_artist(artist)
  # If there is a typo or artist does not exist, do this until it does.
  while (len(song_list) == 0):
    print('')
    print('Sorry, that artist is not in our database.')
    print('Please check the spelling (be mindful of caps!)')
    print('or try another artist.  Please try again.')
    print('')
    artist = raw_input("Please enter an artist (be mindful of Caps!): ")
    song_list = R.retrieve_list_of_songs_by_artist(artist)
  print ('')
  print ('Thank you! These are the songs by that artist in our database:')
  print ('')
  # Print out songs by that artist.
  for item in song_list:
    print item
  print ('')
  # Allow user to select a song and run the simple_recommender above.
  song = raw_input("Please enter a song: ")
  sorted_count = simple_recommender(song=song, artist=artist, plot = 'no')
  if (len(sorted_count) >= 10):
    print ('Fabulous choice!  Other people who listened to this song also listened to:')
    print_recs(sorted_count)
  else:
    # If the artist and song selected are not in the database very often, expand
    # the search to include only the artist.
    print ("Ah, you have unique taste in music!  Let me expand my search to come up with your recommendation...")
    sorted_count = simple_recommender(song='', artist=artist, plot = 'no')
    print ("Expanding the search, I found that people who listen to this artist also listed to these songs: ")
    print_recs(sorted_count)

def user_recommender(user = 'CAEYTUX1332EA3C8E2'):
  ''' This recommender takes the information stored in the user's song list, and
  then searches for others with similar songs in their lists. It collects the users
  for each song and then ranks the other users as most to least similar to the
  user defined above.  The top 3 similar users are chosen, and then songs not
  already in the user's play list are ranked by the most counted.
  The top songs are displayed.To run in python repl type:
    import recommender as R
    R.user_recommender(user = YOUR USER ID)
  Enjoy!'''
  # Retrieve songs list from specified user
  user_list = R.retrieve_songs_from_user(user)
  song_list = []; user_songs = []
  # make a sorted user song list that contains artist, song and play count
  # also make a list of just songs that will be used later to filter recommendations
  for i in range (0, len(user_list)):
    if user_list[i][10] != 'NA':
      song_list.append([user_list[i][8],user_list[i][10],user_list[i][4]])
      user_songs.append(user_list[i][10])
  song_list.sort(reverse = True)
  user_songs.sort(reverse = True)
  print('Your songs are:')
  for i in range (0,len(song_list)):
    print (str(i+1)+'. '+ str(song_list[i][1])+' by ' +str(song_list[i][2]))
  # Now find similar users.  For each song, collect the id's of other users and
  # put them in a list called similar_users(which contains all of their songs too)
  # For simplification, user_ids are collected from similar_users in their own list
  # called ouser_id (other user id) and then sorted.  Other user's songs and artist
  # are designated with an o as the first letter in variable name.
  similar_users = []; ouser_id = []
  for i in range(0,len(song_list)-1):
    song = song_list[i][1]
    artist = song_list[i][2]
    similar_users.append(R.retrieve_users_info_from_song(song, artist))
  for i in range (0, len(similar_users)-1):
    for j in range(0, len(similar_users[i])-1):
      ouser_id.append(similar_users[i][j][1])
  ouser_id.sort(reverse = True)
  # Count and sort by how many times the ousers show up in the list
  myuser = 'NA'
  ouser_count = {}
  for ouser in ouser_id:
    if ouser != user:
      if ouser == myuser:
        count = count + 1
        myuser = ouser
      else:
        myuser = ouser
        count = 1
    ouser_count[ouser] = count
  sorted_ouser_count = sorted(ouser_count.iteritems(), key=operator.itemgetter(1), reverse=True)
  other_song_list = []
  # Tally all of the top 3 other user's songs into a list
  for i in range(0,3):
    other_song_list.append(R.retrieve_songs_from_user(user=sorted_ouser_count[i][0]))
  other_song_list.sort()
  # Count the number of times the other user songs show up in other_song_list and sort them
  osong_count = {}
  for i in range(1,len(other_song_list)-1):
    for j in range(1,len(other_song_list[i])):
      if other_song_list[i][j][4] not in song_list:
        oartist = other_song_list[i][j][4]
        osong = other_song_list[i][j][10]
        try:
          osong_count[oartist,osong] = osong_count[oartist,osong] + 1
        except KeyError:
          osong_count[oartist,osong] = 1
  sorted_osong_count = sorted(osong_count.iteritems(), key=operator.itemgetter(1))
  print('')
  print('User '+user+', you have great taste in music! People with similar play')
  print('lists are also listening to:')
  print('')
  # If user_songs has a song that is identical to those in sorted_osong_count,
  # don't print them as a recommendation.
  a = 0
  for i in range(0,len(sorted_osong_count)):
    if (sorted_osong_count[i][0][1] not in user_songs ):
      a = a + 1
      print(str(a)+'. ' + sorted_osong_count[i][0][1]+' by '+sorted_osong_count[i][0][0])
