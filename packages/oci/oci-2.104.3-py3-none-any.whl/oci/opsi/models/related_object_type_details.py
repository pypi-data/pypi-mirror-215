# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RelatedObjectTypeDetails(object):
    """
    Related object details
    """

    #: A constant which can be used with the type property of a RelatedObjectTypeDetails.
    #: This constant has a value of "SCHEMA_OBJECT"
    TYPE_SCHEMA_OBJECT = "SCHEMA_OBJECT"

    #: A constant which can be used with the type property of a RelatedObjectTypeDetails.
    #: This constant has a value of "SQL"
    TYPE_SQL = "SQL"

    #: A constant which can be used with the type property of a RelatedObjectTypeDetails.
    #: This constant has a value of "DATABASE_PARAMETER"
    TYPE_DATABASE_PARAMETER = "DATABASE_PARAMETER"

    def __init__(self, **kwargs):
        """
        Initializes a new RelatedObjectTypeDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.opsi.models.SqlTypeDetails`
        * :class:`~oci.opsi.models.SchemaObjectTypeDetails`
        * :class:`~oci.opsi.models.DatabaseParameterTypeDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this RelatedObjectTypeDetails.
            Allowed values for this property are: "SCHEMA_OBJECT", "SQL", "DATABASE_PARAMETER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        """
        self.swagger_types = {
            'type': 'str'
        }

        self.attribute_map = {
            'type': 'type'
        }

        self._type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'SQL':
            return 'SqlTypeDetails'

        if type == 'SCHEMA_OBJECT':
            return 'SchemaObjectTypeDetails'

        if type == 'DATABASE_PARAMETER':
            return 'DatabaseParameterTypeDetails'
        else:
            return 'RelatedObjectTypeDetails'

    @property
    def type(self):
        """
        **[Required]** Gets the type of this RelatedObjectTypeDetails.
        Type of related object

        Allowed values for this property are: "SCHEMA_OBJECT", "SQL", "DATABASE_PARAMETER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this RelatedObjectTypeDetails.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this RelatedObjectTypeDetails.
        Type of related object


        :param type: The type of this RelatedObjectTypeDetails.
        :type: str
        """
        allowed_values = ["SCHEMA_OBJECT", "SQL", "DATABASE_PARAMETER"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
