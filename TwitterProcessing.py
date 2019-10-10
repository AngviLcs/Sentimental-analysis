import pandas as pd
import numpy as np
import re
import nltk
from googletrans import Translator
import definedstopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from string import punctuation
from string import digits
import shortwords


#input the source file
data = pd.read_excel('Mergedtwitterdata(without duplicates).xlsx')

#remove urls and case folding
data['noURLtext'] = data['text'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])
data['noURLtext'] = data['noURLtext'].apply(lambda x: re.split('http:\/\/.*', str(x))[0])
data['noURLtextpic'] = data['noURLtext'].apply(lambda x: re.split('.*pic.twitter.com/.*', str(x))[0]).str.lower()

#replace the empty value to be Nan and remove the rows with Nan calue
#data['noURLtextpic'] = data['noURLtextpic'].replace("", np.nan)
data['noURLtextpic'] = data['noURLtextpic'].replace("",np.nan)
data = data.dropna(subset=['noURLtextpic'])

#a method to judge if the sentence contains foreign languange
def judge(keyword):
    return all(ord(c) < 128 for c in keyword.replace('’','').replace('“','').replace('”',''))

#translate the foreign language into English
for i in range(data.iloc[:,0].size):
  if(judge(data.loc[i,'noURLtextpic'])==False):
      translator = Translator()
      data.loc[i, 'noURLtextpic'] = translator.translate(data.loc[i, 'noURLtextpic']).text

#collect short words
short_words=shortwords.getshortwords()

#collect stop words
stop_words=definedstopwords.getList()

#transform the format of short words
for i in range(data.iloc[:,0].size):
    sentence=data.loc[i,'noURLtextpic'].split()
    for j in range(0, len(sentence)):
        if sentence[j] in short_words:
            sentence[j] = sentence[j].replace(sentence[j], short_words[sentence[j]].lower())
    data.loc[i,'noURLtextpic']=" ".join(sentence)

'''
tokenize each sentence into a list of string first and then correct word spelling if wrong,
then remove the stop words and special punctuation
'''
spell=SpellChecker()
for i in range(data.iloc[:,0].size):
    sentence=data.loc[i,'noURLtextpic']
    if(type(sentence)==str):
        word_tokens = word_tokenize(sentence)
        for j in range(0, len(word_tokens)):
            word_tokens[j] = spell.correction(word_tokens[j])

        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = [p for p in filtered_sentence if not p in punctuation]
        data.loc[i,'finaldata']=' '.join(filtered_sentence)

#remove the digit number
remove_digits = str.maketrans('', '', digits)
for i in range(data.iloc[:,0].size):
    if(type(data.loc[i,'finaldata'])==str):
            data.loc[i,'finaldata']=data.loc[i,'finaldata'].translate(remove_digits)

#remove the unnamed columns in dataframe
table = data.columns
table_flag = table.str.contains('Unnamed')
for i in range(len(table)):
    if table_flag[i] :
        data.drop(labels=table[i],axis =1,inplace=True)

#save the data to csv file
data.to_csv('FinalTwitter.csv')

