# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DocumentClassificationOverallMetricsReport(object):
    """
    Overall Metrics report for Document Classification Model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DocumentClassificationOverallMetricsReport object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param mean_average_precision:
            The value to assign to the mean_average_precision property of this DocumentClassificationOverallMetricsReport.
        :type mean_average_precision: float

        :param confidence_entries:
            The value to assign to the confidence_entries property of this DocumentClassificationOverallMetricsReport.
        :type confidence_entries: list[oci.ai_document.models.DocumentClassificationConfidenceEntry]

        """
        self.swagger_types = {
            'mean_average_precision': 'float',
            'confidence_entries': 'list[DocumentClassificationConfidenceEntry]'
        }

        self.attribute_map = {
            'mean_average_precision': 'meanAveragePrecision',
            'confidence_entries': 'confidenceEntries'
        }

        self._mean_average_precision = None
        self._confidence_entries = None

    @property
    def mean_average_precision(self):
        """
        **[Required]** Gets the mean_average_precision of this DocumentClassificationOverallMetricsReport.
        Mean average precision under different thresholds


        :return: The mean_average_precision of this DocumentClassificationOverallMetricsReport.
        :rtype: float
        """
        return self._mean_average_precision

    @mean_average_precision.setter
    def mean_average_precision(self, mean_average_precision):
        """
        Sets the mean_average_precision of this DocumentClassificationOverallMetricsReport.
        Mean average precision under different thresholds


        :param mean_average_precision: The mean_average_precision of this DocumentClassificationOverallMetricsReport.
        :type: float
        """
        self._mean_average_precision = mean_average_precision

    @property
    def confidence_entries(self):
        """
        **[Required]** Gets the confidence_entries of this DocumentClassificationOverallMetricsReport.
        List of document classification confidence report.


        :return: The confidence_entries of this DocumentClassificationOverallMetricsReport.
        :rtype: list[oci.ai_document.models.DocumentClassificationConfidenceEntry]
        """
        return self._confidence_entries

    @confidence_entries.setter
    def confidence_entries(self, confidence_entries):
        """
        Sets the confidence_entries of this DocumentClassificationOverallMetricsReport.
        List of document classification confidence report.


        :param confidence_entries: The confidence_entries of this DocumentClassificationOverallMetricsReport.
        :type: list[oci.ai_document.models.DocumentClassificationConfidenceEntry]
        """
        self._confidence_entries = confidence_entries

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
