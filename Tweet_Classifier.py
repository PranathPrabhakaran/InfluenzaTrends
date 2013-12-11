from nltk import cluster
from nltk.cluster import euclidean_distance
from numpy import array,append
from pandas import DataFrame
from cPickle import load, dump

def KmeansClassifier(df_train,df_test,lst_test):
  lst_features = ['infection_words','posession_words','referring_words','emoticon_happy','emoticon_sad','subj_verb_obj_match','subj_verb_match','verb_obj_match','subj_obj_match','pronoun_noun_match','subject_lastverb_match','subject_flu_match','lastverb_object_match','flu_adjective_match','question_match']
  means = [[1,1,1,0,1,1,1,1,1,1,1,0,1,0,0],[0,0,0,1,0,0,0,0,0,0,0,1,0,1,1]]
  vector = []
  i=0
  while i <  len(df_train):
      arr_row = ()
      for f in lst_features:
        arr_row = append(arr_row,df_train.ix[i][f])
      vector.append(arr_row)
      i+=1
  clusterer = cluster.kmeans.KMeansClusterer(2, euclidean_distance, initial_means=means)#repeats=10,avoid_empty_clusters=True)
  clusterer.cluster(vector[:len(df_train)-10], True, trace = True)

  print clusterer.means()
  vector_test = []
  i=0
  while i <  len(df_test):
      arr_row = ()
      for f in lst_features:
        #print df_features.ix[i][f]
        arr_row = append(arr_row,df_test.ix[i][f])
      vector_test.append(arr_row)
      i+=1
  coordinates_list = []
  index = 0
  while index < len(vector_test):
    print lst_test[index]["text"], "::" ,clusterer.classify(vector_test[index])
    if clusterer.classify(vector_test[index]) == 0:
      coordinates_list.append(lst_test[index]["coordinates"][u'coordinates'])
      print lst_test[index]["coordinates"][u'coordinates']
    index +=1
  return coordinates_list
    
  