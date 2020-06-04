import os
import asyncio
import stopwords as sw
from pprint import pprint
from math import log
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.tokenfilter import POSKeepFilter, CompoundNounFilter, TokenCountFilter


def setup_janome():
    char_filters = [UnicodeNormalizeCharFilter()]
    token_filters = [CompoundNounFilter(), POSKeepFilter("名詞"), TokenCountFilter()]
    analyzer = Analyzer(
        char_filters=char_filters,
        token_filters=token_filters
        )
    return analyzer


analyzer = setup_janome()


def is_stopword(word, text_type):
    if text_type == "en":
        if word in sw.en:
            return True
        else:
            return False
    else:
        return False


def calc_bow(doc):
    text, text_type = doc
    if text_type == "ja":
        bow = {}
        for k, v in analyzer.analyze(text):
            bow[k] = v
        return bow
    elif text_type == "en":
        text = text.replace(",", " ")
        text = text.replace(".", " ")
        words = text.split()
        bow = {}
        for word in words:
            if not is_stopword(word, text_type):
                if word in bow:
                    bow[word] += 1
                else:
                    bow[word] = 1
        return bow
    else:
        return None


def multibow(docs):
    cpuc =  os.cpu_count()
    dlen = len(docs)
    pl = Pool(processes=dlen if cpuc > dlen else cpuc)
    res = pl.map_async(calc_bow, docs)
    res.wait()
    if res.successful():
        return res.get()


def tfidf(bows):
    _pool = {}
    def _acum(k):
        if k not in _pool:
            _pool[k] = 1
        else:
            _pool[k] += 1
        return _pool[k]

    def _tf_idf(bow, doc_freq, N):
        max_freq = bow[max(bow, key=bow.get)]
        tfidf = {
            k: (0.5 + 0.5 * (v / max_freq)) * log((N + 1)/(doc_freq[k] + 1))
            for k, v in bow.items()
        }
        return tfidf

    N = len(bows)
    doc_freq = {
        k: _acum(k)
        for bow in bows for k in bow.keys()
    }

    return [_tf_idf(bow, doc_freq, N) for bow in bows]


def merge(d1, d2):
    _d3 = {**d1, **d2}
    d3 = {
        k: v + d1[k] if  k in d1 and k in d2 else v
        for k, v in _d3.items()
    }
    return d3


def make_dbows(doc_objs):
    domains = []
    docs = []
    for doc_obj in doc_objs:
        domains.append(doc_obj["domain"])
        docs.append((doc_obj["text"], doc_obj["text_type"]))
    bows = multibow(docs)
    dbow = {}
    for domain, bow in zip(domains, bows):
        if domain:
            if domain not in dbow:
                dbow[domain] = bow
            else:
                dbow = merge(dbow, bow)
    return dbow


def domain_tfidf(dbows):
    return {
        domain: tfidf(dbow) for domain, dbow in dbows.items()
    }