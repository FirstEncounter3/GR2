import json
import requests

BASE_URL_API_1 = "https://api.evotor.ru/api/v1/inventories/stores/"
BASE_URL_API_2 = "https://api.evotor.ru/stores/"


def get_stores(token: str) -> list:
    """Get a list of stores"""
    url_for_get_stores = f"{BASE_URL_API_1}search"
    headers = {"X-Authorization": token}

    request = requests.get(url_for_get_stores, headers=headers)
    request.raise_for_status()
    raw_dict = json.loads(request.text)
    screened_list = []
    for i in raw_dict:
        store_uuid = i["uuid"]
        name = i["name"]
        screened_list.append(f"{name}, {store_uuid}")
    return screened_list


def get_receipts(
    since: str, until: str, token: str, store_uuid: str, doc_type: str
) -> str:
    """receive receipts for the specified time, type of document and store"""
    url_for_get_receipts = f"{BASE_URL_API_2}{store_uuid}/documents"
    headers = {"X-Authorization": token}
    params = {"type": doc_type, "since": since, "until": until}

    request = requests.get(url_for_get_receipts, headers=headers, params=params)
    request.raise_for_status()
    return request.text


def get_receipt_by_uuid(store_uuid: str, token: str, receipt_uuid: str) -> str:
    """get receipt by UUID"""
    url_for_get_receipt = f"{BASE_URL_API_2}{store_uuid}/documents/{receipt_uuid}"
    headers = {"X-Authorization": token}

    request = requests.get(url_for_get_receipt, headers=headers)
    request.raise_for_status()
    return request.text


def get_all_goods(store_uuid: str, token: str) -> str:
    """get all goods"""
    url_for_get_goods = f"{BASE_URL_API_2}{store_uuid}/products"
    headers = {"X-Authorization": token}

    request = requests.get(url_for_get_goods, headers=headers)
    request.raise_for_status()
    return request.text


def get_good_by_uuid(store_uuid: str, token: str, product_uuid: str) -> str:
    """get good by UUID"""
    url_for_get_good = f"{BASE_URL_API_2}{store_uuid}/products/{product_uuid}"
    headers = {"X-Authorization": token}

    request = requests.get(url_for_get_good, headers=headers)
    request.raise_for_status()
    return request.text
