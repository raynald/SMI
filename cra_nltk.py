import nltk
import sys
import xlsxwriter
from nltk.corpus import brown
from nltk.corpus import reuters
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, wordpunct_tokenize
from nltk.probability import *
import itertools as it
import networkx as nx
import nltk
import re

# Input
raw = ""
for line in sys.stdin:
    raw += line.strip()
# Word Dict
words = FreqDist()
stopwords = stopwords.words() + ['.', ',', '"', "'", '-', '.-','~']
#first_doc = reuters.sents(reuters.fileids()[0])
sentence = sent_tokenize(raw)
first_doc = []
for t in sentence:
    first_doc += [wordpunct_tokenize(t)]

stopd_sents = [[token.lower() for token in sent if token.lower() not in stopwords]
               for sent in first_doc]
for sentence in stopd_sents:
    for word in sentence:
        words[word.lower()] += 1
tagged_sents = [nltk.pos_tag(sentence) for sentence in stopd_sents]
noun_phrases = [[token for token, tag in sent if re.match(r'NN*|JJ*', tag)]
                        for sent in tagged_sents]
edgelist = [edge for phrase in noun_phrases for edge in it.combinations(phrase, 2)]
G = nx.Graph(edgelist)
index = nx.betweenness_centrality(G)
index_d = nx.degree_centrality(G)

sorted_index = sorted(index.items(), key=lambda x:x[1], reverse=True)
sorted_index_d = sorted(index_d.items(), key=lambda x:x[1], reverse=True)

# Top 10 noun phrases by betweenness centrality:
workbook = xlsxwriter.Workbook('cra_test.xlsx')
worksheet = workbook.add_worksheet()
count = 1
worksheet.write('A1',  'Word')
worksheet.write('B1',  'Occurence')
worksheet.write('C1',  'Betweenness')
worksheet.write('D1',  'Degree')
for word, centr in sorted_index[:10]:
    count += 1
    worksheet.write('A' + str(count),  word)
    worksheet.write('B' + str(count), words[word])
    worksheet.write('C' + str(count), centr)
count = 1
for word, centr in sorted_index_d[:10]:
    count += 1
    worksheet.write('D' + str(count), centr)
workbook.close()
