# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IdentityProviderCorrelationPolicy(object):
    """
    Correlation policy

    **Added In:** 20.1.3

    **SCIM++ Properties:**
    - caseExact: true
    - idcsSearchable: false
    - multiValued: false
    - mutability: immutable
    - required: false
    - returned: default
    - type: complex
    - uniqueness: none
    """

    #: A constant which can be used with the type property of a IdentityProviderCorrelationPolicy.
    #: This constant has a value of "Policy"
    TYPE_POLICY = "Policy"

    def __init__(self, **kwargs):
        """
        Initializes a new IdentityProviderCorrelationPolicy object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this IdentityProviderCorrelationPolicy.
            Allowed values for this property are: "Policy", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param value:
            The value to assign to the value property of this IdentityProviderCorrelationPolicy.
        :type value: str

        :param ref:
            The value to assign to the ref property of this IdentityProviderCorrelationPolicy.
        :type ref: str

        :param display:
            The value to assign to the display property of this IdentityProviderCorrelationPolicy.
        :type display: str

        """
        self.swagger_types = {
            'type': 'str',
            'value': 'str',
            'ref': 'str',
            'display': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'value': 'value',
            'ref': '$ref',
            'display': 'display'
        }

        self._type = None
        self._value = None
        self._ref = None
        self._display = None

    @property
    def type(self):
        """
        **[Required]** Gets the type of this IdentityProviderCorrelationPolicy.
        A label that indicates the type that this references.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsDefaultValue: Policy
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "Policy", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this IdentityProviderCorrelationPolicy.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this IdentityProviderCorrelationPolicy.
        A label that indicates the type that this references.

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsDefaultValue: Policy
         - idcsSearchable: false
         - multiValued: false
         - mutability: immutable
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this IdentityProviderCorrelationPolicy.
        :type: str
        """
        allowed_values = ["Policy"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def value(self):
        """
        **[Required]** Gets the value of this IdentityProviderCorrelationPolicy.
        Policy identifier

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this IdentityProviderCorrelationPolicy.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this IdentityProviderCorrelationPolicy.
        Policy identifier

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this IdentityProviderCorrelationPolicy.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this IdentityProviderCorrelationPolicy.
        Policy URI

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this IdentityProviderCorrelationPolicy.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this IdentityProviderCorrelationPolicy.
        Policy URI

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this IdentityProviderCorrelationPolicy.
        :type: str
        """
        self._ref = ref

    @property
    def display(self):
        """
        Gets the display of this IdentityProviderCorrelationPolicy.
        Policy display name

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this IdentityProviderCorrelationPolicy.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this IdentityProviderCorrelationPolicy.
        Policy display name

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this IdentityProviderCorrelationPolicy.
        :type: str
        """
        self._display = display

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
