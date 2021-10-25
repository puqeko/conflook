"""
YAML files
"""

import io

import yaml

from .default import ConfigDoc
from .json import JSONDoc


class YAMLDoc(ConfigDoc):
    """
    YAML file as dict like config file object.
    """

    def __init__(self, stream=None):
        """
        Create new TOMLDoc from a text stream or file.
        """

        yaml.add_multi_constructor("", YAMLDoc._multi_constr, Loader=yaml.SafeLoader)
        yaml.add_multi_representer("", YAMLDoc._multi_repr, Dumper=yaml.SafeDumper)

        if stream is None:
            doc = yaml.safe_load(io.StringIO(""))  # empty
        else:
            doc = yaml.safe_load(stream)

        super().__init__(doc)

    @staticmethod
    def _multi_constr(loader, tag, node):
        pass

    @staticmethod
    def _multi_repr(dumper, obj):
        pass

    @staticmethod
    def compatible_suffixes():
        return ["yaml", "yml"]

    @staticmethod
    def get_type_description(obj):
        return JSONDoc.get_type_description(obj)
