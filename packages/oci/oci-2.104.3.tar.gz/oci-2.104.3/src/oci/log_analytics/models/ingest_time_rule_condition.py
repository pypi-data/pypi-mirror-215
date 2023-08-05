# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IngestTimeRuleCondition(object):
    """
    The condition(s) to evaluate for an ingest time rule.
    """

    #: A constant which can be used with the kind property of a IngestTimeRuleCondition.
    #: This constant has a value of "FIELD"
    KIND_FIELD = "FIELD"

    def __init__(self, **kwargs):
        """
        Initializes a new IngestTimeRuleCondition object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.log_analytics.models.IngestTimeRuleFieldCondition`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this IngestTimeRuleCondition.
            Allowed values for this property are: "FIELD", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type kind: str

        """
        self.swagger_types = {
            'kind': 'str'
        }

        self.attribute_map = {
            'kind': 'kind'
        }

        self._kind = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['kind']

        if type == 'FIELD':
            return 'IngestTimeRuleFieldCondition'
        else:
            return 'IngestTimeRuleCondition'

    @property
    def kind(self):
        """
        **[Required]** Gets the kind of this IngestTimeRuleCondition.
        Discriminator.

        Allowed values for this property are: "FIELD", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The kind of this IngestTimeRuleCondition.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        Sets the kind of this IngestTimeRuleCondition.
        Discriminator.


        :param kind: The kind of this IngestTimeRuleCondition.
        :type: str
        """
        allowed_values = ["FIELD"]
        if not value_allowed_none_or_none_sentinel(kind, allowed_values):
            kind = 'UNKNOWN_ENUM_VALUE'
        self._kind = kind

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
