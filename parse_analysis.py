import collections
from LAC import LAC
from ddparser import DDParser
from data_collection import textlen
import matplotlib.pyplot as plt
# Read the dictionary from a txt file
def get_dic(corpname):
    dic={}
    doc =open(corpname, 'r')
    for line in doc.readlines():
        line=line.strip()
        k = line.split('\t')[0]
        v = line.split('\t')[-1]
        dic[k]=v
    return dic

def get_corp(textname):
    corpus = []
    doc =open(textname, 'r')
    for line in doc.readlines():
        line=line.strip()
        k = line.split('\t')[0]
        corpus.append(k)
    return corpus

ddp = DDParser(use_pos=True)
# count the frequency of a specific deprel term
def count_rel(text, head, info):
    count = 0
    for i, sentence in enumerate(text):
        if i%1000 == 0:
            print(str(i) + ' sentences have been processed.')
        if sentence[head].count(info) > 0:
            count+= sentence[head].count(info)
    return format(count/len(text), '.2f')

def get_sub(dict):
  count =0
  for sent in dict:
    b = collections.Counter(sent['deprel'])
    c = b['SBV']
    count +=c
  return count

def get_att(dict):
  count =0
  for sent in dict:
    if 'r' in sent['postag']:
      id = list(sent['postag']).index('r')
      if list(sent['deprel'])[id-1] == 'MT' or list(sent['deprel'])[id-1] == 'ATT':
        count +=1
  return count

if __name__=='__main__':
    corpus_46_55 = get_dic('corpus_46_55.txt')
    corpus_56_65 = get_dic('corpus_56_65.txt')
    corpus_66_75 = get_dic('corpus_66_75.txt')
    corpus_76_85 = get_dic('corpus_76_85.txt')
    corpus_86_95 = get_dic('corpus_86_95.txt')
    corpus_96_03 = get_dic('corpus_96_03.txt')

    sents_46_55 = len(corpus_46_55)
    sents_56_65 = len(corpus_56_65)
    sents_66_75 = len(corpus_66_75)
    sents_76_85 = len(corpus_76_85)
    sents_86_95 = len(corpus_86_95)
    sents_96_03 = len(corpus_96_03)

    year_46_55 = textlen(list(corpus_46_55))
    year_56_65 = textlen(list(corpus_56_65))
    year_66_75 = textlen(list(corpus_66_75))
    year_76_85 = textlen(list(corpus_76_85))
    year_86_95 = textlen(list(corpus_86_95))
    year_96_03 = textlen(list(corpus_96_03))

    treebank_46_55 = ddp.parse(list(corpus_46_55))
    treebank_56_65 = ddp.parse(list(corpus_56_65))
    treebank_66_75 = ddp.parse(list(corpus_66_75))
    treebank_76_85 = ddp.parse(list(corpus_76_85))
    treebank_86_95 = ddp.parse(list(corpus_86_95))
    treebank_96_03 = ddp.parse(list(corpus_96_03))

    sub_46_55 = get_sub(treebank_46_55)
    sub_56_65 = get_sub(treebank_56_65)
    sub_66_75 = get_sub(treebank_66_75)
    sub_76_85 = get_sub(treebank_76_85)
    sub_86_95 = get_sub(treebank_86_95)
    sub_96_03 = get_sub(treebank_96_03)

    att_46_55 = get_att(treebank_46_55)
    att_56_65 = get_att(treebank_56_65)
    att_66_75 = get_att(treebank_66_75)
    att_76_85 = get_att(treebank_76_85)
    att_86_95 = get_att(treebank_86_95)
    att_96_03 = get_att(treebank_96_03)

    x = ['1946-1955', '1956-1965', '1966-1975', '1976-1985', '1986-1995', '1996-2003']
    char_len = [int(year_46_55), int(year_56_65),int(year_66_75),int(year_76_85),int(year_86_95),int(year_96_03)]
    sub = [sub_46_55/sents_46_55, sub_56_65/sents_56_65, sub_66_75/sents_66_75, sub_76_85/sents_76_85, sub_86_95/sents_86_95, sub_96_03/sents_96_03]
    att = [att_46_55/sents_46_55, att_56_65/sents_56_65, att_66_75/sents_66_75, att_76_85/sents_76_85, att_86_95/sents_86_95, att_96_03/sents_96_03]

    print('number of characters: ', char_len)
    print('number of sentences: ', sents_46_55, sents_56_65, sents_66_75, sents_76_85, sents_86_95, sents_96_03)
    print('number of subjects:', sub)
    print('number of attributes', att)

    sent = [year_46_55/sents_46_55, year_56_65/sents_56_65, year_66_75/sents_66_75, year_76_85/sents_76_85, year_86_95/sents_86_95, year_96_03/sents_96_03]

    plt.plot(x, sent)
    plt.ylim(30, 48)
    plt.xlabel('time')
    plt.ylabel('number of subject')
    plt.title('The average sentence length of each corpus in different periods of time')
    plt.show()

