# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .document_feature import DocumentFeature
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DocumentTextExtractionFeature(DocumentFeature):
    """
    Text recognition
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DocumentTextExtractionFeature object with values from keyword arguments. The default value of the :py:attr:`~oci.ai_document.models.DocumentTextExtractionFeature.feature_type` attribute
        of this class is ``TEXT_EXTRACTION`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param feature_type:
            The value to assign to the feature_type property of this DocumentTextExtractionFeature.
            Allowed values for this property are: "LANGUAGE_CLASSIFICATION", "TEXT_EXTRACTION", "TABLE_EXTRACTION", "KEY_VALUE_EXTRACTION", "DOCUMENT_CLASSIFICATION"
        :type feature_type: str

        :param generate_searchable_pdf:
            The value to assign to the generate_searchable_pdf property of this DocumentTextExtractionFeature.
        :type generate_searchable_pdf: bool

        """
        self.swagger_types = {
            'feature_type': 'str',
            'generate_searchable_pdf': 'bool'
        }

        self.attribute_map = {
            'feature_type': 'featureType',
            'generate_searchable_pdf': 'generateSearchablePdf'
        }

        self._feature_type = None
        self._generate_searchable_pdf = None
        self._feature_type = 'TEXT_EXTRACTION'

    @property
    def generate_searchable_pdf(self):
        """
        Gets the generate_searchable_pdf of this DocumentTextExtractionFeature.
        Whether or not to generate a searchable PDF file.


        :return: The generate_searchable_pdf of this DocumentTextExtractionFeature.
        :rtype: bool
        """
        return self._generate_searchable_pdf

    @generate_searchable_pdf.setter
    def generate_searchable_pdf(self, generate_searchable_pdf):
        """
        Sets the generate_searchable_pdf of this DocumentTextExtractionFeature.
        Whether or not to generate a searchable PDF file.


        :param generate_searchable_pdf: The generate_searchable_pdf of this DocumentTextExtractionFeature.
        :type: bool
        """
        self._generate_searchable_pdf = generate_searchable_pdf

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
