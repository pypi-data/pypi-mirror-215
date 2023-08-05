# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConfigurationItemAllowedValueDetails(object):
    """
    Allowed value details of configuration item, to validate what value can be assigned to a configuration item.
    """

    #: A constant which can be used with the allowed_value_type property of a ConfigurationItemAllowedValueDetails.
    #: This constant has a value of "LIMIT"
    ALLOWED_VALUE_TYPE_LIMIT = "LIMIT"

    #: A constant which can be used with the allowed_value_type property of a ConfigurationItemAllowedValueDetails.
    #: This constant has a value of "PICK"
    ALLOWED_VALUE_TYPE_PICK = "PICK"

    #: A constant which can be used with the allowed_value_type property of a ConfigurationItemAllowedValueDetails.
    #: This constant has a value of "FREE_TEXT"
    ALLOWED_VALUE_TYPE_FREE_TEXT = "FREE_TEXT"

    def __init__(self, **kwargs):
        """
        Initializes a new ConfigurationItemAllowedValueDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.opsi.models.ConfigurationItemFreeTextAllowedValueDetails`
        * :class:`~oci.opsi.models.ConfigurationItemPickAllowedValueDetails`
        * :class:`~oci.opsi.models.ConfigurationItemLimitAllowedValueDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param allowed_value_type:
            The value to assign to the allowed_value_type property of this ConfigurationItemAllowedValueDetails.
            Allowed values for this property are: "LIMIT", "PICK", "FREE_TEXT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type allowed_value_type: str

        """
        self.swagger_types = {
            'allowed_value_type': 'str'
        }

        self.attribute_map = {
            'allowed_value_type': 'allowedValueType'
        }

        self._allowed_value_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['allowedValueType']

        if type == 'FREE_TEXT':
            return 'ConfigurationItemFreeTextAllowedValueDetails'

        if type == 'PICK':
            return 'ConfigurationItemPickAllowedValueDetails'

        if type == 'LIMIT':
            return 'ConfigurationItemLimitAllowedValueDetails'
        else:
            return 'ConfigurationItemAllowedValueDetails'

    @property
    def allowed_value_type(self):
        """
        **[Required]** Gets the allowed_value_type of this ConfigurationItemAllowedValueDetails.
        Allowed value type of configuration item.

        Allowed values for this property are: "LIMIT", "PICK", "FREE_TEXT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The allowed_value_type of this ConfigurationItemAllowedValueDetails.
        :rtype: str
        """
        return self._allowed_value_type

    @allowed_value_type.setter
    def allowed_value_type(self, allowed_value_type):
        """
        Sets the allowed_value_type of this ConfigurationItemAllowedValueDetails.
        Allowed value type of configuration item.


        :param allowed_value_type: The allowed_value_type of this ConfigurationItemAllowedValueDetails.
        :type: str
        """
        allowed_values = ["LIMIT", "PICK", "FREE_TEXT"]
        if not value_allowed_none_or_none_sentinel(allowed_value_type, allowed_values):
            allowed_value_type = 'UNKNOWN_ENUM_VALUE'
        self._allowed_value_type = allowed_value_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
