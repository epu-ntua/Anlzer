from sentiwordnet_utils import get_scores
from ..processors.postagger import get_all_tags

# extremely subjective
def emotionWtagger(word,postag):
    sentiment_scores = get_scores(word,postag)
    if sentiment_scores[0] == -1:
        return "undefined"
    if sentiment_scores[0] > sentiment_scores[1]:
        if 2 * sentiment_scores[0] > sentiment_scores[2]:
            if sentiment_scores[0] > 2 * sentiment_scores[1]:
                return "excited"
            else:
                return "happy"
    elif sentiment_scores[1] > sentiment_scores[0]:
        if 2 * sentiment_scores[1] > sentiment_scores[2]:
            if sentiment_scores[1] > 2 * sentiment_scores[0]:
                return "angry"
            else:
                return "sad"
    return "neutral"

def emotionTtagger(text):
    emotions = {}
    happy = []
    excited = []
    neutral = []
    sad = []
    angry = []
    tags = get_all_tags(text)
    print tags
    #TODO remove duplicates to reduce required time
    for tagset in tags:
        if tagset[1] in ["VB","JJ"]:
            emotion = emotionWtagger(tagset[0],tagset[1])
            if emotion == "happy":
                happy.append(tagset[0])
            elif emotion == "excited":
                excited.append(tagset[0])
            elif emotion == "sad":
                sad.append(tagset[0])
            elif emotion == "angry":
                angry.append(tagset[0])
            elif emotion == "neutral":
                neutral.append(tagset[0])
    happy = list(set(happy))
    excited = list(set(excited))
    neutral = list(set(neutral))
    sad = list(set(sad))
    angry = list(set(angry))
    emotions["happy"]=happy
    emotions["excited"]=excited
    emotions["neutral"]=neutral
    emotions["sad"]=sad
    emotions["angry"]=angry
    print emotions
    return emotions

def important_noun_creator(text):
    nouns = []
    tags = get_all_tags(text)
    for tag in tags:
        if tag[1] in ["NN","NNS","NNP","NNPS"]:
            nouns.append(tag[0])
    return nouns



