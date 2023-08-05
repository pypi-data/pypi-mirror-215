# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class KeyValueDetectionLabelMetricsReport(object):
    """
    Label Metrics report for Key Value Detection Model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new KeyValueDetectionLabelMetricsReport object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param label:
            The value to assign to the label property of this KeyValueDetectionLabelMetricsReport.
        :type label: str

        :param document_count:
            The value to assign to the document_count property of this KeyValueDetectionLabelMetricsReport.
        :type document_count: int

        :param mean_average_precision:
            The value to assign to the mean_average_precision property of this KeyValueDetectionLabelMetricsReport.
        :type mean_average_precision: float

        :param confidence_entries:
            The value to assign to the confidence_entries property of this KeyValueDetectionLabelMetricsReport.
        :type confidence_entries: list[oci.ai_document.models.KeyValueDetectionConfidenceEntry]

        """
        self.swagger_types = {
            'label': 'str',
            'document_count': 'int',
            'mean_average_precision': 'float',
            'confidence_entries': 'list[KeyValueDetectionConfidenceEntry]'
        }

        self.attribute_map = {
            'label': 'label',
            'document_count': 'documentCount',
            'mean_average_precision': 'meanAveragePrecision',
            'confidence_entries': 'confidenceEntries'
        }

        self._label = None
        self._document_count = None
        self._mean_average_precision = None
        self._confidence_entries = None

    @property
    def label(self):
        """
        Gets the label of this KeyValueDetectionLabelMetricsReport.
        Label name


        :return: The label of this KeyValueDetectionLabelMetricsReport.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """
        Sets the label of this KeyValueDetectionLabelMetricsReport.
        Label name


        :param label: The label of this KeyValueDetectionLabelMetricsReport.
        :type: str
        """
        self._label = label

    @property
    def document_count(self):
        """
        Gets the document_count of this KeyValueDetectionLabelMetricsReport.
        Total test documents in the label.


        :return: The document_count of this KeyValueDetectionLabelMetricsReport.
        :rtype: int
        """
        return self._document_count

    @document_count.setter
    def document_count(self, document_count):
        """
        Sets the document_count of this KeyValueDetectionLabelMetricsReport.
        Total test documents in the label.


        :param document_count: The document_count of this KeyValueDetectionLabelMetricsReport.
        :type: int
        """
        self._document_count = document_count

    @property
    def mean_average_precision(self):
        """
        **[Required]** Gets the mean_average_precision of this KeyValueDetectionLabelMetricsReport.
        Mean average precision under different thresholds


        :return: The mean_average_precision of this KeyValueDetectionLabelMetricsReport.
        :rtype: float
        """
        return self._mean_average_precision

    @mean_average_precision.setter
    def mean_average_precision(self, mean_average_precision):
        """
        Sets the mean_average_precision of this KeyValueDetectionLabelMetricsReport.
        Mean average precision under different thresholds


        :param mean_average_precision: The mean_average_precision of this KeyValueDetectionLabelMetricsReport.
        :type: float
        """
        self._mean_average_precision = mean_average_precision

    @property
    def confidence_entries(self):
        """
        **[Required]** Gets the confidence_entries of this KeyValueDetectionLabelMetricsReport.
        List of key value detection confidence report.


        :return: The confidence_entries of this KeyValueDetectionLabelMetricsReport.
        :rtype: list[oci.ai_document.models.KeyValueDetectionConfidenceEntry]
        """
        return self._confidence_entries

    @confidence_entries.setter
    def confidence_entries(self, confidence_entries):
        """
        Sets the confidence_entries of this KeyValueDetectionLabelMetricsReport.
        List of key value detection confidence report.


        :param confidence_entries: The confidence_entries of this KeyValueDetectionLabelMetricsReport.
        :type: list[oci.ai_document.models.KeyValueDetectionConfidenceEntry]
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
