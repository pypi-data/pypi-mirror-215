# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionDynamicGroup(object):
    """
    Dynamic Group
    """

    #: A constant which can be used with the membership_type property of a ExtensionDynamicGroup.
    #: This constant has a value of "static"
    MEMBERSHIP_TYPE_STATIC = "static"

    #: A constant which can be used with the membership_type property of a ExtensionDynamicGroup.
    #: This constant has a value of "dynamic"
    MEMBERSHIP_TYPE_DYNAMIC = "dynamic"

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionDynamicGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param membership_type:
            The value to assign to the membership_type property of this ExtensionDynamicGroup.
            Allowed values for this property are: "static", "dynamic", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type membership_type: str

        :param membership_rule:
            The value to assign to the membership_rule property of this ExtensionDynamicGroup.
        :type membership_rule: str

        """
        self.swagger_types = {
            'membership_type': 'str',
            'membership_rule': 'str'
        }

        self.attribute_map = {
            'membership_type': 'membershipType',
            'membership_rule': 'membershipRule'
        }

        self._membership_type = None
        self._membership_rule = None

    @property
    def membership_type(self):
        """
        Gets the membership_type of this ExtensionDynamicGroup.
        Membership type

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: always
         - type: string
         - uniqueness: none

        Allowed values for this property are: "static", "dynamic", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The membership_type of this ExtensionDynamicGroup.
        :rtype: str
        """
        return self._membership_type

    @membership_type.setter
    def membership_type(self, membership_type):
        """
        Sets the membership_type of this ExtensionDynamicGroup.
        Membership type

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: always
         - type: string
         - uniqueness: none


        :param membership_type: The membership_type of this ExtensionDynamicGroup.
        :type: str
        """
        allowed_values = ["static", "dynamic"]
        if not value_allowed_none_or_none_sentinel(membership_type, allowed_values):
            membership_type = 'UNKNOWN_ENUM_VALUE'
        self._membership_type = membership_type

    @property
    def membership_rule(self):
        """
        Gets the membership_rule of this ExtensionDynamicGroup.
        Membership rule

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The membership_rule of this ExtensionDynamicGroup.
        :rtype: str
        """
        return self._membership_rule

    @membership_rule.setter
    def membership_rule(self, membership_rule):
        """
        Sets the membership_rule of this ExtensionDynamicGroup.
        Membership rule

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param membership_rule: The membership_rule of this ExtensionDynamicGroup.
        :type: str
        """
        self._membership_rule = membership_rule

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
