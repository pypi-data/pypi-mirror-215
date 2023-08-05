# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UsagePlansPolicy(object):
    """
    Usage plan policies for this deployment
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UsagePlansPolicy object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param token_locations:
            The value to assign to the token_locations property of this UsagePlansPolicy.
        :type token_locations: list[str]

        """
        self.swagger_types = {
            'token_locations': 'list[str]'
        }

        self.attribute_map = {
            'token_locations': 'tokenLocations'
        }

        self._token_locations = None

    @property
    def token_locations(self):
        """
        **[Required]** Gets the token_locations of this UsagePlansPolicy.
        A list of context variables specifying where API tokens may be located in a request.
        Example locations:
          - \"request.headers[token]\"
          - \"request.query[token]\"
          - \"request.auth[Token]\"
          - \"request.path[TOKEN]\"


        :return: The token_locations of this UsagePlansPolicy.
        :rtype: list[str]
        """
        return self._token_locations

    @token_locations.setter
    def token_locations(self, token_locations):
        """
        Sets the token_locations of this UsagePlansPolicy.
        A list of context variables specifying where API tokens may be located in a request.
        Example locations:
          - \"request.headers[token]\"
          - \"request.query[token]\"
          - \"request.auth[Token]\"
          - \"request.path[TOKEN]\"


        :param token_locations: The token_locations of this UsagePlansPolicy.
        :type: list[str]
        """
        self._token_locations = token_locations

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
