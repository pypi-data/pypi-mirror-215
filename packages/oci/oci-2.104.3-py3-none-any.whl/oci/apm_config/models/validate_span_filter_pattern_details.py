# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ValidateSpanFilterPatternDetails(object):
    """
    The request body used to validate a Span Filter pattern.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ValidateSpanFilterPatternDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param filter_text:
            The value to assign to the filter_text property of this ValidateSpanFilterPatternDetails.
        :type filter_text: str

        """
        self.swagger_types = {
            'filter_text': 'str'
        }

        self.attribute_map = {
            'filter_text': 'filterText'
        }

        self._filter_text = None

    @property
    def filter_text(self):
        """
        **[Required]** Gets the filter_text of this ValidateSpanFilterPatternDetails.
        The string that defines the Span Filter expression.


        :return: The filter_text of this ValidateSpanFilterPatternDetails.
        :rtype: str
        """
        return self._filter_text

    @filter_text.setter
    def filter_text(self, filter_text):
        """
        Sets the filter_text of this ValidateSpanFilterPatternDetails.
        The string that defines the Span Filter expression.


        :param filter_text: The filter_text of this ValidateSpanFilterPatternDetails.
        :type: str
        """
        self._filter_text = filter_text

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
