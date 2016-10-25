import re
import nltk
import mechanize
import abbreviations
from abbreviations import answer_abbreviations

def NER_string(answer_candidate):
    br = mechanize.Browser()
    #print('going in ner')
    br.open('http://nlp.stanford.edu:8080/ner/')
    #print('in ner')
    #for f in br.forms():
        #print(f)

    br.select_form(nr=0)
    br.form['classifier'] = ['english.muc.7class.distsim.crf.ser.gz']
    br.form['input'] = answer_candidate
    br.form['outputFormat'] = ['slashTags']
    br.submit()
    return br.response().read()

def extract_ans(nertext):
    s1 = nertext.find('</FORM>')
    s2 = nertext.find('</div>',s1+1)
    s3 = nertext.find('</div>',s2+1)
    s4 = nertext.find('</div>',s3+1)
    s5 = nertext.find('\n',s4)
    s6 = nertext.find('.',s5+1)
    return nertext[s5+1:s6]

def parse_answer(answer,answer_type):
    #correction needed
    answer = answer.replace(answer_type,"")
    answer = re.sub(r'/',"",answer)
    return answer

def answer_the_question(answers,answer_type,final,imp_sentences):
    i = 0
    #print('In ATQ')
    #print('LEN(ANSWERS) = ',len(answers))
    #print('LEN(IMP_SENTENCES) = ',len(imp_sentences))

    save = ""
    for answer in answers:
        
        #Next line returns source code
        #nertext = NER_string(answer)
        #Next line extracts the tagged sentences from the source code
        #final = extract_ans(nertext)

        #print('ANSWER = ',answer)

        if i >= len(imp_sentences):
            break
        
        final_sentence = final[imp_sentences[i]]
        i += 1
        flag = False
        for f in nltk.word_tokenize(final_sentence):
            if f.find(answer_type)!=-1:
                flag = True
                save = save + parse_answer(f,answer_type) + ' '
            else:
                if flag == True and f.find(answer_type) == -1:
                    return save


    return save

"""
def find_abbreviation(question):
    question = re.sub(r'[a-z]+',"",text)
    return question


def answer_abbreviation(question):
    abbr = find_abbreviation(question)
    #Make this function
    ans = retreive_answer(abbr)
    return ans
"""

def answer_processing(answer_type,question,final,imp_sentences):
    #print('In AP')
    if answer_type == "ABBR":
        return answer_abbreviations(question)
    answers = open('C:\Python27\BTP\imp_sentences.txt').read().split('.')
    #print('ANSWERS = ',answers)

    #print('ANSWERS = ',answers)

    if answer_type == "DESC":
        save = ""
    else:
        save = answer_the_question(answers,answer_type,final,imp_sentences)
    
    return save,answers

