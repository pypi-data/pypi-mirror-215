# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionDbCredentialsUser(object):
    """
    Db Credentials User extension
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionDbCredentialsUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param db_user_name:
            The value to assign to the db_user_name property of this ExtensionDbCredentialsUser.
        :type db_user_name: str

        :param db_login_attempts:
            The value to assign to the db_login_attempts property of this ExtensionDbCredentialsUser.
        :type db_login_attempts: int

        """
        self.swagger_types = {
            'db_user_name': 'str',
            'db_login_attempts': 'int'
        }

        self.attribute_map = {
            'db_user_name': 'dbUserName',
            'db_login_attempts': 'dbLoginAttempts'
        }

        self._db_user_name = None
        self._db_login_attempts = None

    @property
    def db_user_name(self):
        """
        Gets the db_user_name of this ExtensionDbCredentialsUser.
        The Database User Name

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readWrite
         - required: false
         - type: string
         - returned: request
         - caseExact: false
         - uniqueness: none
         - idcsSearchable: true


        :return: The db_user_name of this ExtensionDbCredentialsUser.
        :rtype: str
        """
        return self._db_user_name

    @db_user_name.setter
    def db_user_name(self, db_user_name):
        """
        Sets the db_user_name of this ExtensionDbCredentialsUser.
        The Database User Name

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readWrite
         - required: false
         - type: string
         - returned: request
         - caseExact: false
         - uniqueness: none
         - idcsSearchable: true


        :param db_user_name: The db_user_name of this ExtensionDbCredentialsUser.
        :type: str
        """
        self._db_user_name = db_user_name

    @property
    def db_login_attempts(self):
        """
        Gets the db_login_attempts of this ExtensionDbCredentialsUser.
        The number of failed login attempts. The value is reset to 0 after a successful login.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :return: The db_login_attempts of this ExtensionDbCredentialsUser.
        :rtype: int
        """
        return self._db_login_attempts

    @db_login_attempts.setter
    def db_login_attempts(self, db_login_attempts):
        """
        Sets the db_login_attempts of this ExtensionDbCredentialsUser.
        The number of failed login attempts. The value is reset to 0 after a successful login.

        **Added In:** 2102181953

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: integer
         - uniqueness: none


        :param db_login_attempts: The db_login_attempts of this ExtensionDbCredentialsUser.
        :type: int
        """
        self._db_login_attempts = db_login_attempts

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
