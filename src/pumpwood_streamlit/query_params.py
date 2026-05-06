"""Utility functions for URL parameter parsing and encoding.

This module provides URL-safe base64/JSON decoding and encoding for
URL parameters without project-specific knowledge.
"""

import base64
import json
import streamlit as st
import binascii


class URLParams:
    """Class to facilitate management of URL Params.

    Attributes:
        URL_PARAMS (dict): URL query parameters configuration dictionary
            defining required and default values.
    """

    URL_PARAMS = {}

    @classmethod
    def get_url_params(cls):
        """Extract and validate query params from URL.

        Checks if all required parameters (required=True) are
        present in `st.query_params`. If they are, returns a
        dictionary with all parameter values as raw strings.
        If any required parameter is missing, returns None.

        Returns:
            dict or None: Dictionary with parameter values as strings,
                or None if required params are missing.

        Example:
            URLParams.URL_PARAMS = {
                "params": {"required": True},
            }

            # URL: ?params=eyJwbGFudCI6...
            raw = URLParams.get_url_params()
            # raw = {"params": "eyJwbGFudCI6..."}

            # URL without required params:
            raw = URLParams.get_url_params()
            # raw = None
        """
        params = {}
        for param_name, config in cls.URL_PARAMS.items():
            is_required = config.get("required", False)
            default = config.get("default", None)
            value = st.query_params.get(param_name, None)

            if value is None and is_required:
                return None
            params[param_name] = value or default
        return params

    @classmethod
    def has_url_params(cls):
        """Check if all required URL query params are present.

        Returns:
            bool: True if all required parameters defined in
                URL_PARAMS are present in the URL.

        Example:
            if URLParams.has_url_params():
                raw = URLParams.get_url_params()
                params = URLParams.decode_url_params(raw)
            else:
                # Show manual filters
        """
        return cls.get_url_params() is not None

    @classmethod
    def render_filters_section(cls, render_grid, filter_keys=None, **kwargs):
        """Organize the filter section depending on the mode.

        If valid parameters are found in the URL (URL mode), the manual
        filter grid is omitted. Otherwise, the grid rendering function
        is executed.

        Workflow:
            Start -> Normal Mode
              |
            Has URL?
              |
            Yes -> Evaluate filters
              |
            Values valid? -> URL Mode (grid hidden)
              |
            Else -> Normal Mode (grid shown)

        Args:
            render_grid (callable): Function that renders the
                dashboard's manual filter grid.
            filter_keys (list, optional): List of keys that, if present
                in the decoded JSON, activate URL mode. If None, any
                content in the JSON activates the mode.
            **kwargs: Arguments passed to the grid function.

        Example:
            def my_filters(plant_id):
                st.selectbox("Plant", [1, 2], key="plant_id")

            URLParams.render_filters_section(
                render_grid=my_filters,
                filter_keys=["plant_id"],
                plant_id=1,
            )
        """
        is_url_mode = False
        if cls.has_url_params():
            raw = cls.get_url_params()
            url_params = cls.decode_url_params(raw)

            if filter_keys:
                # If any of the specified keys are present
                is_url_mode = any(
                    url_params.get(k) is not None for k in filter_keys
                )
            else:
                # If there is anything in the dictionary
                is_url_mode = len(url_params) > 0

        if not is_url_mode:
            with st.container():
                render_grid(**kwargs)

    @staticmethod
    def decode_url_params(raw_params, key="params"):
        """Decode a URL-safe base64 encoded JSON string from a dictionary.

        Args:
            raw_params (dict): Dictionary with raw URL parameters.
            key (str): Key containing the base64 string. Defaults to "params".

        Returns:
            dict: Decoded dictionary content or an empty dict if decoding,
                UTF-8 conversion, or JSON parsing fails.
        """
        if not raw_params:
            return {}

        params_b64 = raw_params.get(key)
        if not params_b64:
            return {}

        try:
            decoded_bytes = base64.urlsafe_b64decode(params_b64)
            decoded_str = decoded_bytes.decode("utf-8")
            return json.loads(decoded_str)
        except (
            ValueError,
            json.JSONDecodeError,
            TypeError,
            binascii.Error,
        ):
            return {}

    @staticmethod
    def encode_url_params(params_dict):
        """Encode a dictionary to a URL-safe base64 string.

        Args:
            params_dict (dict): Dictionary to encode.

        Returns:
            str: Base64 encoded JSON string.
        """
        json_str = json.dumps(params_dict, ensure_ascii=False)
        b64_bytes = base64.urlsafe_b64encode(json_str.encode("utf-8"))
        return b64_bytes.decode("utf-8")
