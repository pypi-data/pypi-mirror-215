# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RequestSummarizedMetricDataDetails(object):
    """
    The request details for retrieving aggregated data. Use the query and optional properties to filter the returned results.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RequestSummarizedMetricDataDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param namespace_name:
            The value to assign to the namespace_name property of this RequestSummarizedMetricDataDetails.
        :type namespace_name: str

        :param metric_name:
            The value to assign to the metric_name property of this RequestSummarizedMetricDataDetails.
        :type metric_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this RequestSummarizedMetricDataDetails.
        :type compartment_id: str

        :param dimensions:
            The value to assign to the dimensions property of this RequestSummarizedMetricDataDetails.
        :type dimensions: dict(str, DimensionValue)

        :param start_time:
            The value to assign to the start_time property of this RequestSummarizedMetricDataDetails.
        :type start_time: datetime

        :param end_time:
            The value to assign to the end_time property of this RequestSummarizedMetricDataDetails.
        :type end_time: datetime

        """
        self.swagger_types = {
            'namespace_name': 'str',
            'metric_name': 'str',
            'compartment_id': 'str',
            'dimensions': 'dict(str, DimensionValue)',
            'start_time': 'datetime',
            'end_time': 'datetime'
        }

        self.attribute_map = {
            'namespace_name': 'namespaceName',
            'metric_name': 'metricName',
            'compartment_id': 'compartmentId',
            'dimensions': 'dimensions',
            'start_time': 'startTime',
            'end_time': 'endTime'
        }

        self._namespace_name = None
        self._metric_name = None
        self._compartment_id = None
        self._dimensions = None
        self._start_time = None
        self._end_time = None

    @property
    def namespace_name(self):
        """
        **[Required]** Gets the namespace_name of this RequestSummarizedMetricDataDetails.
        The source service or application to use when searching for metric data points to aggregate. For a list of valid namespaces, see :func:`list_namespaces`.


        :return: The namespace_name of this RequestSummarizedMetricDataDetails.
        :rtype: str
        """
        return self._namespace_name

    @namespace_name.setter
    def namespace_name(self, namespace_name):
        """
        Sets the namespace_name of this RequestSummarizedMetricDataDetails.
        The source service or application to use when searching for metric data points to aggregate. For a list of valid namespaces, see :func:`list_namespaces`.


        :param namespace_name: The namespace_name of this RequestSummarizedMetricDataDetails.
        :type: str
        """
        self._namespace_name = namespace_name

    @property
    def metric_name(self):
        """
        **[Required]** Gets the metric_name of this RequestSummarizedMetricDataDetails.
        The name of a metric for retrieving aggregated data. For a list of valid metrics for a given namespace, see :func:`list_metric_properties`.


        :return: The metric_name of this RequestSummarizedMetricDataDetails.
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """
        Sets the metric_name of this RequestSummarizedMetricDataDetails.
        The name of a metric for retrieving aggregated data. For a list of valid metrics for a given namespace, see :func:`list_metric_properties`.


        :param metric_name: The metric_name of this RequestSummarizedMetricDataDetails.
        :type: str
        """
        self._metric_name = metric_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this RequestSummarizedMetricDataDetails.
        The OCID of the compartment to use for authorization to read metrics. To use the root compartment, provide the tenancyId.


        :return: The compartment_id of this RequestSummarizedMetricDataDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this RequestSummarizedMetricDataDetails.
        The OCID of the compartment to use for authorization to read metrics. To use the root compartment, provide the tenancyId.


        :param compartment_id: The compartment_id of this RequestSummarizedMetricDataDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def dimensions(self):
        """
        Gets the dimensions of this RequestSummarizedMetricDataDetails.
        Qualifiers to use when searching for metric data. For a list of valid dimensions for a given metric, see :func:`list_metric_properties`.


        :return: The dimensions of this RequestSummarizedMetricDataDetails.
        :rtype: dict(str, DimensionValue)
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """
        Sets the dimensions of this RequestSummarizedMetricDataDetails.
        Qualifiers to use when searching for metric data. For a list of valid dimensions for a given metric, see :func:`list_metric_properties`.


        :param dimensions: The dimensions of this RequestSummarizedMetricDataDetails.
        :type: dict(str, DimensionValue)
        """
        self._dimensions = dimensions

    @property
    def start_time(self):
        """
        Gets the start_time of this RequestSummarizedMetricDataDetails.
        The beginning of the sampled time range to use when searching for metric data points. Format is defined by <a href=\"https://www.rfc-editor.org/rfc/rfc3339\">RFC3339</a>. The response includes metric data points for the sampled time. Example 2019-02-01T02:02:29.600Z


        :return: The start_time of this RequestSummarizedMetricDataDetails.
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """
        Sets the start_time of this RequestSummarizedMetricDataDetails.
        The beginning of the sampled time range to use when searching for metric data points. Format is defined by <a href=\"https://www.rfc-editor.org/rfc/rfc3339\">RFC3339</a>. The response includes metric data points for the sampled time. Example 2019-02-01T02:02:29.600Z


        :param start_time: The start_time of this RequestSummarizedMetricDataDetails.
        :type: datetime
        """
        self._start_time = start_time

    @property
    def end_time(self):
        """
        Gets the end_time of this RequestSummarizedMetricDataDetails.
        The end of the sampled time range to use when searching for metric data points. Format is defined by <a href=\"https://www.rfc-editor.org/rfc/rfc3339\">RFC3339</a>. The response excludes metric data points for sampled time. Example 2019-02-01T02:02:29.600Z


        :return: The end_time of this RequestSummarizedMetricDataDetails.
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the end_time of this RequestSummarizedMetricDataDetails.
        The end of the sampled time range to use when searching for metric data points. Format is defined by <a href=\"https://www.rfc-editor.org/rfc/rfc3339\">RFC3339</a>. The response excludes metric data points for sampled time. Example 2019-02-01T02:02:29.600Z


        :param end_time: The end_time of this RequestSummarizedMetricDataDetails.
        :type: datetime
        """
        self._end_time = end_time

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
