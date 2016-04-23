import csv
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.snowball import SnowballStemmer
import nltk
from nltk.tokenize import RegexpTokenizer



def get_text_pool(csvfile):
    with open(csvfile) as f_in:
        c = csv.DictReader(f_in)
        rows_in = [r for r in c]
        print rows_in[0].keys()

        rows_out = []
        for r in rows_in:
            s = ''.join([l for l in r['text'] if ord(l)<128])
            rows_out.append(s)

        pool_string = unicode(' '.join(s for s in rows_out), 'utf-8')


    return pool_string

def remove_stop_word(pool_string):
    stop = set(stopwords.words('english'))
    stop.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']) # remove it if you need punctuation

    wordlist = pool_string.split(' ')

    pool_no_stop = [w.lower() for w in wordlist if w.lower() not in stop]
    pool_no_stop = ' '.join(w.lower() for w in pool_no_stop)
    pool_no_stop = [i.lower() for i in wordpunct_tokenize(pool_no_stop) if i.lower() not in stop]

    return pool_no_stop

def stem_pool_string(pool_no_stop):
    stemmer = SnowballStemmer("english")

    pool_stemmed = []
    for w in pool_no_stop:
        pool_stemmed.append(stemmer.stem(w))

    return pool_stemmed

def remove_internet_char(pool_stemmed):
    character_to_discard = ['#','/','//','http','https','@','rt','://']
    for c in pool_stemmed:
        if c.lower() in character_to_discard:
            pool_stemmed.remove(c)
    return pool_stemmed




def remove_less_than_2_letter(pool_stemmed):
    s = ' '.join(w for w in pool_stemmed)
    tokenizer = RegexpTokenizer(r'\w+')
    s = ' '.join(w.lower() for w in tokenizer.tokenize(s) if w.lower().isalpha())
    # print s

    new_s = []

    for w in s.split():
        if len(w) >2 and w not in ['would','could','should','shall']:
            new_s.append(w)

    return new_s

# ted_words = remove_less_than_2_letter(remove_internet_char(stem_pool_string(remove_stop_word(get_text_pool('tedcruz.csv')))))



def count_freq(wordlist):
    w_f_dict = {}
    for w in wordlist:
        w_f_dict[w] = wordlist.count(w)
    return w_f_dict



def make_csv(word_freq_dict, filename):
    top_100 = sorted(word_freq_dict.items(), key = lambda x:x[1], reverse = True)[20:100]

    f_out = open(filename+'.csv','w')

    rows_out = []

    for t in top_100:
        r = {}
        r['word'] = t[0]
        r['freq'] = t[1]
        rows_out.append(r)

    w = csv.DictWriter(f_out, rows_out[0].keys())
    w.writeheader()
    for r in rows_out:
        w.writerow(r)


    f_out.close()
    return


# for f_in, f_out in [('tedcruz.csv','ted_top_100'),('sanders.csv','sanders_top_100'),('JohnKasich.csv','john_top_100'),('HillaryClinton.csv','clinton_top_100'),('trump.csv','trump_top_100'),('tweetStream.csv','all_people_top_100')]:
#     name = count_freq(remove_less_than_2_letter(remove_internet_char(stem_pool_string(remove_stop_word(get_text_pool(f_in))))))
#     make_csv(name,f_out)

make_csv(count_freq(remove_less_than_2_letter(remove_internet_char(stem_pool_string(remove_stop_word(get_text_pool('tweetStream.csv')))))),'all_people_top_100')

