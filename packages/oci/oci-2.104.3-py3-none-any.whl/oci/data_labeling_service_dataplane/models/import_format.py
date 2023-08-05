# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ImportFormat(object):
    """
    File format details used for importing dataset
    """

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "JSONL_CONSOLIDATED"
    NAME_JSONL_CONSOLIDATED = "JSONL_CONSOLIDATED"

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "JSONL_COMPACT_PLUS_CONTENT"
    NAME_JSONL_COMPACT_PLUS_CONTENT = "JSONL_COMPACT_PLUS_CONTENT"

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "CONLL"
    NAME_CONLL = "CONLL"

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "SPACY"
    NAME_SPACY = "SPACY"

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "COCO"
    NAME_COCO = "COCO"

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "YOLO"
    NAME_YOLO = "YOLO"

    #: A constant which can be used with the name property of a ImportFormat.
    #: This constant has a value of "PASCAL_VOC"
    NAME_PASCAL_VOC = "PASCAL_VOC"

    #: A constant which can be used with the version property of a ImportFormat.
    #: This constant has a value of "V2003"
    VERSION_V2003 = "V2003"

    #: A constant which can be used with the version property of a ImportFormat.
    #: This constant has a value of "V5"
    VERSION_V5 = "V5"

    def __init__(self, **kwargs):
        """
        Initializes a new ImportFormat object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ImportFormat.
            Allowed values for this property are: "JSONL_CONSOLIDATED", "JSONL_COMPACT_PLUS_CONTENT", "CONLL", "SPACY", "COCO", "YOLO", "PASCAL_VOC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type name: str

        :param version:
            The value to assign to the version property of this ImportFormat.
            Allowed values for this property are: "V2003", "V5", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type version: str

        """
        self.swagger_types = {
            'name': 'str',
            'version': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'version': 'version'
        }

        self._name = None
        self._version = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this ImportFormat.
        Name of import format

        Allowed values for this property are: "JSONL_CONSOLIDATED", "JSONL_COMPACT_PLUS_CONTENT", "CONLL", "SPACY", "COCO", "YOLO", "PASCAL_VOC", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The name of this ImportFormat.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ImportFormat.
        Name of import format


        :param name: The name of this ImportFormat.
        :type: str
        """
        allowed_values = ["JSONL_CONSOLIDATED", "JSONL_COMPACT_PLUS_CONTENT", "CONLL", "SPACY", "COCO", "YOLO", "PASCAL_VOC"]
        if not value_allowed_none_or_none_sentinel(name, allowed_values):
            name = 'UNKNOWN_ENUM_VALUE'
        self._name = name

    @property
    def version(self):
        """
        Gets the version of this ImportFormat.
        Version of import format

        Allowed values for this property are: "V2003", "V5", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The version of this ImportFormat.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ImportFormat.
        Version of import format


        :param version: The version of this ImportFormat.
        :type: str
        """
        allowed_values = ["V2003", "V5"]
        if not value_allowed_none_or_none_sentinel(version, allowed_values):
            version = 'UNKNOWN_ENUM_VALUE'
        self._version = version

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
