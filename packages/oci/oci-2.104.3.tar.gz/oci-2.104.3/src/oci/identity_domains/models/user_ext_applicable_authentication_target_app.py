# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserExtApplicableAuthenticationTargetApp(object):
    """
    The app against which the user will authenticate. The value is not persisted but rather calculated. If the user's delegatedAuthenticationTargetApp is set, that value is returned. Otherwise, the app returned by evaluating the user's applicable Delegated Authentication Policy is returned.

    **Added In:** 18.1.6

    **SCIM++ Properties:**
    - idcsCompositeKey: [value]
    - multiValued: false
    - mutability: readOnly
    - required: false
    - returned: request
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UserExtApplicableAuthenticationTargetApp object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this UserExtApplicableAuthenticationTargetApp.
        :type value: str

        :param ref:
            The value to assign to the ref property of this UserExtApplicableAuthenticationTargetApp.
        :type ref: str

        :param type:
            The value to assign to the type property of this UserExtApplicableAuthenticationTargetApp.
        :type type: str

        :param display:
            The value to assign to the display property of this UserExtApplicableAuthenticationTargetApp.
        :type display: str

        :param target_request_timeout:
            The value to assign to the target_request_timeout property of this UserExtApplicableAuthenticationTargetApp.
        :type target_request_timeout: int

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'type': 'str',
            'display': 'str',
            'target_request_timeout': 'int'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'type': 'type',
            'display': 'display',
            'target_request_timeout': 'targetRequestTimeout'
        }

        self._value = None
        self._ref = None
        self._type = None
        self._display = None
        self._target_request_timeout = None

    @property
    def value(self):
        """
        Gets the value of this UserExtApplicableAuthenticationTargetApp.
        App identifier

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - caseExact: true
         - multiValued: false
         - mutability: readOnly
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this UserExtApplicableAuthenticationTargetApp.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserExtApplicableAuthenticationTargetApp.
        App identifier

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - caseExact: true
         - multiValued: false
         - mutability: readOnly
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this UserExtApplicableAuthenticationTargetApp.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this UserExtApplicableAuthenticationTargetApp.
        App URI

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this UserExtApplicableAuthenticationTargetApp.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this UserExtApplicableAuthenticationTargetApp.
        App URI

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this UserExtApplicableAuthenticationTargetApp.
        :type: str
        """
        self._ref = ref

    @property
    def type(self):
        """
        **[Required]** Gets the type of this UserExtApplicableAuthenticationTargetApp.
        A label that indicates whether this is an App or IdentitySource.

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The type of this UserExtApplicableAuthenticationTargetApp.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UserExtApplicableAuthenticationTargetApp.
        A label that indicates whether this is an App or IdentitySource.

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this UserExtApplicableAuthenticationTargetApp.
        :type: str
        """
        self._type = type

    @property
    def display(self):
        """
        Gets the display of this UserExtApplicableAuthenticationTargetApp.
        App Display Name

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this UserExtApplicableAuthenticationTargetApp.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this UserExtApplicableAuthenticationTargetApp.
        App Display Name

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this UserExtApplicableAuthenticationTargetApp.
        :type: str
        """
        self._display = display

    @property
    def target_request_timeout(self):
        """
        Gets the target_request_timeout of this UserExtApplicableAuthenticationTargetApp.
        Timeout interval for Synchronization TargetAction in milliseconds

        **Added In:** 18.2.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The target_request_timeout of this UserExtApplicableAuthenticationTargetApp.
        :rtype: int
        """
        return self._target_request_timeout

    @target_request_timeout.setter
    def target_request_timeout(self, target_request_timeout):
        """
        Sets the target_request_timeout of this UserExtApplicableAuthenticationTargetApp.
        Timeout interval for Synchronization TargetAction in milliseconds

        **Added In:** 18.2.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param target_request_timeout: The target_request_timeout of this UserExtApplicableAuthenticationTargetApp.
        :type: int
        """
        self._target_request_timeout = target_request_timeout

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
