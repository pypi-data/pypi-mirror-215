# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceAvailability(object):
    """
    The availability of a given resource limit, based on the usage, tenant service limits, and quotas set for the tenancy.
    Note: We cannot guarantee this data for all the limits. In such cases, these fields will be empty.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceAvailability object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param used:
            The value to assign to the used property of this ResourceAvailability.
        :type used: int

        :param available:
            The value to assign to the available property of this ResourceAvailability.
        :type available: int

        :param fractional_usage:
            The value to assign to the fractional_usage property of this ResourceAvailability.
        :type fractional_usage: float

        :param fractional_availability:
            The value to assign to the fractional_availability property of this ResourceAvailability.
        :type fractional_availability: float

        :param effective_quota_value:
            The value to assign to the effective_quota_value property of this ResourceAvailability.
        :type effective_quota_value: float

        """
        self.swagger_types = {
            'used': 'int',
            'available': 'int',
            'fractional_usage': 'float',
            'fractional_availability': 'float',
            'effective_quota_value': 'float'
        }

        self.attribute_map = {
            'used': 'used',
            'available': 'available',
            'fractional_usage': 'fractionalUsage',
            'fractional_availability': 'fractionalAvailability',
            'effective_quota_value': 'effectiveQuotaValue'
        }

        self._used = None
        self._available = None
        self._fractional_usage = None
        self._fractional_availability = None
        self._effective_quota_value = None

    @property
    def used(self):
        """
        Gets the used of this ResourceAvailability.
        The current usage in the given compartment. To support resources with fractional counts,
        the field rounds up to the nearest integer.


        :return: The used of this ResourceAvailability.
        :rtype: int
        """
        return self._used

    @used.setter
    def used(self, used):
        """
        Sets the used of this ResourceAvailability.
        The current usage in the given compartment. To support resources with fractional counts,
        the field rounds up to the nearest integer.


        :param used: The used of this ResourceAvailability.
        :type: int
        """
        self._used = used

    @property
    def available(self):
        """
        Gets the available of this ResourceAvailability.
        The count of available resources. To support resources with fractional counts,
        the field rounds down to the nearest integer.


        :return: The available of this ResourceAvailability.
        :rtype: int
        """
        return self._available

    @available.setter
    def available(self, available):
        """
        Sets the available of this ResourceAvailability.
        The count of available resources. To support resources with fractional counts,
        the field rounds down to the nearest integer.


        :param available: The available of this ResourceAvailability.
        :type: int
        """
        self._available = available

    @property
    def fractional_usage(self):
        """
        Gets the fractional_usage of this ResourceAvailability.
        The current most accurate usage in the given compartment.


        :return: The fractional_usage of this ResourceAvailability.
        :rtype: float
        """
        return self._fractional_usage

    @fractional_usage.setter
    def fractional_usage(self, fractional_usage):
        """
        Sets the fractional_usage of this ResourceAvailability.
        The current most accurate usage in the given compartment.


        :param fractional_usage: The fractional_usage of this ResourceAvailability.
        :type: float
        """
        self._fractional_usage = fractional_usage

    @property
    def fractional_availability(self):
        """
        Gets the fractional_availability of this ResourceAvailability.
        The most accurate count of available resources.


        :return: The fractional_availability of this ResourceAvailability.
        :rtype: float
        """
        return self._fractional_availability

    @fractional_availability.setter
    def fractional_availability(self, fractional_availability):
        """
        Sets the fractional_availability of this ResourceAvailability.
        The most accurate count of available resources.


        :param fractional_availability: The fractional_availability of this ResourceAvailability.
        :type: float
        """
        self._fractional_availability = fractional_availability

    @property
    def effective_quota_value(self):
        """
        Gets the effective_quota_value of this ResourceAvailability.
        The effective quota value for the given compartment. This field is only present if there is a
        current quota policy affecting the current resource in the target region or availability domain.


        :return: The effective_quota_value of this ResourceAvailability.
        :rtype: float
        """
        return self._effective_quota_value

    @effective_quota_value.setter
    def effective_quota_value(self, effective_quota_value):
        """
        Sets the effective_quota_value of this ResourceAvailability.
        The effective quota value for the given compartment. This field is only present if there is a
        current quota policy affecting the current resource in the target region or availability domain.


        :param effective_quota_value: The effective_quota_value of this ResourceAvailability.
        :type: float
        """
        self._effective_quota_value = effective_quota_value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
