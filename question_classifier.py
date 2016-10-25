import re
import nltk
import random
import pickle

#classifier
def question_features(post):
    features = {}
    #print('In QF')
    #print('POST = ',post)
    for word in nltk.word_tokenize(post):
        #print('WORD = ',word)
        #print('contains(%s)'%word.lower())
        features['contains(%s)'%word.lower()] = True
    #print('FEATURES = ',features)
    return features

def question_features2(post):
    return {'first_word':post.split(' ')[0],'second_word':post.split(' ')[1],'third_word':post.split(' ')[2]}

def get_class(d,post):
    #print('Inside GC')
    #print('d.get(post) = ',d.get(post))
    return d.get(post)

def read_qs_from_file():
    words = open(r"F:\Projects\Research\Major Project\Code\Major file old\training_set5.txt").read().split("\n")
    #words = open("training_set5.txt").read().split("\n")
    new_list = []
    for word in words:
        if word.find("ABBR")!=0:
            new_list.append(word)
    words = new_list
    
    return words

def extract_wordtags(words):
    wordtags = []
    for word in words:
        wordtags.append(word.split(' ')[0])
    return wordtags

def remove_subclasses(wordtags):
    for i in range(0,len(wordtags)):
        wordtags[i] = re.sub('[a-z]+',"",wordtags[i])
    return wordtags

def remove_tags(words):
    for i in range(0,len(words)):
        words[i] = ' '.join(map(str,words[i].split(' ')[1:]))
    return words

def make_dictionary(words,wordtags):
    keys = words
    values = wordtags
    d = {keys[n]:values[n]for n in range(len(keys))}
    return d

def prepare_pickle_file(classifier):
    f = open('my_classifier.pickle','wb')
    pickle.dump(classifier,f)
    f.close()

def prepare_word_and_wordtags():
    #print('In PWAW')
    words = read_qs_from_file()
    #print('WORDS = ',words)
    wordtags = extract_wordtags(words)
    #print('EXTRACT WORDTAGS = ',wordtags)
    wordtags = remove_subclasses(wordtags)
    #print('REMOVE SUBCLASS WORDTAGS = ',wordtags)
    words = remove_tags(words)
    #print('WORDS = ',words)
    d = make_dictionary(words,wordtags)
    #print('D = ',d)
    
    return d,words

def train_classifier(d,words):
    featuresets=[(question_features(word),get_class(d,word)) for word in words]
    #print('Indise TC')
    #print('FEATURESETS = ',featuresets)
    size = int(len(featuresets)*0.99)
    train_set,test_set = featuresets[size:],featuresets[:size]
    #print('size = ',size)
    #print('TRAIN_SET = ',train_set)
    #print('TEST_SET = ',test_set)
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    #print('CLASSIFIER = ',classifier)
    print('Accuaracy is :\t',nltk.classify.accuracy(classifier,test_set))
    return classifier

#Change the question type by the NaiveBayes QC tothe answer type which will be found by the NER

def find_answer_type2(question_type,question):
    if question_type == "DESC:":
        return "DESC"
    if question_type == "ENTY:":
        return "ORGANIZATION"
    if question_type == "HUM:":
        return "PERSON"
    if question_type == "ABBR:":
        return "ABBR"
    abbs=['full form','stands for','stand for','acronym']
    for abb in abbs:
        if question.find(abb)!=-1:
            return "ABBR"
    if question_type == "LOC:":
        return "LOCATION"
    if question_type == "NUM:":
        if question.find("when")!=-1:
            return "DATE"
        else :
            return "NUM"

def find_answer_type(question):
    abbs=['full form','stands for','stand for','acronym']
    for abb in abbs:
        if question.find(abb)!=-1:
            return "ABBR"
    first_word = question.split()[0].lower()
    if first_word=="who":
        return "PERSON"
    if first_word=="where":
        return "LOCATION"
    if first_word=="when":
        return "DATE"

def ret_answer_type2(question):
    #Making dictionary out of word and wordtags
    #print('In RAT2')
    d,words = prepare_word_and_wordtags()
    #print('d=',d)
    #print('words=',words)
    #Training classifier
    classifier = train_classifier(d,words)
    #print('QUESTION_FEATURES = ',question_features(question))
    question_type=classifier.classify(question_features(question))
    print('QUESTION_TYPE = ',question_type)
    answer_type=find_answer_type2(question_type,question)
    print('ANSWER_TYPE = ',answer_type)
    return answer_type

def ret_answer_type(question):
    answer_type = find_answer_type(question)
    return answer_type

#Prepare pickle file so that classifier can be opened from another file
#prepare_pickle_file(classifier)
#question = raw_input()
#print(classifier.classify(question_features(question)))
