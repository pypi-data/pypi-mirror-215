# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RefreshDetails(object):
    """
    Describes a refresh of a fusion environment
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RefreshDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_fusion_environment_id:
            The value to assign to the source_fusion_environment_id property of this RefreshDetails.
        :type source_fusion_environment_id: str

        :param time_finished:
            The value to assign to the time_finished property of this RefreshDetails.
        :type time_finished: datetime

        :param time_of_restoration_point:
            The value to assign to the time_of_restoration_point property of this RefreshDetails.
        :type time_of_restoration_point: datetime

        """
        self.swagger_types = {
            'source_fusion_environment_id': 'str',
            'time_finished': 'datetime',
            'time_of_restoration_point': 'datetime'
        }

        self.attribute_map = {
            'source_fusion_environment_id': 'sourceFusionEnvironmentId',
            'time_finished': 'timeFinished',
            'time_of_restoration_point': 'timeOfRestorationPoint'
        }

        self._source_fusion_environment_id = None
        self._time_finished = None
        self._time_of_restoration_point = None

    @property
    def source_fusion_environment_id(self):
        """
        **[Required]** Gets the source_fusion_environment_id of this RefreshDetails.
        The source environment id for the last refresh


        :return: The source_fusion_environment_id of this RefreshDetails.
        :rtype: str
        """
        return self._source_fusion_environment_id

    @source_fusion_environment_id.setter
    def source_fusion_environment_id(self, source_fusion_environment_id):
        """
        Sets the source_fusion_environment_id of this RefreshDetails.
        The source environment id for the last refresh


        :param source_fusion_environment_id: The source_fusion_environment_id of this RefreshDetails.
        :type: str
        """
        self._source_fusion_environment_id = source_fusion_environment_id

    @property
    def time_finished(self):
        """
        **[Required]** Gets the time_finished of this RefreshDetails.
        The time of when the last refresh finish


        :return: The time_finished of this RefreshDetails.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this RefreshDetails.
        The time of when the last refresh finish


        :param time_finished: The time_finished of this RefreshDetails.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def time_of_restoration_point(self):
        """
        **[Required]** Gets the time_of_restoration_point of this RefreshDetails.
        The point of time of the latest DB backup for the last refresh


        :return: The time_of_restoration_point of this RefreshDetails.
        :rtype: datetime
        """
        return self._time_of_restoration_point

    @time_of_restoration_point.setter
    def time_of_restoration_point(self, time_of_restoration_point):
        """
        Sets the time_of_restoration_point of this RefreshDetails.
        The point of time of the latest DB backup for the last refresh


        :param time_of_restoration_point: The time_of_restoration_point of this RefreshDetails.
        :type: datetime
        """
        self._time_of_restoration_point = time_of_restoration_point

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
