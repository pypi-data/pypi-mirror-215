# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PodConfiguration(object):
    """
    The pod configuration for pods run on virtual nodes of this virtual node pool.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PodConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param subnet_id:
            The value to assign to the subnet_id property of this PodConfiguration.
        :type subnet_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this PodConfiguration.
        :type nsg_ids: list[str]

        :param shape:
            The value to assign to the shape property of this PodConfiguration.
        :type shape: str

        """
        self.swagger_types = {
            'subnet_id': 'str',
            'nsg_ids': 'list[str]',
            'shape': 'str'
        }

        self.attribute_map = {
            'subnet_id': 'subnetId',
            'nsg_ids': 'nsgIds',
            'shape': 'shape'
        }

        self._subnet_id = None
        self._nsg_ids = None
        self._shape = None

    @property
    def subnet_id(self):
        """
        **[Required]** Gets the subnet_id of this PodConfiguration.
        The regional subnet where pods' VNIC will be placed.


        :return: The subnet_id of this PodConfiguration.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this PodConfiguration.
        The regional subnet where pods' VNIC will be placed.


        :param subnet_id: The subnet_id of this PodConfiguration.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this PodConfiguration.
        List of network security group IDs applied to the Pod VNIC.


        :return: The nsg_ids of this PodConfiguration.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this PodConfiguration.
        List of network security group IDs applied to the Pod VNIC.


        :param nsg_ids: The nsg_ids of this PodConfiguration.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    @property
    def shape(self):
        """
        **[Required]** Gets the shape of this PodConfiguration.
        Shape of the pods.


        :return: The shape of this PodConfiguration.
        :rtype: str
        """
        return self._shape

    @shape.setter
    def shape(self, shape):
        """
        Sets the shape of this PodConfiguration.
        Shape of the pods.


        :param shape: The shape of this PodConfiguration.
        :type: str
        """
        self._shape = shape

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
