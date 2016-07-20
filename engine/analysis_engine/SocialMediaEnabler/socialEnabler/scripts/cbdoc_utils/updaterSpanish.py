from ..emotion_taggers.classifier import emotionTtagger, important_noun_creator
import re

products = ["oficina","escritorio","librero"]
services = ["limpieza"]
rprod = re.compile("|".join(r"\b%s\b" % w.lower() for w in products), re.I)
rserv = re.compile("|".join(r"\b%s\b" % w.lower() for w in services), re.I)

def create_product_array(text):
    products_array = re.findall(rprod, text.lower())
    product_set = set(products_array)
    products_array = list(product_set)
    return products_array

def create_service_array(text):
    services_array = re.findall(rserv, text.lower())
    service_set = set(services_array)
    service_array = list(service_set)
    return service_array

def create_service_field(text):
    services  = create_service_array(text)
    sfield = []
    for s in services:
        sfield.append({"name":s})
    print sfield
    return sfield

def create_product_field(text):
    products = create_product_array(text)
    pfield = []
    for p in products:
        pfield.append({"name":p})
    return pfield

def create_emotions_fields(text):
    emotions = emotionTtagger(text)
    emotion_list = ["excited","happy","neutral","sad","angry"]
    sizes = [len(emotions[emotion_list[0]]),len(emotions[emotion_list[1]]),len(emotions[emotion_list[2]]),len(emotions[emotion_list[3]]),len(emotions[emotion_list[4]])]
    ind = sizes.index(max(sizes))
    total = emotion_list[ind] #TODO better assumption???
    print total
    return emotions,total

def create_nouns_field(text):
    nouns = important_noun_creator(text)
    keep_nouns = []
    for noun in nouns:
        if noun not in products:
            if noun not in services:
                keep_nouns.append(noun)
    return keep_nouns

def update_fields(json_text):
    text = (json_text["text_no_url_es"]).replace('_hashtag_',' ')
    json_text["products"]=create_product_field(text)
    json_text["services"]=create_service_field(text)
    emotions = create_emotions_fields(text)
    json_text["senti_tag"]=emotions[1]
    json_text["emotions"]=emotions[0]
    json_text["nouns"] = create_nouns_field(text)
    json_text["text_no_url"]=json_text["text_no_url_es"]
    return  json_text
# print create_service_field("This is a polish sofa for rental and that is a chair next to the sofa")
