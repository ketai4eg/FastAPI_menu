import requests
import json
from typing import Literal, Optional
from tests.config import API_URL

session = requests.Session()


class ApiError(Exception):

    def __init__(self, status_code: int, message: dict | str):
        self.status_code = status_code
        self.message = message


def basic_request(method: Literal['get', 'post', 'patch', 'delete'], path: str, **kwargs) -> dict:
    path = f'{API_URL}/{path}'
    call = getattr(session, method)
    response = call(path, **kwargs)
    if response.status_code >= 400:
        try:
            message = response.json()
        except json.decoder.JSONDecodeError:
            message = response.text
        raise ApiError(response.status_code, message)
    return response.json()


def create_item(title: str, path: str, description: str | None = None, price: Optional[float] = None):
    if price is None:
        return basic_request(
            method='post',
            path=path,
            json={'title': title, 'description': description},
        )
    else:
        return basic_request(
            method='post',
            path=path,
            json={'title': title, 'description': description, 'price': price},
        )


def get_item(path: str):
    return basic_request('get', path)


def patch_item(path: str, patch: dict):
    return basic_request('patch', path, json=patch)


def delete_item(path: str):
    return basic_request('delete', path)
