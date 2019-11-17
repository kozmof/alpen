METADATA_FILE = "metadata.json"
CURENT_FORMAT_VERSION = "1.0"

FORMAT = {
    "1.0": {
        "tag": [],
        "version": "1.0"
    }
}


def init_metadata(file_name):
    key = file_name
    val = FORMAT[CURENT_FORMAT_VERSION]
    return key, val


def version_check(metadata):
    versions = {}

    for v in FORMAT.keys():
        has_all_keys = True
        for key in FORMAT[v].keys():
            if key in not metadata:
                has_all_keys = False
        versions[v] = has_all_keys

    return versions


def recover_missing_keys(metadata, version: str):
    if version == "1.0":
        for key in FORMAT["1.0"].keys():
            if key not in metadata:
                metadata[key] = FORMAT["1.0"][key]
    else:
        raise Exception(f"No such version: {version}")