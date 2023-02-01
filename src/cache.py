
import json
from fastapi.encoders import jsonable_encoder
from src.config import r


def cache_set(d, layer):
    r.set(
        f'{layer}_{jsonable_encoder(d)["id"]}', json.dumps(
            jsonable_encoder(d),
        ),
    )


def cache_get(item_id, layer):
    if r.get(f'{layer}_{item_id}'):
        return json.loads(r.get(f'{layer}_{item_id}'))


def cache_delete(item_id, layer):
    if r.get(f'{layer}_{item_id}'):
        r.delete(f'{layer}_{item_id}')
    return None
