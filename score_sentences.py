import operator
import answer_processing
from answer_processing import NER_string

def add_to_index(index,keyword):
    if keyword in index:
        index[keyword] += 1
    else:
        index[keyword] = 1

def cal_score(diction):
    #print('In CS')
    score = 0
    lis = diction.values()
    #print('DICTION = ',diction)
    #print('LIS = ',lis)
    for l in lis:
        #print('l = ',l)
        score += l
    #print('SCORE = ',score)
    return score

def extract_text(nertext):
    s1 = nertext.find('</FORM>')
    s2 = nertext.find('</div>',s1 + 1)
    s3 = nertext.find('</div>',s2 + 1)
    s4 = nertext.find('</div>',s3 + 1)
    s5 = nertext.find('\n',s4)
    s6 = nertext.find('<div id',s5 + 1)
    return nertext[s5+ 1:s6]

def read_file(query,answer_type):
    score = []
    #print('In RF')
    nertext = NER_string(open('C:\Python27\BTP\imp_info.txt').read())
    #print('reading')
    final = extract_text(nertext)
    final = final.split('.')
    #print('FINAL = ',final)
    l = [] #List for scoring bool values to include that sentences in imp_sentences file or not
    for f in final:
        #print('F = ',f)
        if f.find(answer_type)!= -1:
            #print('APPEND 1')
            l.append(1)
        else:
            #print('APPEND 0')
            l.append(0)
    i = 0 #For printing the sentence number
    j = 0 #For incrementing list pointer
    sentences = open('C:\Python27\BTP\imp_info.txt').read().split('.')
    keys=[]
    #print('L = ',l)
    #print('sentences=',sentences)
    for s in sentences:
        s = s.lower()
        s = s.split(' ')
        #print('S = ',s)
        #print('QUERY = ',query)
        #print('L[J] = ',l[j])
        #print('SCORE = ',score)
        if l[j] == 0:
            score.append(0)
            j += 1
            continue
        dict = {}
        #print('SKIP')
        for w in s:
            for q in query:
                #print('W = ',w)
                #print('Q = ',q)
                if w == q:
                    #print('W = %s Q = %s',w,q)
                    add_to_index(dict,q)
                    break
        #print('DICT = ',dict)
        #print('SENTENCE : ',i,cal_score(dict))
        i += 1
        score.append(cal_score(dict))
        sid = []
        for i in range(0,len(sentences)):
            sid.append(i)
        keys = sid
        values = score
    d = {keys[n]:values[n] for n in range(0,len(keys))}

    return d,final

def sort_sentences(score):
    sorted_score = sorted(score.iteritems(),key = operator.itemgetter(1),reverse=True)
    return sorted_score

def ret_maxscore_sentences(newscore):
    maxi = newscore[0][1]
    for i in range(0,len(newscore)):
        if newscore[i][1]!= maxi:
            break;
    return i,maxi

def write_imp_sentences(newscore):
    #imp_sentences contains the list(index number) of the sentences which have the maximum score
    imp_sentences = []
    index,maxi = ret_maxscore_sentences(newscore)
    for i in range(0,index):
        imp_sentences.append(newscore[i][0])
    #print('INDEX = ',index)
    #print('IMP_SENTENCS = ',imp_sentences)
    sentences = open('C:\Python27\BTP\imp_info.txt').read().split('.')
    #print('s=')
    #for s in sentences:
        #print(s)
    outfile = open('C:\Python27\BTP\imp_sentences.txt','a')
    #outfile.seek(0)
    #outfile.truncate()
    for i in range(0,index):
        outfile.write(sentences[imp_sentences[i]]+'.')
    outfile.close()
    return imp_sentences,maxi

def score_sentences(query,answer_type):
    #print('In SS')
    score,final = read_file(query,answer_type)
    newscore = sort_sentences(score)
    if newscore == []:
        #print('ZERO')
        newscore = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0)]
    if len(newscore) < 7:
        for i in range(len(newscore),8):
            newscore.append((i,0))
    
    #print('NEWSCORE = ',newscore)
    imp_sentences,maxi = write_imp_sentences(newscore)
    #print('FINAL = ',final)
    #print('IMP_SENTENCS = ',imp_sentences)
    #print('MAXI = ',maxi)
    return final,imp_sentences,maxi


