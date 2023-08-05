# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ModelMetrics(object):
    """
    Trained Model Metrics.
    """

    #: A constant which can be used with the model_type property of a ModelMetrics.
    #: This constant has a value of "KEY_VALUE_EXTRACTION"
    MODEL_TYPE_KEY_VALUE_EXTRACTION = "KEY_VALUE_EXTRACTION"

    #: A constant which can be used with the model_type property of a ModelMetrics.
    #: This constant has a value of "DOCUMENT_CLASSIFICATION"
    MODEL_TYPE_DOCUMENT_CLASSIFICATION = "DOCUMENT_CLASSIFICATION"

    def __init__(self, **kwargs):
        """
        Initializes a new ModelMetrics object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.ai_document.models.DocumentClassificationModelMetrics`
        * :class:`~oci.ai_document.models.KeyValueDetectionModelMetrics`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this ModelMetrics.
            Allowed values for this property are: "KEY_VALUE_EXTRACTION", "DOCUMENT_CLASSIFICATION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type model_type: str

        :param dataset_summary:
            The value to assign to the dataset_summary property of this ModelMetrics.
        :type dataset_summary: oci.ai_document.models.DatasetSummary

        """
        self.swagger_types = {
            'model_type': 'str',
            'dataset_summary': 'DatasetSummary'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'dataset_summary': 'datasetSummary'
        }

        self._model_type = None
        self._dataset_summary = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['modelType']

        if type == 'DOCUMENT_CLASSIFICATION':
            return 'DocumentClassificationModelMetrics'

        if type == 'KEY_VALUE_EXTRACTION':
            return 'KeyValueDetectionModelMetrics'
        else:
            return 'ModelMetrics'

    @property
    def model_type(self):
        """
        **[Required]** Gets the model_type of this ModelMetrics.
        The type of custom model trained.

        Allowed values for this property are: "KEY_VALUE_EXTRACTION", "DOCUMENT_CLASSIFICATION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The model_type of this ModelMetrics.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this ModelMetrics.
        The type of custom model trained.


        :param model_type: The model_type of this ModelMetrics.
        :type: str
        """
        allowed_values = ["KEY_VALUE_EXTRACTION", "DOCUMENT_CLASSIFICATION"]
        if not value_allowed_none_or_none_sentinel(model_type, allowed_values):
            model_type = 'UNKNOWN_ENUM_VALUE'
        self._model_type = model_type

    @property
    def dataset_summary(self):
        """
        Gets the dataset_summary of this ModelMetrics.

        :return: The dataset_summary of this ModelMetrics.
        :rtype: oci.ai_document.models.DatasetSummary
        """
        return self._dataset_summary

    @dataset_summary.setter
    def dataset_summary(self, dataset_summary):
        """
        Sets the dataset_summary of this ModelMetrics.

        :param dataset_summary: The dataset_summary of this ModelMetrics.
        :type: oci.ai_document.models.DatasetSummary
        """
        self._dataset_summary = dataset_summary

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
