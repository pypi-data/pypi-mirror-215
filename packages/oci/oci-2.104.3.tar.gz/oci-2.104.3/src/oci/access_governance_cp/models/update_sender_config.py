# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateSenderConfig(object):
    """
    Update to a sender information for email notifications sent by GovernanceInstance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateSenderConfig object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateSenderConfig.
        :type display_name: str

        :param email:
            The value to assign to the email property of this UpdateSenderConfig.
        :type email: str

        :param is_inbox_configured:
            The value to assign to the is_inbox_configured property of this UpdateSenderConfig.
        :type is_inbox_configured: bool

        :param is_resend_notification_email:
            The value to assign to the is_resend_notification_email property of this UpdateSenderConfig.
        :type is_resend_notification_email: bool

        """
        self.swagger_types = {
            'display_name': 'str',
            'email': 'str',
            'is_inbox_configured': 'bool',
            'is_resend_notification_email': 'bool'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'email': 'email',
            'is_inbox_configured': 'isInboxConfigured',
            'is_resend_notification_email': 'isResendNotificationEmail'
        }

        self._display_name = None
        self._email = None
        self._is_inbox_configured = None
        self._is_resend_notification_email = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateSenderConfig.
        The sender's displayName.


        :return: The display_name of this UpdateSenderConfig.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateSenderConfig.
        The sender's displayName.


        :param display_name: The display_name of this UpdateSenderConfig.
        :type: str
        """
        self._display_name = display_name

    @property
    def email(self):
        """
        **[Required]** Gets the email of this UpdateSenderConfig.
        The sender's email.


        :return: The email of this UpdateSenderConfig.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this UpdateSenderConfig.
        The sender's email.


        :param email: The email of this UpdateSenderConfig.
        :type: str
        """
        self._email = email

    @property
    def is_inbox_configured(self):
        """
        **[Required]** Gets the is_inbox_configured of this UpdateSenderConfig.
        Whether the sender email has inbox configured to receive emails.


        :return: The is_inbox_configured of this UpdateSenderConfig.
        :rtype: bool
        """
        return self._is_inbox_configured

    @is_inbox_configured.setter
    def is_inbox_configured(self, is_inbox_configured):
        """
        Sets the is_inbox_configured of this UpdateSenderConfig.
        Whether the sender email has inbox configured to receive emails.


        :param is_inbox_configured: The is_inbox_configured of this UpdateSenderConfig.
        :type: bool
        """
        self._is_inbox_configured = is_inbox_configured

    @property
    def is_resend_notification_email(self):
        """
        Gets the is_resend_notification_email of this UpdateSenderConfig.
        Whether there is a need to resend the verification email.


        :return: The is_resend_notification_email of this UpdateSenderConfig.
        :rtype: bool
        """
        return self._is_resend_notification_email

    @is_resend_notification_email.setter
    def is_resend_notification_email(self, is_resend_notification_email):
        """
        Sets the is_resend_notification_email of this UpdateSenderConfig.
        Whether there is a need to resend the verification email.


        :param is_resend_notification_email: The is_resend_notification_email of this UpdateSenderConfig.
        :type: bool
        """
        self._is_resend_notification_email = is_resend_notification_email

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
