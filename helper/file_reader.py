from ast import literal_eval


def read_request_from_file() -> dict:
    """read a string from the previous request file and convert it to a dictionary"""
    with open("metadata_file", "r", encoding="utf-8") as metadate_file:
        return literal_eval(metadate_file.read())
