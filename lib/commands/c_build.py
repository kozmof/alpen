import os
from lib.commands.core.custom_types import Config
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.build import make_payload_file
from lib.commands.core.spinner import Spinner
from lib.commands.core.tfidf import (
    make_doc_objs,
    make_dbows,
    domain_tfidf
)


def c_build():
    with Spinner("Building documents..."):
        config: Config = load_config()
        doc_dir = get_dir_path("DOCUMENT", config)
        file_names = os.listdir(doc_dir)
        doc_objs, bows = make_doc_objs(file_names, config)
        dbows = make_dbows(doc_objs, bows)
        dtfidf = domain_tfidf(dbows)
        make_payload_file(file_names)