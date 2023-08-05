# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionSelfChangeUser(object):
    """
    Controls whether a user can update themselves or not via User related APIs
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionSelfChangeUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param allow_self_change:
            The value to assign to the allow_self_change property of this ExtensionSelfChangeUser.
        :type allow_self_change: bool

        """
        self.swagger_types = {
            'allow_self_change': 'bool'
        }

        self.attribute_map = {
            'allow_self_change': 'allowSelfChange'
        }

        self._allow_self_change = None

    @property
    def allow_self_change(self):
        """
        Gets the allow_self_change of this ExtensionSelfChangeUser.
        If true, allows requesting user to update themselves. If false, requesting user can't update themself (default).

        **Added In:** 2205182039

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: boolean
         - uniqueness: none


        :return: The allow_self_change of this ExtensionSelfChangeUser.
        :rtype: bool
        """
        return self._allow_self_change

    @allow_self_change.setter
    def allow_self_change(self, allow_self_change):
        """
        Sets the allow_self_change of this ExtensionSelfChangeUser.
        If true, allows requesting user to update themselves. If false, requesting user can't update themself (default).

        **Added In:** 2205182039

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: boolean
         - uniqueness: none


        :param allow_self_change: The allow_self_change of this ExtensionSelfChangeUser.
        :type: bool
        """
        self._allow_self_change = allow_self_change

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
