METADATA_FILE = "metadata.json"
CURENT_FORMAT_VERSION = "1.0"

FORMAT = {
  "tag": [],
  "version": CURENT_FORMAT_VERSION
}


def init_metadata(file_name):
    key = file_name
    val = FORMAT[CURENT_FORMAT_VERSION]
    return key, val


def version_check(metadata):
    if metadata["version"] == CURENT_FORMAT_VERSION:
        return True
    else:
        return False


def recover_missing_keys(metadata):
    for key in FORMAT.keys():
        if key not in metadata:
            metadata[key] = FORMAT[key]

    for key in metadata.keys:
        if key not in FORMAT:
            del metadata[key]

    return metadata