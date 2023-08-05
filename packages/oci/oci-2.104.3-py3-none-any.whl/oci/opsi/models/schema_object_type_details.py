# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .related_object_type_details import RelatedObjectTypeDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SchemaObjectTypeDetails(RelatedObjectTypeDetails):
    """
    Schema object details
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SchemaObjectTypeDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.SchemaObjectTypeDetails.type` attribute
        of this class is ``SCHEMA_OBJECT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this SchemaObjectTypeDetails.
            Allowed values for this property are: "SCHEMA_OBJECT", "SQL", "DATABASE_PARAMETER"
        :type type: str

        :param object_id:
            The value to assign to the object_id property of this SchemaObjectTypeDetails.
        :type object_id: int

        :param owner:
            The value to assign to the owner property of this SchemaObjectTypeDetails.
        :type owner: str

        :param object_name:
            The value to assign to the object_name property of this SchemaObjectTypeDetails.
        :type object_name: str

        :param sub_object_name:
            The value to assign to the sub_object_name property of this SchemaObjectTypeDetails.
        :type sub_object_name: str

        :param object_type:
            The value to assign to the object_type property of this SchemaObjectTypeDetails.
        :type object_type: str

        """
        self.swagger_types = {
            'type': 'str',
            'object_id': 'int',
            'owner': 'str',
            'object_name': 'str',
            'sub_object_name': 'str',
            'object_type': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'object_id': 'objectId',
            'owner': 'owner',
            'object_name': 'objectName',
            'sub_object_name': 'subObjectName',
            'object_type': 'objectType'
        }

        self._type = None
        self._object_id = None
        self._owner = None
        self._object_name = None
        self._sub_object_name = None
        self._object_type = None
        self._type = 'SCHEMA_OBJECT'

    @property
    def object_id(self):
        """
        **[Required]** Gets the object_id of this SchemaObjectTypeDetails.
        Object id (from RDBMS)


        :return: The object_id of this SchemaObjectTypeDetails.
        :rtype: int
        """
        return self._object_id

    @object_id.setter
    def object_id(self, object_id):
        """
        Sets the object_id of this SchemaObjectTypeDetails.
        Object id (from RDBMS)


        :param object_id: The object_id of this SchemaObjectTypeDetails.
        :type: int
        """
        self._object_id = object_id

    @property
    def owner(self):
        """
        **[Required]** Gets the owner of this SchemaObjectTypeDetails.
        Owner of object


        :return: The owner of this SchemaObjectTypeDetails.
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """
        Sets the owner of this SchemaObjectTypeDetails.
        Owner of object


        :param owner: The owner of this SchemaObjectTypeDetails.
        :type: str
        """
        self._owner = owner

    @property
    def object_name(self):
        """
        **[Required]** Gets the object_name of this SchemaObjectTypeDetails.
        Name of object


        :return: The object_name of this SchemaObjectTypeDetails.
        :rtype: str
        """
        return self._object_name

    @object_name.setter
    def object_name(self, object_name):
        """
        Sets the object_name of this SchemaObjectTypeDetails.
        Name of object


        :param object_name: The object_name of this SchemaObjectTypeDetails.
        :type: str
        """
        self._object_name = object_name

    @property
    def sub_object_name(self):
        """
        Gets the sub_object_name of this SchemaObjectTypeDetails.
        Subobject name; for example, partition name


        :return: The sub_object_name of this SchemaObjectTypeDetails.
        :rtype: str
        """
        return self._sub_object_name

    @sub_object_name.setter
    def sub_object_name(self, sub_object_name):
        """
        Sets the sub_object_name of this SchemaObjectTypeDetails.
        Subobject name; for example, partition name


        :param sub_object_name: The sub_object_name of this SchemaObjectTypeDetails.
        :type: str
        """
        self._sub_object_name = sub_object_name

    @property
    def object_type(self):
        """
        **[Required]** Gets the object_type of this SchemaObjectTypeDetails.
        Type of the object (such as TABLE, INDEX)


        :return: The object_type of this SchemaObjectTypeDetails.
        :rtype: str
        """
        return self._object_type

    @object_type.setter
    def object_type(self, object_type):
        """
        Sets the object_type of this SchemaObjectTypeDetails.
        Type of the object (such as TABLE, INDEX)


        :param object_type: The object_type of this SchemaObjectTypeDetails.
        :type: str
        """
        self._object_type = object_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
