# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .unified_agent_parser import UnifiedAgentParser
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UnifiedAgentCriParser(UnifiedAgentParser):
    """
    CRI parser.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UnifiedAgentCriParser object with values from keyword arguments. The default value of the :py:attr:`~oci.logging.models.UnifiedAgentCriParser.parser_type` attribute
        of this class is ``CRI`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param parser_type:
            The value to assign to the parser_type property of this UnifiedAgentCriParser.
            Allowed values for this property are: "AUDITD", "CRI", "JSON", "TSV", "CSV", "NONE", "SYSLOG", "APACHE2", "APACHE_ERROR", "MSGPACK", "REGEXP", "MULTILINE", "GROK", "MULTILINE_GROK"
        :type parser_type: str

        :param field_time_key:
            The value to assign to the field_time_key property of this UnifiedAgentCriParser.
        :type field_time_key: str

        :param types:
            The value to assign to the types property of this UnifiedAgentCriParser.
        :type types: dict(str, str)

        :param null_value_pattern:
            The value to assign to the null_value_pattern property of this UnifiedAgentCriParser.
        :type null_value_pattern: str

        :param is_null_empty_string:
            The value to assign to the is_null_empty_string property of this UnifiedAgentCriParser.
        :type is_null_empty_string: bool

        :param is_estimate_current_event:
            The value to assign to the is_estimate_current_event property of this UnifiedAgentCriParser.
        :type is_estimate_current_event: bool

        :param is_keep_time_key:
            The value to assign to the is_keep_time_key property of this UnifiedAgentCriParser.
        :type is_keep_time_key: bool

        :param timeout_in_milliseconds:
            The value to assign to the timeout_in_milliseconds property of this UnifiedAgentCriParser.
        :type timeout_in_milliseconds: int

        :param is_merge_cri_fields:
            The value to assign to the is_merge_cri_fields property of this UnifiedAgentCriParser.
        :type is_merge_cri_fields: bool

        :param nested_parser:
            The value to assign to the nested_parser property of this UnifiedAgentCriParser.
        :type nested_parser: oci.logging.models.UnifiedJSONParser

        """
        self.swagger_types = {
            'parser_type': 'str',
            'field_time_key': 'str',
            'types': 'dict(str, str)',
            'null_value_pattern': 'str',
            'is_null_empty_string': 'bool',
            'is_estimate_current_event': 'bool',
            'is_keep_time_key': 'bool',
            'timeout_in_milliseconds': 'int',
            'is_merge_cri_fields': 'bool',
            'nested_parser': 'UnifiedJSONParser'
        }

        self.attribute_map = {
            'parser_type': 'parserType',
            'field_time_key': 'fieldTimeKey',
            'types': 'types',
            'null_value_pattern': 'nullValuePattern',
            'is_null_empty_string': 'isNullEmptyString',
            'is_estimate_current_event': 'isEstimateCurrentEvent',
            'is_keep_time_key': 'isKeepTimeKey',
            'timeout_in_milliseconds': 'timeoutInMilliseconds',
            'is_merge_cri_fields': 'isMergeCriFields',
            'nested_parser': 'nestedParser'
        }

        self._parser_type = None
        self._field_time_key = None
        self._types = None
        self._null_value_pattern = None
        self._is_null_empty_string = None
        self._is_estimate_current_event = None
        self._is_keep_time_key = None
        self._timeout_in_milliseconds = None
        self._is_merge_cri_fields = None
        self._nested_parser = None
        self._parser_type = 'CRI'

    @property
    def is_merge_cri_fields(self):
        """
        Gets the is_merge_cri_fields of this UnifiedAgentCriParser.
        If you don't need stream/logtag fields, set this to false.


        :return: The is_merge_cri_fields of this UnifiedAgentCriParser.
        :rtype: bool
        """
        return self._is_merge_cri_fields

    @is_merge_cri_fields.setter
    def is_merge_cri_fields(self, is_merge_cri_fields):
        """
        Sets the is_merge_cri_fields of this UnifiedAgentCriParser.
        If you don't need stream/logtag fields, set this to false.


        :param is_merge_cri_fields: The is_merge_cri_fields of this UnifiedAgentCriParser.
        :type: bool
        """
        self._is_merge_cri_fields = is_merge_cri_fields

    @property
    def nested_parser(self):
        """
        Gets the nested_parser of this UnifiedAgentCriParser.
        Optional nested JSON Parser for CRI Parser. Supported fields are fieldTimeKey, timeFormat, and isKeepTimeKey.


        :return: The nested_parser of this UnifiedAgentCriParser.
        :rtype: oci.logging.models.UnifiedJSONParser
        """
        return self._nested_parser

    @nested_parser.setter
    def nested_parser(self, nested_parser):
        """
        Sets the nested_parser of this UnifiedAgentCriParser.
        Optional nested JSON Parser for CRI Parser. Supported fields are fieldTimeKey, timeFormat, and isKeepTimeKey.


        :param nested_parser: The nested_parser of this UnifiedAgentCriParser.
        :type: oci.logging.models.UnifiedJSONParser
        """
        self._nested_parser = nested_parser

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
