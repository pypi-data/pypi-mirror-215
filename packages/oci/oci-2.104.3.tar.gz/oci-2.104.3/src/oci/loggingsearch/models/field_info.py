# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class FieldInfo(object):
    """
    Contains field schema information.
    """

    #: A constant which can be used with the field_type property of a FieldInfo.
    #: This constant has a value of "STRING"
    FIELD_TYPE_STRING = "STRING"

    #: A constant which can be used with the field_type property of a FieldInfo.
    #: This constant has a value of "NUMBER"
    FIELD_TYPE_NUMBER = "NUMBER"

    #: A constant which can be used with the field_type property of a FieldInfo.
    #: This constant has a value of "BOOLEAN"
    FIELD_TYPE_BOOLEAN = "BOOLEAN"

    #: A constant which can be used with the field_type property of a FieldInfo.
    #: This constant has a value of "ARRAY"
    FIELD_TYPE_ARRAY = "ARRAY"

    def __init__(self, **kwargs):
        """
        Initializes a new FieldInfo object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param field_name:
            The value to assign to the field_name property of this FieldInfo.
        :type field_name: str

        :param field_type:
            The value to assign to the field_type property of this FieldInfo.
            Allowed values for this property are: "STRING", "NUMBER", "BOOLEAN", "ARRAY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type field_type: str

        """
        self.swagger_types = {
            'field_name': 'str',
            'field_type': 'str'
        }

        self.attribute_map = {
            'field_name': 'fieldName',
            'field_type': 'fieldType'
        }

        self._field_name = None
        self._field_type = None

    @property
    def field_name(self):
        """
        **[Required]** Gets the field_name of this FieldInfo.
        Field name


        :return: The field_name of this FieldInfo.
        :rtype: str
        """
        return self._field_name

    @field_name.setter
    def field_name(self, field_name):
        """
        Sets the field_name of this FieldInfo.
        Field name


        :param field_name: The field_name of this FieldInfo.
        :type: str
        """
        self._field_name = field_name

    @property
    def field_type(self):
        """
        **[Required]** Gets the field_type of this FieldInfo.
        Field type -
        * `STRING`: A sequence of characters.
        * `NUMBER`: Numeric type which can be an integer or floating point.
        * `BOOLEAN`: Either true or false.
        * `ARRAY`: An ordered collection of values.

        Allowed values for this property are: "STRING", "NUMBER", "BOOLEAN", "ARRAY", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The field_type of this FieldInfo.
        :rtype: str
        """
        return self._field_type

    @field_type.setter
    def field_type(self, field_type):
        """
        Sets the field_type of this FieldInfo.
        Field type -
        * `STRING`: A sequence of characters.
        * `NUMBER`: Numeric type which can be an integer or floating point.
        * `BOOLEAN`: Either true or false.
        * `ARRAY`: An ordered collection of values.


        :param field_type: The field_type of this FieldInfo.
        :type: str
        """
        allowed_values = ["STRING", "NUMBER", "BOOLEAN", "ARRAY"]
        if not value_allowed_none_or_none_sentinel(field_type, allowed_values):
            field_type = 'UNKNOWN_ENUM_VALUE'
        self._field_type = field_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
