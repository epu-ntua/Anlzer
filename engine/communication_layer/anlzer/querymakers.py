import urllib2
import json
from esQueryUtils import build_social_source_query, build_popular__hashtags_query, build_social_sentiment_query, build_require_all_terms_query, build_get_nouns_query, build_get_words_per_sentiment, build_get_products_query, build_get_services_query, build_get_sentiments_per_ps_query, build_get_result_text, build_get_daily_histogram
__author__ = 'user'

url = "http://[ip]:9200/[index name]/_search?pretty"

def get_sources(start,end,hashtags,sources,accounts,languages,project):
    query = build_social_source_query(start, end, hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_popular_hashtags(start,end,hashtags,sources,accounts,languages,project):
    query = build_popular__hashtags_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_sentiments(start,end,hashtags,sources,accounts,languages,project):
    query = build_social_sentiment_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_inouns(start,end,hashtags,sources,accounts,languages,project):
    query = build_get_nouns_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_iservices(start,end,hashtags,sources,accounts,languages,project):
    query = build_get_services_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_iproducts(start,end,hashtags,sources,accounts,languages,project):
    query = build_get_products_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_isenti_perps(start,end,hashtags,sources,accounts,languages,project):
    query = build_get_sentiments_per_ps_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        return response.read()
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_isentiments(start,end,hashtags,sources,accounts,languages,project):
    sentiments = ["excited","happy","neutral","sad","angry"]
    sentiments_json = {}
    for s in sentiments:
        query = build_get_words_per_sentiment(start,end,hashtags,s,sources,accounts,languages,project)
        try:
            response = urllib2.urlopen(url,query)
            text = response.read()
            res = json.loads(text)
            resu = res['aggregations']['words']['buckets']
            sentiments_json[s] = resu
        except urllib2.URLError as err:
            print(err.message)
            return {}
    return sentiments_json


def get_num_of_docs_with_all_terms(start,end,hashtags,sources,accounts,languages,project):
    query = build_require_all_terms_query(start, end,hashtags,sources,accounts,languages,project)
    try:
        response = urllib2.urlopen(url,query)
        response = response.read()
        res = json.loads(response)
        total = res['hits']['total']
        return total
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_text_from_results(start,end,hashtags,sources,accounts,languages,project):
    query = build_get_result_text(start, end,hashtags,sources,accounts,languages,project)
    url_no_meta = url + '&filter_path=hits.hits.fields.*'
    try:
        response = urllib2.urlopen(url_no_meta,query)
        response = response.read()
        res = json.loads(response)
        if 'hits' in res:
            total = res['hits']
            return total
        else:
            return {"hits":[]}
    except urllib2.URLError as err:
        print(err.message)
        return []

def get_daily_histogram(start,end,hashtags,sources,accounts,languages,project):
    query = build_get_daily_histogram(start, end,hashtags,sources,accounts,languages,project)
    url_no_meta = url + '&filter_path=aggregations.*'
    try:
        response = urllib2.urlopen(url_no_meta,query)
        response = response.read()
        res = json.loads(response)
        if 'aggregations' in res:
            total = res['aggregations']
            return total
        else:
            return {"aggregations":[]}
    except urllib2.URLError as err:
        print(err.message)
        return []
