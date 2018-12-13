# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 19:08:07 2018

@author: Alinna Chen
"""

from newsapi import NewsApiClient
from TradeEmulator.companies_list import SYMBOLS, NAMES, INDUSTRY
import os
import json
from datetime import datetime, timedelta


def newsByCompanyName(companies, N):
    '''
    Get news articles for given companies and given amount of days
    
    param: companies (list) of company names
    param: N (int) number of days of news to search for
    '''
    newsapi = NewsApiClient(api_key='68bc4b7a03e24374b6b55d7c080825c3')
    result= dict()
    for company in companies:
        all_articles = newsapi.get_everything(q=company,
                                              sources='bbc-news, cnbc',
                                              from_param=datetime.now() - timedelta(days=N),
                                              language='en',
                                              sort_by='relevancy')
        result[company] = all_articles
        
    return result
# test run
news = newsByCompanyName(['Apple','Google','General Motors'])
