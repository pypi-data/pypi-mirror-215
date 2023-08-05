# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionUserStateUser(object):
    """
    This extension defines attributes used to manage account passwords within a service provider. The extension is typically applied to a User resource, but MAY be applied to other resources that use passwords.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionUserStateUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param last_successful_login_date:
            The value to assign to the last_successful_login_date property of this ExtensionUserStateUser.
        :type last_successful_login_date: str

        :param previous_successful_login_date:
            The value to assign to the previous_successful_login_date property of this ExtensionUserStateUser.
        :type previous_successful_login_date: str

        :param last_failed_login_date:
            The value to assign to the last_failed_login_date property of this ExtensionUserStateUser.
        :type last_failed_login_date: str

        :param login_attempts:
            The value to assign to the login_attempts property of this ExtensionUserStateUser.
        :type login_attempts: int

        :param recovery_attempts:
            The value to assign to the recovery_attempts property of this ExtensionUserStateUser.
        :type recovery_attempts: int

        :param recovery_enroll_attempts:
            The value to assign to the recovery_enroll_attempts property of this ExtensionUserStateUser.
        :type recovery_enroll_attempts: int

        :param max_concurrent_sessions:
            The value to assign to the max_concurrent_sessions property of this ExtensionUserStateUser.
        :type max_concurrent_sessions: int

        :param recovery_locked:
            The value to assign to the recovery_locked property of this ExtensionUserStateUser.
        :type recovery_locked: oci.identity_domains.models.UserExtRecoveryLocked

        :param locked:
            The value to assign to the locked property of this ExtensionUserStateUser.
        :type locked: oci.identity_domains.models.UserExtLocked

        """
        self.swagger_types = {
            'last_successful_login_date': 'str',
            'previous_successful_login_date': 'str',
            'last_failed_login_date': 'str',
            'login_attempts': 'int',
            'recovery_attempts': 'int',
            'recovery_enroll_attempts': 'int',
            'max_concurrent_sessions': 'int',
            'recovery_locked': 'UserExtRecoveryLocked',
            'locked': 'UserExtLocked'
        }

        self.attribute_map = {
            'last_successful_login_date': 'lastSuccessfulLoginDate',
            'previous_successful_login_date': 'previousSuccessfulLoginDate',
            'last_failed_login_date': 'lastFailedLoginDate',
            'login_attempts': 'loginAttempts',
            'recovery_attempts': 'recoveryAttempts',
            'recovery_enroll_attempts': 'recoveryEnrollAttempts',
            'max_concurrent_sessions': 'maxConcurrentSessions',
            'recovery_locked': 'recoveryLocked',
            'locked': 'locked'
        }

        self._last_successful_login_date = None
        self._previous_successful_login_date = None
        self._last_failed_login_date = None
        self._login_attempts = None
        self._recovery_attempts = None
        self._recovery_enroll_attempts = None
        self._max_concurrent_sessions = None
        self._recovery_locked = None
        self._locked = None

    @property
    def last_successful_login_date(self):
        """
        Gets the last_successful_login_date of this ExtensionUserStateUser.
        The last successful login date

        **SCIM++ Properties:**
         - idcsSearchable: true
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The last_successful_login_date of this ExtensionUserStateUser.
        :rtype: str
        """
        return self._last_successful_login_date

    @last_successful_login_date.setter
    def last_successful_login_date(self, last_successful_login_date):
        """
        Sets the last_successful_login_date of this ExtensionUserStateUser.
        The last successful login date

        **SCIM++ Properties:**
         - idcsSearchable: true
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param last_successful_login_date: The last_successful_login_date of this ExtensionUserStateUser.
        :type: str
        """
        self._last_successful_login_date = last_successful_login_date

    @property
    def previous_successful_login_date(self):
        """
        Gets the previous_successful_login_date of this ExtensionUserStateUser.
        The previous successful login date

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The previous_successful_login_date of this ExtensionUserStateUser.
        :rtype: str
        """
        return self._previous_successful_login_date

    @previous_successful_login_date.setter
    def previous_successful_login_date(self, previous_successful_login_date):
        """
        Sets the previous_successful_login_date of this ExtensionUserStateUser.
        The previous successful login date

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param previous_successful_login_date: The previous_successful_login_date of this ExtensionUserStateUser.
        :type: str
        """
        self._previous_successful_login_date = previous_successful_login_date

    @property
    def last_failed_login_date(self):
        """
        Gets the last_failed_login_date of this ExtensionUserStateUser.
        The last failed login date

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :return: The last_failed_login_date of this ExtensionUserStateUser.
        :rtype: str
        """
        return self._last_failed_login_date

    @last_failed_login_date.setter
    def last_failed_login_date(self, last_failed_login_date):
        """
        Sets the last_failed_login_date of this ExtensionUserStateUser.
        The last failed login date

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: dateTime
         - uniqueness: none


        :param last_failed_login_date: The last_failed_login_date of this ExtensionUserStateUser.
        :type: str
        """
        self._last_failed_login_date = last_failed_login_date

    @property
    def login_attempts(self):
        """
        Gets the login_attempts of this ExtensionUserStateUser.
        The number of failed login attempts. The value is reset to 0 after a successful login.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :return: The login_attempts of this ExtensionUserStateUser.
        :rtype: int
        """
        return self._login_attempts

    @login_attempts.setter
    def login_attempts(self, login_attempts):
        """
        Sets the login_attempts of this ExtensionUserStateUser.
        The number of failed login attempts. The value is reset to 0 after a successful login.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsAllowUpdatesInReadOnlyMode: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :param login_attempts: The login_attempts of this ExtensionUserStateUser.
        :type: int
        """
        self._login_attempts = login_attempts

    @property
    def recovery_attempts(self):
        """
        Gets the recovery_attempts of this ExtensionUserStateUser.
        The number of failed recovery attempts. The value is reset to 0 after a successful login.

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :return: The recovery_attempts of this ExtensionUserStateUser.
        :rtype: int
        """
        return self._recovery_attempts

    @recovery_attempts.setter
    def recovery_attempts(self, recovery_attempts):
        """
        Sets the recovery_attempts of this ExtensionUserStateUser.
        The number of failed recovery attempts. The value is reset to 0 after a successful login.

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :param recovery_attempts: The recovery_attempts of this ExtensionUserStateUser.
        :type: int
        """
        self._recovery_attempts = recovery_attempts

    @property
    def recovery_enroll_attempts(self):
        """
        Gets the recovery_enroll_attempts of this ExtensionUserStateUser.
        The number of failed account recovery enrollment attempts.

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :return: The recovery_enroll_attempts of this ExtensionUserStateUser.
        :rtype: int
        """
        return self._recovery_enroll_attempts

    @recovery_enroll_attempts.setter
    def recovery_enroll_attempts(self, recovery_enroll_attempts):
        """
        Sets the recovery_enroll_attempts of this ExtensionUserStateUser.
        The number of failed account recovery enrollment attempts.

        **Added In:** 19.1.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :param recovery_enroll_attempts: The recovery_enroll_attempts of this ExtensionUserStateUser.
        :type: int
        """
        self._recovery_enroll_attempts = recovery_enroll_attempts

    @property
    def max_concurrent_sessions(self):
        """
        Gets the max_concurrent_sessions of this ExtensionUserStateUser.
        Maximum number of concurrent sessions for a User

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsMaxValue: 999
         - idcsMinValue: 1
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :return: The max_concurrent_sessions of this ExtensionUserStateUser.
        :rtype: int
        """
        return self._max_concurrent_sessions

    @max_concurrent_sessions.setter
    def max_concurrent_sessions(self, max_concurrent_sessions):
        """
        Sets the max_concurrent_sessions of this ExtensionUserStateUser.
        Maximum number of concurrent sessions for a User

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - caseExact: false
         - idcsMaxValue: 999
         - idcsMinValue: 1
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: integer
         - uniqueness: none


        :param max_concurrent_sessions: The max_concurrent_sessions of this ExtensionUserStateUser.
        :type: int
        """
        self._max_concurrent_sessions = max_concurrent_sessions

    @property
    def recovery_locked(self):
        """
        Gets the recovery_locked of this ExtensionUserStateUser.

        :return: The recovery_locked of this ExtensionUserStateUser.
        :rtype: oci.identity_domains.models.UserExtRecoveryLocked
        """
        return self._recovery_locked

    @recovery_locked.setter
    def recovery_locked(self, recovery_locked):
        """
        Sets the recovery_locked of this ExtensionUserStateUser.

        :param recovery_locked: The recovery_locked of this ExtensionUserStateUser.
        :type: oci.identity_domains.models.UserExtRecoveryLocked
        """
        self._recovery_locked = recovery_locked

    @property
    def locked(self):
        """
        Gets the locked of this ExtensionUserStateUser.

        :return: The locked of this ExtensionUserStateUser.
        :rtype: oci.identity_domains.models.UserExtLocked
        """
        return self._locked

    @locked.setter
    def locked(self, locked):
        """
        Sets the locked of this ExtensionUserStateUser.

        :param locked: The locked of this ExtensionUserStateUser.
        :type: oci.identity_domains.models.UserExtLocked
        """
        self._locked = locked

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
