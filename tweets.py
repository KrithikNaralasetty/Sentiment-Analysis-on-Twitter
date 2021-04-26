import os
import tweepy as tw
import pandas as pd

def authenticate():
	consumer_key = "ugDc5vsJPr72kxiHbISR15SJU"
	consumer_secret_key = "wDFQ4xRrUTMsZfhqGRKdQiqF2ZQ6YHDalEtfBpUwUARPhkJyPL"
	access_token = "2377130262-okTKiPKVWKt0pGwgj4wyPPUFRPpvEuyZvVtOrKw"
	access_token_secret = "rrONH7xppgmsWct3uUAjwFJj65fcEjuQcwgmFYVHQ309c"
	auth = tw.OAuthHandler(consumer_key,consumer_secret_key)
	auth.set_access_token(access_token,access_token_secret)
	return tw.API(auth,wait_on_rate_limit=True)

if __name__ == "__main__":
	api = authenticate()
	search_user = str(input("Enter the Twitter Id of a person: "))
	try:
		Tweets = tw.Cursor(api.user_timeline,search_user,exclude_replies = True).items(100)
		for tweet in Tweets:
			print(str(tweet.text),end = "\n")
			# entity = tweet.entities
			# if entity['urls'] != []:
			# 	print(entity['urls'][0]['url'],end = "\n")
			# else:
			# 	print(entity)
		print(tweet.user.id,end = "\n")
	except tw.TweepError:
		print("Error Occured")