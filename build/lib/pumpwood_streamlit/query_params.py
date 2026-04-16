"""Utility functions for URL parameter parsing and encoding.

This module provides generic base64/JSON decoding and encoding for 
URL parameters without project-specific knowledge.
"""

import base64
import json


def decode_url_params(raw_params, key="params"):
    """Decode a base64 encoded JSON from a dictionary.

    Args:
        raw_params (dict): Dictionary with raw URL parameters.
        key (str): Key containing the base64 string. Default is "params".

    Returns:
        dict: Decoded dictionary content or empty dict if fails.
    """
    if not raw_params:
        return {}

    params_b64 = raw_params.get(key)
    if not params_b64:
        return {}

    try:
        decoded_bytes = base64.b64decode(params_b64)
        decoded_str = decoded_bytes.decode("utf-8")
        return json.loads(decoded_str)
    except (
        ValueError, json.JSONDecodeError, TypeError, base64.binascii.Error):
        return {}


def encode_url_params(params_dict):
    """Encode a dictionary to a base64 string.

    Args:
        params_dict (dict): Dictionary to encode.

    Returns:
        str: Base64 encoded JSON string.
    """
    json_str = json.dumps(params_dict, ensure_ascii=False)
    b64_bytes = base64.b64encode(json_str.encode("utf-8"))
    return b64_bytes.decode("utf-8")
