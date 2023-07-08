import json


def decoder(from_object) -> str:
    """decoding the received object"""
    decoded_json = json.loads(from_object)
    return json.dumps(decoded_json, ensure_ascii=False, indent=4)
