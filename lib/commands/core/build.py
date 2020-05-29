import os
import json
from hashlib import sha256
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.custom_types import Config
from lib.commands.core.metadata import load_metadata
from lib.commands.core.tag import load_tag_data
from lib.commands.core.domain import load_domain_data

"""
publish/payload/page/[uuid].json
               /title.payload.json
               /tag.payload.json
               /domain.payload.json
"""


def dump(payload, f, debug):
    if debug:
        json.dump(payload, f, indent=4, sort_keys=True, ensure_ascii=True)
    else:
        json.dump(payload, f, ensure_ascii=True)


def to_hash(file_name, hashs):
    return hashs.get(file_name, None)


def extract(file_names, spec_file_names, hash_map):
    return list(filter(
            None,
            [
                to_hash(spec_file_name, hash_map) for spec_file_name in spec_file_names
                if spec_file_name in file_names
            ]
        ))


def load(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            return f.read()
    else:
        return ""


def load_json(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            return json.load(f)


def make_payload_file(file_names, debug=True):
    print(type(file_names))
    config: Config = load_config()
    root_dir = config["root_path"]
    doc_dir = get_dir_path("DOCUMENT", config)
    history_dir = get_dir_path("HISTORY", config)

    metadata = load_metadata(config) or []
    tag_data = load_tag_data(config) or {}
    domain_data = load_domain_data(config) or {}

    payload_title = {}
    payload_tag = {}
    hash_map = {}

    save_path_payload_dir = "{root_dir}/publish/payload/".format(
        root_dir=root_dir
    )
    save_path_page_dir = "{payload_dir}/page".format(
        payload_dir=save_path_payload_dir
    )
    save_path_title = "{save_dir}/title.payload.json".format(
        save_dir=save_path_payload_dir
    )
    save_path_tag = "{save_dir}/tag.payload.json".format(
        save_dir=save_path_payload_dir
    )
    save_path_domain = "{save_dir}/domain.payload.json".format(
        save_dir=save_path_payload_dir
    )

    if not os.path.isdir(save_path_page_dir):
        os.makedirs(save_path_page_dir)

    for file_name in file_names:
        payload_page = {}
        doc = load(f"{doc_dir}/{file_name}")
        if doc:
            hsh = sha256(doc)
            hash_map[file_name] = hsh
            title = doc.split("\n")[0]
            history = load_json(
                f"{history_dir}/{os.path.splitext(file_name)[0]}-{os.path.splitext(file_name)[1]}.json"
            )
            tag = metadata[file_name].get("tag", []) if file_name in metadata else []
            domain = metadata[file_name].get("domain", []) if file_name in metadata else []
            publish_date = metadata[file_name].get("publish")
            revise_date = metadata[file_name].get("revise")
            uuid = metadata[file_name].get("uuid")
            rel_path = "./{}".format(uuid)

            payload_title[hsh] = {
                "title": title,
                "tag": tag,
                "domain": domain,
                "publishDate": publish_date,
                "reviseDate": revise_date,
                "relPath": rel_path
            }

            payload_page = {
                "fileName": file_name,
                "doc": doc,
                "history": history,
                "tag": tag,
                "domain": domain,
                "publishDate": publish_date,
                "reviseDate": revise_date
            }
            save_path_page = "{save_dir}/{build_file_page}.json".format(
                save_dir=save_path_page_dir,
                build_file_page=file_name
                )

            with open(save_path_page, "w") as f:
                dump(payload_page, f, debug)

    with open(save_path_title, "w") as f:
        dump(payload_title, f, debug)

    payload_tag = {
        tag: extract(file_names, tagged_files, hash_map) for tag, tagged_files in tag_data.items()
    }
    with open(save_path_tag, "w") as f:
        dump(payload_tag, f, debug)

    payload_domain = {
        domain: extract(file_names, domain_files, hash_map) for tag, domain_files in domain_data.items()
    }
    with open(save_path_domain, "w") as f:
        dump(payload_domain, f, debug)