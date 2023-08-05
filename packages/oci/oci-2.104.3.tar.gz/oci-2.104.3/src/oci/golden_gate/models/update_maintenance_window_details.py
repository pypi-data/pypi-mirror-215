# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateMaintenanceWindowDetails(object):
    """
    Defines the maintenance window for update operation, when automatic actions can be performed.
    """

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "MONDAY"
    DAY_MONDAY = "MONDAY"

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "TUESDAY"
    DAY_TUESDAY = "TUESDAY"

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "WEDNESDAY"
    DAY_WEDNESDAY = "WEDNESDAY"

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "THURSDAY"
    DAY_THURSDAY = "THURSDAY"

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "FRIDAY"
    DAY_FRIDAY = "FRIDAY"

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "SATURDAY"
    DAY_SATURDAY = "SATURDAY"

    #: A constant which can be used with the day property of a UpdateMaintenanceWindowDetails.
    #: This constant has a value of "SUNDAY"
    DAY_SUNDAY = "SUNDAY"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateMaintenanceWindowDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param day:
            The value to assign to the day property of this UpdateMaintenanceWindowDetails.
            Allowed values for this property are: "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"
        :type day: str

        :param start_hour:
            The value to assign to the start_hour property of this UpdateMaintenanceWindowDetails.
        :type start_hour: int

        """
        self.swagger_types = {
            'day': 'str',
            'start_hour': 'int'
        }

        self.attribute_map = {
            'day': 'day',
            'start_hour': 'startHour'
        }

        self._day = None
        self._start_hour = None

    @property
    def day(self):
        """
        **[Required]** Gets the day of this UpdateMaintenanceWindowDetails.
        Days of the week.

        Allowed values for this property are: "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"


        :return: The day of this UpdateMaintenanceWindowDetails.
        :rtype: str
        """
        return self._day

    @day.setter
    def day(self, day):
        """
        Sets the day of this UpdateMaintenanceWindowDetails.
        Days of the week.


        :param day: The day of this UpdateMaintenanceWindowDetails.
        :type: str
        """
        allowed_values = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
        if not value_allowed_none_or_none_sentinel(day, allowed_values):
            raise ValueError(
                "Invalid value for `day`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._day = day

    @property
    def start_hour(self):
        """
        **[Required]** Gets the start_hour of this UpdateMaintenanceWindowDetails.
        Start hour for maintenance period. Hour is in UTC.


        :return: The start_hour of this UpdateMaintenanceWindowDetails.
        :rtype: int
        """
        return self._start_hour

    @start_hour.setter
    def start_hour(self, start_hour):
        """
        Sets the start_hour of this UpdateMaintenanceWindowDetails.
        Start hour for maintenance period. Hour is in UTC.


        :param start_hour: The start_hour of this UpdateMaintenanceWindowDetails.
        :type: int
        """
        self._start_hour = start_hour

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
