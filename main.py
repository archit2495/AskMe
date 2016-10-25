import nltk
import pickle
import time
import question_classifier
from question_classifier import ret_answer_type2
import IR
from IR import get_all_links 
import formulate_query 
from formulate_query import ret_query
import score_paras
from score_paras import score_paras
import score_sentences 
from score_sentences import score_sentences
import answer_processing 
from answer_processing import answer_processing

where_questions = open('C:\Python27\BTP\Test Data\where.txt')
file1 = open('C:\Python27\BTP\para.txt','a')
file1.seek(0)
file1.truncate()
file1.close()
file1 = open('C:\Python27\BTP\imp_info.txt','a')
file1.seek(0)
file1.truncate()
file1.close()
file1 = open('C:\Python27\BTP\imp_sentences.txt','a')
file1.seek(0)
file1.truncate()
file1.close()

for question in where_questions:
    start = time.time()
    #Taking input
    print('\n')
    print(question)
    question = question.lower()
    #Module 1 - Question Classifier
    answer_type = ret_answer_type2(question)
    if(answer_type==None):
        #print('Hello')
        answer_type = "DESC"
    print('ANSWER TYPE : ',answer_type)
    
        
    #Module 2 - Information Extraction
    
    if answer_type != "ABBR":
        print('Fetching information from Web')
        get_all_links(question)
    #Module 3 - Formulate Query Words
    if answer_type != "ABBR":
        print('Formulating query')
        query = ret_query(question)
        print(query)
    #Moduke 4 - Scoring paras and sentences
    if answer_type != "ABBR":
        print('Scoring paras')
        score_paras(query)
        print('Scoring sentences')
        final,imp_sentences,maxi = score_sentences(query,answer_type)
    #Module 5 - Answer Processing
    print('Scoring Answers')
    answer,answers = answer_processing(answer_type,question,final,imp_sentences)
    print('Answer : ',answer)
    print('Relevant Information : ',answers)
    end = time.time()
    print("The time taken by code is ",end - start)
    #Module 6 - Store questions ans answers
    records = open(r'C:\Python27\BTP\records.txt','a')
    records.seek(0)
    records.truncate()
    records.write('Question:\t' + str(question) + "Answer:\t"+str(answer)+'\n'+"Time:\t"+str(end-start)+'\n\n')
    records.close()
    #Deleting the temporary files
    import os
    directory = 'C:\Python27\BTP'
    os.chdir(directory)
    os.unlink('para.txt')
    os.unlink('imp_info.txt')
    os.unlink('imp_sentences.txt')

