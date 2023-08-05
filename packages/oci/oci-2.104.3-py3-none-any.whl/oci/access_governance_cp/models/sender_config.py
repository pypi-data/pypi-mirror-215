# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SenderConfig(object):
    """
    The sender information for email notifications sent by GovernanceInstance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SenderConfig object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this SenderConfig.
        :type display_name: str

        :param email:
            The value to assign to the email property of this SenderConfig.
        :type email: str

        :param is_verified:
            The value to assign to the is_verified property of this SenderConfig.
        :type is_verified: bool

        :param time_verify_response_expiry:
            The value to assign to the time_verify_response_expiry property of this SenderConfig.
        :type time_verify_response_expiry: datetime

        :param is_inbox_configured:
            The value to assign to the is_inbox_configured property of this SenderConfig.
        :type is_inbox_configured: bool

        """
        self.swagger_types = {
            'display_name': 'str',
            'email': 'str',
            'is_verified': 'bool',
            'time_verify_response_expiry': 'datetime',
            'is_inbox_configured': 'bool'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'email': 'email',
            'is_verified': 'isVerified',
            'time_verify_response_expiry': 'timeVerifyResponseExpiry',
            'is_inbox_configured': 'isInboxConfigured'
        }

        self._display_name = None
        self._email = None
        self._is_verified = None
        self._time_verify_response_expiry = None
        self._is_inbox_configured = None

    @property
    def display_name(self):
        """
        Gets the display_name of this SenderConfig.
        The sender's displayName.


        :return: The display_name of this SenderConfig.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this SenderConfig.
        The sender's displayName.


        :param display_name: The display_name of this SenderConfig.
        :type: str
        """
        self._display_name = display_name

    @property
    def email(self):
        """
        Gets the email of this SenderConfig.
        The sender's email.


        :return: The email of this SenderConfig.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this SenderConfig.
        The sender's email.


        :param email: The email of this SenderConfig.
        :type: str
        """
        self._email = email

    @property
    def is_verified(self):
        """
        Gets the is_verified of this SenderConfig.
        Whether or not the sender's email has been verified.


        :return: The is_verified of this SenderConfig.
        :rtype: bool
        """
        return self._is_verified

    @is_verified.setter
    def is_verified(self, is_verified):
        """
        Sets the is_verified of this SenderConfig.
        Whether or not the sender's email has been verified.


        :param is_verified: The is_verified of this SenderConfig.
        :type: bool
        """
        self._is_verified = is_verified

    @property
    def time_verify_response_expiry(self):
        """
        Gets the time_verify_response_expiry of this SenderConfig.
        The time when the verify response needs to be received by.


        :return: The time_verify_response_expiry of this SenderConfig.
        :rtype: datetime
        """
        return self._time_verify_response_expiry

    @time_verify_response_expiry.setter
    def time_verify_response_expiry(self, time_verify_response_expiry):
        """
        Sets the time_verify_response_expiry of this SenderConfig.
        The time when the verify response needs to be received by.


        :param time_verify_response_expiry: The time_verify_response_expiry of this SenderConfig.
        :type: datetime
        """
        self._time_verify_response_expiry = time_verify_response_expiry

    @property
    def is_inbox_configured(self):
        """
        Gets the is_inbox_configured of this SenderConfig.
        Whether the sender email has inbox configured to receive emails.


        :return: The is_inbox_configured of this SenderConfig.
        :rtype: bool
        """
        return self._is_inbox_configured

    @is_inbox_configured.setter
    def is_inbox_configured(self, is_inbox_configured):
        """
        Sets the is_inbox_configured of this SenderConfig.
        Whether the sender email has inbox configured to receive emails.


        :param is_inbox_configured: The is_inbox_configured of this SenderConfig.
        :type: bool
        """
        self._is_inbox_configured = is_inbox_configured

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
