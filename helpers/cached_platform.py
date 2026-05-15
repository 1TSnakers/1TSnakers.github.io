# cached_platform.py
#
# Drop-in replacement for Python's built-in `platform` module.
#
# Usage:
#   import cached_platform as platform
#
# Behaves like the real platform module, except values are loaded
# from a cached JSON snapshot for consistency and portability.
#
# Think of it like cryogenically freezing your PC specs and thawing
# them out later on another machine. Tiny hardware time capsule.

import json
import os
import platform as _real_platform

CACHE_FILE = "helpers/.platform_cache.json"


def censor_json_values(data, target_value):
    """
    Recursively searches through a JSON-like object and replaces
    matching values with asterisks.
    """

    replacement = "*" * len(str(target_value))

    if isinstance(data, dict):
        return {
            key: censor_json_values(value, target_value)
            for key, value in data.items()
        }

    elif isinstance(data, list):
        return [
            censor_json_values(item, target_value)
            for item in data
        ]

    elif data == target_value:
        return replacement

    return data


def _build_cache():
    """Extract all safe callable attributes from the real platform module."""
    specs = {}

    for attr_name in dir(_real_platform):

        # Ignore internals and weird low-level helpers
        if attr_name.startswith('_'):
            continue

        attr = getattr(_real_platform, attr_name)

        if callable(attr):
            try:
                result = attr()

                if isinstance(result, (str, tuple, list, dict, int, float)):
                    specs[attr_name] = (
                        list(result)
                        if isinstance(result, tuple)
                        else result
                    )

            except Exception:
                # Skip methods requiring parameters/platform specifics
                continue

    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

    with open(CACHE_FILE, "w") as f:
        json.dump(
            censor_json_values(specs, _real_platform.node()),
            f,
            indent=4
        )

    return specs


def _load_cache(force_refresh=False):
    """Load cached specs or rebuild if needed."""

    if force_refresh or not os.path.exists(CACHE_FILE):
        return _build_cache()

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


# Load cached data immediately
_cached = _load_cache()


# ----------------------------
# Dynamic drop-in magic sauce
# ----------------------------

def __getattr__(name):
    """
    Makes this module behave like the real platform module.

    Example:
        platform.system()
        platform.machine()
        platform.version()
    """

    if name in _cached:

        value = _cached[name]

        # Return a callable to mimic real platform functions
        def wrapper(*args, **kwargs):
            return value

        return wrapper

    raise AttributeError(f"module 'cached_platform' has no attribute '{name}'")


# ----------------------------
# Optional helper utilities
# ----------------------------

def refresh():
    """
    Rebuilds the hardware cache manually.
    """
    global _cached
    _cached = _load_cache(force_refresh=True)


def raw_cache():
    """
    Returns the raw cached dictionary.
    """
    return _cached


# ----------------------------
# Example test
# ----------------------------

if __name__ == "__main__":

    print("Cached system:", system())
    print("Cached machine:", machine())
    print("Cached node:", node())

    print()
    print(f"Loaded {len(_cached)} cached platform attributes.")

    # Tiny bit of comedy:
    # Congratulations. Your hardware has now been laminated.