import hashlib
import json


def generate_boq_hash(boq_json: dict) -> str:
    """
    Deterministic SHA-256 hash of BOQ content.
    Order-safe and reproducible.
    """
    normalized = json.dumps(boq_json, sort_keys=True)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
