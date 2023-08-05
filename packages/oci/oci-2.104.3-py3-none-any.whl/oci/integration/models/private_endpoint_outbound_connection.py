# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .outbound_connection import OutboundConnection
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PrivateEndpointOutboundConnection(OutboundConnection):
    """
    Details required for creating Private Endpoint Outbound Connection (ReverseConnection).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PrivateEndpointOutboundConnection object with values from keyword arguments. The default value of the :py:attr:`~oci.integration.models.PrivateEndpointOutboundConnection.outbound_connection_type` attribute
        of this class is ``PRIVATE_ENDPOINT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param outbound_connection_type:
            The value to assign to the outbound_connection_type property of this PrivateEndpointOutboundConnection.
            Allowed values for this property are: "PRIVATE_ENDPOINT", "NONE"
        :type outbound_connection_type: str

        :param subnet_id:
            The value to assign to the subnet_id property of this PrivateEndpointOutboundConnection.
        :type subnet_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this PrivateEndpointOutboundConnection.
        :type nsg_ids: list[str]

        """
        self.swagger_types = {
            'outbound_connection_type': 'str',
            'subnet_id': 'str',
            'nsg_ids': 'list[str]'
        }

        self.attribute_map = {
            'outbound_connection_type': 'outboundConnectionType',
            'subnet_id': 'subnetId',
            'nsg_ids': 'nsgIds'
        }

        self._outbound_connection_type = None
        self._subnet_id = None
        self._nsg_ids = None
        self._outbound_connection_type = 'PRIVATE_ENDPOINT'

    @property
    def subnet_id(self):
        """
        **[Required]** Gets the subnet_id of this PrivateEndpointOutboundConnection.
        Customer Private Network VCN Subnet OCID. This is a required argument.


        :return: The subnet_id of this PrivateEndpointOutboundConnection.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this PrivateEndpointOutboundConnection.
        Customer Private Network VCN Subnet OCID. This is a required argument.


        :param subnet_id: The subnet_id of this PrivateEndpointOutboundConnection.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this PrivateEndpointOutboundConnection.
        One or more Network security group Ids. This is an optional argument.


        :return: The nsg_ids of this PrivateEndpointOutboundConnection.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this PrivateEndpointOutboundConnection.
        One or more Network security group Ids. This is an optional argument.


        :param nsg_ids: The nsg_ids of this PrivateEndpointOutboundConnection.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
