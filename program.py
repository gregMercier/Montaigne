#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-user-timeline
#  - displays a user's current timeline.
#-----------------------------------------------------------------------

from twitter import *
import time
import os
import list_twitte


#creat dictionnary for Twitter accound and Name of the personality



#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
config = {}
exec(compile(open("F:\INNOV\WORKSPACE_TWITTER\Script_Python\config.py", "rb").read(), "config.py", 'exec'), config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
		auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


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

	
	# print (results)
	
	#Script to bypass the 200 limit of count
	
	
	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	
	# #save most recent tweets
	# alltweets.extend(results)
	
	# #save the id of the oldest tweet less one
	# oldest = alltweets[-1]['id'] -1
	# print (str(oldest))


	# # results = twitter.statuses.user_timeline(screen_name = user,count=5,max_id=oldest,since_id=returnback_array[0])
	# # alltweets.extend(results)
	
	# # for status in alltweets:
	# # 	print (str(status['created_at']), str(status['id']))
	# #keep grabbing tweets until there are no tweets left to grab
	# while len(results) > 0:
	# 	print ("getting tweets before %s" % (oldest))
			
	# 	#all subsiquent requests use the max_id param to prevent duplicates
	# 	results = twitter.statuses.user_timeline(screen_name = user,count=5,max_id=oldest,since_id=returnback_array[0], tweet_mode='extended')
		
	# 	#save most recent tweets
	# 	alltweets.extend(results)
		
	# 	#update the id of the oldest tweet less one
	# 	oldest = alltweets[-1]['id'] -1
		
	# 	print ("...%s tweets downloaded so far for user" % (len(alltweets)))
	# 	print ("oldest tweet:" + str(oldest))
	
	
	
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
	
	
#-----------------------------------------------------------------------
# this is the user we're going to query.
#-----------------------------------------------------------------------

list1=['lauredlr','c_erhel_deputee','mandonthierry','brunoretailleau','christianpaul58','franckriester','pbloche','martinemartinel','EPhilippe_LH','jcgaudin']
list2=['gerardcollomb','jlmoudenc','cestrosi','Johanna_Rolland','roland_ries','saurel2014','nathalieappere','hubertfalco','PerdriauGael','fhollande']
list3=['manuelvalls','LaurentFabius','RoyalSegolene','benoithamon','montebourg','MarisolTouraine','JY_LeDrian','BCazeneuve','najatvb','mlebranchu']
list4=['aurelifil','pierremoscovici','anne_hidalgo','martineaubry','jeanmarcayrault','fleurpellerin','vincent_peillon','claudebartolone','GBachelay','BrunoLeRoux']
list5=['axellelemaire','CECKERT56','jccambadelis','cecileduflot','josebove','JVPlace','JLMelenchon','plaurent_pcf','olbesancenot','christineboutin']
list6=['n_arthaud','DupontAignan','ChTaubira','SylviaPinel','JMBaylet','bayrou','Herve_Morin','Chantal_Jouanno','ramayade','yvesjego']
list7=['NicolasSarkozy','jf_cope','francoisfillon','nk_m','BrunoLeMaire','CGueant','alainjuppe','vpecresse','datirachida','lucchatel']
list8=['xavierbertrand','francoisbaroin','jpraffarin','laurentwauquiez','villepin','BernardAccoyer','ECiotti','DAUBRESSE_MP','MLP_officiel','lepenjm']
list9=['louis_aliot','gilbertcollard','Marion_M_Le_Pen','f_philippot','harlemdesir','AVidalies','Th_Braillard','yjadot','evajoly','emmanuelmaurel']
list10=['MatthiasFekl','MAlliotMarie','nadine__morano','JeanArthuis','ericpiolle','frebsamen','christophebechu','jm_leguen','ClotildeVALTER','slefoll']
list11=['valliniandre','PatrickKanner','MyriamElKhomri','goulardsylvie','arnauddanjean']



iter_file=0
for user in list1:
	dir_corpus = "F:\\INNOV\\DATA\\TWITTER\\list1\\"+user+"\\"
	dir_resume = "F:\\INNOV\\WORKSPACE_TWITTER\\resume_tweets\\"
	if not os.path.exists(dir_corpus) :
		os.makedirs(dir_corpus);
	if not os.path.exists(dir_resume):
		os.makedirs(dir_resume);
	print ("user:"+user)
	# print ("file_name:"+dir_corpus+filelist[iter_file])
	iter_file=iter_file+1	
	get_user_tweets(user, dir_corpus)

	
