import pymongo
from pymongo import MongoClient
from nltk import word_tokenize
import re
from collections import Counter
from nltk.corpus import stopwords

client  = MongoClient()

db = client['electiondata']

collection = db['tweets']

total_tweets  = collection.count()
total_rts = collection.count({ "retweeted_status" : { "$exists" : True }})  
total_original =  collection.count({ "retweeted_status" : { "$exists" : False }})


print "Total Number of Tweets: "
print  total_tweets
print "Total Number of RTs: "
print  total_rts
print "Total Number of Original Tweets: "
print  total_original


regex_str = [
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


stopwords = stopwords.words('english') + ['RT']
all_tokens = []

for tweet_data in collection.find():
	if 'text' in tweet_data:
		tokens =  preprocess(tweet_data["text"].encode('ascii','ignore').lower())
		#tokens = word_tokenize(tweet_data["text"].encode('ascii','ignore'))
		all_tokens += tokens
frequencies = Counter(all_tokens)

#for token,count in frequencies.most_common(50):
#	if token in stopwords or len(token)<2:
#		continue
#	print token,count

flag = 0
data1 = []
words = []
for token, count in frequencies.most_common(): #iteritems()
	if token.startswith('#') and flag<10:
		print token, count
		flag +=1
		data1.append(count)
		words.append(token)


from highcharts import Highchart

chart = Highchart()
options = {
'chart': {
        'type':'column'},
'title':{
        'text':'Top 10 Hashtags'},
'xAxis':{
        'categories':words},
'yAxis':{
        'title':{
                'text':'Number of times mentioned'}
        },
}
chart.set_dict_options(options)
chart.add_data_set(data1, 'column', 'Count')
chart.save_file('./column-highcharts')


chart2 = Highchart()
options = {
'chart': {
	'type':'column'},
'title':{
	'text':'Original Tweets and Retweeted Tweets'},
'xAxis':{
	'categories':['Original','Retweets']},
'yAxis':{
	'title':{
		'text':'Number of tweets'}
	},
}
data2 = [total_original, total_rts]
chart2.set_dict_options(options)
chart2.add_data_set(data2, 'column', 'Count')
chart2.save_file('./OTs_vs_RTs')


#fav = collection.count({ "retweeted_status" : { "$exists" : False }}, {"favorite_count" : {"$ne" : 0}})

#print  "Fav count on original"
#print  fav
#print "Top 10 #Hashtags"
#print  collection.aggregate({"$sort": {"_id":-1}}, {"$match": {"entities.hashtags.text":{"$exists" : True}}}, { "$limit" :100},{ "$unwind" :"$entities.hashtags"}, {"$project" : {"entities.hashtags.text":1,"_id":0}}, {"$group" :{"_id":{"$toLower":"$entities.hashtags.text"}, "count" : { "$sum" : 1 }}}, {"$sort":{"count":-1}}, {"$limit":10})

