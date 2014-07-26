from flask import Flask
app = Flask(__name__)

@app.route('/')
def run_recommender():
  return 'Welcome to the recommender!'

if __name__ == '__main__':
  app.run()


##################################
##################################
app = Flask(__name__)
@app.route('/')
@app.route('/run_recommender')
def run_recommender():
  return ('Welcome to the recommender!')

app.run(debug = True)
  #print ('Based on your song '+ song + ' by ' + artist +' we recommend:')
#  if (len(sorted_count) >= 3):
#    for i in range (1,4):
#      print (str(i)+'. '+ str(sorted_count[len(sorted_count)-i][0][1])+' by ' +str(sorted_count[len(sorted_count)-i][0][0]))
  #elif (len(sorted_count) < 3 and len(sorted_count) > 0):
  #    print ("There wasn't enough people who chose this song in our database.  Let me try")
  #    print ("expanding the ")
  #else:
  #  print("Huh, there isn't enough info in our database.")

  #return other_user_info
