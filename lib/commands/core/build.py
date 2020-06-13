import os
import json
from copy import deepcopy
from uuid import uuid4
from hashlib import sha256
from lib.commands.core.configure import load_config
from lib.commands.core.dir_ops import get_dir_path
from lib.commands.core.custom_types import Config
from lib.commands.core.metadata import load_metadata, init_metadata, dump_metadata_json
from lib.commands.core.tag import load_tag_data
from lib.commands.core.domain import load_domain_data
from lib.commands.core.git import make_time_stamp


"""
publish/payload/page/[uuid].payload.json
               /title.payload.json
               /tag.payload.json
               /domain.payload.json
"""


def extract(file_names, spec_file_names):
    return [
        spec_file_name for spec_file_name in spec_file_names
        if spec_file_name in file_names
    ]


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


def dump_json(payload, f, debug):
    if debug:
        json.dump(payload, f, indent=4, sort_keys=True, ensure_ascii=True)
    else:
        json.dump(payload, f, ensure_ascii=True)


def make_payload_file(file_names, debug=True):
    config: Config = load_config()
    root_dir = config["root_path"]
    doc_dir = get_dir_path("DOCUMENT", config)
    history_dir = get_dir_path("HISTORY", config)

    metadata = load_metadata(config) or {}
    for file_name in file_names:
        if file_name not in metadata:
            metadata = {**deepcopy(metadata), **dict([init_metadata(file_name)])}
            metadata[file_name]["first_finish"] = make_time_stamp()
        elif metadata[file_name].get("first_finish", None):
            metadata[file_name]["revise"] = make_time_stamp()
            if not metadata[file_name].get("uuid"):
                print("Metadata doesn't have uuid. Regenerate uuid...")
                metadata[file_name]["uuid"] = uuid4()
    dump_metadata_json(metadata, config)

    tag_data = load_tag_data(config) or {}
    domain_data = load_domain_data(config) or {}

    payload_title = {}
    payload_tag = {}

    save_path_payload_dir = f"{root_dir}/publish/payload"
    save_path_page_dir = f"{save_path_payload_dir}/page"
    save_path_title = f"{save_path_payload_dir}/title.payload.json"
    save_path_tag = f"{save_path_payload_dir}/tag.payload.json"
    save_path_domain = f"{save_path_payload_dir}/domain.payload.json"

    if not os.path.isdir(save_path_page_dir):
        os.makedirs(save_path_page_dir)

    for file_name in file_names:
        payload_page = {}
        doc = load(f"{doc_dir}/{file_name}")
        if doc:
            title = doc.split("\n")[0]
            history = load_json(
                f"{history_dir}/{os.path.splitext(file_name)[0]}-{os.path.splitext(file_name)[1]}.json"
            )
            tag = metadata[file_name].get("tag", []) if file_name in metadata else []
            domain = metadata[file_name].get("domain", []) if file_name in metadata else []
            ff_date = metadata[file_name].get("first_finish")
            revise_date = metadata[file_name].get("revise")
            uuid = metadata[file_name].get("uuid")
            rel_path = f"./{uuid}"

            payload_title[file_name] = {
                "title": title,
                "tag": tag,
                "domain": domain,
                "firstFinishDate": ff_date,
                "reviseDate": revise_date,
                "relPath": rel_path,
                "uuid": uuid
            }

            payload_page = {
                "fileName": file_name,
                "doc": doc,
                "history": history,
                "tag": tag,
                "domain": domain,
                "firstFinishDate": ff_date,
                "reviseDate": revise_date
            }
            save_path_page = f"{save_path_page_dir}/{file_name}.payload.json"

            with open(save_path_page, "w") as f:
                dump_json(payload_page, f, debug)

    with open(save_path_title, "w") as f:
        dump_json(payload_title, f, debug)

    with open(save_path_tag, "w") as f:
        payload_tag = {
            tag: extract(file_names, tagged_files) for tag, tagged_files in tag_data.items()
        }
        dump_json(payload_tag, f, debug)

    with open(save_path_domain, "w") as f:
        payload_domain = {
            domain: extract(file_names, domain_files) for domain, domain_files in domain_data.items()
        }
        dump_json(payload_domain, f, debug)


def prep_title_source(path):
    # title/index.tsx
    with open(f"{path}/index.tsx", "w") as f:
        f.write(...)


def prep_page_source(path, config):
    root_dir = config["root_path"]
    payload_dir = f"{root_dir}/publish/payload"
    path_title = f"{payload_dir}/title.payload.json"
    with open(path_title, "r") as f:
        titles = json.load(f)
    for info in titles.values():
        uuid = info["uuid"]
        if not os.path.isdir(sub_path := f"{path}/{uuid}"):
            os.mkdir(sub_path)
        # page/123e4567-e89b-12d3-a456-426614174000/index.tsx
        with open(f"{sub_path}/index.tsx", "w") as f:
            f.write(...)


def prep_tag_source(path, config):
    root_dir = config["root_path"]
    payload_dir = f"{root_dir}/publish/payload"
    path_tag = f"{payload_dir}/tag.payload.json"
    # tag/index.tsx
    with open(f"{path}/index.tsx", "w") as f:
        f.write(...)
    with open(path_tag, "r") as f:
        tags = json.load(f)
    for tag in tags.items():
        if not os.path.isdir(sub_path := f"{path}/{tag}"):
            os.mkdir(sub_path)
        # tag/{tag}/index.tsx
        with open(f"{sub_path}/index.tsx", "w") as f:
            f.write(...)


def prep_domain_source(path, config):
    root_dir = config["root_path"]
    payload_dir = f"{root_dir}/publish/payload"
    path_domain = f"{payload_dir}/domain.payload.json"
    with open(f"{path}/domain_home.tsx", "w") as f:
        f.write(...)
    with open(path_domain, "r") as f:
        domains = json.load(f)
    for domain in domains.items():
        if not os.path.isdir(sub_path := f"{path}/{domain}"):
            os.mkdir(sub_path)
        # domain/{domain}/index.tsx
        with open(f"{sub_path}/index.tsx", "w") as f:
            f.write(...)


def make_index_tree(src):
    config: Config = load_config()
    if not os.path.isdir(path := f"{src}/title"):
        os.makedirs(path)
        prep_title_source(path)
    if not os.path.isdir(path := f"{src}/page"):
        os.makedirs(path)
        prep_page_source(path,config)
    if not os.path.isdir(path := f"{src}/tag"):
        os.makedirs(path)
        prep_tag_source(path, config)
    if not os.path.isdir(path := f"{src}/domain"):
        os.makedirs(path)
        prep_domain_source(path, config)