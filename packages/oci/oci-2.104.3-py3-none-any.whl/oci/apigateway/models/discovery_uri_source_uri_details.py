# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .source_uri_details import SourceUriDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DiscoveryUriSourceUriDetails(SourceUriDetails):
    """
    Discovery Uri information.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DiscoveryUriSourceUriDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.apigateway.models.DiscoveryUriSourceUriDetails.type` attribute
        of this class is ``DISCOVERY_URI`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this DiscoveryUriSourceUriDetails.
            Allowed values for this property are: "DISCOVERY_URI", "VALIDATION_BLOCK"
        :type type: str

        :param uri:
            The value to assign to the uri property of this DiscoveryUriSourceUriDetails.
        :type uri: str

        """
        self.swagger_types = {
            'type': 'str',
            'uri': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'uri': 'uri'
        }

        self._type = None
        self._uri = None
        self._type = 'DISCOVERY_URI'

    @property
    def uri(self):
        """
        **[Required]** Gets the uri of this DiscoveryUriSourceUriDetails.
        The discovery URI for the auth server.


        :return: The uri of this DiscoveryUriSourceUriDetails.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this DiscoveryUriSourceUriDetails.
        The discovery URI for the auth server.


        :param uri: The uri of this DiscoveryUriSourceUriDetails.
        :type: str
        """
        self._uri = uri

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
