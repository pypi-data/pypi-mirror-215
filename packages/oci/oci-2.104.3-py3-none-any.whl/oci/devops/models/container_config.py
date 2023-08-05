# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ContainerConfig(object):
    """
    Specifies the container configuration.
    """

    #: A constant which can be used with the container_config_type property of a ContainerConfig.
    #: This constant has a value of "CONTAINER_INSTANCE_CONFIG"
    CONTAINER_CONFIG_TYPE_CONTAINER_INSTANCE_CONFIG = "CONTAINER_INSTANCE_CONFIG"

    def __init__(self, **kwargs):
        """
        Initializes a new ContainerConfig object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.devops.models.ContainerInstanceConfig`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param container_config_type:
            The value to assign to the container_config_type property of this ContainerConfig.
            Allowed values for this property are: "CONTAINER_INSTANCE_CONFIG", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type container_config_type: str

        """
        self.swagger_types = {
            'container_config_type': 'str'
        }

        self.attribute_map = {
            'container_config_type': 'containerConfigType'
        }

        self._container_config_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['containerConfigType']

        if type == 'CONTAINER_INSTANCE_CONFIG':
            return 'ContainerInstanceConfig'
        else:
            return 'ContainerConfig'

    @property
    def container_config_type(self):
        """
        **[Required]** Gets the container_config_type of this ContainerConfig.
        Container configuration type.

        Allowed values for this property are: "CONTAINER_INSTANCE_CONFIG", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The container_config_type of this ContainerConfig.
        :rtype: str
        """
        return self._container_config_type

    @container_config_type.setter
    def container_config_type(self, container_config_type):
        """
        Sets the container_config_type of this ContainerConfig.
        Container configuration type.


        :param container_config_type: The container_config_type of this ContainerConfig.
        :type: str
        """
        allowed_values = ["CONTAINER_INSTANCE_CONFIG"]
        if not value_allowed_none_or_none_sentinel(container_config_type, allowed_values):
            container_config_type = 'UNKNOWN_ENUM_VALUE'
        self._container_config_type = container_config_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
