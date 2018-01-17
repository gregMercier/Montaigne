
Programm scrapping Twitter (Python version 3.5)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**First step: Access to the Twitter API**

These tokens are needed for user authentifications.
Credentials can be generate via Twitter's Application Management:https//apps.twitter.com/app/new

* consumer_key = **"XXXXXXXXXXXXXXXXXXXXXXXXXX"**	
* consumer_secret = **"XXXXXXXXXXXXXXXXXXXXXXXXXX"**
* access_key = **"XXXXXXXXXXXXXXXXXXXXXXXXXX"**
* access_secret = **"XXXXXXXXXXXXXXXXXXXXXXXXXX"**

*Theses informations are saved in a config.py file*

**We mainly import the python twitter library**

.. code:: ipython3

    #-----------------------------------------------------------------------
    # twitter-user-timeline
    #  - displays a user's current timeline.
    #-----------------------------------------------------------------------
    
    from twitter import *
    import time
    import os
    import list_twitte

**Once these libraries are imported, we can load our credentials**

.. code:: ipython3

    #-----------------------------------------------------------------------
    # load our API credentials 
    #-----------------------------------------------------------------------
    config = {}
    exec(compile(open("F:\INNOV\WORKSPACE_TWITTER\Script_Python\config.py", "rb").read(), "config.py", 'exec'), config)

**We use these credentials in an object API**

.. code:: ipython3

    #-----------------------------------------------------------------------
    # create twitter API object
    #-----------------------------------------------------------------------
    twitter = Twitter(
    		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

**Now we create two python functions:**

First : *get_last_import()* : function that returns the last tweet id
about our personality and bypasses tweet retrieval limitation

.. code:: ipython3

    def get_last_import():
    	# for fn in os.listdir(dir_corpus):
    	# 	if fn.endswith('.xml'):
    	# 		print (fn)
    	# 		os.path.getmtime(dir_corpus+fn)
    
    	# print (os.path.getmtime(dir_corpus+"//manuelvalls1186.xml"))
    
    	dated_files = [(os.path.getmtime(dir_corpus+fn), os.path.basename(dir_corpus+fn)) for fn in os.listdir(dir_corpus) if fn.endswith('.xml')]
    	# print (dated_files)
    	dated_files.sort()
    	dated_files.reverse()
    	# print (dated_files)
    	try:
    		newest = dated_files[0][1]
    		separated=newest.split('-');
    		id_oldest=separated[1]
    		order_oldest=separated[2]
    		print(user+": newest:"+newest)
    		print(user+": id_oldest:"+id_oldest)
    		print(user+": order_oldest:"+order_oldest)
    	except:
    		id_oldest=''
    		order_oldest=''
    
    	returnarray = [id_oldest,order_oldest]
    	return returnarray

The second function:
		*get_user_tweets()* : function that allows to fill in the control log file and implements the xml file with the information we are interested in
This function uses two parameters the twitter username and the location of the destination xml file

We use a list that will contain all the twitter information

If we don't have user's information yet, we get the last 200 tweets 


.. code:: ipython3

    def get_user_tweets(user, dir_file):
    	# print ("here comes user: "+user)
    	#-----------------------------------------------------------------------
    	# query the user timeline.
    	# twitter API docs:
    	# https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    	#-----------------------------------------------------------------------
    
    	#initialize a list to hold all the tweepy Tweets
    	alltweets = []	
    	# Check if we've already get the tweets
    	returnback_array=get_last_import()
    	if returnback_array[0] == '':
    		i=0
    		print("there's no history")
    		results = twitter.statuses.user_timeline(screen_name = user, count = 200, tweet_mode='extended')
    		alltweets.extend(results)
    	
    		#save the id of the oldest tweet less one
    		oldest = alltweets[-1]['id'] -1
    		print (str(oldest))
    	
    	
    		# results = twitter.statuses.user_timeline(screen_name = user,count=5,max_id=oldest,since_id=returnback_array[0])
    		# alltweets.extend(results)
    		
    		# for status in alltweets:
    		# 	print (str(status['created_at']), str(status['id']))
    		#keep grabbing tweets until there are no tweets left to grab
    		while len(results) > 0:
    			print ("getting tweets before %s" % (oldest))
    				
    			#all subsiquent requests use the max_id param to prevent duplicates
    			results = twitter.statuses.user_timeline(screen_name = user,count=200,max_id=oldest, tweet_mode='extended')
    			
    			#save most recent tweets
    			alltweets.extend(results)
    			
    			#update the id of the oldest tweet less one
    			oldest = alltweets[-1]['id'] -1
    			
    			print ("...%s tweets downloaded so far for user" % (len(alltweets)))
    			print ("oldest tweet:" + str(oldest))
                
    #if any information exists, we join it with the last tweet id and the next 200 tweets
    
    	else:
    		try:
    			i=int(returnback_array[1])+1
    			print("Already history, begin with:"+returnback_array[0])
    			results = twitter.statuses.user_timeline(screen_name = user, count =200,since_id=returnback_array[0], tweet_mode='extended')
    			alltweets.extend(results)
    		
    			#save the id of the oldest tweet less one
    			oldest = alltweets[-1]['id'] -1
    			print (str(oldest))
    		except:
    			print ('Oops! No more tweets to get!')
    	
    		# results = twitter.statuses.user_timeline(screen_name = user,count=5,max_id=oldest,since_id=returnback_array[0])
    		# alltweets.extend(results)
    		
    		# for status in alltweets:
    		# 	print (str(status['created_at']), str(status['id']))
    		#keep grabbing tweets until there are no tweets left to grab
    		while len(results) > 0:
    			print ("getting tweets before %s" % (oldest))
    				
    			#all subsiquent requests use the max_id param to prevent duplicates
    			results = twitter.statuses.user_timeline(screen_name = user,count=200,max_id=oldest,since_id=returnback_array[0], tweet_mode='extended')
    			
    			#save most recent tweets
    			alltweets.extend(results)
    			
    			#update the id of the oldest tweet less one
    			oldest = alltweets[-1]['id'] -1
    			
    			print ("...%s tweets downloaded so far for user" % (len(alltweets)))
    			print ("oldest tweet:" + str(oldest))

**All information is inserted into an xml file that is named by the username and tweet id, a file by tweet**

.. code:: ipython3

    #-----------------------------------------------------------------------
    	# loop through each status item, and print its content.
    	#-----------------------------------------------------------------------
    	
    	alltweets.reverse()
    	resume = open(dir_resume+user+".txt","w", errors='ignore')
    	for status in alltweets:
    		# print(status)
    		# print (oldest)
    		# if status['id'] == oldest:
    		# 	print("created_file:oldest:"+status['id'])
    		# 	destination = open(dir_file+user+'-'+oldest+'-'+str(i)+"_.xml","w",encoding='ascii', errors='ignore')
    		# else:
    		#Définir fichier de sortie:
    		destination = open(dir_file+user+'-'+str(status['id'])+'-'+str(i)+'-'+".xml","w", errors='ignore')
    		
    		#change format date
    		ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(status["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
    		# print (status ["text"])		
    		#write to the output file
    		re_tweet=0
    		if status["full_text"].startswith("RT"):
    			re_tweet=1 
    		destination.write("<?xml version=\"1.0\"?><Tweet><Id>%s</Id><Date>%s</Date><Text>%s</Text><Identifiant>%s</Identifiant><Source>%s</Source><Name_personality>%s</Name_personality><ReTweet>%s</ReTweet></Tweet>" % 
    			(status['id'], ts, status["full_text"],user,"Twitter",list_twitte.reference_twitter.get(user), str(re_tweet)));
    		resume.write("%s;%s;%s\n" % (status['id'], ts, status['full_text']));
    		destination.close()
    		
    		# print ("(%s) %s" % (status["created_at"], status["text"].encode("ascii")))
    		i=i+1
    		#print ("(%s) @%s %s" % (result["created_at"], result["user"]["screen_name"], result["text"]))  .encode("ascii", "ignore")
    	print ("Number of tweets" + user+": "+ str(i))
    	resume.close()

**Inside a control log file we have …**

* user:lauredlr
* lauredlr: newest:lauredlr-928992602304712704-4669-.xml
* lauredlr: id_oldest:928992602304712704
* lauredlr: order_oldest:4669
* Already history, begin with:928992602304712704
* 932896436739543039
* getting tweets before 932896436739543039
* 240 tweets downloaded so far for user
* oldest tweet:929960070460395519
* getting tweets before 929960070460395519
* 240 tweets downloaded so far for user
* oldest tweet:929960070460395519
* Number of tweetlauredlr: 4910

* user:c_erhel_deputee
* c_erhel_deputee: newest:c_erhel_deputee-860556311750209536-3344-.xml
* c_erhel_deputee: id_oldest:860556311750209536
* c_erhel_deputee: order_oldest:3344
* Already history, begin with:860556311750209536
* Oops! No more tweets to get!
* Number of tweetsc_erhel_deputee: 3345

..........



**inside an xml file we have....**

* <?xml version="1.0"?>
* <Tweet>
* <Id>575788670856335362</Id>
* <Date>2015-03-11 22:41:31</Date>
* <Text>RT @ecologiEnergie: [#Sendai2015] "Important de donner les infos nécessaires aux citoyens, professionnels et décideurs @RoyalSegolene http:…</Text>
* <Identifiant>RoyalSegolene</Identifiant>
* <Source>Twitter</Source>
* <Name_personality>Ségolène Royal</Name_personality>
* <ReTweet>1</ReTweet>
* </Tweet>
