from nltk import WordNetLemmatizer, pos_tag
from Tokenizer import tokenize
from Template_Match import *
from Tweet_Classifier import KmeansClassifier
from pandas import DataFrame
import pygmaps
import re

def tweet_feature_extractor(dict_tweet, lst_req_features):
  dict_new_tweet = {}
  for feature in lst_req_features:
    if re.search("\S+::\S+",feature):
      match = re.search("(\S+)::(\S+)",feature)
      if match.group(1) in dict_tweet:
        if match.group(2) in dict_tweet[match.group(1)]:
          if dict_tweet[match.group(1)][match.group(2)] != None or dict_tweet[match.group(1)][match.group(2)] != "":
            if isinstance(dict_tweet[match.group(1)][match.group(2)],basestring):
              #print dict_tweet[match.group(1)][match.group(2)]
              dict_new_tweet[match.group(2)] = dict_tweet[match.group(1)][match.group(2)].encode('utf-8','ignore')
            else:
              dict_new_tweet[match.group(2)] = dict_tweet[match.group(1)][match.group(2)]
    else:
      if feature in dict_tweet:
        if dict_tweet[feature] != None or dict_tweet[feature] != "":
          if isinstance(dict_tweet[feature],basestring):
            #print feature,"::",dict_tweet[feature]
            dict_new_tweet[feature] = dict_tweet[feature].encode('utf-8','ignore')
          else:
            dict_new_tweet[feature] = dict_tweet[feature]
  return dict_new_tweet
  
if __name__=='__main__':
  
  dict_tweet = {}
  lst_tweets = []
  lst_tokenized_tweets = []
  file = open("D:\\Projects\\Python\\Twitter_Flu_Trends\\flutweets_complete.txt",'rU')
  line = file.readline()
  wnl = WordNetLemmatizer()
  
  req_tweet_features = ["text", "user::location", "coordinates","created_at","user::time_zone"]
  
  lst_templates = ['infection_words','posession_words','referring_words','emoticon_happy','emoticon_sad','subj_verb_obj_match','subj_verb_match','verb_obj_match','subj_obj_match','pronoun_noun_match','subject_lastverb_match','subject_flu_match','lastverb_object_match','flu_adjective_match','question_match']
  
  while line != "":
    line.strip('\n')
    if not re.search(r"^RT",line):
      #line = line.encode('utf-8','ignore')
      dict_tweet = eval(line) 
      lst_tweets.append(dict_tweet)
    line = file.readline()
    
      
  for tweet in lst_tweets:
  
    if tweet[u'user'][u'time_zone']!=None:
      if re.search(r"US",tweet[u'user'][u'time_zone']):
        tweet = tweet_feature_extractor(tweet,req_tweet_features)    
        tokenized_text = tokenize(tweet["text"])
        token = map(lambda a: a.encode('utf-8','ignore'),tokenized_text)
        lemm_token = [wnl.lemmatize(word) for word in token]
        tweet["text"] = pos_tag(lemm_token)
        lst_tokenized_tweets.append(tweet)
    #print tweet 
  
  lst_tweet_with_coordinates = []
  lst_tweet_without_coordinates = []
  for tweet in lst_tokenized_tweets:
    if tweet["coordinates"] == None:
      lst_tweet_without_coordinates.append(tweet)
    else:
      lst_tweet_with_coordinates.append(tweet)
  
  if len(lst_tweet_without_coordinates) > 0:
    df_train_template = template_match_table_gen(lst_tweet_without_coordinates)
  
  if len(lst_tweet_with_coordinates) > 0:
    df_test_template = template_match_table_gen(lst_tweet_with_coordinates)
  
  cord_list = KmeansClassifier(df_train_template,df_test_template,lst_tweet_with_coordinates)
  
  mymap = pygmaps.maps(39.50, -98.35, 4)
  #mymap.setgrids(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)
  for x in cord_list:
    mymap.addpoint(x[1], x[0], "#0000FF")
    #mymap.addradpoint(37.429, -122.145, 95, "#FF0000")
  #path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
  #mymap.addpath(path,"#00FF00")
  mymap.draw('./mymap.html')

  