from nltk.corpus import sentiwordnet as swn
from nltk.corpus.reader import WordNetError

# returns the average positive, negative and objective scores from the first 3 synsets of a given word
# acceptable pos tags should be compatible with NLTK postagger output
# returns -1,-1,-1 if not able to find synsets
def get_scores(word , postag):
    count = 0
    pos_score = 0
    neg_score = 0
    obj_score = 0
    tag = postag_to_sentiwordnet_tag_restricted(postag)
    if tag is None:
        return -1,-1,-1
    try:
        for i in range(1,4):
            word_scores = swn.senti_synset(word+'.'+tag+'.0'+str(i))
            if word_scores is None:
                return -1,-1,-1
            # print word_scores
            # print word_scores.obj_score()
            pos_score += word_scores.pos_score()
            neg_score += word_scores.neg_score()
            obj_score += word_scores.obj_score()
            count += 1
    except WordNetError:
        print "oups"
    if count > 0:
        pos_score /= count
        neg_score /= count
        obj_score /= count
    return pos_score,neg_score,obj_score

# NTLK postagger tag transformed to sentiwordnet POS tag
def postag_to_sentiwordnet_tag(tag):
    if tag in ["NN","NNS","NNP","NNPS"]:
        return "n"
    elif tag in ['VB','VBN','VBD','VBG','VBZ','VBP']:
        return "v"
    elif tag in ["JJ","JJR","JJS"]:
        return "a"
    return "n" #TODO should think of a better default

def postag_to_sentiwordnet_tag_restricted(tag):
    if tag in ["NN","NNS","NNP","NNPS"]:
        return "n"
    elif tag in ['VB']:
        return "v"
    elif tag in ["JJ"]:
        return "a"
    return None #TODO should think of a better default

