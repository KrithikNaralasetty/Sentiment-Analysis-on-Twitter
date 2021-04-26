# importing necessary modules and functions
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
import tweepy as tw
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import pickle
from keras.models import load_model

# loadnig tokenizer
# csv = './sentiment_tweets.csv'
# my_df = pd.read_csv(csv,index_col=0)
# x = my_df.text
# y = my_df.target
# SEED = 2000
# x_train, x_validation_and_test, y_train, y_validation_and_test = train_test_split(x, y, test_size=.02, random_state=SEED)
# tokenizer = Tokenizer(num_words=100000)
# tokenizer.fit_on_texts(x_train)
# with open('tokenizer.pickle','wb') as handle:
#     pickle.dump(tokenizer,handle,protocol = pickle.HIGHEST_PROTOCOL)
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# authentication for twitter API


def authenticate():
    consumer_key = "ugDc5vsJPr72kxiHbISR15SJU"
    consumer_secret_key = "wDFQ4xRrUTMsZfhqGRKdQiqF2ZQ6YHDalEtfBpUwUARPhkJyPL"
    access_token = "2377130262-okTKiPKVWKt0pGwgj4wyPPUFRPpvEuyZvVtOrKw"
    access_token_secret = "rrONH7xppgmsWct3uUAjwFJj65fcEjuQcwgmFYVHQ309c"
    auth = tw.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth, wait_on_rate_limit=True)

# Retrieving tweets from Twitter using the Twitter API


def get_tweets():
    api = authenticate()
    search_user = str(input("Enter the Twitter Id of a person: "))
    x_input = []
    n = int(input("Enter number of Recent Tweets to anlyze: "))
    try:
        Tweets = tw.Cursor(api.user_timeline, search_user,
                           exclude_replies=True).items(n)
        for tweet in Tweets:
            x_input.append(tweet.text)
    except tw.TweepError:
        print("Error Occured")
    return (x_input)

# getting the model preditions


def predictions(tweet_texts, tokenizer):
    sequences_test = tokenizer.texts_to_sequences(tweet_texts)
    x_test_seq = pad_sequences(sequences_test, maxlen=45)
    model = load_model('CNN_best_weights.02-0.8292.hdf5')
    output_senti = model.predict(x_test_seq)
    test_result = []
    for i in output_senti:
        test_result.append(i[0])
    return test_result

# function to clean tweets


def tweet_cleaner(text):
    tok = WordPunctTokenizer()
    pat1 = r'@[A-Za-z0-9]+'
    pat2 = r'https?://[A-Za-z0-9./]+'
    combined_pat = r'|'.join((pat1, pat2))
    www_pat = r'www.[^ ]+'
    negations_dic = {"isn't": "is not", "aren't": "are not", "wasn't": "was not", "weren't": "were not",
                     "haven't": "have not", "hasn't": "has not", "hadn't": "had not", "won't": "will not",
                     "wouldn't": "would not", "don't": "do not", "doesn't": "does not", "didn't": "did not",
                     "can't": "can not", "couldn't": "could not", "shouldn't": "should not", "mightn't": "might not",
                     "mustn't": "must not", "I'm": "I am", "he's": "he is", "she's": "she is", "that's": "that is", "where's": "where is",
                     "how's": "how is", "\'ll": " will", "\'re": " are", "\'d": " would", "\'ve": " have", "let's": "let us", "you're": "you are", "it's": "it is"}
    neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    stripped = re.sub(combined_pat, '', souped)
    stripped = re.sub(www_pat, '', stripped)
    lower_case = stripped.lower()
    neg_handled = neg_pattern.sub(
        lambda x: negations_dic[x.group()], lower_case)
    letters_only = re.sub("[^a-zA-Z]", " ", neg_handled)
    words = [x for x in tok.tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()


# main program
if __name__ == '__main__':
    x_input = get_tweets()
    n = len(x_input)
    print("Cleaning and parsing the tweets...\n")
    clean_tweet_texts = []
    for i in range(0, n):
        clean_tweet_texts.append(tweet_cleaner(x_input[i]))
    print("Cleaned and parsed Tweets...")
    print("Predicting the values...")
    output_senti = predictions(clean_tweet_texts, tokenizer)
    tweet_number = list(i for i in range(1, n+1))
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(tweet_number, output_senti, color='r')
    plt.ylabel("Sentiment scale")
    plt.xlabel("Recent "+str(n)+" tweets")
    plt.show()
    average = sum(output_senti)//n
    with average as i:
        if i in range(0, 0.46):
            print("The user is a negative influencer")
        elif i in range(0.46, 0.64):
            print("The user is a neutral influencer")
        else:
            print("The user is a positie inffuencer")