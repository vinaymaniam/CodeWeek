# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 19:08:07 2018

@author: Alinna Chen
"""

import os
import json
from datetime import datetime, timedelta
import pandas as pd

from newsapi import NewsApiClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer # dict doesnt use porter stem


def newsByCompanyName(companies, N):
    '''
    Get news articles for given companies and given amount of days
    
    param: companies (dict) of company names as keys and position as values
    param: N (int) number of days of news to search for
    '''
    from_date = (datetime.now() - timedelta(days=N)).strftime("%Y-%m-%d")
    newsapi = NewsApiClient(api_key='68bc4b7a03e24374b6b55d7c080825c3')
    result= dict()
    for company in companies:
        wordsToSearchFor = company  # TODO: enhance search by searching for keywords related to the company and not just the name
        all_articles = newsapi.get_everything(q=wordsToSearchFor, 
                                              sources='bbc-news, cnbc',
                                              from_param=from_date,
                                              language='en',
                                              sort_by='relevancy')
        result[company] = all_articles
        
    return result


def getStem (tokenizedArticle):
    stemmer = SnowballStemmer("english")
    new_list = []
    for word in tokenizedArticle:
        new_list.append(stemmer.stem(word))
    return new_list


def getScore(bagOfWords, dictionary):
    score= 0 
    for word in bagOfWords:
        if word in dictionary:
            score =+ 1
        else:
            pass
    return score


def containsPolarityChange(bagOfWords):
    if 'not' in bagOfWords or 'dont' in bagOfWords or 'wont' in bagOfWords:
        return True
    else:
        return False

def getDictionaries():
    tokenizer = RegexpTokenizer(r'\w+')
    result = {}
    hiv4Dict = pd.read_csv('HIV4Dictionary.csv')
    positiveWords = hiv4Dict.Entry[hiv4Dict.Positiv=='Positiv']
    negativeWords = hiv4Dict.Entry[hiv4Dict.Negativ=='Negativ']
    result['positive'] = [tokenizer.tokenize(item.lower())[0] for item in positiveWords]
    result['negative'] = [tokenizer.tokenize(item.lower())[0]  for item in negativeWords]
    
    return result


def getSentiment(text, dictionary):
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized = tokenizer.tokenize(text)
    bagOfWords = getStem(tokenized)
    score = getScore(bagOfWords, dictionary)
    
    if containsPolarityChange(bagOfWords):
        score = -1 * score
        
    return score

def aggregate(sentiments):
    # TODO: change this to a more meaningful aggregate, currently it is a simple average
    if sentiments:
        return sum(sentiments)/len(sentiments)
    else:
        return 0

def main():
    result = {}
    top20Positions = {'Apple':1000, 'Google':500, 'Berkshire':100} # TODO: link this to the trades
    news = newsByCompanyName(top20Positions, 1)
    dictionaries = getDictionaries()
    dictionaryToUse = dictionaries['positive'] # TODO: we can explore using both the positive and negative dictionary
    
    for company in top20Positions:
        articles = news[company]['articles']
        
        # can use 'title' or 'description' or 'content'
        sentiments = [getSentiment(article['title'], dictionaryToUse) for article in articles]
        
        result[company] = {'position':top20Positions[company], 
                          'sentiment':aggregate(sentiments),
                          'articles': articles}
    
    with open('back_end_output.json', 'w') as outfile:  
        json.dump(result, outfile)
        
if __name__ == "__main__":
    main()