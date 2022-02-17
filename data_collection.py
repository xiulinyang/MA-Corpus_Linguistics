import urllib
from urllib import request
import re
from bs4 import BeautifulSoup as bf
import datetime
import ssl
import random




ssl._create_default_https_context = ssl._create_unverified_context
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


'''FUNCTIONS USED TO EXTRACT DATA FROM PEOPLE'S DAILY AND REFERENCE NEWS'''
# get the data to form the complete web links.
def get_date(start, end):
    datalist = []
    datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        datalist.append(datestart.strftime('%Y-%m-%d'))
    return datalist

# define a function generating all possible urls for newspaper extraction.
def get_url(time1, time2,num):
    base_url ='https://www.laoziliao.net/rmrb/'
    url_collection = []
    for date in get_date(time1,time2):
        url = base_url + str(date) + '-' + '1'
        url_collection.append(url)
    url_collection= random.sample(url_collection, num)
    return url_collection

# Define a function to extract and clean the data from People's Daily/Reference News
def get_text(time1, time2, num):
    collection = get_url(time1, time2, num)
    txt_info ={}
    for i, url in enumerate(collection):
        if i%5 == 0:
            print(str(i) + ' urls have been read. And the current url is ' + str(url))
        req = urllib.request.Request(url=url, headers=headers)
        res = urllib.request.urlopen(req).read().decode('utf-8')
        text = bf(res, 'html.parser').find_all('div', class_='article')
        text2 = re.sub(r'(<br/>)|(</*div\s*(class="article")*>)', '', str(text))
        text3 = re.sub(r'【.*】', ' ', text2)
        text_final = text3.split()
        for para in text_final:
            if len(para) > 30:
                # Usually if the length of a sentence is smaller than 30, it is a title.
                txt_info[para] = url[-12:-8]
    return txt_info

# the function of cutting sentences
def cut_sents(textlist):
    new_sents = {}
    for text, year in textlist.items():
        sents = re.split(r'(。”*"*）*」*|！”*"*）*」*|？”*"*|\.{6}”*」"*）*|……"*）*"*」*|；"*|：)', text.strip(' '))
        for i in range(int(len(sents) / 2)):
            sent = sents[2 * i] + sents[2 * i + 1]
            if '：' not in sent:
                new_sents[sent] = year
    return new_sents



# calculate the number of characters; the text is a list
def textlen(text):
    num = 0
    for i in range(len(text)):
        num += len(text[i])
    return num

# randomly pick out a specific number of sentences to form the corpus of various time spans.
def build_corpus(text, num1, num2):
    corpus_meta ={}
    text = cut_sents(text)
    for i in range(1, len(text)):
        corpus = random.sample(list(text), i)
        text_len = textlen(corpus)
        if num1 < text_len & text_len < num2:
            for sent in corpus:
                corpus_meta[sent] = text[sent]
            return corpus_meta


# save the text and its information
def save_text(docname, dict):
    with open(docname, 'w', encoding='utf-8') as filework:
        for key, value in dict.items():
            filework.write(key + '\t' + str(value) +'\n')


if __name__=='__main__':
    text_46_55 = get_text('1946-05-10', '1955-12-31', 50)
    text_56_65 = get_text('1956-01-01', '1965-12-31', 50)
    text_66_75 = get_text('1966-01-01', '1975-12-31', 50)
    text_76_85 = get_text('1976-01-01', '1985-12-31', 50)
    text_86_95 = get_text('1986-01-01', '1995-12-31', 50)
    text_96_03 = get_text('1996-01-01', '2003-12-31', 50)

    corpus_46_55 = build_corpus(text_46_55, 166500, 167000)
    corpus_56_65 = build_corpus(text_56_65, 166500, 167000)
    corpus_66_75 = build_corpus(text_66_75, 166500, 167000)
    corpus_76_85 = build_corpus(text_76_85, 166500, 167000)
    corpus_86_95 = build_corpus(text_86_95, 166500, 167000)
    corpus_96_03 = build_corpus(text_96_03, 166500, 167000)

    save_text('corpus_46_55.txt', corpus_46_55)
    save_text('corpus_56_65.txt', corpus_56_65)
    save_text('corpus_66_75.txt', corpus_66_75)
    save_text('corpus_76_85.txt', corpus_76_85)
    save_text('corpus_86_95.txt', corpus_86_95)
    save_text('corpus_96_03.txt', corpus_96_03)

    print('How many characters in each corpus?')
    print(textlen(list(corpus_46_55)))
    print(textlen(list(corpus_56_65)))
    print(textlen(list(corpus_66_75)))
    print(textlen(list(corpus_76_85)))
    print(textlen(list(corpus_86_95)))
    print(textlen(list(corpus_96_03)))
