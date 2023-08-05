# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AlarmDimensionStatesEntry(object):
    """
    A timestamped alarm state entry for a metric stream.
    """

    #: A constant which can be used with the status property of a AlarmDimensionStatesEntry.
    #: This constant has a value of "FIRING"
    STATUS_FIRING = "FIRING"

    #: A constant which can be used with the status property of a AlarmDimensionStatesEntry.
    #: This constant has a value of "OK"
    STATUS_OK = "OK"

    def __init__(self, **kwargs):
        """
        Initializes a new AlarmDimensionStatesEntry object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param dimensions:
            The value to assign to the dimensions property of this AlarmDimensionStatesEntry.
        :type dimensions: dict(str, str)

        :param status:
            The value to assign to the status property of this AlarmDimensionStatesEntry.
            Allowed values for this property are: "FIRING", "OK", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param timestamp:
            The value to assign to the timestamp property of this AlarmDimensionStatesEntry.
        :type timestamp: datetime

        """
        self.swagger_types = {
            'dimensions': 'dict(str, str)',
            'status': 'str',
            'timestamp': 'datetime'
        }

        self.attribute_map = {
            'dimensions': 'dimensions',
            'status': 'status',
            'timestamp': 'timestamp'
        }

        self._dimensions = None
        self._status = None
        self._timestamp = None

    @property
    def dimensions(self):
        """
        **[Required]** Gets the dimensions of this AlarmDimensionStatesEntry.
        Indicator of the metric stream associated with the alarm state entry. Includes one or more dimension key-value pairs.


        :return: The dimensions of this AlarmDimensionStatesEntry.
        :rtype: dict(str, str)
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """
        Sets the dimensions of this AlarmDimensionStatesEntry.
        Indicator of the metric stream associated with the alarm state entry. Includes one or more dimension key-value pairs.


        :param dimensions: The dimensions of this AlarmDimensionStatesEntry.
        :type: dict(str, str)
        """
        self._dimensions = dimensions

    @property
    def status(self):
        """
        **[Required]** Gets the status of this AlarmDimensionStatesEntry.
        Transition state (status value) associated with the alarm state entry.

        Example: `FIRING`

        Allowed values for this property are: "FIRING", "OK", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this AlarmDimensionStatesEntry.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AlarmDimensionStatesEntry.
        Transition state (status value) associated with the alarm state entry.

        Example: `FIRING`


        :param status: The status of this AlarmDimensionStatesEntry.
        :type: str
        """
        allowed_values = ["FIRING", "OK"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def timestamp(self):
        """
        **[Required]** Gets the timestamp of this AlarmDimensionStatesEntry.
        Transition time associated with the alarm state entry. Format defined by RFC3339.

        Example: `2022-02-01T01:02:29.600Z`


        :return: The timestamp of this AlarmDimensionStatesEntry.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this AlarmDimensionStatesEntry.
        Transition time associated with the alarm state entry. Format defined by RFC3339.

        Example: `2022-02-01T01:02:29.600Z`


        :param timestamp: The timestamp of this AlarmDimensionStatesEntry.
        :type: datetime
        """
        self._timestamp = timestamp

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
