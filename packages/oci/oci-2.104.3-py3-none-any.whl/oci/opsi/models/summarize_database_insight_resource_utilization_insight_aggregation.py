# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SummarizeDatabaseInsightResourceUtilizationInsightAggregation(object):
    """
    Insights response containing current/projected groups for storage or CPU.
    """

    #: A constant which can be used with the resource_metric property of a SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
    #: This constant has a value of "CPU"
    RESOURCE_METRIC_CPU = "CPU"

    #: A constant which can be used with the resource_metric property of a SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
    #: This constant has a value of "STORAGE"
    RESOURCE_METRIC_STORAGE = "STORAGE"

    #: A constant which can be used with the resource_metric property of a SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
    #: This constant has a value of "IO"
    RESOURCE_METRIC_IO = "IO"

    #: A constant which can be used with the resource_metric property of a SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
    #: This constant has a value of "MEMORY"
    RESOURCE_METRIC_MEMORY = "MEMORY"

    #: A constant which can be used with the resource_metric property of a SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
    #: This constant has a value of "MEMORY_PGA"
    RESOURCE_METRIC_MEMORY_PGA = "MEMORY_PGA"

    #: A constant which can be used with the resource_metric property of a SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
    #: This constant has a value of "MEMORY_SGA"
    RESOURCE_METRIC_MEMORY_SGA = "MEMORY_SGA"

    def __init__(self, **kwargs):
        """
        Initializes a new SummarizeDatabaseInsightResourceUtilizationInsightAggregation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_interval_start:
            The value to assign to the time_interval_start property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type time_interval_start: datetime

        :param time_interval_end:
            The value to assign to the time_interval_end property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type time_interval_end: datetime

        :param high_utilization_threshold:
            The value to assign to the high_utilization_threshold property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type high_utilization_threshold: int

        :param low_utilization_threshold:
            The value to assign to the low_utilization_threshold property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type low_utilization_threshold: int

        :param resource_metric:
            The value to assign to the resource_metric property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
            Allowed values for this property are: "CPU", "STORAGE", "IO", "MEMORY", "MEMORY_PGA", "MEMORY_SGA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_metric: str

        :param projected_utilization:
            The value to assign to the projected_utilization property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type projected_utilization: oci.opsi.models.ResourceInsightProjectedUtilization

        :param current_utilization:
            The value to assign to the current_utilization property of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type current_utilization: oci.opsi.models.ResourceInsightCurrentUtilization

        """
        self.swagger_types = {
            'time_interval_start': 'datetime',
            'time_interval_end': 'datetime',
            'high_utilization_threshold': 'int',
            'low_utilization_threshold': 'int',
            'resource_metric': 'str',
            'projected_utilization': 'ResourceInsightProjectedUtilization',
            'current_utilization': 'ResourceInsightCurrentUtilization'
        }

        self.attribute_map = {
            'time_interval_start': 'timeIntervalStart',
            'time_interval_end': 'timeIntervalEnd',
            'high_utilization_threshold': 'highUtilizationThreshold',
            'low_utilization_threshold': 'lowUtilizationThreshold',
            'resource_metric': 'resourceMetric',
            'projected_utilization': 'projectedUtilization',
            'current_utilization': 'currentUtilization'
        }

        self._time_interval_start = None
        self._time_interval_end = None
        self._high_utilization_threshold = None
        self._low_utilization_threshold = None
        self._resource_metric = None
        self._projected_utilization = None
        self._current_utilization = None

    @property
    def time_interval_start(self):
        """
        **[Required]** Gets the time_interval_start of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        The start timestamp that was passed into the request.


        :return: The time_interval_start of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: datetime
        """
        return self._time_interval_start

    @time_interval_start.setter
    def time_interval_start(self, time_interval_start):
        """
        Sets the time_interval_start of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        The start timestamp that was passed into the request.


        :param time_interval_start: The time_interval_start of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: datetime
        """
        self._time_interval_start = time_interval_start

    @property
    def time_interval_end(self):
        """
        **[Required]** Gets the time_interval_end of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        The end timestamp that was passed into the request.


        :return: The time_interval_end of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: datetime
        """
        return self._time_interval_end

    @time_interval_end.setter
    def time_interval_end(self, time_interval_end):
        """
        Sets the time_interval_end of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        The end timestamp that was passed into the request.


        :param time_interval_end: The time_interval_end of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: datetime
        """
        self._time_interval_end = time_interval_end

    @property
    def high_utilization_threshold(self):
        """
        **[Required]** Gets the high_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        Percent value in which a resource metric is considered highly utilized.


        :return: The high_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: int
        """
        return self._high_utilization_threshold

    @high_utilization_threshold.setter
    def high_utilization_threshold(self, high_utilization_threshold):
        """
        Sets the high_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        Percent value in which a resource metric is considered highly utilized.


        :param high_utilization_threshold: The high_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: int
        """
        self._high_utilization_threshold = high_utilization_threshold

    @property
    def low_utilization_threshold(self):
        """
        **[Required]** Gets the low_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        Percent value in which a resource metric is considered lowly utilized.


        :return: The low_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: int
        """
        return self._low_utilization_threshold

    @low_utilization_threshold.setter
    def low_utilization_threshold(self, low_utilization_threshold):
        """
        Sets the low_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        Percent value in which a resource metric is considered lowly utilized.


        :param low_utilization_threshold: The low_utilization_threshold of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: int
        """
        self._low_utilization_threshold = low_utilization_threshold

    @property
    def resource_metric(self):
        """
        **[Required]** Gets the resource_metric of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        Defines the type of resource metric (example: CPU, STORAGE)

        Allowed values for this property are: "CPU", "STORAGE", "IO", "MEMORY", "MEMORY_PGA", "MEMORY_SGA", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The resource_metric of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: str
        """
        return self._resource_metric

    @resource_metric.setter
    def resource_metric(self, resource_metric):
        """
        Sets the resource_metric of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        Defines the type of resource metric (example: CPU, STORAGE)


        :param resource_metric: The resource_metric of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: str
        """
        allowed_values = ["CPU", "STORAGE", "IO", "MEMORY", "MEMORY_PGA", "MEMORY_SGA"]
        if not value_allowed_none_or_none_sentinel(resource_metric, allowed_values):
            resource_metric = 'UNKNOWN_ENUM_VALUE'
        self._resource_metric = resource_metric

    @property
    def projected_utilization(self):
        """
        **[Required]** Gets the projected_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.

        :return: The projected_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: oci.opsi.models.ResourceInsightProjectedUtilization
        """
        return self._projected_utilization

    @projected_utilization.setter
    def projected_utilization(self, projected_utilization):
        """
        Sets the projected_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.

        :param projected_utilization: The projected_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: oci.opsi.models.ResourceInsightProjectedUtilization
        """
        self._projected_utilization = projected_utilization

    @property
    def current_utilization(self):
        """
        **[Required]** Gets the current_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.

        :return: The current_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :rtype: oci.opsi.models.ResourceInsightCurrentUtilization
        """
        return self._current_utilization

    @current_utilization.setter
    def current_utilization(self, current_utilization):
        """
        Sets the current_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.

        :param current_utilization: The current_utilization of this SummarizeDatabaseInsightResourceUtilizationInsightAggregation.
        :type: oci.opsi.models.ResourceInsightCurrentUtilization
        """
        self._current_utilization = current_utilization

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
