# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionThirdPartyAuthenticationFactorSettings(object):
    """
    This extension defines attributes used to manage Multi-Factor Authentication settings of third party provider
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionThirdPartyAuthenticationFactorSettings object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param duo_security_settings:
            The value to assign to the duo_security_settings property of this ExtensionThirdPartyAuthenticationFactorSettings.
        :type duo_security_settings: oci.identity_domains.models.AuthenticationFactorSettingsDuoSecuritySettings

        """
        self.swagger_types = {
            'duo_security_settings': 'AuthenticationFactorSettingsDuoSecuritySettings'
        }

        self.attribute_map = {
            'duo_security_settings': 'duoSecuritySettings'
        }

        self._duo_security_settings = None

    @property
    def duo_security_settings(self):
        """
        Gets the duo_security_settings of this ExtensionThirdPartyAuthenticationFactorSettings.

        :return: The duo_security_settings of this ExtensionThirdPartyAuthenticationFactorSettings.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsDuoSecuritySettings
        """
        return self._duo_security_settings

    @duo_security_settings.setter
    def duo_security_settings(self, duo_security_settings):
        """
        Sets the duo_security_settings of this ExtensionThirdPartyAuthenticationFactorSettings.

        :param duo_security_settings: The duo_security_settings of this ExtensionThirdPartyAuthenticationFactorSettings.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsDuoSecuritySettings
        """
        self._duo_security_settings = duo_security_settings

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
