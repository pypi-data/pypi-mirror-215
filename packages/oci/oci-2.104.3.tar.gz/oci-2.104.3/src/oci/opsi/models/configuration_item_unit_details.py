# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConfigurationItemUnitDetails(object):
    """
    Unit details of configuration item.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ConfigurationItemUnitDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param unit:
            The value to assign to the unit property of this ConfigurationItemUnitDetails.
        :type unit: str

        :param display_name:
            The value to assign to the display_name property of this ConfigurationItemUnitDetails.
        :type display_name: str

        """
        self.swagger_types = {
            'unit': 'str',
            'display_name': 'str'
        }

        self.attribute_map = {
            'unit': 'unit',
            'display_name': 'displayName'
        }

        self._unit = None
        self._display_name = None

    @property
    def unit(self):
        """
        Gets the unit of this ConfigurationItemUnitDetails.
        Unit of configuration item.


        :return: The unit of this ConfigurationItemUnitDetails.
        :rtype: str
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """
        Sets the unit of this ConfigurationItemUnitDetails.
        Unit of configuration item.


        :param unit: The unit of this ConfigurationItemUnitDetails.
        :type: str
        """
        self._unit = unit

    @property
    def display_name(self):
        """
        Gets the display_name of this ConfigurationItemUnitDetails.
        User-friendly display name for the configuration item unit.


        :return: The display_name of this ConfigurationItemUnitDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ConfigurationItemUnitDetails.
        User-friendly display name for the configuration item unit.


        :param display_name: The display_name of this ConfigurationItemUnitDetails.
        :type: str
        """
        self._display_name = display_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
