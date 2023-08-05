# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .container_volume import ContainerVolume
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ContainerEmptyDirVolume(ContainerVolume):
    """
    The empty director of container
    """

    #: A constant which can be used with the backing_store property of a ContainerEmptyDirVolume.
    #: This constant has a value of "EPHEMERAL_STORAGE"
    BACKING_STORE_EPHEMERAL_STORAGE = "EPHEMERAL_STORAGE"

    #: A constant which can be used with the backing_store property of a ContainerEmptyDirVolume.
    #: This constant has a value of "MEMORY"
    BACKING_STORE_MEMORY = "MEMORY"

    def __init__(self, **kwargs):
        """
        Initializes a new ContainerEmptyDirVolume object with values from keyword arguments. The default value of the :py:attr:`~oci.container_instances.models.ContainerEmptyDirVolume.volume_type` attribute
        of this class is ``EMPTYDIR`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ContainerEmptyDirVolume.
        :type name: str

        :param volume_type:
            The value to assign to the volume_type property of this ContainerEmptyDirVolume.
            Allowed values for this property are: "EMPTYDIR", "CONFIGFILE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type volume_type: str

        :param backing_store:
            The value to assign to the backing_store property of this ContainerEmptyDirVolume.
            Allowed values for this property are: "EPHEMERAL_STORAGE", "MEMORY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type backing_store: str

        """
        self.swagger_types = {
            'name': 'str',
            'volume_type': 'str',
            'backing_store': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'volume_type': 'volumeType',
            'backing_store': 'backingStore'
        }

        self._name = None
        self._volume_type = None
        self._backing_store = None
        self._volume_type = 'EMPTYDIR'

    @property
    def backing_store(self):
        """
        Gets the backing_store of this ContainerEmptyDirVolume.
        Volume type that we are using for empty dir where it could be either File Storage or Memory

        Allowed values for this property are: "EPHEMERAL_STORAGE", "MEMORY", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The backing_store of this ContainerEmptyDirVolume.
        :rtype: str
        """
        return self._backing_store

    @backing_store.setter
    def backing_store(self, backing_store):
        """
        Sets the backing_store of this ContainerEmptyDirVolume.
        Volume type that we are using for empty dir where it could be either File Storage or Memory


        :param backing_store: The backing_store of this ContainerEmptyDirVolume.
        :type: str
        """
        allowed_values = ["EPHEMERAL_STORAGE", "MEMORY"]
        if not value_allowed_none_or_none_sentinel(backing_store, allowed_values):
            backing_store = 'UNKNOWN_ENUM_VALUE'
        self._backing_store = backing_store

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
