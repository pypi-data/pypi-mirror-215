# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class FlattenDetails(object):
    """
    Details for the flatten operator.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new FlattenDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param flatten_projection_preferences:
            The value to assign to the flatten_projection_preferences property of this FlattenDetails.
        :type flatten_projection_preferences: oci.data_integration.models.FlattenProjectionPreferences

        :param flatten_attribute_root:
            The value to assign to the flatten_attribute_root property of this FlattenDetails.
        :type flatten_attribute_root: str

        :param flatten_attribute_path:
            The value to assign to the flatten_attribute_path property of this FlattenDetails.
        :type flatten_attribute_path: str

        :param flatten_columns:
            The value to assign to the flatten_columns property of this FlattenDetails.
        :type flatten_columns: list[oci.data_integration.models.TypedObject]

        :param key:
            The value to assign to the key property of this FlattenDetails.
        :type key: str

        :param model_type:
            The value to assign to the model_type property of this FlattenDetails.
        :type model_type: str

        :param model_version:
            The value to assign to the model_version property of this FlattenDetails.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this FlattenDetails.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param object_status:
            The value to assign to the object_status property of this FlattenDetails.
        :type object_status: int

        """
        self.swagger_types = {
            'flatten_projection_preferences': 'FlattenProjectionPreferences',
            'flatten_attribute_root': 'str',
            'flatten_attribute_path': 'str',
            'flatten_columns': 'list[TypedObject]',
            'key': 'str',
            'model_type': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'object_status': 'int'
        }

        self.attribute_map = {
            'flatten_projection_preferences': 'flattenProjectionPreferences',
            'flatten_attribute_root': 'flattenAttributeRoot',
            'flatten_attribute_path': 'flattenAttributePath',
            'flatten_columns': 'flattenColumns',
            'key': 'key',
            'model_type': 'modelType',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'object_status': 'objectStatus'
        }

        self._flatten_projection_preferences = None
        self._flatten_attribute_root = None
        self._flatten_attribute_path = None
        self._flatten_columns = None
        self._key = None
        self._model_type = None
        self._model_version = None
        self._parent_ref = None
        self._object_status = None

    @property
    def flatten_projection_preferences(self):
        """
        Gets the flatten_projection_preferences of this FlattenDetails.

        :return: The flatten_projection_preferences of this FlattenDetails.
        :rtype: oci.data_integration.models.FlattenProjectionPreferences
        """
        return self._flatten_projection_preferences

    @flatten_projection_preferences.setter
    def flatten_projection_preferences(self, flatten_projection_preferences):
        """
        Sets the flatten_projection_preferences of this FlattenDetails.

        :param flatten_projection_preferences: The flatten_projection_preferences of this FlattenDetails.
        :type: oci.data_integration.models.FlattenProjectionPreferences
        """
        self._flatten_projection_preferences = flatten_projection_preferences

    @property
    def flatten_attribute_root(self):
        """
        Gets the flatten_attribute_root of this FlattenDetails.
        The string of flatten attribute column name where the flatten process starts.


        :return: The flatten_attribute_root of this FlattenDetails.
        :rtype: str
        """
        return self._flatten_attribute_root

    @flatten_attribute_root.setter
    def flatten_attribute_root(self, flatten_attribute_root):
        """
        Sets the flatten_attribute_root of this FlattenDetails.
        The string of flatten attribute column name where the flatten process starts.


        :param flatten_attribute_root: The flatten_attribute_root of this FlattenDetails.
        :type: str
        """
        self._flatten_attribute_root = flatten_attribute_root

    @property
    def flatten_attribute_path(self):
        """
        Gets the flatten_attribute_path of this FlattenDetails.
        The string of flatten attribute path in flattenAttributeRoot from upper level to leaf/targeted level concatenated with dot(.).


        :return: The flatten_attribute_path of this FlattenDetails.
        :rtype: str
        """
        return self._flatten_attribute_path

    @flatten_attribute_path.setter
    def flatten_attribute_path(self, flatten_attribute_path):
        """
        Sets the flatten_attribute_path of this FlattenDetails.
        The string of flatten attribute path in flattenAttributeRoot from upper level to leaf/targeted level concatenated with dot(.).


        :param flatten_attribute_path: The flatten_attribute_path of this FlattenDetails.
        :type: str
        """
        self._flatten_attribute_path = flatten_attribute_path

    @property
    def flatten_columns(self):
        """
        Gets the flatten_columns of this FlattenDetails.
        The array of flatten columns which are the input to flatten.


        :return: The flatten_columns of this FlattenDetails.
        :rtype: list[oci.data_integration.models.TypedObject]
        """
        return self._flatten_columns

    @flatten_columns.setter
    def flatten_columns(self, flatten_columns):
        """
        Sets the flatten_columns of this FlattenDetails.
        The array of flatten columns which are the input to flatten.


        :param flatten_columns: The flatten_columns of this FlattenDetails.
        :type: list[oci.data_integration.models.TypedObject]
        """
        self._flatten_columns = flatten_columns

    @property
    def key(self):
        """
        Gets the key of this FlattenDetails.
        The key of the object.


        :return: The key of this FlattenDetails.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this FlattenDetails.
        The key of the object.


        :param key: The key of this FlattenDetails.
        :type: str
        """
        self._key = key

    @property
    def model_type(self):
        """
        Gets the model_type of this FlattenDetails.
        The type of the object.


        :return: The model_type of this FlattenDetails.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this FlattenDetails.
        The type of the object.


        :param model_type: The model_type of this FlattenDetails.
        :type: str
        """
        self._model_type = model_type

    @property
    def model_version(self):
        """
        Gets the model_version of this FlattenDetails.
        The model version of an object.


        :return: The model_version of this FlattenDetails.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this FlattenDetails.
        The model version of an object.


        :param model_version: The model_version of this FlattenDetails.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this FlattenDetails.

        :return: The parent_ref of this FlattenDetails.
        :rtype: oci.data_integration.models.ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this FlattenDetails.

        :param parent_ref: The parent_ref of this FlattenDetails.
        :type: oci.data_integration.models.ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def object_status(self):
        """
        Gets the object_status of this FlattenDetails.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this FlattenDetails.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this FlattenDetails.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this FlattenDetails.
        :type: int
        """
        self._object_status = object_status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
