"""TF-IDF utilities
"""
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
from typing import Tuple, List, Optional


def load(path: str) -> str:
    """Load a file

    Args:
        path (str): A file path

    Returns:
        str: Data of a file
    """
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    else:
        return ""


def setup_janome():
    """An analyzer to tokenize japanese texts which only counts nouns

    Returns:
        Analyzer: Janome analyzer
    """
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


def is_stopword(word: str, text_type: str) -> bool:
    """Check stop-words

    Args:
        word (str): A word to be checked
        text_type (en): A language type

    Returns:
        bool: True if a word is a stop-word
    """
    if text_type == "en":
        if word in sw.en:
            return True
        else:
            return False
    else:
        return False


def calc_bow(doc: Tuple[str, str]) -> dict:
    """Calculate Bag of Words

    Args:
        doc (Tuple[str, str]): A pair of a text and a language type

    Returns:
        dict: A BoW
    """
    analyzer = setup_janome()
    text, text_type = doc

    if text_type == "ja":
        bow = {}
        for k, v in analyzer.analyze(text):
            bow[k] = v
        return bow

    elif text_type == "en":
        text = text.replace(",", " ")\
                   .replace(".", " ")
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


def multibow(docs: List[Tuple[str, str]]) -> List[dict]:
    """Execute multiprocessing of calcurating BoW

    Args:
        docs (List[Tuple[str, str]]): A bunch of pairs of a text and a language type

    Returns:
        List[dict]: A bunch of BoWs
    """
    cpuc =  os.cpu_count()
    dlen = len(docs)

    with Pool(processes=dlen or 1 if cpuc > dlen else cpuc) as pl:
        res = pl.map(calc_bow, docs)

    return res


def tfidf(bows: List[dict]) -> List[dict]:
    """Calculate TF-IDF

    Args:
        bows (List[dict]): A bunch of BoWs

    Returns:
        List[dict]: TF-IDFs based on BoWs
    """
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


def merge(d1: dict, d2: dict) -> dict:
    """Merge dictioanries which values have a `+` operator

    Args:
        d1 (dict): dict A
        d2 (dict): dict B

    Returns:
        dict: dict A + B
    """
    _d3 = {**d1, **d2}
    d3 = {
        k: v + d1[k] if  k in d1 and k in d2 else v
        for k, v in _d3.items()
    }
    return d3


def make_doc_obj(
    file_name: str,
    doc_dir: str,
    metadata: dict,
    text: str,
    text_type: str,
    bow: dict,
    tfidf: dict) -> Optional[dict]:
    """Make a document object

    Args:
        file_name (str): A file name
        doc_dir (str): A path of document directory
        metadata (dict): Metadata of document
        text (str): Text data
        text_type (str): A language type
        bow (dict): Bow
        tfidf (dict): TF-IDF 

    Returns:
        Optional[dict]: A document object
    """
    if text:
        doc_obj = {}
        doc_obj["text"] = text
        doc_obj["domain"] = metadata[file_name]["domain"]
        doc_obj["text_type"] = text_type
        doc_obj["bow"] = bow
        doc_obj["tfidf"] = tfidf
        return doc_obj


def make_doc_objs(file_names: List[str], config: dict) -> Tuple[dict, dict]:
    """Make document objects and BoWs given file names

    Args:
        file_names (List[str]): File names 
        config (dict): Config data

    Returns:
        Tuple[dict, dict]: Document objects and BoWs without empty documents
    """
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


def make_dbow(domains_bow: Tuple[dict, dict]) -> dict:
    """Make domain specific BoWs

    Args:
        domains_bow (dict): Domains and BoW which is related to domains

    Returns:
        dict: A domain specific BoW
    """
    domains, bow = domains_bow
    dbow = {}
    for domain in domains:
        if domain:
            if domain not in dbow:
                dbow[domain] = bow
            else:
                dbow[domain] = merge(dbow, bow)
    return dbow


def make_dbows(doc_objs: List[dict], bows: List[dict]) -> dict:
    """Make domain specific BoWs from given document objects

    Args:
        doc_objs (List[dict]): Document objects
        bows (List[dict]): BoWs of document objects which are same indices

    Returns:
        dict: All domain specific BoWs
    """
    assert len(doc_objs) == len(bows)

    domain_pile = [doc_obj["domain"] for doc_obj in doc_objs]
    cpuc =  os.cpu_count()
    dlen = len(bows)

    with Pool(processes=dlen or 1 if cpuc > dlen else cpuc) as pl:
        _dbows = pl.map(make_dbow, zip(domain_pile, bows))

    dbows = {}
    for _dbow in _dbows:
        dbows = merge(dbows, _dbow)

    return dbows


def domain_tfidf(dbows: dict) -> dict:
    """Make domain specific TF-IDF

    Args:
        dbows (dict): Domanin specific BoWs

    Returns:
        dict: Domain specific TF-IDF
    """
    domain_dbow = list(zip(*dbows.items()))
    return {
        domain_dbow[0][i]: dbow for i, dbow in enumerate(tfidf(domain_dbow[1]))
    }