Simple recommenders with deterministic collaborative filtering and vote-counting
===================================================================================

Recommender systems filter information to predict how a user would like a given item.  A variety of recommenders are in everyday use in online commerce- many online shopping websites now contain a “users who (watched, purchased, “liked”, etc.) this item also (watched, purchased, etc.) this other item.  I was interested in learning more about how these systems work, and so I built simple recommenders using [The Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/), a publicly available collection of audio features for a million contemporary popular music tracks.  In this exercise, I focused on the [Echo Nest Taste Profile Subset](http://labrosa.ee.columbia.edu/millionsong/tasteprofile), which contains the official user dataset of the Million Song Dataset. In this dataset, there are over a million unique users with over 384,000 unique songs.  Each user play list contains:

1. A unique user ID code
2. All the songs in their play list that include
	* song name and id
	* artist name and id
	* the number of times the song was played

Classification and prediction models common to data mining/machine learning techniques are not used in these recommenders.  John Tukey is famous for saying “all models are wrong- some models are useful” (to be fair however, Mr. Tukey did not live in a world of Big Data).  Another good quote is “keep it simple stupid”.  Recognizing that a scalable, model-based solution to the problem may ultimately have the most utility for other applications, such complexity should be justified.  Hence, to start, I decided on a simple, deterministic approach for these recommenders.  

Below I outline the steps for making my recommenders, including downloading the data, putting it into a database, and finally using it in the recommenders.  *Section 5. Recommenders* includes more information on the logic and how they are run.    

1. **Collecting the Data**
	A catalog for 120k users (about 10% of the total user catalog) is provided [here](http://labrosa.ee.columbia.edu/millionsong/sites/default/files/tasteprofile/taste_profile_usercat_120k.txt), as well as on this github repo under DATA/taste_profile_usercat_120l.txt.  The information in this file contains a unique customer name and id.  The id can be used with an API key to extract the user's song list.  The files /CODE/data_downloads.py contains functions that allow you to 1. get a list of users, 2. download the user play list, and 3. get a dictionary of user songs. Note: I didn't want anyone looking at my API key, so the script to configure the API key was not pushed to the repo.  Instead, in data_downloads.py, I explain how to make your own script with your own API key that should be in your CODE directory.  

2. **Creating a Database**
	In order to make sense out of the data collected, I made an SQLite3 database.  The code to build the bones of the database is DATA/DB/build_DB/create_music_user_db.sql.  The header of the file explains how it should be run.

3. **Populating the Database**
	I used python with the SQLite3 module to populate my database.  This script is located in CODE/populate_db.py.  Directions on how to run this script are included at the top of the script.  Note:  The database must be created and the table must be empty before running this script.  DATA ISSUE: some song lists had missing song names and play counts.  There weren't many in the subset I downloaded, so when they occurred I treated them by saying the play_count = 9999 and the song_name is 'NA'.  The populated database that I used is DATA/DB/music_user.db. In /DATA/DB/diagnostics.py there are some functions for listing some characteristics of the database.  My database was only a small fraction of the total, so it was nice to see what I had.

4. **Retrieving Data from the Database**
	I used python with the SQLite3 module to make scripts that will retrieve data from the SQLite3 database. The code /CODE/retrieve.py contains scripts that extracts items from the database and converts them into a usable format.

5. **The Recommenders**
The logic behind the simple recommender is now described.  For a given input song, si, the recommender finds other users who have si in their history, generates a list of all their playlists, and reports back a list of unique songs excluding si sorted in descending frequency of occurrence.  For naming convention lets call the list of users with si in their play list the similar user population.  Note here that I do not use the “number of times played” information.  This is because this information in the raw can lead to bias, since users that have less diverse tastes, or simply have a longer playlist, will have more influence or weighting on the outcomes.  Instead, I used the logic that the value of the recommendation comes from the strength of association between si and other songs, and what better method than to use their co-occurrences among users- leading to the simple “vote-counting” approach. It turns out this approach mimics what is called collaborative filtering- so there is the name for it if you care.  
	Having more interest and a bit of time, a second, slightly-more complicated version of the first recommender was constructed.  This time instead of a single song being the input, the entire playlist of a given user is the input data.  Lets call this given user the target-user.  The second recommender works by inputing the playlist of the target-user (one is supplied by default  but who ever runs it can specify their own user), and for each song in the input play list and puts them into a list.  The recommender then counts the number of times the other users appear in the list.  The one that is counted the most is assumed to be the most similar. Then, the three most similar users are selected as final similar users. Next, the playlists of the final similar users are used to populate a list of songs that excludes those songs that co-occur in the target-users’ playlist (why would we recommend a song already on the target person’s play list?), and a second list of similar songs is created and the songs are counted and sorted (in the case of ties, the order is alphabetical).  This second recommender takes advantage of the hierarchical nature of the data- first by selecting users with co-occurring songs, and then by ranking the songs in their playlists.  Here I selected an arbitrary number of similar users (3), which limits the potential for separation of songs by ranking (since the maximum frequency possible is 3 and the minimum is 1), but I think it’s sufficient to demonstrate the utility and logic of working with datasets that have a hierarchical structure.
	I used python to develop my recommenders.   In /CODE/recommender.py I have two recommenders, as described above, as well as in the code.  The recommender that provides recommendations based only on a selected song is called simple_recommender().  You can choose to plot the counts from the top ten songs.  Directions on how to do that are included in the code.  You can also run the simple_recommender in a fancy way that asks the user for input using the function run_simple_recommender().  Here the user is prompted to provide an artist, and if that artist is present in the database, the user is provided with a list of available songs to select from.  Once a song is selected, the recommender is off and running.   
	The second recommender that takes into consideration the selected user's entire play list is called user_recommender().   More information about this recommender is included in the code.  *All recommenders have information on how to run them in the code.*

