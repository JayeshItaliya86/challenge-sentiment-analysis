# Import libraries
import numpy as np 
import pandas as pd
import re
import string

# for all NLP related operations on text
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

# To identify the sentiment of text
from textblob import TextBlob

# To expanding the dispay of text column
pd.options.display.max_columns = 100

# To load the data
data = pd.read_csv("./data/tweets_scraped.csv", encoding="ISO-8859-1")

# To take only the tweet column from the dataset and make a dataframe
df = pd.DataFrame(data['tweet'])

# To remove '@names' from the tweets
def remove_pattern(text, pattern_regex):
    r = re.findall(pattern_regex, text)
    for i in r:
        text = re.sub(i, '', text)
    return text 

# To keep cleaned tweets in a new column called 'tweets'
df['tweets'] = np.vectorize(remove_pattern)(df['tweet'], "@[\w]* | *RT*")

# To remove the links(http | https)
cleaned_tweets = []

for index, row in df.iterrows():
    # Here we are filtering out all the words that contains link
    words_without_links = [word for word in row.tweets.split() if 'http' not in word]
    cleaned_tweets.append(' '.join(words_without_links))

df['tweets'] = cleaned_tweets

# To remove punctuations
string.punctuation

def remove_punctuation(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    text = re.sub("[^a-zA-Z0-9]+", " ", text)
    text = text.lower()
    return text

df['absolute_tweets'] = df['tweets'].apply(lambda x: remove_punctuation(x))

# To remove tweets with empty text
df = df[df['absolute_tweets']!='']

# To reset the index after remove the duplicate rows
df = df.reset_index(drop=True)

# To drop duplicate rows
df = df.drop_duplicates(subset=['tweets'], keep=False)

# To remove the stopwords
# downloading stopwords corpus
nltk.download('stopwords')
stopwords = set(stopwords.words("english"))

stopwords_set = set(stopwords)
cleaned_tweets_stopwords = []

for index, row in df.iterrows():
    
    # filerting out all the stopwords 
    words_without_stopwords = [word for word in row.absolute_tweets.split() if not word in stopwords_set and '#' not in word.lower()]
    
    # finally creating tweets list of tuples containing stopwords(list) and sentimentType 
    cleaned_tweets_stopwords.append(' '.join(words_without_stopwords))
    
df['absolute_tweets'] = cleaned_tweets_stopwords

# To fetch the sentiments using Textblob
def fetch_sentiment_using_textblob(text):
    analysis = TextBlob(text)
    return 'pos' if analysis.sentiment.polarity >= 0 else 'neg'

sentiments_using_textblob = df.absolute_tweets.apply(lambda tweet: fetch_sentiment_using_textblob(tweet))

# To add the sentiment in the dataset
df['sentiment'] = sentiments_using_textblob

# To drop unneeded columns from dataset
df = df.drop(["tweet", "tweets"], axis=1)



