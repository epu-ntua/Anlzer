def build_popular__hashtags_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    query = '{ "size": 0, "aggs": { "sources": { "terms": { "field": "doc.entities.hashtags.text", "size": 10, "order": ' \
            '{ "_count": "desc" } } } }, "query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
             '"filter": { "bool": { "must": ' \
            '[ ' \
            '{"terms" : { "doc.lang" : ['+languages+']}},' \
            + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } }' \
            ' ], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_social_source_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, "aggs": { "sources": { "terms": { "field": "doc.source", "size": 5, "order": ' \
            '{ "_count": "desc" } } } }, "query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must": ' \
            '[ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } }' \
            ' ], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_social_sentiment_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, "aggs": { "sources": { "terms": { "field": "doc.senti_tag", "size": 5, "order": ' \
            '{ "_count": "desc" } } } }, "query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
             '"filter": { "bool": { "must": ' \
            '[ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } } ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_require_all_terms_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ 	"size": 0, ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", ' \
            '"query": '+keywords+', "default_operator": "AND" } }, ' \
            '"filter": { "bool": { "must": ' \
            '[' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } }' \
            '], "must_not": [] } } } '
    print query
    return query

def build_get_nouns_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, "aggs": { "nouns": { "terms": { "field": "doc.nouns", "size": 50, "order": ' \
            '{ "_count": "desc" } } } }, "query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must": ' \
            '[ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } } ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_get_services_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, ' \
            '"aggs": { "services": { "terms": { "field": "doc.services.name", "size": 5, "order": { "_count": "desc" } }, ' \
            '"aggs": { "products": { "terms": { "field": "doc.products.name", "size": 5, "order": { "_count": "desc" } } } } } },' \
            '"query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must":' \
            ' [ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } } ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_get_products_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, ' \
            '"aggs": { "products": { "terms": { "field": "doc.products.name", "size": 5, "order": { "_count": "desc" } }, ' \
            '"aggs": { "services": { "terms": { "field": "doc.services.name", "size": 5, "order": { "_count": "desc" } } } } } },' \
            '"query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must":' \
            ' [ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } } ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_get_sentiments_per_ps_query(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, ' \
            '"aggs": { "services": { "terms": { "field": "doc.services.name", "size": 5, "order": { "_count": "desc" } }, ' \
            '"aggs": { "products": { "terms": { "field": "doc.products.name", "size": 5, "order": { "_count": "desc" } }, ' \
            '"aggs": { "sentiment": { "terms": { "field": "doc.senti_tag", "size": 5, "order": { "_count": "desc" } } } } } } } },' \
            '"query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must": ' \
            '[ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } },' \
            '{"exists": {"field": "doc.services.name"}},{"exists": {"field": "doc.products.name"}} ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_get_words_per_sentiment(start,end,keywords,sentiment,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, ' \
            '"aggs": { 	 "words": { "terms": { "field": "doc.emotions.'+sentiment+'", "size": 10, "order": { "_count": "desc" } } } },' \
            '"query": { "filtered": { ' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must": ' \
            '[ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } } ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query

def build_get_result_text(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ');
    query = '{"fields":["doc.text","doc.user_screen_name","doc.user_name","doc.lang","doc.created_at","doc.source","doc.senti_tag"],' \
            '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": ' \
            '{ "must": [' \
            '{ "terms": { "doc.lang": ['+languages+'] } }, ' \
             + accounts_filter + \
            '{ "terms": { "doc.source": ['+sources+'] } }, ' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } }' \
            '], ' \
            '"must_not": [] } } }'
    print query
    return query

def build_get_daily_histogram(start,end,keywords,sources,accounts,languages,project):
    accounts_filter = ""
    if not (accounts=="\"*\""):
        accounts_filter = '{"terms" : { "doc.user_screen_name" : ['+accounts+']}},'
    keywords = keywords.replace(',',' ')
    query = '{ "size": 0, ' \
            '"aggs": { "daily_results": { "date_histogram": { "field": "doc.created_at", "interval": "day", "format": "yyyy-MM-dd" } } },' \
            '"query": { "filtered": { ' \
    '"query": { "query_string": { "default_field": "doc.text_no_url", "query": '+keywords+' } }, ' \
            '"filter": { "bool": { "must": ' \
            '[ ' \
                '{"terms" : { "doc.lang" : ['+languages+']}},' \
     + accounts_filter + \
    '{"terms" : { "doc.source" : ['+sources+']}},' \
            '{ "range": { "doc.created_at": { "gte": '+start+', "lte": '+end+', "format": "epoch_millis" } } } ' \
            '], ' \
            '"must_not": [] } } } } }'
    print query
    return query



