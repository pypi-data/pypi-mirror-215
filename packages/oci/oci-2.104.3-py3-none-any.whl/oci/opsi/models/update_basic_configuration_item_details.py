# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_configuration_item_details import UpdateConfigurationItemDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateBasicConfigurationItemDetails(UpdateConfigurationItemDetails):
    """
    Configuration item details for OPSI configuration update.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateBasicConfigurationItemDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.UpdateBasicConfigurationItemDetails.config_item_type` attribute
        of this class is ``BASIC`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_item_type:
            The value to assign to the config_item_type property of this UpdateBasicConfigurationItemDetails.
            Allowed values for this property are: "BASIC"
        :type config_item_type: str

        :param name:
            The value to assign to the name property of this UpdateBasicConfigurationItemDetails.
        :type name: str

        :param value:
            The value to assign to the value property of this UpdateBasicConfigurationItemDetails.
        :type value: str

        """
        self.swagger_types = {
            'config_item_type': 'str',
            'name': 'str',
            'value': 'str'
        }

        self.attribute_map = {
            'config_item_type': 'configItemType',
            'name': 'name',
            'value': 'value'
        }

        self._config_item_type = None
        self._name = None
        self._value = None
        self._config_item_type = 'BASIC'

    @property
    def name(self):
        """
        Gets the name of this UpdateBasicConfigurationItemDetails.
        Name of configuration item.


        :return: The name of this UpdateBasicConfigurationItemDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UpdateBasicConfigurationItemDetails.
        Name of configuration item.


        :param name: The name of this UpdateBasicConfigurationItemDetails.
        :type: str
        """
        self._name = name

    @property
    def value(self):
        """
        Gets the value of this UpdateBasicConfigurationItemDetails.
        Value of configuration item.


        :return: The value of this UpdateBasicConfigurationItemDetails.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UpdateBasicConfigurationItemDetails.
        Value of configuration item.


        :param value: The value of this UpdateBasicConfigurationItemDetails.
        :type: str
        """
        self._value = value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
