# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetailedDescription(object):
    """
    The detailed description of an object.
    """

    #: A constant which can be used with the model_type property of a DetailedDescription.
    #: This constant has a value of "DETAILED_DESCRIPTION"
    MODEL_TYPE_DETAILED_DESCRIPTION = "DETAILED_DESCRIPTION"

    def __init__(self, **kwargs):
        """
        Initializes a new DetailedDescription object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this DetailedDescription.
            Allowed values for this property are: "DETAILED_DESCRIPTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type model_type: str

        :param key:
            The value to assign to the key property of this DetailedDescription.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this DetailedDescription.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this DetailedDescription.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this DetailedDescription.
        :type name: str

        :param object_version:
            The value to assign to the object_version property of this DetailedDescription.
        :type object_version: int

        :param object_status:
            The value to assign to the object_status property of this DetailedDescription.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this DetailedDescription.
        :type identifier: str

        :param metadata:
            The value to assign to the metadata property of this DetailedDescription.
        :type metadata: oci.data_integration.models.ObjectMetadata

        :param logo:
            The value to assign to the logo property of this DetailedDescription.
        :type logo: str

        :param detailed_description:
            The value to assign to the detailed_description property of this DetailedDescription.
        :type detailed_description: str

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'object_version': 'int',
            'object_status': 'int',
            'identifier': 'str',
            'metadata': 'ObjectMetadata',
            'logo': 'str',
            'detailed_description': 'str'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'object_version': 'objectVersion',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'metadata': 'metadata',
            'logo': 'logo',
            'detailed_description': 'detailedDescription'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._object_version = None
        self._object_status = None
        self._identifier = None
        self._metadata = None
        self._logo = None
        self._detailed_description = None

    @property
    def model_type(self):
        """
        Gets the model_type of this DetailedDescription.
        The type of the published object.

        Allowed values for this property are: "DETAILED_DESCRIPTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The model_type of this DetailedDescription.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this DetailedDescription.
        The type of the published object.


        :param model_type: The model_type of this DetailedDescription.
        :type: str
        """
        allowed_values = ["DETAILED_DESCRIPTION"]
        if not value_allowed_none_or_none_sentinel(model_type, allowed_values):
            model_type = 'UNKNOWN_ENUM_VALUE'
        self._model_type = model_type

    @property
    def key(self):
        """
        Gets the key of this DetailedDescription.
        Generated key that can be used in API calls to identify task. On scenarios where reference to the task is needed, a value can be passed in create.


        :return: The key of this DetailedDescription.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this DetailedDescription.
        Generated key that can be used in API calls to identify task. On scenarios where reference to the task is needed, a value can be passed in create.


        :param key: The key of this DetailedDescription.
        :type: str
        """
        self._key = key

    @property
    def model_version(self):
        """
        Gets the model_version of this DetailedDescription.
        The object's model version.


        :return: The model_version of this DetailedDescription.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this DetailedDescription.
        The object's model version.


        :param model_version: The model_version of this DetailedDescription.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this DetailedDescription.

        :return: The parent_ref of this DetailedDescription.
        :rtype: oci.data_integration.models.ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this DetailedDescription.

        :param parent_ref: The parent_ref of this DetailedDescription.
        :type: oci.data_integration.models.ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def name(self):
        """
        Gets the name of this DetailedDescription.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :return: The name of this DetailedDescription.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DetailedDescription.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :param name: The name of this DetailedDescription.
        :type: str
        """
        self._name = name

    @property
    def object_version(self):
        """
        Gets the object_version of this DetailedDescription.
        The version of the object that is used to track changes in the object instance.


        :return: The object_version of this DetailedDescription.
        :rtype: int
        """
        return self._object_version

    @object_version.setter
    def object_version(self, object_version):
        """
        Sets the object_version of this DetailedDescription.
        The version of the object that is used to track changes in the object instance.


        :param object_version: The object_version of this DetailedDescription.
        :type: int
        """
        self._object_version = object_version

    @property
    def object_status(self):
        """
        Gets the object_status of this DetailedDescription.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this DetailedDescription.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this DetailedDescription.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this DetailedDescription.
        :type: int
        """
        self._object_status = object_status

    @property
    def identifier(self):
        """
        Gets the identifier of this DetailedDescription.
        Value can only contain upper case letters, underscore, and numbers. It should begin with upper case letter or underscore. The value can be modified.


        :return: The identifier of this DetailedDescription.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this DetailedDescription.
        Value can only contain upper case letters, underscore, and numbers. It should begin with upper case letter or underscore. The value can be modified.


        :param identifier: The identifier of this DetailedDescription.
        :type: str
        """
        self._identifier = identifier

    @property
    def metadata(self):
        """
        Gets the metadata of this DetailedDescription.

        :return: The metadata of this DetailedDescription.
        :rtype: oci.data_integration.models.ObjectMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this DetailedDescription.

        :param metadata: The metadata of this DetailedDescription.
        :type: oci.data_integration.models.ObjectMetadata
        """
        self._metadata = metadata

    @property
    def logo(self):
        """
        Gets the logo of this DetailedDescription.
        Base64 encoded image to represent logo of the object.


        :return: The logo of this DetailedDescription.
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """
        Sets the logo of this DetailedDescription.
        Base64 encoded image to represent logo of the object.


        :param logo: The logo of this DetailedDescription.
        :type: str
        """
        self._logo = logo

    @property
    def detailed_description(self):
        """
        Gets the detailed_description of this DetailedDescription.
        Base64 encoded rich text description of the object.


        :return: The detailed_description of this DetailedDescription.
        :rtype: str
        """
        return self._detailed_description

    @detailed_description.setter
    def detailed_description(self, detailed_description):
        """
        Sets the detailed_description of this DetailedDescription.
        Base64 encoded rich text description of the object.


        :param detailed_description: The detailed_description of this DetailedDescription.
        :type: str
        """
        self._detailed_description = detailed_description

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
