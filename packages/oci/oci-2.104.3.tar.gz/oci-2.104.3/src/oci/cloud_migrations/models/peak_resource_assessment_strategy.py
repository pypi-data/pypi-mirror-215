# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .resource_assessment_strategy import ResourceAssessmentStrategy
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PeakResourceAssessmentStrategy(ResourceAssessmentStrategy):
    """
    Peak usage based strategy.
    """

    #: A constant which can be used with the metric_type property of a PeakResourceAssessmentStrategy.
    #: This constant has a value of "AUTO"
    METRIC_TYPE_AUTO = "AUTO"

    #: A constant which can be used with the metric_type property of a PeakResourceAssessmentStrategy.
    #: This constant has a value of "HISTORICAL"
    METRIC_TYPE_HISTORICAL = "HISTORICAL"

    #: A constant which can be used with the metric_type property of a PeakResourceAssessmentStrategy.
    #: This constant has a value of "RUNTIME"
    METRIC_TYPE_RUNTIME = "RUNTIME"

    #: A constant which can be used with the metric_time_window property of a PeakResourceAssessmentStrategy.
    #: This constant has a value of "1d"
    METRIC_TIME_WINDOW_1D = "1d"

    #: A constant which can be used with the metric_time_window property of a PeakResourceAssessmentStrategy.
    #: This constant has a value of "7d"
    METRIC_TIME_WINDOW_7D = "7d"

    #: A constant which can be used with the metric_time_window property of a PeakResourceAssessmentStrategy.
    #: This constant has a value of "30d"
    METRIC_TIME_WINDOW_30D = "30d"

    def __init__(self, **kwargs):
        """
        Initializes a new PeakResourceAssessmentStrategy object with values from keyword arguments. The default value of the :py:attr:`~oci.cloud_migrations.models.PeakResourceAssessmentStrategy.strategy_type` attribute
        of this class is ``PEAK`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param resource_type:
            The value to assign to the resource_type property of this PeakResourceAssessmentStrategy.
            Allowed values for this property are: "CPU", "MEMORY", "ALL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_type: str

        :param strategy_type:
            The value to assign to the strategy_type property of this PeakResourceAssessmentStrategy.
            Allowed values for this property are: "AS_IS", "AVERAGE", "PEAK", "PERCENTILE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type strategy_type: str

        :param adjustment_multiplier:
            The value to assign to the adjustment_multiplier property of this PeakResourceAssessmentStrategy.
        :type adjustment_multiplier: float

        :param metric_type:
            The value to assign to the metric_type property of this PeakResourceAssessmentStrategy.
            Allowed values for this property are: "AUTO", "HISTORICAL", "RUNTIME", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type metric_type: str

        :param metric_time_window:
            The value to assign to the metric_time_window property of this PeakResourceAssessmentStrategy.
            Allowed values for this property are: "1d", "7d", "30d", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type metric_time_window: str

        """
        self.swagger_types = {
            'resource_type': 'str',
            'strategy_type': 'str',
            'adjustment_multiplier': 'float',
            'metric_type': 'str',
            'metric_time_window': 'str'
        }

        self.attribute_map = {
            'resource_type': 'resourceType',
            'strategy_type': 'strategyType',
            'adjustment_multiplier': 'adjustmentMultiplier',
            'metric_type': 'metricType',
            'metric_time_window': 'metricTimeWindow'
        }

        self._resource_type = None
        self._strategy_type = None
        self._adjustment_multiplier = None
        self._metric_type = None
        self._metric_time_window = None
        self._strategy_type = 'PEAK'

    @property
    def adjustment_multiplier(self):
        """
        Gets the adjustment_multiplier of this PeakResourceAssessmentStrategy.
        The real resource usage is multiplied to this number before making any recommendation.


        :return: The adjustment_multiplier of this PeakResourceAssessmentStrategy.
        :rtype: float
        """
        return self._adjustment_multiplier

    @adjustment_multiplier.setter
    def adjustment_multiplier(self, adjustment_multiplier):
        """
        Sets the adjustment_multiplier of this PeakResourceAssessmentStrategy.
        The real resource usage is multiplied to this number before making any recommendation.


        :param adjustment_multiplier: The adjustment_multiplier of this PeakResourceAssessmentStrategy.
        :type: float
        """
        self._adjustment_multiplier = adjustment_multiplier

    @property
    def metric_type(self):
        """
        Gets the metric_type of this PeakResourceAssessmentStrategy.
        The current state of the migration plan.

        Allowed values for this property are: "AUTO", "HISTORICAL", "RUNTIME", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The metric_type of this PeakResourceAssessmentStrategy.
        :rtype: str
        """
        return self._metric_type

    @metric_type.setter
    def metric_type(self, metric_type):
        """
        Sets the metric_type of this PeakResourceAssessmentStrategy.
        The current state of the migration plan.


        :param metric_type: The metric_type of this PeakResourceAssessmentStrategy.
        :type: str
        """
        allowed_values = ["AUTO", "HISTORICAL", "RUNTIME"]
        if not value_allowed_none_or_none_sentinel(metric_type, allowed_values):
            metric_type = 'UNKNOWN_ENUM_VALUE'
        self._metric_type = metric_type

    @property
    def metric_time_window(self):
        """
        Gets the metric_time_window of this PeakResourceAssessmentStrategy.
        The current state of the migration plan.

        Allowed values for this property are: "1d", "7d", "30d", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The metric_time_window of this PeakResourceAssessmentStrategy.
        :rtype: str
        """
        return self._metric_time_window

    @metric_time_window.setter
    def metric_time_window(self, metric_time_window):
        """
        Sets the metric_time_window of this PeakResourceAssessmentStrategy.
        The current state of the migration plan.


        :param metric_time_window: The metric_time_window of this PeakResourceAssessmentStrategy.
        :type: str
        """
        allowed_values = ["1d", "7d", "30d"]
        if not value_allowed_none_or_none_sentinel(metric_time_window, allowed_values):
            metric_time_window = 'UNKNOWN_ENUM_VALUE'
        self._metric_time_window = metric_time_window

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
