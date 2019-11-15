"""Prediction of Users based on Tweet embeddings."""
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA

def predict_user(user1_name, user2_name, tweet_text, cache=None):
    """Determine and return which user is more likely to say something"""
    user_set = pickle.dumps((user1_name, user2_name))
    if cache and cache.exists(user_set):
        log_reg = pickle.loads(cache.get(user_set))
    else:
        #if not already in the cache, we add users as user 1 and user 2
        user1 = User.query.filter(User.name == user1_name).one()#pull username
        user2 = User.query.filter(User.name == user2_name).one()
        #get their embeddings
        user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])#numpy array embeddings
        user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
        #split into array
        embeddings = np.vstack([user1_embeddings, user2_embeddings])#to series of 0 and 1 to train
        labels = np.concatenate([np.ones(len(user1.tweets)),#for length
                                 np.zeros(len(user2.tweets))])#zeros for length of 2
        #fit the LogisticRegression model
        log_reg = LogisticRegression().fit(embeddings, labels)#fit model on embeddings and labels
        cache and cache.set(user_set, pickle.dumps(log_reg))#optional caching
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')#tweet embedding with basilica
    return log_reg.predict(np.array(tweet_embedding).reshape(1, -1))#return array