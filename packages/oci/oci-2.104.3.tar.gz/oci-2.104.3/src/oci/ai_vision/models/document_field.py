# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DocumentField(object):
    """
    Form field.
    """

    #: A constant which can be used with the field_type property of a DocumentField.
    #: This constant has a value of "LINE_ITEM_GROUP"
    FIELD_TYPE_LINE_ITEM_GROUP = "LINE_ITEM_GROUP"

    #: A constant which can be used with the field_type property of a DocumentField.
    #: This constant has a value of "LINE_ITEM"
    FIELD_TYPE_LINE_ITEM = "LINE_ITEM"

    #: A constant which can be used with the field_type property of a DocumentField.
    #: This constant has a value of "LINE_ITEM_FIELD"
    FIELD_TYPE_LINE_ITEM_FIELD = "LINE_ITEM_FIELD"

    #: A constant which can be used with the field_type property of a DocumentField.
    #: This constant has a value of "KEY_VALUE"
    FIELD_TYPE_KEY_VALUE = "KEY_VALUE"

    def __init__(self, **kwargs):
        """
        Initializes a new DocumentField object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param field_type:
            The value to assign to the field_type property of this DocumentField.
            Allowed values for this property are: "LINE_ITEM_GROUP", "LINE_ITEM", "LINE_ITEM_FIELD", "KEY_VALUE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type field_type: str

        :param field_label:
            The value to assign to the field_label property of this DocumentField.
        :type field_label: oci.ai_vision.models.FieldLabel

        :param field_name:
            The value to assign to the field_name property of this DocumentField.
        :type field_name: oci.ai_vision.models.FieldName

        :param field_value:
            The value to assign to the field_value property of this DocumentField.
        :type field_value: oci.ai_vision.models.FieldValue

        """
        self.swagger_types = {
            'field_type': 'str',
            'field_label': 'FieldLabel',
            'field_name': 'FieldName',
            'field_value': 'FieldValue'
        }

        self.attribute_map = {
            'field_type': 'fieldType',
            'field_label': 'fieldLabel',
            'field_name': 'fieldName',
            'field_value': 'fieldValue'
        }

        self._field_type = None
        self._field_label = None
        self._field_name = None
        self._field_value = None

    @property
    def field_type(self):
        """
        **[Required]** Gets the field_type of this DocumentField.
        The field type.

        Allowed values for this property are: "LINE_ITEM_GROUP", "LINE_ITEM", "LINE_ITEM_FIELD", "KEY_VALUE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The field_type of this DocumentField.
        :rtype: str
        """
        return self._field_type

    @field_type.setter
    def field_type(self, field_type):
        """
        Sets the field_type of this DocumentField.
        The field type.


        :param field_type: The field_type of this DocumentField.
        :type: str
        """
        allowed_values = ["LINE_ITEM_GROUP", "LINE_ITEM", "LINE_ITEM_FIELD", "KEY_VALUE"]
        if not value_allowed_none_or_none_sentinel(field_type, allowed_values):
            field_type = 'UNKNOWN_ENUM_VALUE'
        self._field_type = field_type

    @property
    def field_label(self):
        """
        Gets the field_label of this DocumentField.

        :return: The field_label of this DocumentField.
        :rtype: oci.ai_vision.models.FieldLabel
        """
        return self._field_label

    @field_label.setter
    def field_label(self, field_label):
        """
        Sets the field_label of this DocumentField.

        :param field_label: The field_label of this DocumentField.
        :type: oci.ai_vision.models.FieldLabel
        """
        self._field_label = field_label

    @property
    def field_name(self):
        """
        Gets the field_name of this DocumentField.

        :return: The field_name of this DocumentField.
        :rtype: oci.ai_vision.models.FieldName
        """
        return self._field_name

    @field_name.setter
    def field_name(self, field_name):
        """
        Sets the field_name of this DocumentField.

        :param field_name: The field_name of this DocumentField.
        :type: oci.ai_vision.models.FieldName
        """
        self._field_name = field_name

    @property
    def field_value(self):
        """
        **[Required]** Gets the field_value of this DocumentField.

        :return: The field_value of this DocumentField.
        :rtype: oci.ai_vision.models.FieldValue
        """
        return self._field_value

    @field_value.setter
    def field_value(self, field_value):
        """
        Sets the field_value of this DocumentField.

        :param field_value: The field_value of this DocumentField.
        :type: oci.ai_vision.models.FieldValue
        """
        self._field_value = field_value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
