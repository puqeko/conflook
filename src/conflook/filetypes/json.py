"""
JSON files
"""

import json

from .default import ConfigDoc


class JSONDoc(ConfigDoc):
    """
    JSON file as dict like config file object.
    """

    def __init__(self, stream=None):
        """
        Create new JSONDoc from a text stream or file.
        """

        if stream is None:
            doc = json.loads("")  # empty
        else:
            doc = json.loads(stream.read())

        super().__init__(doc)

    @staticmethod
    def _compatible_suffixes():
        return ["json"]
