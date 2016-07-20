import nltk
from nltk import word_tokenize

# return all nouns in a given text
def get_nouns(input_text):
    text = word_tokenize(input_text)
    postags = nltk.pos_tag(text)
    nouns = []
    for tag in postags:
        if tag[1]=='NN' or tag[1]=='NNS' or tag[1]=='NNP' or tag[1]=='NNPS':
            nouns.append(tag[0])
    return nouns

#return all adjectives in a given text
def get_adjectives(input_text):
    text = word_tokenize(input_text)
    postags = nltk.pos_tag(text)
    adjectives = []
    for tag in postags:
        if tag[1]=='JJ' or tag[1]=='JJR' or tag[1]=='JJS':
            adjectives.append(tag[0])
    return adjectives

#return all verbs in a given text
def get_verbs(input_text):
    text = word_tokenize(input_text)
    postags = nltk.pos_tag(text)
    verbs = []
    for tag in postags:
        if tag[1]=='VB' or tag[1]=='VBN' or tag[1]=='VBD' or tag[1]=='VBG' or tag[1]=='VBZ' or tag[1]=='VBP':
            verbs.append(tag[0])
    return verbs

#return only the nouns found in a list of keywords like the one returned by RAKE, i.e. [(keyword,X),(keyword,X)...]
def filter_nouns(input_text,keywords):
    nouns = get_nouns(input_text)
    filtered = [k for k in keywords if k[0] in nouns]
    return filtered

#return only the adjectives found in a list of keywords like the one returned by RAKE, i.e. [(keyword,X),(keyword,X)...]
def filter_adjectives(input_text,keywords):
    adjectives = get_adjectives(input_text)
    filtered = [k for k in keywords if k[0] in adjectives]
    return filtered

#http://stackoverflow.com/questions/10106901/elegant-find-sub-list-in-list
def all_noun_expression_finder(text):
    mylist = nltk.pos_tag(word_tokenize(text))
    patterns = [('NNP','NNP'),('NNP','NNPS'),('NN','NN'),('NN','NNS')]
    matches = []
    for pattern in patterns:
        for i in range(len(mylist)-1):
            if mylist[i][1] == pattern[0] and mylist[i+1][1] == pattern[1]:
                matches.append(mylist[i][0]+" "+mylist[i+1][0])
    unique_matches = list(set(matches))
    return unique_matches

def proper_noun_expression_finder(text):
    mylist = nltk.pos_tag(word_tokenize(text))
    patterns = [('NNP','NNP'),('NNP','NNPS')]
    matches = []
    for pattern in patterns:
        for i in range(len(mylist)-1):
            if mylist[i][1] == pattern[0] and mylist[i+1][1] == pattern[1]:
                matches.append(mylist[i][0]+" "+mylist[i+1][0])
    unique_matches = list(set(matches))
    return unique_matches

def get_all_tags(text):
    return nltk.pos_tag(word_tokenize(text))

# def test():
#     input_text = "You are the best."
#     text = word_tokenize(input_text)
#     postags = nltk.pos_tag(text)
#     print postags

