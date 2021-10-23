"""
Define abstract config file representation.
"""

import difflib
import functools
import pathlib
from abc import abstractmethod
from collections.abc import Mapping, Sequence


def is_keychar(char):
    """
    Return True if char is A-Z, a-z, or 0-9.
    """
    if ord(char) >= ord("A") and ord(char) <= ord("Z"):
        return True
    if ord(char) >= ord("a") and ord(char) <= ord("z"):
        return True
    if ord(char) >= ord("0") and ord(char) <= ord("9"):
        return True
    return False


class ConfigDoc(Mapping):
    """
    Abstract config file representation as a nested dictionary like object or list.
    """

    @abstractmethod
    def __init__(self, obj):
        """
        Initalise with a dict/list like obj.
        """
        self._doc = obj  # {} or [] like

    @property
    @staticmethod
    @abstractmethod
    def _compatible_suffixes():
        """
        Should return a list of strings which are valid file extensions.
        """
        return []

    def has_compatible_suffix(self, filename):
        """
        Return true if the filename extension is compatable with this handler.
        """
        ext = pathlib.Path(filename).suffix.strip(".").lower()
        return ext in self._compatible_suffixes

    def follow_keypath(self, keypath, approx=False):
        """
        Follow the path through nested dicts as described by keypath.

        Keypath is a dot seporated path of keys containing "A-Za-z0-9_-", or if the
        key is of the form [idx] where idx is an integer then index to idx in the
        sequence. Eg "path.to.[2].thing". Obviously, not all keys can be addressed
        in this format.

        If approx is True, follow either
        - the shortest key for which the given key is a prefix
        - a close matching key as determined by difflib

        Returns the value at the end of keypath and the actual keypath followed.
        Raises a KeyError if the keypath is invalid.
        """

        keys = keypath.split(".")
        cur = self._doc
        pos = 0
        actual_path = []
        for key in keys:
            cur_path = ".".join(actual_path + [key])

            # List indexing
            if len(key) > 2 and key[0] == "[" and key[-1] == "]":
                if not all(ord("0") <= ord(c) <= ord("9") for c in key[1:-1]):
                    raise KeyError(f"Index for '{cur_path}' must be an integer.")
                if isinstance(cur, Sequence):
                    idx = int(key[1:-1])
                    if idx > len(cur) - 1:
                        KeyError(f"Index for '{cur_path}' out of range [{len(cur)}].")
                    cur = cur[idx]
                    pos += len(key) - 1
                    actual_path.append(f"[{idx}]")
                    continue
                raise KeyError(f"Value at '{cur_path}' is not indexible.")

            # Dictionary keys
            if len(key) > 0 and all(is_keychar(c) for c in key):
                if not isinstance(cur, Mapping):
                    raise KeyError(
                        f"Value at '{cur_path}' is not an explorable mapping."
                    )

                if key in cur:
                    cur = cur[key]
                    pos += len(key) - 1
                    actual_path.append(key)
                    continue

                if approx:
                    fprefix = functools.partial(lambda s, k: s.startswith(k), k=key)
                    prefixs = list(sorted(filter(fprefix, cur.keys())))
                    closest = difflib.get_close_matches(key, cur.keys())
                    if prefixs or closest:
                        choice = (prefixs or closest)[0]
                        cur = cur[choice]
                        pos += len(key) - 1
                        actual_path.append(choice)
                        continue

                    raise KeyError(f"No close matches for {cur_path}'.")

                raise KeyError(f"No key '{cur_path}'.")

            raise KeyError(
                "Invalid keypath. Keypath is a dot seporated path "
                'of keys containing "A-Za-z0-9_-", or if the key '
                "is of the form [idx] where idx is an integer then "
                "index to idx in the sequence."
                f"{keypath}"
                " " * pos + "^"
            )

        return cur, ".".join(actual_path)

    def try_follow_keypath(self, keypath, approx=False):
        """
        Same as follow_keypath() but if a KeyError occurs catch it, returning
        a None value and a string describing the error.
        """

        try:
            value, actual_path = self.follow_keypath(keypath, approx)
        except KeyError as err:
            return None, str(err)
        else:
            return value, actual_path

    def __getitem__(self, key):
        if isinstance(self._doc, (Mapping, Sequence)):
            return self._doc[key]
        raise KeyError

    def __iter__(self):
        return iter(self._doc)

    def __len__(self):
        return len(self._doc)

    def __repr__(self):
        return repr(self._doc)
