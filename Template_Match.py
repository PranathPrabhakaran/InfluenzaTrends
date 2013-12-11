from pandas import DataFrame, Series
import re

sym_word_infection = [word.strip("\n\r") for word in open("D:\Projects\Python\Twitter_Flu_Trends\Text Words\Infection.txt","rU")]
#print sym_word_infection

word_possession = [word.strip("\n\r") for word in open("D:\Projects\Python\Twitter_Flu_Trends\Text Words\Possesion.txt","rU")]
#print word_possession

word_others = [word.strip("\n\r") for word in open("D:\Projects\Python\Twitter_Flu_Trends\Text Words\Subject.txt","rU")]
#print word_others


mycompile = lambda pat:  re.compile(pat,  re.UNICODE)

def findmatch(lst_tag_sent,lst_words):
  for k,w in lst_tag_sent:
    if k in lst_words:
      return True
  return False
  
def findEmoticons(lst_tag_sent):
  ## Emoticons
  NormalEyes = r'[:=]'
  Wink = r'[;]'

  #NoseArea = r'[(|o|O|-)]*'   ## rather tight precision, \S might be reasonable...
  NoseArea = r'\S*'   ## rather tight precision, \S might be reasonable...

  HappyMouths = r'[D\)\]]+'
  SadMouths = r'[\(\[]+'
  Tongue = r'[pP]+'
  OtherMouths = r'[doO/\\]'  # remove forward slash if http://'s aren't cleaned
  
  
  Happy_RE =  mycompile( '(\^_\^|' + NormalEyes + NoseArea + HappyMouths + ')')
  Sad_RE = mycompile(NormalEyes + NoseArea + SadMouths)
  for token,tag in lst_tag_sent:
    if Happy_RE.search(token):
      return "happy"
    if Sad_RE.search(token):
      return "sad"
  
def phraseSegment(lst_tag_sent):
  PunctChars = r'''[,.]'''
  Punct = '%s+' % PunctChars
  Punct_RE = mycompile(Punct)
  lst_phrased_sent = []
  index = 0
  start = 0
  for token,tag in lst_tag_sent: 
    if Punct_RE.search(tag):
      lst_phrased_sent.append(lst_tag_sent[start:index])
      start = index+1
    else:
      index +=1
      continue
    
#    lst_phrased_sent.append(lst_phrase)
  lst_phrased_sent.append(lst_tag_sent[start:index+1])
  return lst_phrased_sent
  
def matchtuples(lst_phrases):
  #lst_phrases = phraseSegment(lst_tag_sent)
  lst_dicts = []
  for lst_phrase in lst_phrases:
    dict_phrase = {}
    for token,tag in lst_phrase:
      if re.search(r"N|PR.+",tag) and  "subject" not in dict_phrase:
        dict_phrase["subject"] = (token,tag)
      if re.search(r"V.+",tag) and  "verb" not in dict_phrase:
        dict_phrase["verb"] = (token,tag)
      if re.search(r"N|PR.+",tag) and "object" not in dict_phrase and "verb" in dict_phrase :  
        dict_phrase["object"] = (token,tag)

    lst_dicts.append(dict_phrase) 
  return lst_dicts

def find_pronoun_noun(lst_phrases):
  list_matches =[]
  for phrase in lst_phrases:
    dict_match = {}
    for token,tag in phrase:
      if re.search(r"PR.+",tag) and  "pronoun" not in dict_match:
        dict_match["pronoun"] = token
      if re.search(r"N.+",tag):
        dict_match["noun"] = token
    list_matches.append(dict_match)
  return list_matches

def find_subj_lastverb(lst_phrases):
  lst_dicts = []
  for lst_phrase in lst_phrases:
    dict_phrase = {}
    for token,tag in lst_phrase:
      if re.search(r"N|PR.+",tag) and  "subject" not in dict_phrase:
        dict_phrase["subject"] = (token,tag)
      if re.search(r"V.+",tag) and  "subject" in dict_phrase:
        dict_phrase["verb"] = token
    lst_dicts.append(dict_phrase) 
  return lst_dicts
  
def find_subj_flu(lst_phrases):
  flag = False
  for lst_phrase in lst_phrases:
    verb_flag = 0
    for tag,token in lst_phrase:
      if re.search(r"V.+",tag):
        break
      elif re.search(r"N.+",tag) and token in word_possession:
        flag = True
        return flag
  return flag

def find_lastverb_object(lst_phrases):
  lst_dicts = []
  for lst_phrase in lst_phrases:
    dict_phrase = {}
    for token,tag in lst_phrase:
      if re.search(r"V.+",tag):
        dict_phrase["verb"] = token
      if re.search(r"N|PR.+",tag) and  "verb" in dict_phrase:
        dict_phrase["object"] = token
    lst_dicts.append(dict_phrase) 
  return lst_dicts  
   
def flu_adjective_match(lst_phrases):
  flag = False
  for lst_phrase in lst_phrases:
    for tag,token in lst_phrase:
      if re.search(r"JJ.+",tag) and token in word_possession:
        flag = True
        return flag
  return flag
  
def question_match(lst_phrases):
  for lst_phrase in lst_phrases:
    index = 50
    for tag,token in lst_phrase:
      if re.search(r"N.+",tag):
        index = 1
      elif re.search(r"\?+",token):
        if index == 1:
          return True
      else:
        index+=1
  return False      
      

def template_match_table_gen(dict_tweets): 
  df_feature = DataFrame(columns = ['infection_words','posession_words','referring_words','emoticon_happy','emoticon_sad','subj_verb_obj_match','subj_verb_match','verb_obj_match','subj_obj_match','pronoun_noun_match','subject_lastverb_match','subject_flu_match','lastverb_object_match','flu_adjective_match','question_match'])
  index_num = 0
  for tweets in dict_tweets:
    #print sent
    series_temp_feature = Series(index = ['infection_words','posession_words','referring_words','emoticon_happy','emoticon_sad','subj_verb_obj_match','subj_verb_match','verb_obj_match','subj_obj_match','pronoun_noun_match','subject_lastverb_match','subject_flu_match','lastverb_object_match','flu_adjective_match','question_match'])
    #infection words
    if findmatch(tweets["text"],sym_word_infection):
      series_temp_feature['infection_words'] = 1
    else:
      series_temp_feature['infection_words'] = 0
      #possession words
    if findmatch(tweets["text"],word_possession):
      series_temp_feature['posession_words'] = 1
    else:
      series_temp_feature['posession_words'] = 0
    #refer to people
    if findmatch(tweets["text"],word_others):
      series_temp_feature['referring_words'] = 1
    else:
      series_temp_feature['referring_words'] = 0
    #emoticons  
    emotion = findEmoticons(tweets["text"])
    if emotion == "happy":
      series_temp_feature['emoticon_happy'] = 1
    else:
      series_temp_feature['emoticon_happy'] = 0
    if emotion == "sad":
      series_temp_feature['emoticon_sad'] = 1
    else:
      series_temp_feature['emoticon_sad'] = 0
    
    lst_phrases = phraseSegment(tweets["text"])
    
    series_temp_feature['subj_verb_obj_match'] = 0
    series_temp_feature['subj_verb_match'] = 0
    series_temp_feature['verb_obj_match'] = 0
    series_temp_feature['subj_obj_match'] = 0
    #print phraseSegment(tweets["text"]["text"])
    lst_templates = matchtuples(lst_phrases)
    for template in lst_templates:
      #print template["verb"][0] in sym_word_infection, template["subject"][0] in word_others, template["object"][0] in word_possession
      if "subject" in template and "verb" in template and "object" in template:
        if template["verb"][0] and sym_word_infection and (template["subject"][0] in word_others or template["subject"][1] == "NNP") and template["object"][0] in word_possession:
          series_temp_feature['subj_verb_obj_match'] = 1
      elif "subject" in template and "verb" in template:
        if template["verb"][0] and sym_word_infection and (template["subject"][0] in word_others or template["subject"][1] == "NNP"):
          series_temp_feature['subj_verb_match'] = 1
      elif "object" in template and "verb" in template:
        if template["verb"][0] and sym_word_infection and template["object"][0] in word_possession:    
          series_temp_feature['verb_obj_match'] = 1
      elif "subject" in template and "object" in template:
        if (template["subject"][0] in word_others or template["subject"][1] == "NNP") and template["object"][0] in word_possession:
          series_temp_feature['subj_obj_match'] = 1
    
    #pronoun noun pair
    series_temp_feature['pronoun_noun_match'] = 0
    lst_matches = find_pronoun_noun(lst_phrases)
    for match in lst_matches:
      if "pronoun" in match and "noun" in match:
        if match["pronoun"] in word_others and match["noun"] in word_possession:
          series_temp_feature['pronoun_noun_match'] = 1
    
    series_temp_feature['subject_lastverb_match'] = 0  
    lst_matches = find_subj_lastverb(lst_phrases)
    for match in lst_matches:
      if "subject" in match and "verb" in match:
        if (template["subject"][0] in word_others or template["subject"][1] == "NNP") and match["verb"] in sym_word_infection:
          series_temp_feature['subject_lastverb_match'] = 1
    
    series_temp_feature['subject_flu_match'] = 0  
    if find_subj_flu(lst_phrases):
      series_temp_feature['subject_flu_match'] = 1

    series_temp_feature['lastverb_object_match'] = 0  
    lst_matches = find_lastverb_object(lst_phrases)
    for match in lst_matches:
      if "object" in match and "verb" in match:
        if match["object"] in word_possession and match["verb"] in sym_word_infection:
          series_temp_feature['lastverb_object_match'] = 1
    
    series_temp_feature['flu_adjective_match'] = 0  
    if flu_adjective_match(lst_phrases):
      series_temp_feature['flu_adjective_match'] = 1
    
    series_temp_feature['question_match'] = 0  
    if question_match(lst_phrases):
      series_temp_feature['question_match'] = 1
    
    df_feature = df_feature.append(series_temp_feature,ignore_index = True)
    index_num +=1
  return df_feature
  
  
