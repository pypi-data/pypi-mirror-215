# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ManagementAgentProperty(object):
    """
    Property item in name/value pair, with optional unit type.
    """

    #: A constant which can be used with the units property of a ManagementAgentProperty.
    #: This constant has a value of "PERCENTAGE"
    UNITS_PERCENTAGE = "PERCENTAGE"

    #: A constant which can be used with the units property of a ManagementAgentProperty.
    #: This constant has a value of "MB"
    UNITS_MB = "MB"

    def __init__(self, **kwargs):
        """
        Initializes a new ManagementAgentProperty object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ManagementAgentProperty.
        :type name: str

        :param values:
            The value to assign to the values property of this ManagementAgentProperty.
        :type values: list[str]

        :param units:
            The value to assign to the units property of this ManagementAgentProperty.
            Allowed values for this property are: "PERCENTAGE", "MB", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type units: str

        """
        self.swagger_types = {
            'name': 'str',
            'values': 'list[str]',
            'units': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'values': 'values',
            'units': 'units'
        }

        self._name = None
        self._values = None
        self._units = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this ManagementAgentProperty.
        Name of the property


        :return: The name of this ManagementAgentProperty.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ManagementAgentProperty.
        Name of the property


        :param name: The name of this ManagementAgentProperty.
        :type: str
        """
        self._name = name

    @property
    def values(self):
        """
        **[Required]** Gets the values of this ManagementAgentProperty.
        Values of the property


        :return: The values of this ManagementAgentProperty.
        :rtype: list[str]
        """
        return self._values

    @values.setter
    def values(self, values):
        """
        Sets the values of this ManagementAgentProperty.
        Values of the property


        :param values: The values of this ManagementAgentProperty.
        :type: list[str]
        """
        self._values = values

    @property
    def units(self):
        """
        Gets the units of this ManagementAgentProperty.
        Unit for the property

        Allowed values for this property are: "PERCENTAGE", "MB", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The units of this ManagementAgentProperty.
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """
        Sets the units of this ManagementAgentProperty.
        Unit for the property


        :param units: The units of this ManagementAgentProperty.
        :type: str
        """
        allowed_values = ["PERCENTAGE", "MB"]
        if not value_allowed_none_or_none_sentinel(units, allowed_values):
            units = 'UNKNOWN_ENUM_VALUE'
        self._units = units

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
