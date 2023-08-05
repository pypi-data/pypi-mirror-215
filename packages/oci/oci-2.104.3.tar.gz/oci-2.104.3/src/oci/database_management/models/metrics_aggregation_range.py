# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MetricsAggregationRange(object):
    """
    The set of aggregated data returned for a metric.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MetricsAggregationRange object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param header:
            The value to assign to the header property of this MetricsAggregationRange.
        :type header: oci.database_management.models.DbManagementAnalyticsMetric

        :param metrics:
            The value to assign to the metrics property of this MetricsAggregationRange.
        :type metrics: list[oci.database_management.models.DbManagementAnalyticsMetric]

        :param range_start_time_in_epoch_seconds:
            The value to assign to the range_start_time_in_epoch_seconds property of this MetricsAggregationRange.
        :type range_start_time_in_epoch_seconds: int

        :param range_end_time_in_epoch_seconds:
            The value to assign to the range_end_time_in_epoch_seconds property of this MetricsAggregationRange.
        :type range_end_time_in_epoch_seconds: int

        """
        self.swagger_types = {
            'header': 'DbManagementAnalyticsMetric',
            'metrics': 'list[DbManagementAnalyticsMetric]',
            'range_start_time_in_epoch_seconds': 'int',
            'range_end_time_in_epoch_seconds': 'int'
        }

        self.attribute_map = {
            'header': 'header',
            'metrics': 'metrics',
            'range_start_time_in_epoch_seconds': 'rangeStartTimeInEpochSeconds',
            'range_end_time_in_epoch_seconds': 'rangeEndTimeInEpochSeconds'
        }

        self._header = None
        self._metrics = None
        self._range_start_time_in_epoch_seconds = None
        self._range_end_time_in_epoch_seconds = None

    @property
    def header(self):
        """
        Gets the header of this MetricsAggregationRange.

        :return: The header of this MetricsAggregationRange.
        :rtype: oci.database_management.models.DbManagementAnalyticsMetric
        """
        return self._header

    @header.setter
    def header(self, header):
        """
        Sets the header of this MetricsAggregationRange.

        :param header: The header of this MetricsAggregationRange.
        :type: oci.database_management.models.DbManagementAnalyticsMetric
        """
        self._header = header

    @property
    def metrics(self):
        """
        Gets the metrics of this MetricsAggregationRange.
        The list of metrics returned for the specified request. Each of the metrics
        has a `metricName` and additional properties like `metadata`, `dimensions`.
        If a property is not set, then use the value from `header`.

        Suppose `m` be an item in the `metrics` array:
        - If `m.metricName` is not set, use `header.metricName` instead
        - If `m.durationInSeconds` is not set, use `header.durationInSeconds` instead
        - If `m.dimensions` is not set, use `header.dimensions` instead
        - If `m.metadata` is not set, use `header.metadata` instead


        :return: The metrics of this MetricsAggregationRange.
        :rtype: list[oci.database_management.models.DbManagementAnalyticsMetric]
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics):
        """
        Sets the metrics of this MetricsAggregationRange.
        The list of metrics returned for the specified request. Each of the metrics
        has a `metricName` and additional properties like `metadata`, `dimensions`.
        If a property is not set, then use the value from `header`.

        Suppose `m` be an item in the `metrics` array:
        - If `m.metricName` is not set, use `header.metricName` instead
        - If `m.durationInSeconds` is not set, use `header.durationInSeconds` instead
        - If `m.dimensions` is not set, use `header.dimensions` instead
        - If `m.metadata` is not set, use `header.metadata` instead


        :param metrics: The metrics of this MetricsAggregationRange.
        :type: list[oci.database_management.models.DbManagementAnalyticsMetric]
        """
        self._metrics = metrics

    @property
    def range_start_time_in_epoch_seconds(self):
        """
        Gets the range_start_time_in_epoch_seconds of this MetricsAggregationRange.
        The beginning of the time range (inclusive) of the returned metric data.


        :return: The range_start_time_in_epoch_seconds of this MetricsAggregationRange.
        :rtype: int
        """
        return self._range_start_time_in_epoch_seconds

    @range_start_time_in_epoch_seconds.setter
    def range_start_time_in_epoch_seconds(self, range_start_time_in_epoch_seconds):
        """
        Sets the range_start_time_in_epoch_seconds of this MetricsAggregationRange.
        The beginning of the time range (inclusive) of the returned metric data.


        :param range_start_time_in_epoch_seconds: The range_start_time_in_epoch_seconds of this MetricsAggregationRange.
        :type: int
        """
        self._range_start_time_in_epoch_seconds = range_start_time_in_epoch_seconds

    @property
    def range_end_time_in_epoch_seconds(self):
        """
        Gets the range_end_time_in_epoch_seconds of this MetricsAggregationRange.
        The end of the time range (exclusive) of the returned metric data.


        :return: The range_end_time_in_epoch_seconds of this MetricsAggregationRange.
        :rtype: int
        """
        return self._range_end_time_in_epoch_seconds

    @range_end_time_in_epoch_seconds.setter
    def range_end_time_in_epoch_seconds(self, range_end_time_in_epoch_seconds):
        """
        Sets the range_end_time_in_epoch_seconds of this MetricsAggregationRange.
        The end of the time range (exclusive) of the returned metric data.


        :param range_end_time_in_epoch_seconds: The range_end_time_in_epoch_seconds of this MetricsAggregationRange.
        :type: int
        """
        self._range_end_time_in_epoch_seconds = range_end_time_in_epoch_seconds

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
