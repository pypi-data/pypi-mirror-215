# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class FieldName(object):
    """
    The name of a form field.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new FieldName object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this FieldName.
        :type name: str

        :param confidence:
            The value to assign to the confidence property of this FieldName.
        :type confidence: float

        :param bounding_polygon:
            The value to assign to the bounding_polygon property of this FieldName.
        :type bounding_polygon: oci.ai_vision.models.BoundingPolygon

        :param word_indexes:
            The value to assign to the word_indexes property of this FieldName.
        :type word_indexes: list[int]

        """
        self.swagger_types = {
            'name': 'str',
            'confidence': 'float',
            'bounding_polygon': 'BoundingPolygon',
            'word_indexes': 'list[int]'
        }

        self.attribute_map = {
            'name': 'name',
            'confidence': 'confidence',
            'bounding_polygon': 'boundingPolygon',
            'word_indexes': 'wordIndexes'
        }

        self._name = None
        self._confidence = None
        self._bounding_polygon = None
        self._word_indexes = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this FieldName.
        The name of the field.


        :return: The name of this FieldName.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FieldName.
        The name of the field.


        :param name: The name of this FieldName.
        :type: str
        """
        self._name = name

    @property
    def confidence(self):
        """
        Gets the confidence of this FieldName.
        The confidence score between 0 and 1.


        :return: The confidence of this FieldName.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """
        Sets the confidence of this FieldName.
        The confidence score between 0 and 1.


        :param confidence: The confidence of this FieldName.
        :type: float
        """
        self._confidence = confidence

    @property
    def bounding_polygon(self):
        """
        Gets the bounding_polygon of this FieldName.

        :return: The bounding_polygon of this FieldName.
        :rtype: oci.ai_vision.models.BoundingPolygon
        """
        return self._bounding_polygon

    @bounding_polygon.setter
    def bounding_polygon(self, bounding_polygon):
        """
        Sets the bounding_polygon of this FieldName.

        :param bounding_polygon: The bounding_polygon of this FieldName.
        :type: oci.ai_vision.models.BoundingPolygon
        """
        self._bounding_polygon = bounding_polygon

    @property
    def word_indexes(self):
        """
        Gets the word_indexes of this FieldName.
        The indexes of the words in the field name.


        :return: The word_indexes of this FieldName.
        :rtype: list[int]
        """
        return self._word_indexes

    @word_indexes.setter
    def word_indexes(self, word_indexes):
        """
        Sets the word_indexes of this FieldName.
        The indexes of the words in the field name.


        :param word_indexes: The word_indexes of this FieldName.
        :type: list[int]
        """
        self._word_indexes = word_indexes

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
