# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdatePoolDetails(object):
    """
    The details required to update a given pool with ```poolId```.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdatePoolDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdatePoolDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdatePoolDetails.
        :type description: str

        :param configurations:
            The value to assign to the configurations property of this UpdatePoolDetails.
        :type configurations: list[oci.data_flow.models.PoolConfig]

        :param schedules:
            The value to assign to the schedules property of this UpdatePoolDetails.
        :type schedules: list[oci.data_flow.models.PoolSchedule]

        :param idle_timeout_in_minutes:
            The value to assign to the idle_timeout_in_minutes property of this UpdatePoolDetails.
        :type idle_timeout_in_minutes: int

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdatePoolDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdatePoolDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'configurations': 'list[PoolConfig]',
            'schedules': 'list[PoolSchedule]',
            'idle_timeout_in_minutes': 'int',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'configurations': 'configurations',
            'schedules': 'schedules',
            'idle_timeout_in_minutes': 'idleTimeoutInMinutes',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._description = None
        self._configurations = None
        self._schedules = None
        self._idle_timeout_in_minutes = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdatePoolDetails.
        A user-friendly name. It does not have to be unique. Avoid entering confidential information.


        :return: The display_name of this UpdatePoolDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdatePoolDetails.
        A user-friendly name. It does not have to be unique. Avoid entering confidential information.


        :param display_name: The display_name of this UpdatePoolDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this UpdatePoolDetails.
        A user-friendly description. Avoid entering confidential information.


        :return: The description of this UpdatePoolDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdatePoolDetails.
        A user-friendly description. Avoid entering confidential information.


        :param description: The description of this UpdatePoolDetails.
        :type: str
        """
        self._description = description

    @property
    def configurations(self):
        """
        Gets the configurations of this UpdatePoolDetails.
        List of PoolConfig items.


        :return: The configurations of this UpdatePoolDetails.
        :rtype: list[oci.data_flow.models.PoolConfig]
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        """
        Sets the configurations of this UpdatePoolDetails.
        List of PoolConfig items.


        :param configurations: The configurations of this UpdatePoolDetails.
        :type: list[oci.data_flow.models.PoolConfig]
        """
        self._configurations = configurations

    @property
    def schedules(self):
        """
        Gets the schedules of this UpdatePoolDetails.
        A list of schedules for pool to auto start and stop.


        :return: The schedules of this UpdatePoolDetails.
        :rtype: list[oci.data_flow.models.PoolSchedule]
        """
        return self._schedules

    @schedules.setter
    def schedules(self, schedules):
        """
        Sets the schedules of this UpdatePoolDetails.
        A list of schedules for pool to auto start and stop.


        :param schedules: The schedules of this UpdatePoolDetails.
        :type: list[oci.data_flow.models.PoolSchedule]
        """
        self._schedules = schedules

    @property
    def idle_timeout_in_minutes(self):
        """
        Gets the idle_timeout_in_minutes of this UpdatePoolDetails.
        Optional timeout value in minutes used to auto stop Pools. A Pool will be auto stopped after inactivity for this amount of time period.
        If value not set, pool will not be auto stopped auto.


        :return: The idle_timeout_in_minutes of this UpdatePoolDetails.
        :rtype: int
        """
        return self._idle_timeout_in_minutes

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, idle_timeout_in_minutes):
        """
        Sets the idle_timeout_in_minutes of this UpdatePoolDetails.
        Optional timeout value in minutes used to auto stop Pools. A Pool will be auto stopped after inactivity for this amount of time period.
        If value not set, pool will not be auto stopped auto.


        :param idle_timeout_in_minutes: The idle_timeout_in_minutes of this UpdatePoolDetails.
        :type: int
        """
        self._idle_timeout_in_minutes = idle_timeout_in_minutes

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdatePoolDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdatePoolDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdatePoolDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdatePoolDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdatePoolDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdatePoolDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdatePoolDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdatePoolDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
