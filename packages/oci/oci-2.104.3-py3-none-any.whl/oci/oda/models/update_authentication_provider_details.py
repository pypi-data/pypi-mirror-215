# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateAuthenticationProviderDetails(object):
    """
    Properties to update an Authentication Provider.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateAuthenticationProviderDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param token_endpoint_url:
            The value to assign to the token_endpoint_url property of this UpdateAuthenticationProviderDetails.
        :type token_endpoint_url: str

        :param authorization_endpoint_url:
            The value to assign to the authorization_endpoint_url property of this UpdateAuthenticationProviderDetails.
        :type authorization_endpoint_url: str

        :param short_authorization_code_request_url:
            The value to assign to the short_authorization_code_request_url property of this UpdateAuthenticationProviderDetails.
        :type short_authorization_code_request_url: str

        :param revoke_token_endpoint_url:
            The value to assign to the revoke_token_endpoint_url property of this UpdateAuthenticationProviderDetails.
        :type revoke_token_endpoint_url: str

        :param client_id:
            The value to assign to the client_id property of this UpdateAuthenticationProviderDetails.
        :type client_id: str

        :param client_secret:
            The value to assign to the client_secret property of this UpdateAuthenticationProviderDetails.
        :type client_secret: str

        :param scopes:
            The value to assign to the scopes property of this UpdateAuthenticationProviderDetails.
        :type scopes: str

        :param subject_claim:
            The value to assign to the subject_claim property of this UpdateAuthenticationProviderDetails.
        :type subject_claim: str

        :param refresh_token_retention_period_in_days:
            The value to assign to the refresh_token_retention_period_in_days property of this UpdateAuthenticationProviderDetails.
        :type refresh_token_retention_period_in_days: int

        :param redirect_url:
            The value to assign to the redirect_url property of this UpdateAuthenticationProviderDetails.
        :type redirect_url: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateAuthenticationProviderDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateAuthenticationProviderDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'token_endpoint_url': 'str',
            'authorization_endpoint_url': 'str',
            'short_authorization_code_request_url': 'str',
            'revoke_token_endpoint_url': 'str',
            'client_id': 'str',
            'client_secret': 'str',
            'scopes': 'str',
            'subject_claim': 'str',
            'refresh_token_retention_period_in_days': 'int',
            'redirect_url': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'token_endpoint_url': 'tokenEndpointUrl',
            'authorization_endpoint_url': 'authorizationEndpointUrl',
            'short_authorization_code_request_url': 'shortAuthorizationCodeRequestUrl',
            'revoke_token_endpoint_url': 'revokeTokenEndpointUrl',
            'client_id': 'clientId',
            'client_secret': 'clientSecret',
            'scopes': 'scopes',
            'subject_claim': 'subjectClaim',
            'refresh_token_retention_period_in_days': 'refreshTokenRetentionPeriodInDays',
            'redirect_url': 'redirectUrl',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._token_endpoint_url = None
        self._authorization_endpoint_url = None
        self._short_authorization_code_request_url = None
        self._revoke_token_endpoint_url = None
        self._client_id = None
        self._client_secret = None
        self._scopes = None
        self._subject_claim = None
        self._refresh_token_retention_period_in_days = None
        self._redirect_url = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def token_endpoint_url(self):
        """
        Gets the token_endpoint_url of this UpdateAuthenticationProviderDetails.
        The IDPs URL for requesting access tokens.


        :return: The token_endpoint_url of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._token_endpoint_url

    @token_endpoint_url.setter
    def token_endpoint_url(self, token_endpoint_url):
        """
        Sets the token_endpoint_url of this UpdateAuthenticationProviderDetails.
        The IDPs URL for requesting access tokens.


        :param token_endpoint_url: The token_endpoint_url of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._token_endpoint_url = token_endpoint_url

    @property
    def authorization_endpoint_url(self):
        """
        Gets the authorization_endpoint_url of this UpdateAuthenticationProviderDetails.
        The IDPs URL for the page that users authenticate with by entering the user name and password.


        :return: The authorization_endpoint_url of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._authorization_endpoint_url

    @authorization_endpoint_url.setter
    def authorization_endpoint_url(self, authorization_endpoint_url):
        """
        Sets the authorization_endpoint_url of this UpdateAuthenticationProviderDetails.
        The IDPs URL for the page that users authenticate with by entering the user name and password.


        :param authorization_endpoint_url: The authorization_endpoint_url of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._authorization_endpoint_url = authorization_endpoint_url

    @property
    def short_authorization_code_request_url(self):
        """
        Gets the short_authorization_code_request_url of this UpdateAuthenticationProviderDetails.
        A shortened version of the authorization URL, which you can get from a URL shortener service (one that allows
        you to send query parameters).  You might need this because the generated authorization-code-request URL
        could be too long for SMS and older smart phones.


        :return: The short_authorization_code_request_url of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._short_authorization_code_request_url

    @short_authorization_code_request_url.setter
    def short_authorization_code_request_url(self, short_authorization_code_request_url):
        """
        Sets the short_authorization_code_request_url of this UpdateAuthenticationProviderDetails.
        A shortened version of the authorization URL, which you can get from a URL shortener service (one that allows
        you to send query parameters).  You might need this because the generated authorization-code-request URL
        could be too long for SMS and older smart phones.


        :param short_authorization_code_request_url: The short_authorization_code_request_url of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._short_authorization_code_request_url = short_authorization_code_request_url

    @property
    def revoke_token_endpoint_url(self):
        """
        Gets the revoke_token_endpoint_url of this UpdateAuthenticationProviderDetails.
        If you want to revoke all the refresh tokens and access tokens of the logged-in user from a dialog flow, then
        you need the IDP's revoke refresh token URL. If you provide this URL, then you can use the System.OAuth2ResetTokens
        component to revoke the user's tokens for this service.


        :return: The revoke_token_endpoint_url of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._revoke_token_endpoint_url

    @revoke_token_endpoint_url.setter
    def revoke_token_endpoint_url(self, revoke_token_endpoint_url):
        """
        Sets the revoke_token_endpoint_url of this UpdateAuthenticationProviderDetails.
        If you want to revoke all the refresh tokens and access tokens of the logged-in user from a dialog flow, then
        you need the IDP's revoke refresh token URL. If you provide this URL, then you can use the System.OAuth2ResetTokens
        component to revoke the user's tokens for this service.


        :param revoke_token_endpoint_url: The revoke_token_endpoint_url of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._revoke_token_endpoint_url = revoke_token_endpoint_url

    @property
    def client_id(self):
        """
        Gets the client_id of this UpdateAuthenticationProviderDetails.
        The client ID for the IDP application (OAuth Client) that was registered as described in Identity Provider Registration.
        With Microsoft identity platform, use the application ID.


        :return: The client_id of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._client_id

    @client_id.setter
    def client_id(self, client_id):
        """
        Sets the client_id of this UpdateAuthenticationProviderDetails.
        The client ID for the IDP application (OAuth Client) that was registered as described in Identity Provider Registration.
        With Microsoft identity platform, use the application ID.


        :param client_id: The client_id of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._client_id = client_id

    @property
    def client_secret(self):
        """
        Gets the client_secret of this UpdateAuthenticationProviderDetails.
        The client secret for the IDP application (OAuth Client) that was registered as described in Identity Provider
        Registration. With Microsoft identity platform, use the application secret.


        :return: The client_secret of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._client_secret

    @client_secret.setter
    def client_secret(self, client_secret):
        """
        Sets the client_secret of this UpdateAuthenticationProviderDetails.
        The client secret for the IDP application (OAuth Client) that was registered as described in Identity Provider
        Registration. With Microsoft identity platform, use the application secret.


        :param client_secret: The client_secret of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._client_secret = client_secret

    @property
    def scopes(self):
        """
        Gets the scopes of this UpdateAuthenticationProviderDetails.
        A space-separated list of the scopes that must be included when Digital Assistant requests an access token from
        the provider. Include all the scopes that are required to access the resources. If refresh tokens are enabled,
        include the scope that\u2019s necessary to get the refresh token (typically offline_access).


        :return: The scopes of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._scopes

    @scopes.setter
    def scopes(self, scopes):
        """
        Sets the scopes of this UpdateAuthenticationProviderDetails.
        A space-separated list of the scopes that must be included when Digital Assistant requests an access token from
        the provider. Include all the scopes that are required to access the resources. If refresh tokens are enabled,
        include the scope that\u2019s necessary to get the refresh token (typically offline_access).


        :param scopes: The scopes of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._scopes = scopes

    @property
    def subject_claim(self):
        """
        Gets the subject_claim of this UpdateAuthenticationProviderDetails.
        The access-token profile claim to use to identify the user.


        :return: The subject_claim of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._subject_claim

    @subject_claim.setter
    def subject_claim(self, subject_claim):
        """
        Sets the subject_claim of this UpdateAuthenticationProviderDetails.
        The access-token profile claim to use to identify the user.


        :param subject_claim: The subject_claim of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._subject_claim = subject_claim

    @property
    def refresh_token_retention_period_in_days(self):
        """
        Gets the refresh_token_retention_period_in_days of this UpdateAuthenticationProviderDetails.
        The number of days to keep the refresh token in the Digital Assistant cache.


        :return: The refresh_token_retention_period_in_days of this UpdateAuthenticationProviderDetails.
        :rtype: int
        """
        return self._refresh_token_retention_period_in_days

    @refresh_token_retention_period_in_days.setter
    def refresh_token_retention_period_in_days(self, refresh_token_retention_period_in_days):
        """
        Sets the refresh_token_retention_period_in_days of this UpdateAuthenticationProviderDetails.
        The number of days to keep the refresh token in the Digital Assistant cache.


        :param refresh_token_retention_period_in_days: The refresh_token_retention_period_in_days of this UpdateAuthenticationProviderDetails.
        :type: int
        """
        self._refresh_token_retention_period_in_days = refresh_token_retention_period_in_days

    @property
    def redirect_url(self):
        """
        Gets the redirect_url of this UpdateAuthenticationProviderDetails.
        The OAuth Redirect URL.


        :return: The redirect_url of this UpdateAuthenticationProviderDetails.
        :rtype: str
        """
        return self._redirect_url

    @redirect_url.setter
    def redirect_url(self, redirect_url):
        """
        Sets the redirect_url of this UpdateAuthenticationProviderDetails.
        The OAuth Redirect URL.


        :param redirect_url: The redirect_url of this UpdateAuthenticationProviderDetails.
        :type: str
        """
        self._redirect_url = redirect_url

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateAuthenticationProviderDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this UpdateAuthenticationProviderDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateAuthenticationProviderDetails.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this UpdateAuthenticationProviderDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateAuthenticationProviderDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this UpdateAuthenticationProviderDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateAuthenticationProviderDetails.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this UpdateAuthenticationProviderDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
