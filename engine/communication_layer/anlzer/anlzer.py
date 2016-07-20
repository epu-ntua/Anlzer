#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from querymakers import  get_sources, get_popular_hashtags, get_sentiments, get_num_of_docs_with_all_terms, get_inouns, get_iproducts, get_isenti_perps, get_isentiments, get_iservices, get_text_from_results, get_daily_histogram
import json
from utils import validate_parameters

app = Flask(__name__)

@app.route('/anlzer/api/v1.0/basic_stats/', methods=['GET'])
def get_stats():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    # make query
    text = get_sources(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['sources']['buckets']
    sources_json = {value:0 for value in ["twitter","facebook","instagram"]}
    total = res['hits']['total']
    for source in resu:
        sources_json[source['key']] = source['doc_count']
    final = {}
    final['sources'] = sources_json
    final['docs_with_all_keywords'] = int(get_num_of_docs_with_all_terms(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"]))
    final['total_docs'] = total
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/top_hashtags/', methods=['GET'])
def get_top_hashtags():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_popular_hashtags(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['sources']['buckets']
    # sources_json = {}
    hashtags = []
    for source in resu:
        new_hash = {}
        new_hash["name"] = source['key']
        new_hash["count"] = source['doc_count']
        hashtags.append(new_hash)
    final = {}
    final['hashtags'] = hashtags
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/sentiments/', methods=['GET'])
def get_emotions():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_sentiments(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['sources']['buckets']
    sources_json = {value:0 for value in ["angry","sad","neutral","happy","excited"]}
    total = res['hits']['total']
    for source in resu:
        sources_json[source['key']] = source['doc_count']
    final = {}
    final['sentiments'] = sources_json
    final['total_docs'] = total
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/nouns/', methods=['GET'])
def get_nouns():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_inouns(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['nouns']['buckets']
    final = {}
    final['nouns'] = resu
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/productsser/', methods=['GET'])
def get_products():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_iproducts(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['products']['buckets']
    final = {}
    final['products'] = resu
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/servicespro/', methods=['GET'])
def get_services():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_iservices(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['services']['buckets']
    final = {}
    final['services'] = resu
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/sentiwords/', methods=['GET'])
def get_senti_words():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_isentiments(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    final = {}
    final['sentiments'] = text
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/pspairsenti/', methods=['GET'])
def get_senti_pspairs():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_isenti_perps(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    res = json.loads(text)
    resu = res['aggregations']['services']['buckets']
    final = {}
    final['services'] = resu
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/textresults/', methods=['GET'])
def get_text_results():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_text_from_results(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    final = {}
    final['results'] = text
    return jsonify(**final)

@app.route('/anlzer/api/v1.0/daily_histogram/', methods=['GET'])
def get_daily_results():
    val = validate_parameters(request)
    if "error" in val:
        abort(make_response(val["error"],400))
    text = get_daily_histogram(val["start"],val["end"],val["keywords"],val["sources"],val["accounts"],val["languages"],val["project"])
    final = {}
    final['results'] = text
    return jsonify(**final)

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')
