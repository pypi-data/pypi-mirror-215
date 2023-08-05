# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserEmails(object):
    """
    A complex attribute representing emails
    """

    #: A constant which can be used with the type property of a UserEmails.
    #: This constant has a value of "work"
    TYPE_WORK = "work"

    #: A constant which can be used with the type property of a UserEmails.
    #: This constant has a value of "home"
    TYPE_HOME = "home"

    #: A constant which can be used with the type property of a UserEmails.
    #: This constant has a value of "other"
    TYPE_OTHER = "other"

    #: A constant which can be used with the type property of a UserEmails.
    #: This constant has a value of "recovery"
    TYPE_RECOVERY = "recovery"

    def __init__(self, **kwargs):
        """
        Initializes a new UserEmails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this UserEmails.
        :type value: str

        :param type:
            The value to assign to the type property of this UserEmails.
            Allowed values for this property are: "work", "home", "other", "recovery", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param primary:
            The value to assign to the primary property of this UserEmails.
        :type primary: bool

        :param secondary:
            The value to assign to the secondary property of this UserEmails.
        :type secondary: bool

        :param verified:
            The value to assign to the verified property of this UserEmails.
        :type verified: bool

        :param pending_verification_data:
            The value to assign to the pending_verification_data property of this UserEmails.
        :type pending_verification_data: str

        """
        self.swagger_types = {
            'value': 'str',
            'type': 'str',
            'primary': 'bool',
            'secondary': 'bool',
            'verified': 'bool',
            'pending_verification_data': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'type': 'type',
            'primary': 'primary',
            'secondary': 'secondary',
            'verified': 'verified',
            'pending_verification_data': 'pendingVerificationData'
        }

        self._value = None
        self._type = None
        self._primary = None
        self._secondary = None
        self._verified = None
        self._pending_verification_data = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this UserEmails.
        Email address

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this UserEmails.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserEmails.
        Email address

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this UserEmails.
        :type: str
        """
        self._value = value

    @property
    def type(self):
        """
        **[Required]** Gets the type of this UserEmails.
        Type of email address

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "work", "home", "other", "recovery", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this UserEmails.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UserEmails.
        Type of email address

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param type: The type of this UserEmails.
        :type: str
        """
        allowed_values = ["work", "home", "other", "recovery"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def primary(self):
        """
        Gets the primary of this UserEmails.
        A Boolean value that indicates whether the email address is the primary email address. The primary attribute value 'true' MUST appear no more than once.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The primary of this UserEmails.
        :rtype: bool
        """
        return self._primary

    @primary.setter
    def primary(self, primary):
        """
        Sets the primary of this UserEmails.
        A Boolean value that indicates whether the email address is the primary email address. The primary attribute value 'true' MUST appear no more than once.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param primary: The primary of this UserEmails.
        :type: bool
        """
        self._primary = primary

    @property
    def secondary(self):
        """
        Gets the secondary of this UserEmails.
        A Boolean value that indicates whether the email address is the secondary email address. The secondary attribute value 'true' MUST appear no more than once.

        **Added In:** 18.2.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The secondary of this UserEmails.
        :rtype: bool
        """
        return self._secondary

    @secondary.setter
    def secondary(self, secondary):
        """
        Sets the secondary of this UserEmails.
        A Boolean value that indicates whether the email address is the secondary email address. The secondary attribute value 'true' MUST appear no more than once.

        **Added In:** 18.2.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param secondary: The secondary of this UserEmails.
        :type: bool
        """
        self._secondary = secondary

    @property
    def verified(self):
        """
        Gets the verified of this UserEmails.
        A Boolean value that indicates whether or not the e-mail address is verified

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The verified of this UserEmails.
        :rtype: bool
        """
        return self._verified

    @verified.setter
    def verified(self, verified):
        """
        Sets the verified of this UserEmails.
        A Boolean value that indicates whether or not the e-mail address is verified

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param verified: The verified of this UserEmails.
        :type: bool
        """
        self._verified = verified

    @property
    def pending_verification_data(self):
        """
        Gets the pending_verification_data of this UserEmails.
        Pending e-mail address verification

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The pending_verification_data of this UserEmails.
        :rtype: str
        """
        return self._pending_verification_data

    @pending_verification_data.setter
    def pending_verification_data(self, pending_verification_data):
        """
        Sets the pending_verification_data of this UserEmails.
        Pending e-mail address verification

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - caseExact: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param pending_verification_data: The pending_verification_data of this UserEmails.
        :type: str
        """
        self._pending_verification_data = pending_verification_data

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
