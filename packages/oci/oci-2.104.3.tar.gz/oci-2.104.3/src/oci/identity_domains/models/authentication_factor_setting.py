# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AuthenticationFactorSetting(object):
    """
    Multi Factor Authentication Settings for Tenant
    """

    #: A constant which can be used with the idcs_prevented_operations property of a AuthenticationFactorSetting.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a AuthenticationFactorSetting.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a AuthenticationFactorSetting.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "EMAIL"
    USER_ENROLLMENT_DISABLED_FACTORS_EMAIL = "EMAIL"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "SMS"
    USER_ENROLLMENT_DISABLED_FACTORS_SMS = "SMS"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "TOTP"
    USER_ENROLLMENT_DISABLED_FACTORS_TOTP = "TOTP"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "PUSH"
    USER_ENROLLMENT_DISABLED_FACTORS_PUSH = "PUSH"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "OFFLINETOTP"
    USER_ENROLLMENT_DISABLED_FACTORS_OFFLINETOTP = "OFFLINETOTP"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "VOICE"
    USER_ENROLLMENT_DISABLED_FACTORS_VOICE = "VOICE"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "PHONE_CALL"
    USER_ENROLLMENT_DISABLED_FACTORS_PHONE_CALL = "PHONE_CALL"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "THIRDPARTY"
    USER_ENROLLMENT_DISABLED_FACTORS_THIRDPARTY = "THIRDPARTY"

    #: A constant which can be used with the user_enrollment_disabled_factors property of a AuthenticationFactorSetting.
    #: This constant has a value of "FIDO_AUTHENTICATOR"
    USER_ENROLLMENT_DISABLED_FACTORS_FIDO_AUTHENTICATOR = "FIDO_AUTHENTICATOR"

    def __init__(self, **kwargs):
        """
        Initializes a new AuthenticationFactorSetting object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AuthenticationFactorSetting.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this AuthenticationFactorSetting.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this AuthenticationFactorSetting.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this AuthenticationFactorSetting.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this AuthenticationFactorSetting.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this AuthenticationFactorSetting.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this AuthenticationFactorSetting.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this AuthenticationFactorSetting.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this AuthenticationFactorSetting.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this AuthenticationFactorSetting.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this AuthenticationFactorSetting.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this AuthenticationFactorSetting.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this AuthenticationFactorSetting.
        :type tenancy_ocid: str

        :param email_enabled:
            The value to assign to the email_enabled property of this AuthenticationFactorSetting.
        :type email_enabled: bool

        :param sms_enabled:
            The value to assign to the sms_enabled property of this AuthenticationFactorSetting.
        :type sms_enabled: bool

        :param phone_call_enabled:
            The value to assign to the phone_call_enabled property of this AuthenticationFactorSetting.
        :type phone_call_enabled: bool

        :param totp_enabled:
            The value to assign to the totp_enabled property of this AuthenticationFactorSetting.
        :type totp_enabled: bool

        :param push_enabled:
            The value to assign to the push_enabled property of this AuthenticationFactorSetting.
        :type push_enabled: bool

        :param bypass_code_enabled:
            The value to assign to the bypass_code_enabled property of this AuthenticationFactorSetting.
        :type bypass_code_enabled: bool

        :param security_questions_enabled:
            The value to assign to the security_questions_enabled property of this AuthenticationFactorSetting.
        :type security_questions_enabled: bool

        :param fido_authenticator_enabled:
            The value to assign to the fido_authenticator_enabled property of this AuthenticationFactorSetting.
        :type fido_authenticator_enabled: bool

        :param yubico_otp_enabled:
            The value to assign to the yubico_otp_enabled property of this AuthenticationFactorSetting.
        :type yubico_otp_enabled: bool

        :param mfa_enrollment_type:
            The value to assign to the mfa_enrollment_type property of this AuthenticationFactorSetting.
        :type mfa_enrollment_type: str

        :param mfa_enabled_category:
            The value to assign to the mfa_enabled_category property of this AuthenticationFactorSetting.
        :type mfa_enabled_category: str

        :param hide_backup_factor_enabled:
            The value to assign to the hide_backup_factor_enabled property of this AuthenticationFactorSetting.
        :type hide_backup_factor_enabled: bool

        :param auto_enroll_email_factor_disabled:
            The value to assign to the auto_enroll_email_factor_disabled property of this AuthenticationFactorSetting.
        :type auto_enroll_email_factor_disabled: bool

        :param user_enrollment_disabled_factors:
            The value to assign to the user_enrollment_disabled_factors property of this AuthenticationFactorSetting.
            Allowed values for items in this list are: "EMAIL", "SMS", "TOTP", "PUSH", "OFFLINETOTP", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type user_enrollment_disabled_factors: list[str]

        :param email_settings:
            The value to assign to the email_settings property of this AuthenticationFactorSetting.
        :type email_settings: oci.identity_domains.models.AuthenticationFactorSettingsEmailSettings

        :param third_party_factor:
            The value to assign to the third_party_factor property of this AuthenticationFactorSetting.
        :type third_party_factor: oci.identity_domains.models.AuthenticationFactorSettingsThirdPartyFactor

        :param notification_settings:
            The value to assign to the notification_settings property of this AuthenticationFactorSetting.
        :type notification_settings: oci.identity_domains.models.AuthenticationFactorSettingsNotificationSettings

        :param identity_store_settings:
            The value to assign to the identity_store_settings property of this AuthenticationFactorSetting.
        :type identity_store_settings: oci.identity_domains.models.AuthenticationFactorSettingsIdentityStoreSettings

        :param bypass_code_settings:
            The value to assign to the bypass_code_settings property of this AuthenticationFactorSetting.
        :type bypass_code_settings: oci.identity_domains.models.AuthenticationFactorSettingsBypassCodeSettings

        :param client_app_settings:
            The value to assign to the client_app_settings property of this AuthenticationFactorSetting.
        :type client_app_settings: oci.identity_domains.models.AuthenticationFactorSettingsClientAppSettings

        :param endpoint_restrictions:
            The value to assign to the endpoint_restrictions property of this AuthenticationFactorSetting.
        :type endpoint_restrictions: oci.identity_domains.models.AuthenticationFactorSettingsEndpointRestrictions

        :param compliance_policy:
            The value to assign to the compliance_policy property of this AuthenticationFactorSetting.
        :type compliance_policy: list[oci.identity_domains.models.AuthenticationFactorSettingsCompliancePolicy]

        :param totp_settings:
            The value to assign to the totp_settings property of this AuthenticationFactorSetting.
        :type totp_settings: oci.identity_domains.models.AuthenticationFactorSettingsTotpSettings

        :param urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings:
            The value to assign to the urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings property of this AuthenticationFactorSetting.
        :type urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings: oci.identity_domains.models.ExtensionThirdPartyAuthenticationFactorSettings

        :param urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings:
            The value to assign to the urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings property of this AuthenticationFactorSetting.
        :type urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings: oci.identity_domains.models.ExtensionFidoAuthenticationFactorSettings

        """
        self.swagger_types = {
            'id': 'str',
            'ocid': 'str',
            'schemas': 'list[str]',
            'meta': 'Meta',
            'idcs_created_by': 'IdcsCreatedBy',
            'idcs_last_modified_by': 'IdcsLastModifiedBy',
            'idcs_prevented_operations': 'list[str]',
            'tags': 'list[Tags]',
            'delete_in_progress': 'bool',
            'idcs_last_upgraded_in_release': 'str',
            'domain_ocid': 'str',
            'compartment_ocid': 'str',
            'tenancy_ocid': 'str',
            'email_enabled': 'bool',
            'sms_enabled': 'bool',
            'phone_call_enabled': 'bool',
            'totp_enabled': 'bool',
            'push_enabled': 'bool',
            'bypass_code_enabled': 'bool',
            'security_questions_enabled': 'bool',
            'fido_authenticator_enabled': 'bool',
            'yubico_otp_enabled': 'bool',
            'mfa_enrollment_type': 'str',
            'mfa_enabled_category': 'str',
            'hide_backup_factor_enabled': 'bool',
            'auto_enroll_email_factor_disabled': 'bool',
            'user_enrollment_disabled_factors': 'list[str]',
            'email_settings': 'AuthenticationFactorSettingsEmailSettings',
            'third_party_factor': 'AuthenticationFactorSettingsThirdPartyFactor',
            'notification_settings': 'AuthenticationFactorSettingsNotificationSettings',
            'identity_store_settings': 'AuthenticationFactorSettingsIdentityStoreSettings',
            'bypass_code_settings': 'AuthenticationFactorSettingsBypassCodeSettings',
            'client_app_settings': 'AuthenticationFactorSettingsClientAppSettings',
            'endpoint_restrictions': 'AuthenticationFactorSettingsEndpointRestrictions',
            'compliance_policy': 'list[AuthenticationFactorSettingsCompliancePolicy]',
            'totp_settings': 'AuthenticationFactorSettingsTotpSettings',
            'urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings': 'ExtensionThirdPartyAuthenticationFactorSettings',
            'urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings': 'ExtensionFidoAuthenticationFactorSettings'
        }

        self.attribute_map = {
            'id': 'id',
            'ocid': 'ocid',
            'schemas': 'schemas',
            'meta': 'meta',
            'idcs_created_by': 'idcsCreatedBy',
            'idcs_last_modified_by': 'idcsLastModifiedBy',
            'idcs_prevented_operations': 'idcsPreventedOperations',
            'tags': 'tags',
            'delete_in_progress': 'deleteInProgress',
            'idcs_last_upgraded_in_release': 'idcsLastUpgradedInRelease',
            'domain_ocid': 'domainOcid',
            'compartment_ocid': 'compartmentOcid',
            'tenancy_ocid': 'tenancyOcid',
            'email_enabled': 'emailEnabled',
            'sms_enabled': 'smsEnabled',
            'phone_call_enabled': 'phoneCallEnabled',
            'totp_enabled': 'totpEnabled',
            'push_enabled': 'pushEnabled',
            'bypass_code_enabled': 'bypassCodeEnabled',
            'security_questions_enabled': 'securityQuestionsEnabled',
            'fido_authenticator_enabled': 'fidoAuthenticatorEnabled',
            'yubico_otp_enabled': 'yubicoOtpEnabled',
            'mfa_enrollment_type': 'mfaEnrollmentType',
            'mfa_enabled_category': 'mfaEnabledCategory',
            'hide_backup_factor_enabled': 'hideBackupFactorEnabled',
            'auto_enroll_email_factor_disabled': 'autoEnrollEmailFactorDisabled',
            'user_enrollment_disabled_factors': 'userEnrollmentDisabledFactors',
            'email_settings': 'emailSettings',
            'third_party_factor': 'thirdPartyFactor',
            'notification_settings': 'notificationSettings',
            'identity_store_settings': 'identityStoreSettings',
            'bypass_code_settings': 'bypassCodeSettings',
            'client_app_settings': 'clientAppSettings',
            'endpoint_restrictions': 'endpointRestrictions',
            'compliance_policy': 'compliancePolicy',
            'totp_settings': 'totpSettings',
            'urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:thirdParty:AuthenticationFactorSettings',
            'urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:fido:AuthenticationFactorSettings'
        }

        self._id = None
        self._ocid = None
        self._schemas = None
        self._meta = None
        self._idcs_created_by = None
        self._idcs_last_modified_by = None
        self._idcs_prevented_operations = None
        self._tags = None
        self._delete_in_progress = None
        self._idcs_last_upgraded_in_release = None
        self._domain_ocid = None
        self._compartment_ocid = None
        self._tenancy_ocid = None
        self._email_enabled = None
        self._sms_enabled = None
        self._phone_call_enabled = None
        self._totp_enabled = None
        self._push_enabled = None
        self._bypass_code_enabled = None
        self._security_questions_enabled = None
        self._fido_authenticator_enabled = None
        self._yubico_otp_enabled = None
        self._mfa_enrollment_type = None
        self._mfa_enabled_category = None
        self._hide_backup_factor_enabled = None
        self._auto_enroll_email_factor_disabled = None
        self._user_enrollment_disabled_factors = None
        self._email_settings = None
        self._third_party_factor = None
        self._notification_settings = None
        self._identity_store_settings = None
        self._bypass_code_settings = None
        self._client_app_settings = None
        self._endpoint_restrictions = None
        self._compliance_policy = None
        self._totp_settings = None
        self._urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings = None
        self._urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings = None

    @property
    def id(self):
        """
        Gets the id of this AuthenticationFactorSetting.
        Unique identifier for the SCIM Resource as defined by the Service Provider. Each representation of the Resource MUST include a non-empty id value. This identifier MUST be unique across the Service Provider's entire set of Resources. It MUST be a stable, non-reassignable identifier that does not change when the same Resource is returned in subsequent requests. The value of the id attribute is always issued by the Service Provider and MUST never be specified by the Service Consumer. bulkId: is a reserved keyword and MUST NOT be used in the unique identifier.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: always
         - type: string
         - uniqueness: global


        :return: The id of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AuthenticationFactorSetting.
        Unique identifier for the SCIM Resource as defined by the Service Provider. Each representation of the Resource MUST include a non-empty id value. This identifier MUST be unique across the Service Provider's entire set of Resources. It MUST be a stable, non-reassignable identifier that does not change when the same Resource is returned in subsequent requests. The value of the id attribute is always issued by the Service Provider and MUST never be specified by the Service Consumer. bulkId: is a reserved keyword and MUST NOT be used in the unique identifier.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: always
         - type: string
         - uniqueness: global


        :param id: The id of this AuthenticationFactorSetting.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this AuthenticationFactorSetting.
        Unique OCI identifier for the SCIM Resource.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: global


        :return: The ocid of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this AuthenticationFactorSetting.
        Unique OCI identifier for the SCIM Resource.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: default
         - type: string
         - uniqueness: global


        :param ocid: The ocid of this AuthenticationFactorSetting.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this AuthenticationFactorSetting.
        REQUIRED. The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. This specification defines URIs for User, Group, and a standard \\\"enterprise\\\" extension. All representations of SCIM schema MUST include a non-zero value array with value(s) of the URIs supported by that representation. Duplicate values MUST NOT be included. Value order is not specified and MUST not impact behavior.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The schemas of this AuthenticationFactorSetting.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this AuthenticationFactorSetting.
        REQUIRED. The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. This specification defines URIs for User, Group, and a standard \\\"enterprise\\\" extension. All representations of SCIM schema MUST include a non-zero value array with value(s) of the URIs supported by that representation. Duplicate values MUST NOT be included. Value order is not specified and MUST not impact behavior.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param schemas: The schemas of this AuthenticationFactorSetting.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this AuthenticationFactorSetting.

        :return: The meta of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this AuthenticationFactorSetting.

        :param meta: The meta of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this AuthenticationFactorSetting.

        :return: The idcs_created_by of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this AuthenticationFactorSetting.

        :param idcs_created_by: The idcs_created_by of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this AuthenticationFactorSetting.

        :return: The idcs_last_modified_by of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this AuthenticationFactorSetting.

        :param idcs_last_modified_by: The idcs_last_modified_by of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this AuthenticationFactorSetting.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none

        Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The idcs_prevented_operations of this AuthenticationFactorSetting.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this AuthenticationFactorSetting.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this AuthenticationFactorSetting.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this AuthenticationFactorSetting.
        A list of tags on this resource.

        **SCIM++ Properties:**
         - idcsCompositeKey: [key, value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The tags of this AuthenticationFactorSetting.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this AuthenticationFactorSetting.
        A list of tags on this resource.

        **SCIM++ Properties:**
         - idcsCompositeKey: [key, value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param tags: The tags of this AuthenticationFactorSetting.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this AuthenticationFactorSetting.
        A boolean flag indicating this resource in the process of being deleted. Usually set to true when synchronous deletion of the resource would take too long.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The delete_in_progress of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this AuthenticationFactorSetting.
        A boolean flag indicating this resource in the process of being deleted. Usually set to true when synchronous deletion of the resource would take too long.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param delete_in_progress: The delete_in_progress of this AuthenticationFactorSetting.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this AuthenticationFactorSetting.
        The release number when the resource was upgraded.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :return: The idcs_last_upgraded_in_release of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this AuthenticationFactorSetting.
        The release number when the resource was upgraded.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this AuthenticationFactorSetting.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this AuthenticationFactorSetting.
        OCI Domain Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The domain_ocid of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this AuthenticationFactorSetting.
        OCI Domain Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param domain_ocid: The domain_ocid of this AuthenticationFactorSetting.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this AuthenticationFactorSetting.
        OCI Compartment Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The compartment_ocid of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this AuthenticationFactorSetting.
        OCI Compartment Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param compartment_ocid: The compartment_ocid of this AuthenticationFactorSetting.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this AuthenticationFactorSetting.
        OCI Tenant Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The tenancy_ocid of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this AuthenticationFactorSetting.
        OCI Tenant Id (ocid) in which the resource lives.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param tenancy_ocid: The tenancy_ocid of this AuthenticationFactorSetting.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def email_enabled(self):
        """
        Gets the email_enabled of this AuthenticationFactorSetting.
        If true, indicates that the EMAIL channel is enabled for authentication

        **Added In:** 18.1.2

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The email_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._email_enabled

    @email_enabled.setter
    def email_enabled(self, email_enabled):
        """
        Sets the email_enabled of this AuthenticationFactorSetting.
        If true, indicates that the EMAIL channel is enabled for authentication

        **Added In:** 18.1.2

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param email_enabled: The email_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._email_enabled = email_enabled

    @property
    def sms_enabled(self):
        """
        **[Required]** Gets the sms_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Short Message Service (SMS) channel is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The sms_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._sms_enabled

    @sms_enabled.setter
    def sms_enabled(self, sms_enabled):
        """
        Sets the sms_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Short Message Service (SMS) channel is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param sms_enabled: The sms_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._sms_enabled = sms_enabled

    @property
    def phone_call_enabled(self):
        """
        Gets the phone_call_enabled of this AuthenticationFactorSetting.
        If true, indicates that the phone (PHONE_CALL) channel is enabled for authentication

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The phone_call_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._phone_call_enabled

    @phone_call_enabled.setter
    def phone_call_enabled(self, phone_call_enabled):
        """
        Sets the phone_call_enabled of this AuthenticationFactorSetting.
        If true, indicates that the phone (PHONE_CALL) channel is enabled for authentication

        **Added In:** 20.1.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param phone_call_enabled: The phone_call_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._phone_call_enabled = phone_call_enabled

    @property
    def totp_enabled(self):
        """
        **[Required]** Gets the totp_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Mobile App One Time Passcode channel is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The totp_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._totp_enabled

    @totp_enabled.setter
    def totp_enabled(self, totp_enabled):
        """
        Sets the totp_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Mobile App One Time Passcode channel is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param totp_enabled: The totp_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._totp_enabled = totp_enabled

    @property
    def push_enabled(self):
        """
        **[Required]** Gets the push_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Mobile App Push Notification channel is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The push_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._push_enabled

    @push_enabled.setter
    def push_enabled(self, push_enabled):
        """
        Sets the push_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Mobile App Push Notification channel is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param push_enabled: The push_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._push_enabled = push_enabled

    @property
    def bypass_code_enabled(self):
        """
        **[Required]** Gets the bypass_code_enabled of this AuthenticationFactorSetting.
        If true, indicates that Bypass Code is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The bypass_code_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._bypass_code_enabled

    @bypass_code_enabled.setter
    def bypass_code_enabled(self, bypass_code_enabled):
        """
        Sets the bypass_code_enabled of this AuthenticationFactorSetting.
        If true, indicates that Bypass Code is enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param bypass_code_enabled: The bypass_code_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._bypass_code_enabled = bypass_code_enabled

    @property
    def security_questions_enabled(self):
        """
        **[Required]** Gets the security_questions_enabled of this AuthenticationFactorSetting.
        If true, indicates that Security Questions are enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The security_questions_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._security_questions_enabled

    @security_questions_enabled.setter
    def security_questions_enabled(self, security_questions_enabled):
        """
        Sets the security_questions_enabled of this AuthenticationFactorSetting.
        If true, indicates that Security Questions are enabled for authentication

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: boolean
         - uniqueness: none


        :param security_questions_enabled: The security_questions_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._security_questions_enabled = security_questions_enabled

    @property
    def fido_authenticator_enabled(self):
        """
        Gets the fido_authenticator_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Fido Authenticator channels are enabled for authentication

        **Added In:** 2009232244

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The fido_authenticator_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._fido_authenticator_enabled

    @fido_authenticator_enabled.setter
    def fido_authenticator_enabled(self, fido_authenticator_enabled):
        """
        Sets the fido_authenticator_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Fido Authenticator channels are enabled for authentication

        **Added In:** 2009232244

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param fido_authenticator_enabled: The fido_authenticator_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._fido_authenticator_enabled = fido_authenticator_enabled

    @property
    def yubico_otp_enabled(self):
        """
        Gets the yubico_otp_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Yubico OTP is enabled for authentication

        **Added In:** 2109090424

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The yubico_otp_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._yubico_otp_enabled

    @yubico_otp_enabled.setter
    def yubico_otp_enabled(self, yubico_otp_enabled):
        """
        Sets the yubico_otp_enabled of this AuthenticationFactorSetting.
        If true, indicates that the Yubico OTP is enabled for authentication

        **Added In:** 2109090424

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param yubico_otp_enabled: The yubico_otp_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._yubico_otp_enabled = yubico_otp_enabled

    @property
    def mfa_enrollment_type(self):
        """
        **[Required]** Gets the mfa_enrollment_type of this AuthenticationFactorSetting.
        Specifies if Multi-Factor Authentication enrollment is mandatory or optional for a user

        **Deprecated Since: 18.1.2**

        **SCIM++ Properties:**
         - idcsCanonicalValueSourceFilter: attrName eq \"mfaEnrollmentType\" and attrValues.value eq \"$(mfaEnrollmentType)\"
         - idcsCanonicalValueSourceResourceType: AllowedValue
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The mfa_enrollment_type of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._mfa_enrollment_type

    @mfa_enrollment_type.setter
    def mfa_enrollment_type(self, mfa_enrollment_type):
        """
        Sets the mfa_enrollment_type of this AuthenticationFactorSetting.
        Specifies if Multi-Factor Authentication enrollment is mandatory or optional for a user

        **Deprecated Since: 18.1.2**

        **SCIM++ Properties:**
         - idcsCanonicalValueSourceFilter: attrName eq \"mfaEnrollmentType\" and attrValues.value eq \"$(mfaEnrollmentType)\"
         - idcsCanonicalValueSourceResourceType: AllowedValue
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param mfa_enrollment_type: The mfa_enrollment_type of this AuthenticationFactorSetting.
        :type: str
        """
        self._mfa_enrollment_type = mfa_enrollment_type

    @property
    def mfa_enabled_category(self):
        """
        Gets the mfa_enabled_category of this AuthenticationFactorSetting.
        Specifies the category of people for whom Multi-Factor Authentication is enabled. This is a readOnly attribute which reflects the value of mfaEnabledCategory attribute in SsoSettings

        **Deprecated Since: 18.1.2**

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The mfa_enabled_category of this AuthenticationFactorSetting.
        :rtype: str
        """
        return self._mfa_enabled_category

    @mfa_enabled_category.setter
    def mfa_enabled_category(self, mfa_enabled_category):
        """
        Sets the mfa_enabled_category of this AuthenticationFactorSetting.
        Specifies the category of people for whom Multi-Factor Authentication is enabled. This is a readOnly attribute which reflects the value of mfaEnabledCategory attribute in SsoSettings

        **Deprecated Since: 18.1.2**

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param mfa_enabled_category: The mfa_enabled_category of this AuthenticationFactorSetting.
        :type: str
        """
        self._mfa_enabled_category = mfa_enabled_category

    @property
    def hide_backup_factor_enabled(self):
        """
        Gets the hide_backup_factor_enabled of this AuthenticationFactorSetting.
        If true, indicates that 'Show backup factor(s)' button will be hidden during authentication

        **Added In:** 19.3.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The hide_backup_factor_enabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._hide_backup_factor_enabled

    @hide_backup_factor_enabled.setter
    def hide_backup_factor_enabled(self, hide_backup_factor_enabled):
        """
        Sets the hide_backup_factor_enabled of this AuthenticationFactorSetting.
        If true, indicates that 'Show backup factor(s)' button will be hidden during authentication

        **Added In:** 19.3.3

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param hide_backup_factor_enabled: The hide_backup_factor_enabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._hide_backup_factor_enabled = hide_backup_factor_enabled

    @property
    def auto_enroll_email_factor_disabled(self):
        """
        Gets the auto_enroll_email_factor_disabled of this AuthenticationFactorSetting.
        If true, indicates that email will not be enrolled as a MFA factor automatically if it a account recovery factor

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The auto_enroll_email_factor_disabled of this AuthenticationFactorSetting.
        :rtype: bool
        """
        return self._auto_enroll_email_factor_disabled

    @auto_enroll_email_factor_disabled.setter
    def auto_enroll_email_factor_disabled(self, auto_enroll_email_factor_disabled):
        """
        Sets the auto_enroll_email_factor_disabled of this AuthenticationFactorSetting.
        If true, indicates that email will not be enrolled as a MFA factor automatically if it a account recovery factor

        **Added In:** 2011192329

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param auto_enroll_email_factor_disabled: The auto_enroll_email_factor_disabled of this AuthenticationFactorSetting.
        :type: bool
        """
        self._auto_enroll_email_factor_disabled = auto_enroll_email_factor_disabled

    @property
    def user_enrollment_disabled_factors(self):
        """
        Gets the user_enrollment_disabled_factors of this AuthenticationFactorSetting.
        Factors for which enrollment should be blocked for End User

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for items in this list are: "EMAIL", "SMS", "TOTP", "PUSH", "OFFLINETOTP", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The user_enrollment_disabled_factors of this AuthenticationFactorSetting.
        :rtype: list[str]
        """
        return self._user_enrollment_disabled_factors

    @user_enrollment_disabled_factors.setter
    def user_enrollment_disabled_factors(self, user_enrollment_disabled_factors):
        """
        Sets the user_enrollment_disabled_factors of this AuthenticationFactorSetting.
        Factors for which enrollment should be blocked for End User

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param user_enrollment_disabled_factors: The user_enrollment_disabled_factors of this AuthenticationFactorSetting.
        :type: list[str]
        """
        allowed_values = ["EMAIL", "SMS", "TOTP", "PUSH", "OFFLINETOTP", "VOICE", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR"]
        if user_enrollment_disabled_factors:
            user_enrollment_disabled_factors[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in user_enrollment_disabled_factors]
        self._user_enrollment_disabled_factors = user_enrollment_disabled_factors

    @property
    def email_settings(self):
        """
        Gets the email_settings of this AuthenticationFactorSetting.

        :return: The email_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsEmailSettings
        """
        return self._email_settings

    @email_settings.setter
    def email_settings(self, email_settings):
        """
        Sets the email_settings of this AuthenticationFactorSetting.

        :param email_settings: The email_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsEmailSettings
        """
        self._email_settings = email_settings

    @property
    def third_party_factor(self):
        """
        Gets the third_party_factor of this AuthenticationFactorSetting.

        :return: The third_party_factor of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsThirdPartyFactor
        """
        return self._third_party_factor

    @third_party_factor.setter
    def third_party_factor(self, third_party_factor):
        """
        Sets the third_party_factor of this AuthenticationFactorSetting.

        :param third_party_factor: The third_party_factor of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsThirdPartyFactor
        """
        self._third_party_factor = third_party_factor

    @property
    def notification_settings(self):
        """
        **[Required]** Gets the notification_settings of this AuthenticationFactorSetting.

        :return: The notification_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsNotificationSettings
        """
        return self._notification_settings

    @notification_settings.setter
    def notification_settings(self, notification_settings):
        """
        Sets the notification_settings of this AuthenticationFactorSetting.

        :param notification_settings: The notification_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsNotificationSettings
        """
        self._notification_settings = notification_settings

    @property
    def identity_store_settings(self):
        """
        Gets the identity_store_settings of this AuthenticationFactorSetting.

        :return: The identity_store_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsIdentityStoreSettings
        """
        return self._identity_store_settings

    @identity_store_settings.setter
    def identity_store_settings(self, identity_store_settings):
        """
        Sets the identity_store_settings of this AuthenticationFactorSetting.

        :param identity_store_settings: The identity_store_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsIdentityStoreSettings
        """
        self._identity_store_settings = identity_store_settings

    @property
    def bypass_code_settings(self):
        """
        **[Required]** Gets the bypass_code_settings of this AuthenticationFactorSetting.

        :return: The bypass_code_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsBypassCodeSettings
        """
        return self._bypass_code_settings

    @bypass_code_settings.setter
    def bypass_code_settings(self, bypass_code_settings):
        """
        Sets the bypass_code_settings of this AuthenticationFactorSetting.

        :param bypass_code_settings: The bypass_code_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsBypassCodeSettings
        """
        self._bypass_code_settings = bypass_code_settings

    @property
    def client_app_settings(self):
        """
        **[Required]** Gets the client_app_settings of this AuthenticationFactorSetting.

        :return: The client_app_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsClientAppSettings
        """
        return self._client_app_settings

    @client_app_settings.setter
    def client_app_settings(self, client_app_settings):
        """
        Sets the client_app_settings of this AuthenticationFactorSetting.

        :param client_app_settings: The client_app_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsClientAppSettings
        """
        self._client_app_settings = client_app_settings

    @property
    def endpoint_restrictions(self):
        """
        **[Required]** Gets the endpoint_restrictions of this AuthenticationFactorSetting.

        :return: The endpoint_restrictions of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsEndpointRestrictions
        """
        return self._endpoint_restrictions

    @endpoint_restrictions.setter
    def endpoint_restrictions(self, endpoint_restrictions):
        """
        Sets the endpoint_restrictions of this AuthenticationFactorSetting.

        :param endpoint_restrictions: The endpoint_restrictions of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsEndpointRestrictions
        """
        self._endpoint_restrictions = endpoint_restrictions

    @property
    def compliance_policy(self):
        """
        **[Required]** Gets the compliance_policy of this AuthenticationFactorSetting.
        Compliance Policy that defines actions to be taken when a condition is violated

        **SCIM++ Properties:**
         - idcsCompositeKey: [name]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The compliance_policy of this AuthenticationFactorSetting.
        :rtype: list[oci.identity_domains.models.AuthenticationFactorSettingsCompliancePolicy]
        """
        return self._compliance_policy

    @compliance_policy.setter
    def compliance_policy(self, compliance_policy):
        """
        Sets the compliance_policy of this AuthenticationFactorSetting.
        Compliance Policy that defines actions to be taken when a condition is violated

        **SCIM++ Properties:**
         - idcsCompositeKey: [name]
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: true
         - returned: default
         - type: complex
         - uniqueness: none


        :param compliance_policy: The compliance_policy of this AuthenticationFactorSetting.
        :type: list[oci.identity_domains.models.AuthenticationFactorSettingsCompliancePolicy]
        """
        self._compliance_policy = compliance_policy

    @property
    def totp_settings(self):
        """
        **[Required]** Gets the totp_settings of this AuthenticationFactorSetting.

        :return: The totp_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.AuthenticationFactorSettingsTotpSettings
        """
        return self._totp_settings

    @totp_settings.setter
    def totp_settings(self, totp_settings):
        """
        Sets the totp_settings of this AuthenticationFactorSetting.

        :param totp_settings: The totp_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.AuthenticationFactorSettingsTotpSettings
        """
        self._totp_settings = totp_settings

    @property
    def urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings(self):
        """
        Gets the urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings of this AuthenticationFactorSetting.

        :return: The urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.ExtensionThirdPartyAuthenticationFactorSettings
        """
        return self._urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings

    @urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings.setter
    def urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings(self, urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings):
        """
        Sets the urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings of this AuthenticationFactorSetting.

        :param urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings: The urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.ExtensionThirdPartyAuthenticationFactorSettings
        """
        self._urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings = urnietfparamsscimschemasoracleidcsextensionthird_party_authentication_factor_settings

    @property
    def urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings(self):
        """
        Gets the urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings of this AuthenticationFactorSetting.

        :return: The urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings of this AuthenticationFactorSetting.
        :rtype: oci.identity_domains.models.ExtensionFidoAuthenticationFactorSettings
        """
        return self._urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings

    @urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings.setter
    def urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings(self, urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings):
        """
        Sets the urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings of this AuthenticationFactorSetting.

        :param urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings: The urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings of this AuthenticationFactorSetting.
        :type: oci.identity_domains.models.ExtensionFidoAuthenticationFactorSettings
        """
        self._urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings = urnietfparamsscimschemasoracleidcsextensionfido_authentication_factor_settings

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
