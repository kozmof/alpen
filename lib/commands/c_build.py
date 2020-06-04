import os
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.build import make_payload_file


def load(path):
    with open(path, "r") as f:
        return f.read()


def c_build():
    from lib.commands.core.tfidf import tfidf, multibow
    config: Config = load_config()
    doc_dir = get_dir_path("DOCUMENT", config)
    doc_files = os.listdir(doc_dir)
    docs = [load(f"{doc_dir}/{doc_file}") for doc_file in doc_files]
    tfidfs = tfidf(
        bows=multibow(docs=docs)
    )
    # TODO grouping
    make_payload_file(doc_files)