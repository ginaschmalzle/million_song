import retrieve as R
import operator

''' This code builds programs that recommend songs based on the song you picked'''

def simple_recommender(song='When I Grow Up', artist = 'The Pussycat Dolls'):
  ''' This recommender searches for other people that also downloaded the song,
  then looks at their song lists.  It counts the number of times a song was
  listened to and ranks them.'''
  other_user_info = R.retrieve_users_info_from_song(song= song, artist=artist)
  other_user_songs = []; count_dict = {}; sorted_count = []
  for line in other_user_info:
    other_user_songs.append(R.retrieve_songs_from_user(line[1]))
  for i in range(0, len(other_user_songs)):
    for j in range(0, len(other_user_songs [i])):
      uartist = other_user_songs[i][j][4]
      usong = other_user_songs[i][j][10]
      play_count = other_user_songs[i][j][8]
      try:
          count_dict[uartist,usong] = count_dict[uartist,usong]
      except KeyError:
          count_dict[uartist,usong] = 1
    sorted_count = sorted(count_dict.iteritems(), key=operator.itemgetter(1))
  print ('Based on your song '+ song + ' by ' + artist +' we recommend:')

  if (len(sorted_count) >= 3):
    print ('1. '+ sorted_count[len(sorted_count)-1][0][1]+' by ' +sorted_count[len(sorted_count)-1][0][0])
    print ('2. '+ sorted_count[len(sorted_count)-2][0][1]+' by ' +sorted_count[len(sorted_count)-2][0][0])
    print ('3. '+ sorted_count[len(sorted_count)-3][0][1]+' by ' +sorted_count[len(sorted_count)-3][0][0])
  elif (len(sorted_count) == 2):
    print ('1. '+ sorted_count[len(sorted_count)-1][0][1]+' by ' +sorted_count[len(sorted_count)-1][0][0])
    print ('2. '+ sorted_count[len(sorted_count)-2][0][1]+' by ' +sorted_count[len(sorted_count)-2][0][0])
  elif (len(sorted_count) == 1):
    print ('1. '+ sorted_count[len(sorted_count)-1][0][1]+' by ' +sorted_count[len(sorted_count)-1][0][0])
  else:
    print("Huh, there isn't enough info in our database.")

  #return other_user_info
