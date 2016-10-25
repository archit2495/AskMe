import operator
def add_to_index(index,keyword):
    if keyword in index:
        index[keyword] += 1
    else:
        index[keyword] = 1

def cal_score(diction):
    score = 0
    lis = diction.values()
    for l in lis:
        score += 1
    return score

def read_file(query):
    score = []
    #print('In RF')
    para = open('C:\Python27\BTP\para.txt').read().split('\n\n')
    #print('para=',para)
    #print('para length=',len(para))
    for p in para:
        p = p.lower()
        #print('p=',p)
        diction = {}
        word = p.split()
        #print('word=',word)
        for w in word:
            #print('word=',w)
            for q in query:
                #print('q=',q)
                if w == q:
                    #print('got it')
                    add_to_index(diction,q)
                    break
        score.append(cal_score(diction))
        paraid = []
        for i in range(0,len(para)):
            paraid.append(i)
        keys = paraid
        values = score
        #print('score = ',score)
        #print('values = ',values)
        #print(keys)
        #print('keys length = ',len(keys))
        #n = 0
        #print('in\n')
        """
        while n<len(keys):
            print(n)
            print(len(keys))
            #print(' ')
            values[n]=keys[n]
            n+=1
        d=keys
        """
    d = {keys[n]:values[n] for n in range(0,len(keys))}
    #print('D = ',d)
    return d

def sort_paras(score):
    sorted_score = sorted(score.iteritems(),key = operator.itemgetter(1),reverse=True)
    return sorted_score

def write_imp_para(newscore):
    imp_info = []
    for i in range(0,7):
        imp_info.append(newscore[i][0])
    para = open('C:\Python27\BTP\para.txt').read().split('\n\n')
    outfile = open('C:\Python27\BTP\imp_info.txt','a')
    #outfile.seek(0)
    #outfile.truncate()
    for i in range(0,7):
        outfile.write(para[imp_info[i]])
    outfile.close()

def score_paras(query):
    score = read_file(query)
    newscore = sort_paras(score)
    write_imp_para(newscore)
