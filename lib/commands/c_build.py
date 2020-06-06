import os
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.build import make_payload_file
from lib.commands.core.tfidf import (
    make_doc_objs,
    make_dbows,
    domain_tfidf
)


def c_build():
    from lib.commands.core.tfidf import tfidf, multibow
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    doc_files = os.listdir(doc_dir)
    file_names = [f"{doc_dir}/{doc_file}" for doc_file in doc_files]
    doc_objs = make_doc_objs(file_names, config)
    dbows = make_dbows(doc_objs)
    dtfidf = domain_tfidf(dbows)
    make_payload_file(doc_files)