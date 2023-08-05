# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MaintenanceWindowSchedule(object):
    """
    Details used to schedule maintenance window.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MaintenanceWindowSchedule object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_started:
            The value to assign to the time_started property of this MaintenanceWindowSchedule.
        :type time_started: datetime

        :param time_ended:
            The value to assign to the time_ended property of this MaintenanceWindowSchedule.
        :type time_ended: datetime

        """
        self.swagger_types = {
            'time_started': 'datetime',
            'time_ended': 'datetime'
        }

        self.attribute_map = {
            'time_started': 'timeStarted',
            'time_ended': 'timeEnded'
        }

        self._time_started = None
        self._time_ended = None

    @property
    def time_started(self):
        """
        Gets the time_started of this MaintenanceWindowSchedule.
        Start time for the maintenance window, expressed in `RFC 3339`__ timestamp format.
        Example: `2020-02-12T22:47:12.613Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_started of this MaintenanceWindowSchedule.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this MaintenanceWindowSchedule.
        Start time for the maintenance window, expressed in `RFC 3339`__ timestamp format.
        Example: `2020-02-12T22:47:12.613Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_started: The time_started of this MaintenanceWindowSchedule.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_ended(self):
        """
        Gets the time_ended of this MaintenanceWindowSchedule.
        End time for the maintenance window, expressed in `RFC 3339`__ timestamp format.
        Example: `2020-02-12T22:47:12.613Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_ended of this MaintenanceWindowSchedule.
        :rtype: datetime
        """
        return self._time_ended

    @time_ended.setter
    def time_ended(self, time_ended):
        """
        Sets the time_ended of this MaintenanceWindowSchedule.
        End time for the maintenance window, expressed in `RFC 3339`__ timestamp format.
        Example: `2020-02-12T22:47:12.613Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_ended: The time_ended of this MaintenanceWindowSchedule.
        :type: datetime
        """
        self._time_ended = time_ended

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
