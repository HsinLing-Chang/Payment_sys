import hashlib
import json


def req_hash(req: dict) -> str:
    body = json.dumps(req, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()
