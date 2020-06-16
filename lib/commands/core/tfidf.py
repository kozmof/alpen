import os
import asyncio
import lib.commands.core.stopwords as sw
from pprint import pprint
from math import log
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from langdetect import detect
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.metadata import load_metadata


def load(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    else:
        return ""


def setup_janome():
    from janome.analyzer import Analyzer
    from janome.charfilter import UnicodeNormalizeCharFilter
    from janome.tokenfilter import POSKeepFilter, CompoundNounFilter, TokenCountFilter

    char_filters = [UnicodeNormalizeCharFilter()]
    token_filters = [CompoundNounFilter(), POSKeepFilter("名詞"), TokenCountFilter()]
    analyzer = Analyzer(
        char_filters=char_filters,
        token_filters=token_filters
        )

    return analyzer


def is_stopword(word, text_type):
    if text_type == "en":
        if word in sw.en:
            return True
        else:
            return False
    else:
        return False


def calc_bow(doc):
    analyzer = setup_janome()
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
        return {}


def multibow(docs):
    cpuc =  os.cpu_count()
    dlen = len(docs)

    with Pool(processes=dlen or 1 if cpuc > dlen else cpuc) as pl:
        res = pl.map(calc_bow, docs)

    return res


def tfidf(bows):
    _pool = {}
    def _acum(k):
        if k not in _pool:
            _pool[k] = 1
        else:
            _pool[k] += 1
        return _pool[k]

    def _tf_idf(bow, doc_freq, N):
        if bow:
            max_freq = bow[max(bow, key=bow.get)]
            tfidf = {
                k: (0.5 + 0.5 * (v / max_freq)) * log((N + 1)/(doc_freq[k]))
                for k, v in bow.items()
            }
            return tfidf
        else:
            return {}

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


def de_merge(d1, d2):
    _d3 = {
        k: v - d2[k] if k in d1 else v
        for k,  v in d1.items()
    }
    d3 = {k: v for k, v in _d3.items() if v}
    return d3


def make_doc_obj(file_name, doc_dir, metadata, text, text_type, bow, tfidf):
    if text:
        doc_obj = {}
        doc_obj["text"] = text
        doc_obj["domain"] = metadata[file_name]["domain"]
        doc_obj["text_type"] = text_type
        doc_obj["bow"] = bow
        doc_obj["tfidf"] = tfidf
        return doc_obj


def make_doc_objs(file_names, config):
    doc_dir = get_dir_path("DOCUMENT", config)
    metadata = load_metadata(config)
    docs = [
        (text := load(f"{doc_dir}/{file_name}"), detect(text) if text else '') for file_name in file_names
    ]
    bows = multibow(docs)
    tfidfs = tfidf(bows=bows)

    assert (len(file_names) ==
            len(docs) ==
            len(bows) == 
            len(tfidfs))
               
    doc_objs = [
        dobj for i, file_name in enumerate(file_names)
        if (dobj := make_doc_obj(
            file_name=file_name,
            doc_dir=doc_dir,
            metadata=metadata,
            text=docs[i][0],
            text_type=docs[i][1],
            bow=bows[i],
            tfidf=tfidfs[i]))
        ]
    bows = [bows[i] for i, doc in enumerate(docs) if doc]
    return doc_objs, bows


def make_dbow(domains_bow):
    domains, bow = domains_bow
    dbow = {}
    for domain in domains:
        if domain:
            if domain not in dbow:
                dbow[domain] = bow
            else:
                dbow[domain] = merge(dbow, bow)
    return dbow



def make_dbows(doc_objs, bows):
    assert len(doc_objs) == len(bows)

    domain_pile = [doc_obj["domain"] for doc_obj in doc_objs]
    cpuc =  os.cpu_count()
    dlen = len(bows)

    with Pool(processes=dlen or 1 if cpuc > dlen else cpuc) as pl:
        dbows = pl.map(make_dbow, zip(domain_pile, bows))

    dbow = {}
    for _dbow in dbows:
        dbow = merge(dbow, _dbow)

    return dbow


def domain_tfidf(dbows):
    domain_dbow = list(zip(*dbows.items()))
    return {
        domain_dbow[0][i]: dbow for i, dbow in enumerate(tfidf(domain_dbow[1]))
    }