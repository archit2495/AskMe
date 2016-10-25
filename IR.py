import urllib
import urllib2
import re

def clean_para(para):
    
    para = re.sub('<[^>]*>',"",para)
    para = re.sub('&[^;]*;',"",para)
    #para = re.sub(r'\[[0-9]+\]'," ",para)
    para = re.sub(r'\[\.\.\.\]'," ",para)
    para = re.sub(r'more>'," ",para)
    para = re.sub(r'>'," ",para)
    para = re.sub(r'<'," ",para)
    para = re.sub(r'[\.]+',".",para)
    para = re.sub(r'[\.]+',".",para)
    para = re.sub(r'Mr\.',"",para)
    para = re.sub(r'Mrs\.',"",para)
    para = re.sub(r'Dr\.',"",para)
    para = re.sub(r'Shri\.',"",para)
    para = re.sub(r',',"",para)
    """
    
    para = re.sub(r'<[a-zA-Z0-9/\\\-%#@()!\$:\^`~&|\*\"\'\,\[\]=\+\._;?]+>',"",para)
    #para = re.sub(r'[0-9]',"",para)
    para = re.sub(r'\[\.\.\.\]',"",para)
    para = re.sub(r'more>',"",para)
    para = re.sub(r'>',"",para)
    para = re.sub(r'<',"",para)
    para = re.sub(r'[\.]+',".",para)
    para = re.sub(r'[\.]+',".",para)
    para = re.sub(r'Mr\.',"",para)
    para = re.sub(r'Mrs\.',"",para)
    para = re.sub(r'Dr\.',"",para)
    para = re.sub(r',',"",para)
    
    #para = re.sub(r'[^a-zA-Z0-9/\\\-%#@()!\$:\^`~&|\*"\'\,\[\]=\+\._;?<>]',"",para)
    #para = ''.join(para.split())
    """
    return para
def write_file(text):
    write_para = clean_para(text)
    fob = open('C:\Python27\BTP\para.txt','a')
    fob.write(write_para)
    fob.write('\n\n')
    fob.close

def get_next_target(page):
    start_text = page.find('<span class="st">')
    end_text = page.find('</span>',start_text + 1)
    text = page[start_text + 17:end_text]
    return text,end_text

def ret_sourcecode(query):
    #print(query)
    query = query.replace(' ','+')
    #print(query)
    url = "http://www.google.com/search?q="+query
    req = urllib2.Request(url,headers = {'User-Agent':'Chrome/53.0.2785.143'})
    #req = urllib2.Request(url)
    #print('req',req)
    com = urllib2.urlopen(req)
    #print('com',com)
    #print('com.read',com.read())
    return com.read()

def get_all_links(query):
    source_code = ret_sourcecode(query)
    page = source_code
    #print('page=',page)
    for b in range(0,10):
        text,endpos = get_next_target(page)
        #print('text=',text)
        #print('endpos=',endpos)
        write_file(text)
        page = page[endpos:]







