# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionMfaUser(object):
    """
    This extension defines attributes used to manage Multi-Factor Authentication within a service provider. The extension is typically applied to a User resource, but MAY be applied to other resources that use MFA.
    """

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "EMAIL"
    PREFERRED_AUTHENTICATION_FACTOR_EMAIL = "EMAIL"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "SMS"
    PREFERRED_AUTHENTICATION_FACTOR_SMS = "SMS"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "TOTP"
    PREFERRED_AUTHENTICATION_FACTOR_TOTP = "TOTP"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "PUSH"
    PREFERRED_AUTHENTICATION_FACTOR_PUSH = "PUSH"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "OFFLINETOTP"
    PREFERRED_AUTHENTICATION_FACTOR_OFFLINETOTP = "OFFLINETOTP"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "USERNAME_PASSWORD"
    PREFERRED_AUTHENTICATION_FACTOR_USERNAME_PASSWORD = "USERNAME_PASSWORD"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "SECURITY_QUESTIONS"
    PREFERRED_AUTHENTICATION_FACTOR_SECURITY_QUESTIONS = "SECURITY_QUESTIONS"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "VOICE"
    PREFERRED_AUTHENTICATION_FACTOR_VOICE = "VOICE"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "PHONE_CALL"
    PREFERRED_AUTHENTICATION_FACTOR_PHONE_CALL = "PHONE_CALL"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "THIRDPARTY"
    PREFERRED_AUTHENTICATION_FACTOR_THIRDPARTY = "THIRDPARTY"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "FIDO_AUTHENTICATOR"
    PREFERRED_AUTHENTICATION_FACTOR_FIDO_AUTHENTICATOR = "FIDO_AUTHENTICATOR"

    #: A constant which can be used with the preferred_authentication_factor property of a ExtensionMfaUser.
    #: This constant has a value of "YUBICO_OTP"
    PREFERRED_AUTHENTICATION_FACTOR_YUBICO_OTP = "YUBICO_OTP"

    #: A constant which can be used with the mfa_status property of a ExtensionMfaUser.
    #: This constant has a value of "ENROLLED"
    MFA_STATUS_ENROLLED = "ENROLLED"

    #: A constant which can be used with the mfa_status property of a ExtensionMfaUser.
    #: This constant has a value of "IGNORED"
    MFA_STATUS_IGNORED = "IGNORED"

    #: A constant which can be used with the mfa_status property of a ExtensionMfaUser.
    #: This constant has a value of "UN_ENROLLED"
    MFA_STATUS_UN_ENROLLED = "UN_ENROLLED"

    #: A constant which can be used with the mfa_status property of a ExtensionMfaUser.
    #: This constant has a value of "DISABLED"
    MFA_STATUS_DISABLED = "DISABLED"

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionMfaUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param preferred_authentication_factor:
            The value to assign to the preferred_authentication_factor property of this ExtensionMfaUser.
            Allowed values for this property are: "EMAIL", "SMS", "TOTP", "PUSH", "OFFLINETOTP", "USERNAME_PASSWORD", "SECURITY_QUESTIONS", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type preferred_authentication_factor: str

        :param mfa_status:
            The value to assign to the mfa_status property of this ExtensionMfaUser.
            Allowed values for this property are: "ENROLLED", "IGNORED", "UN_ENROLLED", "DISABLED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type mfa_status: str

        :param preferred_third_party_vendor:
            The value to assign to the preferred_third_party_vendor property of this ExtensionMfaUser.
        :type preferred_third_party_vendor: str

        :param preferred_authentication_method:
            The value to assign to the preferred_authentication_method property of this ExtensionMfaUser.
        :type preferred_authentication_method: str

        :param login_attempts:
            The value to assign to the login_attempts property of this ExtensionMfaUser.
        :type login_attempts: int

        :param mfa_enabled_on:
            The value to assign to the mfa_enabled_on property of this ExtensionMfaUser.
        :type mfa_enabled_on: str

        :param mfa_ignored_apps:
            The value to assign to the mfa_ignored_apps property of this ExtensionMfaUser.
        :type mfa_ignored_apps: list[str]

        :param preferred_device:
            The value to assign to the preferred_device property of this ExtensionMfaUser.
        :type preferred_device: oci.identity_domains.models.UserExtPreferredDevice

        :param devices:
            The value to assign to the devices property of this ExtensionMfaUser.
        :type devices: list[oci.identity_domains.models.UserExtDevices]

        :param bypass_codes:
            The value to assign to the bypass_codes property of this ExtensionMfaUser.
        :type bypass_codes: list[oci.identity_domains.models.UserExtBypassCodes]

        :param trusted_user_agents:
            The value to assign to the trusted_user_agents property of this ExtensionMfaUser.
        :type trusted_user_agents: list[oci.identity_domains.models.UserExtTrustedUserAgents]

        """
        self.swagger_types = {
            'preferred_authentication_factor': 'str',
            'mfa_status': 'str',
            'preferred_third_party_vendor': 'str',
            'preferred_authentication_method': 'str',
            'login_attempts': 'int',
            'mfa_enabled_on': 'str',
            'mfa_ignored_apps': 'list[str]',
            'preferred_device': 'UserExtPreferredDevice',
            'devices': 'list[UserExtDevices]',
            'bypass_codes': 'list[UserExtBypassCodes]',
            'trusted_user_agents': 'list[UserExtTrustedUserAgents]'
        }

        self.attribute_map = {
            'preferred_authentication_factor': 'preferredAuthenticationFactor',
            'mfa_status': 'mfaStatus',
            'preferred_third_party_vendor': 'preferredThirdPartyVendor',
            'preferred_authentication_method': 'preferredAuthenticationMethod',
            'login_attempts': 'loginAttempts',
            'mfa_enabled_on': 'mfaEnabledOn',
            'mfa_ignored_apps': 'mfaIgnoredApps',
            'preferred_device': 'preferredDevice',
            'devices': 'devices',
            'bypass_codes': 'bypassCodes',
            'trusted_user_agents': 'trustedUserAgents'
        }

        self._preferred_authentication_factor = None
        self._mfa_status = None
        self._preferred_third_party_vendor = None
        self._preferred_authentication_method = None
        self._login_attempts = None
        self._mfa_enabled_on = None
        self._mfa_ignored_apps = None
        self._preferred_device = None
        self._devices = None
        self._bypass_codes = None
        self._trusted_user_agents = None

    @property
    def preferred_authentication_factor(self):
        """
        Gets the preferred_authentication_factor of this ExtensionMfaUser.
        Preferred Authentication Factor Type

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "EMAIL", "SMS", "TOTP", "PUSH", "OFFLINETOTP", "USERNAME_PASSWORD", "SECURITY_QUESTIONS", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The preferred_authentication_factor of this ExtensionMfaUser.
        :rtype: str
        """
        return self._preferred_authentication_factor

    @preferred_authentication_factor.setter
    def preferred_authentication_factor(self, preferred_authentication_factor):
        """
        Sets the preferred_authentication_factor of this ExtensionMfaUser.
        Preferred Authentication Factor Type

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param preferred_authentication_factor: The preferred_authentication_factor of this ExtensionMfaUser.
        :type: str
        """
        allowed_values = ["EMAIL", "SMS", "TOTP", "PUSH", "OFFLINETOTP", "USERNAME_PASSWORD", "SECURITY_QUESTIONS", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP"]
        if not value_allowed_none_or_none_sentinel(preferred_authentication_factor, allowed_values):
            preferred_authentication_factor = 'UNKNOWN_ENUM_VALUE'
        self._preferred_authentication_factor = preferred_authentication_factor

    @property
    def mfa_status(self):
        """
        Gets the mfa_status of this ExtensionMfaUser.
        User Opted for MFA

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "ENROLLED", "IGNORED", "UN_ENROLLED", "DISABLED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The mfa_status of this ExtensionMfaUser.
        :rtype: str
        """
        return self._mfa_status

    @mfa_status.setter
    def mfa_status(self, mfa_status):
        """
        Sets the mfa_status of this ExtensionMfaUser.
        User Opted for MFA

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param mfa_status: The mfa_status of this ExtensionMfaUser.
        :type: str
        """
        allowed_values = ["ENROLLED", "IGNORED", "UN_ENROLLED", "DISABLED"]
        if not value_allowed_none_or_none_sentinel(mfa_status, allowed_values):
            mfa_status = 'UNKNOWN_ENUM_VALUE'
        self._mfa_status = mfa_status

    @property
    def preferred_third_party_vendor(self):
        """
        Gets the preferred_third_party_vendor of this ExtensionMfaUser.
        Preferred Third party vendor name

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


        :return: The preferred_third_party_vendor of this ExtensionMfaUser.
        :rtype: str
        """
        return self._preferred_third_party_vendor

    @preferred_third_party_vendor.setter
    def preferred_third_party_vendor(self, preferred_third_party_vendor):
        """
        Sets the preferred_third_party_vendor of this ExtensionMfaUser.
        Preferred Third party vendor name

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


        :param preferred_third_party_vendor: The preferred_third_party_vendor of this ExtensionMfaUser.
        :type: str
        """
        self._preferred_third_party_vendor = preferred_third_party_vendor

    @property
    def preferred_authentication_method(self):
        """
        Gets the preferred_authentication_method of this ExtensionMfaUser.
        Preferred Authentication method

        **Added In:** 2009232244

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The preferred_authentication_method of this ExtensionMfaUser.
        :rtype: str
        """
        return self._preferred_authentication_method

    @preferred_authentication_method.setter
    def preferred_authentication_method(self, preferred_authentication_method):
        """
        Sets the preferred_authentication_method of this ExtensionMfaUser.
        Preferred Authentication method

        **Added In:** 2009232244

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param preferred_authentication_method: The preferred_authentication_method of this ExtensionMfaUser.
        :type: str
        """
        self._preferred_authentication_method = preferred_authentication_method

    @property
    def login_attempts(self):
        """
        Gets the login_attempts of this ExtensionMfaUser.
        Number of incorrect Multi Factor Authentication login attempts made by this user. The user gets locked, if this reaches the threshold specified in the maxIncorrectAttempts attribute in AuthenticationFactorSettings

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The login_attempts of this ExtensionMfaUser.
        :rtype: int
        """
        return self._login_attempts

    @login_attempts.setter
    def login_attempts(self, login_attempts):
        """
        Sets the login_attempts of this ExtensionMfaUser.
        Number of incorrect Multi Factor Authentication login attempts made by this user. The user gets locked, if this reaches the threshold specified in the maxIncorrectAttempts attribute in AuthenticationFactorSettings

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param login_attempts: The login_attempts of this ExtensionMfaUser.
        :type: int
        """
        self._login_attempts = login_attempts

    @property
    def mfa_enabled_on(self):
        """
        Gets the mfa_enabled_on of this ExtensionMfaUser.
        This represents the date when the user enrolled for multi factor authentication. This will be set to null, when the user resets his factors.

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The mfa_enabled_on of this ExtensionMfaUser.
        :rtype: str
        """
        return self._mfa_enabled_on

    @mfa_enabled_on.setter
    def mfa_enabled_on(self, mfa_enabled_on):
        """
        Sets the mfa_enabled_on of this ExtensionMfaUser.
        This represents the date when the user enrolled for multi factor authentication. This will be set to null, when the user resets his factors.

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param mfa_enabled_on: The mfa_enabled_on of this ExtensionMfaUser.
        :type: str
        """
        self._mfa_enabled_on = mfa_enabled_on

    @property
    def mfa_ignored_apps(self):
        """
        Gets the mfa_ignored_apps of this ExtensionMfaUser.
        User MFA Ignored Apps Identifiers

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The mfa_ignored_apps of this ExtensionMfaUser.
        :rtype: list[str]
        """
        return self._mfa_ignored_apps

    @mfa_ignored_apps.setter
    def mfa_ignored_apps(self, mfa_ignored_apps):
        """
        Sets the mfa_ignored_apps of this ExtensionMfaUser.
        User MFA Ignored Apps Identifiers

        **Added In:** 19.2.1

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param mfa_ignored_apps: The mfa_ignored_apps of this ExtensionMfaUser.
        :type: list[str]
        """
        self._mfa_ignored_apps = mfa_ignored_apps

    @property
    def preferred_device(self):
        """
        Gets the preferred_device of this ExtensionMfaUser.

        :return: The preferred_device of this ExtensionMfaUser.
        :rtype: oci.identity_domains.models.UserExtPreferredDevice
        """
        return self._preferred_device

    @preferred_device.setter
    def preferred_device(self, preferred_device):
        """
        Sets the preferred_device of this ExtensionMfaUser.

        :param preferred_device: The preferred_device of this ExtensionMfaUser.
        :type: oci.identity_domains.models.UserExtPreferredDevice
        """
        self._preferred_device = preferred_device

    @property
    def devices(self):
        """
        Gets the devices of this ExtensionMfaUser.
        A list of devices enrolled by the user.

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The devices of this ExtensionMfaUser.
        :rtype: list[oci.identity_domains.models.UserExtDevices]
        """
        return self._devices

    @devices.setter
    def devices(self, devices):
        """
        Sets the devices of this ExtensionMfaUser.
        A list of devices enrolled by the user.

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param devices: The devices of this ExtensionMfaUser.
        :type: list[oci.identity_domains.models.UserExtDevices]
        """
        self._devices = devices

    @property
    def bypass_codes(self):
        """
        Gets the bypass_codes of this ExtensionMfaUser.
        A list of bypass codes belongs to user

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The bypass_codes of this ExtensionMfaUser.
        :rtype: list[oci.identity_domains.models.UserExtBypassCodes]
        """
        return self._bypass_codes

    @bypass_codes.setter
    def bypass_codes(self, bypass_codes):
        """
        Sets the bypass_codes of this ExtensionMfaUser.
        A list of bypass codes belongs to user

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param bypass_codes: The bypass_codes of this ExtensionMfaUser.
        :type: list[oci.identity_domains.models.UserExtBypassCodes]
        """
        self._bypass_codes = bypass_codes

    @property
    def trusted_user_agents(self):
        """
        Gets the trusted_user_agents of this ExtensionMfaUser.
        A list of trusted User Agents owned by this user. Multi-Factored Authentication uses Trusted User Agents to authenticate users.  A User Agent is software application that a user uses to issue requests. For example, a User Agent could be a particular browser (possibly one of several executing on a desktop or laptop) or a particular mobile application (again, oneof several executing on a particular mobile device). A User Agent is trusted once the Multi-Factor Authentication has verified it in some way.

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The trusted_user_agents of this ExtensionMfaUser.
        :rtype: list[oci.identity_domains.models.UserExtTrustedUserAgents]
        """
        return self._trusted_user_agents

    @trusted_user_agents.setter
    def trusted_user_agents(self, trusted_user_agents):
        """
        Sets the trusted_user_agents of this ExtensionMfaUser.
        A list of trusted User Agents owned by this user. Multi-Factored Authentication uses Trusted User Agents to authenticate users.  A User Agent is software application that a user uses to issue requests. For example, a User Agent could be a particular browser (possibly one of several executing on a desktop or laptop) or a particular mobile application (again, oneof several executing on a particular mobile device). A User Agent is trusted once the Multi-Factor Authentication has verified it in some way.

        **Added In:** 18.3.6

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param trusted_user_agents: The trusted_user_agents of this ExtensionMfaUser.
        :type: list[oci.identity_domains.models.UserExtTrustedUserAgents]
        """
        self._trusted_user_agents = trusted_user_agents

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
