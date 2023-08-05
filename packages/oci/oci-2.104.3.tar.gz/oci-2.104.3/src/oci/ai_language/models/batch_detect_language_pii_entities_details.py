# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BatchDetectLanguagePiiEntitiesDetails(object):
    """
    The documents details to detect personal identification information.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new BatchDetectLanguagePiiEntitiesDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this BatchDetectLanguagePiiEntitiesDetails.
        :type compartment_id: str

        :param documents:
            The value to assign to the documents property of this BatchDetectLanguagePiiEntitiesDetails.
        :type documents: list[oci.ai_language.models.TextDocument]

        :param masking:
            The value to assign to the masking property of this BatchDetectLanguagePiiEntitiesDetails.
        :type masking: dict(str, PiiEntityMasking)

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'documents': 'list[TextDocument]',
            'masking': 'dict(str, PiiEntityMasking)'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'documents': 'documents',
            'masking': 'masking'
        }

        self._compartment_id = None
        self._documents = None
        self._masking = None

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this BatchDetectLanguagePiiEntitiesDetails.
        The `OCID`__ of the compartment that calls the API, inference will be served from pre trained model

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this BatchDetectLanguagePiiEntitiesDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this BatchDetectLanguagePiiEntitiesDetails.
        The `OCID`__ of the compartment that calls the API, inference will be served from pre trained model

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this BatchDetectLanguagePiiEntitiesDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def documents(self):
        """
        **[Required]** Gets the documents of this BatchDetectLanguagePiiEntitiesDetails.
        List of documents to detect personal identification information.


        :return: The documents of this BatchDetectLanguagePiiEntitiesDetails.
        :rtype: list[oci.ai_language.models.TextDocument]
        """
        return self._documents

    @documents.setter
    def documents(self, documents):
        """
        Sets the documents of this BatchDetectLanguagePiiEntitiesDetails.
        List of documents to detect personal identification information.


        :param documents: The documents of this BatchDetectLanguagePiiEntitiesDetails.
        :type: list[oci.ai_language.models.TextDocument]
        """
        self._documents = documents

    @property
    def masking(self):
        """
        Gets the masking of this BatchDetectLanguagePiiEntitiesDetails.
        Mask recognized PII entities with different modes.


        :return: The masking of this BatchDetectLanguagePiiEntitiesDetails.
        :rtype: dict(str, PiiEntityMasking)
        """
        return self._masking

    @masking.setter
    def masking(self, masking):
        """
        Sets the masking of this BatchDetectLanguagePiiEntitiesDetails.
        Mask recognized PII entities with different modes.


        :param masking: The masking of this BatchDetectLanguagePiiEntitiesDetails.
        :type: dict(str, PiiEntityMasking)
        """
        self._masking = masking

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
