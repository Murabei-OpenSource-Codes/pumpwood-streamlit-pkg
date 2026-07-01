"""Utility functions for URL parameter parsing and encoding.

Provides base64/JSON encode and decode helpers used by
``PumpwoodStreamlitDashboard.render_filters_section()`` to read
filter values from deep-link query strings.

Typical usage:

```python
from pumpwood_streamlit.query_params import (
    decode_url_params, encode_url_params)

encoded = encode_url_params({"plant_id": 1, "date": "2026-01-01"})
# URL: ?params=<encoded>

raw = {"params": encoded}
filters = decode_url_params(raw)
```
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
