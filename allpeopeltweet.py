import csv
import pickle
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

with open('tweetStream.csv') as f:
    words = []
    for i in f:
        for w in i.split():
            words.append(w)

# print len(words)


w2 = []
for w in words:
    if w.isalpha() and len(w) >2:
        w2.append(w)


stemmer = SnowballStemmer("english")

w3 = []
for w in w2:
    if w.lower() not in stopwords.words('english'):

        w3.append(stemmer.stem(w.lower()))

w_f_dict = {}
for w in set(w3):
    w_f_dict[w] = w3.count(w)

w3 = sorted(w_f_dict.items(), key = lambda x:x[1], reverse = True)[:300]


rows_out = []
for w in set(w3):
    r = {}
    r['w'] = w
    r['f'] = w3.count(w)
    rows_out.append(r)

with open('all_people_words_top_300.csv','w') as f_out:
    w = csv.DictWriter(f_out, fieldnames = rows_out[0].keys())
    w.writeheader()
    for r in rows_out:
        w.writerow(r)






