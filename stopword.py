import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
from string import punctuation

stop_words = set(stopwords.words('english'))
spell=SpellChecker()
punctuation=punctuation.replace("'","£")
data = pd.read_csv('testtwitter3.csv')

for i in range(data.iloc[:,0].size):
    sentence=data.loc[i,'noURLtextpic']
    word_tokens = word_tokenize(sentence)
    for j in range(0, len(word_tokens)):
        word_tokens[j] = spell.correction(word_tokens[j])

    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = [p for p in filtered_sentence if not p in punctuation]
    data.loc[i,'finaldata']=' '.join(filtered_sentence)

data.to_csv('testtwitter3.csv')