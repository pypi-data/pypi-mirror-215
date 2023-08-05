# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateDetectAnomalyJobDetails(object):
    """
    The information to be updated for the DetectAnomalyJob.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateDetectAnomalyJobDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param description:
            The value to assign to the description property of this UpdateDetectAnomalyJobDetails.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this UpdateDetectAnomalyJobDetails.
        :type display_name: str

        """
        self.swagger_types = {
            'description': 'str',
            'display_name': 'str'
        }

        self.attribute_map = {
            'description': 'description',
            'display_name': 'displayName'
        }

        self._description = None
        self._display_name = None

    @property
    def description(self):
        """
        Gets the description of this UpdateDetectAnomalyJobDetails.
        A short description of the detect anomaly job.


        :return: The description of this UpdateDetectAnomalyJobDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateDetectAnomalyJobDetails.
        A short description of the detect anomaly job.


        :param description: The description of this UpdateDetectAnomalyJobDetails.
        :type: str
        """
        self._description = description

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateDetectAnomalyJobDetails.
        Detect anomaly job display name.


        :return: The display_name of this UpdateDetectAnomalyJobDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateDetectAnomalyJobDetails.
        Detect anomaly job display name.


        :param display_name: The display_name of this UpdateDetectAnomalyJobDetails.
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
