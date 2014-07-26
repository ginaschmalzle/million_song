The Million Song Recommender Project
=========================================

Background:  The [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/) is a publicly available collection of audio features for a million contemporary popular music tracks.  I am focusing on the [Echo Nest Taste Profile Subset](http://labrosa.ee.columbia.edu/millionsong/tasteprofile), which contains the official user dataset of the Million Song Dataset. In this dataset, there are over a million unique users with over 384,000 unique songs.  Each user play list contains:

1. A unique user ID code
2. All the songs in their play list that include
	a.song name and id
	b artist name and id
	c. the number of times the song was played

Given this information, I made two recommenders.  The first recommender assumes no prior knowledge of the user's playlist. It finds other people who have played the selected song in their history, and pulls up other songs from all their playlists, counts the number of times the song appears in people's playlists and spits out the top songs from their lists.  The second recommender is more complex.  It takes a given user's entire song list, and finds other users that are most similar to their play list.  From that information, the second recommender spits out songs from the similar users' song list that is not in the original user's song list.  Below is a description of how I did it:

1. **Collecting the Data**
	A catalog for 120k users (about 10% of the total user catalog) is provided [here](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/tasteprofile/taste_profile_usercat_120k.txt), as well as on this github repo under DATA/taste_profile_usercat_120l.txt.  The information in this file contains a unique customer name and id.  The id can be used with an API key to extract the user's song list.  The files /CODE/data_downloads.py contains functions that allow you to 1. get a list of users, 2. download the user play list, and 3. get a dictionary of user songs. Note: I didn't want anyone looking at my API key.  So the script to configure the API key was not pushed to the repo.  Instead, in data_downloads.py, I explain how to make your own script with your own API key that should be in your CODE directory.  

2. **Creating a Database**
	In order to make sense out of the data collected, I made an SQLite3 database.  The code to build the bones of the database is DATA/DB/build_DB/create_music_user_db.sql.  The header of the file explains how it should be run.

3. **Populating the Database**
	I used python with the SQLite3 module to populate my database.  This script is located in CODE/populate_db.py.  Directions on how to run this script are included at the top of the script.  Note:  The database must be created and the table must be empty before running this script.  DATA ISSUE: some song lists had missing song names and play counts.  There weren't many in the subset I downloaded, so when they occurred I treated them by saying the play count = 9999 and the song_name is 'NA'.  The populated database is DATA/DB/music_user.db.

4. **Retrieving Data from the Database**
	I used python with the SQLite3 module to make scripts that will retrieve data from the SQLite3 database. The code /CODE/retrieve.py contains scripts that extracts items from the database and converts them into a usable format.

5. **The Recommenders**
	I used python to develop my recommenders.   In /CODE/recommender.py I have two recommenders, as described above, as well as in the code.  The recommender that provides recommendations based only on a selected song is called simple_recommender().  You can choose to plot the counts from the top ten songs.  Directions on how to do that are included in the code.  You can also run the simple_recommender in a fancy way that asks the user for input using the function run_simple_recommender().
	The second recommender that takes into consideration the selected user's entire play list is called user_recommender().   More information about this recommender is included in the code.  
	All recommenders have information on how to run them in the code.
