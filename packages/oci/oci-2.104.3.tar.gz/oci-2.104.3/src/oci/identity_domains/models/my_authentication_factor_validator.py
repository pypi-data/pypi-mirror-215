# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyAuthenticationFactorValidator(object):
    """
    Validate any given Authentication Factor
    """

    #: A constant which can be used with the idcs_prevented_operations property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "USERNAME_PASSWORD"
    AUTH_FACTOR_USERNAME_PASSWORD = "USERNAME_PASSWORD"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "PUSH"
    AUTH_FACTOR_PUSH = "PUSH"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "TOTP"
    AUTH_FACTOR_TOTP = "TOTP"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "EMAIL"
    AUTH_FACTOR_EMAIL = "EMAIL"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "SMS"
    AUTH_FACTOR_SMS = "SMS"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "VOICE"
    AUTH_FACTOR_VOICE = "VOICE"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "BYPASSCODE"
    AUTH_FACTOR_BYPASSCODE = "BYPASSCODE"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "SECURITY_QUESTIONS"
    AUTH_FACTOR_SECURITY_QUESTIONS = "SECURITY_QUESTIONS"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "TRUST_TOKEN"
    AUTH_FACTOR_TRUST_TOKEN = "TRUST_TOKEN"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "PHONE_CALL"
    AUTH_FACTOR_PHONE_CALL = "PHONE_CALL"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "THIRDPARTY"
    AUTH_FACTOR_THIRDPARTY = "THIRDPARTY"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "FIDO_AUTHENTICATOR"
    AUTH_FACTOR_FIDO_AUTHENTICATOR = "FIDO_AUTHENTICATOR"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "YUBICO_OTP"
    AUTH_FACTOR_YUBICO_OTP = "YUBICO_OTP"

    #: A constant which can be used with the auth_factor property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "KMSI_TOKEN"
    AUTH_FACTOR_KMSI_TOKEN = "KMSI_TOKEN"

    #: A constant which can be used with the scenario property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "ENROLLMENT"
    SCENARIO_ENROLLMENT = "ENROLLMENT"

    #: A constant which can be used with the scenario property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "AUTHENTICATION"
    SCENARIO_AUTHENTICATION = "AUTHENTICATION"

    #: A constant which can be used with the status property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "SUCCESS"
    STATUS_SUCCESS = "SUCCESS"

    #: A constant which can be used with the status property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "FAILURE"
    STATUS_FAILURE = "FAILURE"

    #: A constant which can be used with the type property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "SAML"
    TYPE_SAML = "SAML"

    #: A constant which can be used with the type property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "OIDC"
    TYPE_OIDC = "OIDC"

    #: A constant which can be used with the preference_type property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "PASSWORDLESS"
    PREFERENCE_TYPE_PASSWORDLESS = "PASSWORDLESS"

    #: A constant which can be used with the preference_type property of a MyAuthenticationFactorValidator.
    #: This constant has a value of "MFA"
    PREFERENCE_TYPE_MFA = "MFA"

    def __init__(self, **kwargs):
        """
        Initializes a new MyAuthenticationFactorValidator object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this MyAuthenticationFactorValidator.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this MyAuthenticationFactorValidator.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this MyAuthenticationFactorValidator.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this MyAuthenticationFactorValidator.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this MyAuthenticationFactorValidator.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this MyAuthenticationFactorValidator.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this MyAuthenticationFactorValidator.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this MyAuthenticationFactorValidator.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this MyAuthenticationFactorValidator.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this MyAuthenticationFactorValidator.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this MyAuthenticationFactorValidator.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this MyAuthenticationFactorValidator.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this MyAuthenticationFactorValidator.
        :type tenancy_ocid: str

        :param auth_factor:
            The value to assign to the auth_factor property of this MyAuthenticationFactorValidator.
            Allowed values for this property are: "USERNAME_PASSWORD", "PUSH", "TOTP", "EMAIL", "SMS", "VOICE", "BYPASSCODE", "SECURITY_QUESTIONS", "TRUST_TOKEN", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", "KMSI_TOKEN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type auth_factor: str

        :param scenario:
            The value to assign to the scenario property of this MyAuthenticationFactorValidator.
            Allowed values for this property are: "ENROLLMENT", "AUTHENTICATION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type scenario: str

        :param request_id:
            The value to assign to the request_id property of this MyAuthenticationFactorValidator.
        :type request_id: str

        :param otp_code:
            The value to assign to the otp_code property of this MyAuthenticationFactorValidator.
        :type otp_code: str

        :param device_id:
            The value to assign to the device_id property of this MyAuthenticationFactorValidator.
        :type device_id: str

        :param status:
            The value to assign to the status property of this MyAuthenticationFactorValidator.
            Allowed values for this property are: "SUCCESS", "FAILURE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param user_id:
            The value to assign to the user_id property of this MyAuthenticationFactorValidator.
        :type user_id: str

        :param user_name:
            The value to assign to the user_name property of this MyAuthenticationFactorValidator.
        :type user_name: str

        :param display_name:
            The value to assign to the display_name property of this MyAuthenticationFactorValidator.
        :type display_name: str

        :param message:
            The value to assign to the message property of this MyAuthenticationFactorValidator.
        :type message: str

        :param type:
            The value to assign to the type property of this MyAuthenticationFactorValidator.
            Allowed values for this property are: "SAML", "OIDC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param update_user_preference:
            The value to assign to the update_user_preference property of this MyAuthenticationFactorValidator.
        :type update_user_preference: bool

        :param preference_type:
            The value to assign to the preference_type property of this MyAuthenticationFactorValidator.
            Allowed values for this property are: "PASSWORDLESS", "MFA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type preference_type: str

        :param security_questions:
            The value to assign to the security_questions property of this MyAuthenticationFactorValidator.
        :type security_questions: list[oci.identity_domains.models.MyAuthenticationFactorValidatorSecurityQuestions]

        :param name:
            The value to assign to the name property of this MyAuthenticationFactorValidator.
        :type name: str

        :param platform:
            The value to assign to the platform property of this MyAuthenticationFactorValidator.
        :type platform: str

        :param location:
            The value to assign to the location property of this MyAuthenticationFactorValidator.
        :type location: str

        :param trusted_token_id:
            The value to assign to the trusted_token_id property of this MyAuthenticationFactorValidator.
        :type trusted_token_id: str

        :param kmsi_token_id:
            The value to assign to the kmsi_token_id property of this MyAuthenticationFactorValidator.
        :type kmsi_token_id: str

        :param policy_enabled_second_factors:
            The value to assign to the policy_enabled_second_factors property of this MyAuthenticationFactorValidator.
        :type policy_enabled_second_factors: list[str]

        :param create_trusted_agent:
            The value to assign to the create_trusted_agent property of this MyAuthenticationFactorValidator.
        :type create_trusted_agent: bool

        :param create_kmsi_token:
            The value to assign to the create_kmsi_token property of this MyAuthenticationFactorValidator.
        :type create_kmsi_token: bool

        :param is_acc_rec_enabled:
            The value to assign to the is_acc_rec_enabled property of this MyAuthenticationFactorValidator.
        :type is_acc_rec_enabled: bool

        :param policy_trusted_frequency_mins:
            The value to assign to the policy_trusted_frequency_mins property of this MyAuthenticationFactorValidator.
        :type policy_trusted_frequency_mins: int

        :param third_party_factor:
            The value to assign to the third_party_factor property of this MyAuthenticationFactorValidator.
        :type third_party_factor: oci.identity_domains.models.MyAuthenticationFactorValidatorThirdPartyFactor

        :param additional_attributes:
            The value to assign to the additional_attributes property of this MyAuthenticationFactorValidator.
        :type additional_attributes: list[oci.identity_domains.models.MyAuthenticationFactorValidatorAdditionalAttributes]

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
            'auth_factor': 'str',
            'scenario': 'str',
            'request_id': 'str',
            'otp_code': 'str',
            'device_id': 'str',
            'status': 'str',
            'user_id': 'str',
            'user_name': 'str',
            'display_name': 'str',
            'message': 'str',
            'type': 'str',
            'update_user_preference': 'bool',
            'preference_type': 'str',
            'security_questions': 'list[MyAuthenticationFactorValidatorSecurityQuestions]',
            'name': 'str',
            'platform': 'str',
            'location': 'str',
            'trusted_token_id': 'str',
            'kmsi_token_id': 'str',
            'policy_enabled_second_factors': 'list[str]',
            'create_trusted_agent': 'bool',
            'create_kmsi_token': 'bool',
            'is_acc_rec_enabled': 'bool',
            'policy_trusted_frequency_mins': 'int',
            'third_party_factor': 'MyAuthenticationFactorValidatorThirdPartyFactor',
            'additional_attributes': 'list[MyAuthenticationFactorValidatorAdditionalAttributes]'
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
            'auth_factor': 'authFactor',
            'scenario': 'scenario',
            'request_id': 'requestId',
            'otp_code': 'otpCode',
            'device_id': 'deviceId',
            'status': 'status',
            'user_id': 'userId',
            'user_name': 'userName',
            'display_name': 'displayName',
            'message': 'message',
            'type': 'type',
            'update_user_preference': 'updateUserPreference',
            'preference_type': 'preferenceType',
            'security_questions': 'securityQuestions',
            'name': 'name',
            'platform': 'platform',
            'location': 'location',
            'trusted_token_id': 'trustedTokenId',
            'kmsi_token_id': 'kmsiTokenId',
            'policy_enabled_second_factors': 'policyEnabledSecondFactors',
            'create_trusted_agent': 'createTrustedAgent',
            'create_kmsi_token': 'createKmsiToken',
            'is_acc_rec_enabled': 'isAccRecEnabled',
            'policy_trusted_frequency_mins': 'policyTrustedFrequencyMins',
            'third_party_factor': 'thirdPartyFactor',
            'additional_attributes': 'additionalAttributes'
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
        self._auth_factor = None
        self._scenario = None
        self._request_id = None
        self._otp_code = None
        self._device_id = None
        self._status = None
        self._user_id = None
        self._user_name = None
        self._display_name = None
        self._message = None
        self._type = None
        self._update_user_preference = None
        self._preference_type = None
        self._security_questions = None
        self._name = None
        self._platform = None
        self._location = None
        self._trusted_token_id = None
        self._kmsi_token_id = None
        self._policy_enabled_second_factors = None
        self._create_trusted_agent = None
        self._create_kmsi_token = None
        self._is_acc_rec_enabled = None
        self._policy_trusted_frequency_mins = None
        self._third_party_factor = None
        self._additional_attributes = None

    @property
    def id(self):
        """
        Gets the id of this MyAuthenticationFactorValidator.
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


        :return: The id of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MyAuthenticationFactorValidator.
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


        :param id: The id of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this MyAuthenticationFactorValidator.
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


        :return: The ocid of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this MyAuthenticationFactorValidator.
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


        :param ocid: The ocid of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this MyAuthenticationFactorValidator.
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


        :return: The schemas of this MyAuthenticationFactorValidator.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this MyAuthenticationFactorValidator.
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


        :param schemas: The schemas of this MyAuthenticationFactorValidator.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this MyAuthenticationFactorValidator.

        :return: The meta of this MyAuthenticationFactorValidator.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this MyAuthenticationFactorValidator.

        :param meta: The meta of this MyAuthenticationFactorValidator.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this MyAuthenticationFactorValidator.

        :return: The idcs_created_by of this MyAuthenticationFactorValidator.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this MyAuthenticationFactorValidator.

        :param idcs_created_by: The idcs_created_by of this MyAuthenticationFactorValidator.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this MyAuthenticationFactorValidator.

        :return: The idcs_last_modified_by of this MyAuthenticationFactorValidator.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this MyAuthenticationFactorValidator.

        :param idcs_last_modified_by: The idcs_last_modified_by of this MyAuthenticationFactorValidator.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this MyAuthenticationFactorValidator.
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


        :return: The idcs_prevented_operations of this MyAuthenticationFactorValidator.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this MyAuthenticationFactorValidator.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this MyAuthenticationFactorValidator.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this MyAuthenticationFactorValidator.
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


        :return: The tags of this MyAuthenticationFactorValidator.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this MyAuthenticationFactorValidator.
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


        :param tags: The tags of this MyAuthenticationFactorValidator.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this MyAuthenticationFactorValidator.
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


        :return: The delete_in_progress of this MyAuthenticationFactorValidator.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this MyAuthenticationFactorValidator.
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


        :param delete_in_progress: The delete_in_progress of this MyAuthenticationFactorValidator.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this MyAuthenticationFactorValidator.
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


        :return: The idcs_last_upgraded_in_release of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this MyAuthenticationFactorValidator.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this MyAuthenticationFactorValidator.
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


        :return: The domain_ocid of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this MyAuthenticationFactorValidator.
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


        :param domain_ocid: The domain_ocid of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this MyAuthenticationFactorValidator.
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


        :return: The compartment_ocid of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this MyAuthenticationFactorValidator.
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


        :param compartment_ocid: The compartment_ocid of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this MyAuthenticationFactorValidator.
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


        :return: The tenancy_ocid of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this MyAuthenticationFactorValidator.
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


        :param tenancy_ocid: The tenancy_ocid of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def auth_factor(self):
        """
        **[Required]** Gets the auth_factor of this MyAuthenticationFactorValidator.
        Authentication Factor which is being validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: true
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false

        Allowed values for this property are: "USERNAME_PASSWORD", "PUSH", "TOTP", "EMAIL", "SMS", "VOICE", "BYPASSCODE", "SECURITY_QUESTIONS", "TRUST_TOKEN", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", "KMSI_TOKEN", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The auth_factor of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._auth_factor

    @auth_factor.setter
    def auth_factor(self, auth_factor):
        """
        Sets the auth_factor of this MyAuthenticationFactorValidator.
        Authentication Factor which is being validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: true
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param auth_factor: The auth_factor of this MyAuthenticationFactorValidator.
        :type: str
        """
        allowed_values = ["USERNAME_PASSWORD", "PUSH", "TOTP", "EMAIL", "SMS", "VOICE", "BYPASSCODE", "SECURITY_QUESTIONS", "TRUST_TOKEN", "PHONE_CALL", "THIRDPARTY", "FIDO_AUTHENTICATOR", "YUBICO_OTP", "KMSI_TOKEN"]
        if not value_allowed_none_or_none_sentinel(auth_factor, allowed_values):
            auth_factor = 'UNKNOWN_ENUM_VALUE'
        self._auth_factor = auth_factor

    @property
    def scenario(self):
        """
        **[Required]** Gets the scenario of this MyAuthenticationFactorValidator.
        Specifies whether the service is being used to enroll or validate a factor

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: true
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false

        Allowed values for this property are: "ENROLLMENT", "AUTHENTICATION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The scenario of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._scenario

    @scenario.setter
    def scenario(self, scenario):
        """
        Sets the scenario of this MyAuthenticationFactorValidator.
        Specifies whether the service is being used to enroll or validate a factor

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: true
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param scenario: The scenario of this MyAuthenticationFactorValidator.
        :type: str
        """
        allowed_values = ["ENROLLMENT", "AUTHENTICATION"]
        if not value_allowed_none_or_none_sentinel(scenario, allowed_values):
            scenario = 'UNKNOWN_ENUM_VALUE'
        self._scenario = scenario

    @property
    def request_id(self):
        """
        Gets the request_id of this MyAuthenticationFactorValidator.
        Request ID which is being validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :return: The request_id of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this MyAuthenticationFactorValidator.
        Request ID which is being validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param request_id: The request_id of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._request_id = request_id

    @property
    def otp_code(self):
        """
        Gets the otp_code of this MyAuthenticationFactorValidator.
        The One Time Passcode which needs to be validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: never
         - uniqueness: none
         - idcsSensitive: encrypt
         - idcsSearchable: false


        :return: The otp_code of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._otp_code

    @otp_code.setter
    def otp_code(self, otp_code):
        """
        Sets the otp_code of this MyAuthenticationFactorValidator.
        The One Time Passcode which needs to be validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: never
         - uniqueness: none
         - idcsSensitive: encrypt
         - idcsSearchable: false


        :param otp_code: The otp_code of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._otp_code = otp_code

    @property
    def device_id(self):
        """
        Gets the device_id of this MyAuthenticationFactorValidator.
        Device id whose factor is being validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :return: The device_id of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._device_id

    @device_id.setter
    def device_id(self, device_id):
        """
        Sets the device_id of this MyAuthenticationFactorValidator.
        Device id whose factor is being validated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param device_id: The device_id of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._device_id = device_id

    @property
    def status(self):
        """
        Gets the status of this MyAuthenticationFactorValidator.
        Validation status returned in the response

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readOnly
         - returned: default
         - uniqueness: none
         - idcsSearchable: false

        Allowed values for this property are: "SUCCESS", "FAILURE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this MyAuthenticationFactorValidator.
        Validation status returned in the response

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readOnly
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param status: The status of this MyAuthenticationFactorValidator.
        :type: str
        """
        allowed_values = ["SUCCESS", "FAILURE"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def user_id(self):
        """
        Gets the user_id of this MyAuthenticationFactorValidator.
        User guid for whom the validation has initiated. Optional.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :return: The user_id of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """
        Sets the user_id of this MyAuthenticationFactorValidator.
        User guid for whom the validation has initiated. Optional.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param user_id: The user_id of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._user_id = user_id

    @property
    def user_name(self):
        """
        Gets the user_name of this MyAuthenticationFactorValidator.
        User name for whom the validation has initiated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false
         - idcsPii: true


        :return: The user_name of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this MyAuthenticationFactorValidator.
        User name for whom the validation has initiated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false
         - idcsPii: true


        :param user_name: The user_name of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._user_name = user_name

    @property
    def display_name(self):
        """
        Gets the display_name of this MyAuthenticationFactorValidator.
        Display name of the verified device

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :return: The display_name of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this MyAuthenticationFactorValidator.
        Display name of the verified device

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param display_name: The display_name of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._display_name = display_name

    @property
    def message(self):
        """
        Gets the message of this MyAuthenticationFactorValidator.
        Validator message which is passed by the client. When it is a PUSH notification, it can be a rejection message.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :return: The message of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this MyAuthenticationFactorValidator.
        Validator message which is passed by the client. When it is a PUSH notification, it can be a rejection message.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: readWrite
         - returned: default
         - uniqueness: none
         - idcsSearchable: false


        :param message: The message of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._message = message

    @property
    def type(self):
        """
        Gets the type of this MyAuthenticationFactorValidator.
        type indicating whether the flow is OIDC, SAML etc.,

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: default
         - uniqueness: none

        Allowed values for this property are: "SAML", "OIDC", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this MyAuthenticationFactorValidator.
        type indicating whether the flow is OIDC, SAML etc.,

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: default
         - uniqueness: none


        :param type: The type of this MyAuthenticationFactorValidator.
        :type: str
        """
        allowed_values = ["SAML", "OIDC"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def update_user_preference(self):
        """
        Gets the update_user_preference of this MyAuthenticationFactorValidator.
        Indicates whether to update user preferred mfa factor or not

        **SCIM++ Properties:**
         - type: boolean
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The update_user_preference of this MyAuthenticationFactorValidator.
        :rtype: bool
        """
        return self._update_user_preference

    @update_user_preference.setter
    def update_user_preference(self, update_user_preference):
        """
        Sets the update_user_preference of this MyAuthenticationFactorValidator.
        Indicates whether to update user preferred mfa factor or not

        **SCIM++ Properties:**
         - type: boolean
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param update_user_preference: The update_user_preference of this MyAuthenticationFactorValidator.
        :type: bool
        """
        self._update_user_preference = update_user_preference

    @property
    def preference_type(self):
        """
        Gets the preference_type of this MyAuthenticationFactorValidator.
        Indicates whether to user passwordless factor to be updated or mfa factor to be updated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none

        Allowed values for this property are: "PASSWORDLESS", "MFA", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The preference_type of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._preference_type

    @preference_type.setter
    def preference_type(self, preference_type):
        """
        Sets the preference_type of this MyAuthenticationFactorValidator.
        Indicates whether to user passwordless factor to be updated or mfa factor to be updated

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param preference_type: The preference_type of this MyAuthenticationFactorValidator.
        :type: str
        """
        allowed_values = ["PASSWORDLESS", "MFA"]
        if not value_allowed_none_or_none_sentinel(preference_type, allowed_values):
            preference_type = 'UNKNOWN_ENUM_VALUE'
        self._preference_type = preference_type

    @property
    def security_questions(self):
        """
        Gets the security_questions of this MyAuthenticationFactorValidator.
        List of security questions the user has submitted to get authenticated.

        **SCIM++ Properties:**
         - type: complex
         - multiValued: true
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none
         - idcsSearchable: false


        :return: The security_questions of this MyAuthenticationFactorValidator.
        :rtype: list[oci.identity_domains.models.MyAuthenticationFactorValidatorSecurityQuestions]
        """
        return self._security_questions

    @security_questions.setter
    def security_questions(self, security_questions):
        """
        Sets the security_questions of this MyAuthenticationFactorValidator.
        List of security questions the user has submitted to get authenticated.

        **SCIM++ Properties:**
         - type: complex
         - multiValued: true
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none
         - idcsSearchable: false


        :param security_questions: The security_questions of this MyAuthenticationFactorValidator.
        :type: list[oci.identity_domains.models.MyAuthenticationFactorValidatorSecurityQuestions]
        """
        self._security_questions = security_questions

    @property
    def name(self):
        """
        Gets the name of this MyAuthenticationFactorValidator.
        Name of the client to be trusted

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The name of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MyAuthenticationFactorValidator.
        Name of the client to be trusted

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param name: The name of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._name = name

    @property
    def platform(self):
        """
        Gets the platform of this MyAuthenticationFactorValidator.
        Platform of the client to be trusted

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The platform of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Sets the platform of this MyAuthenticationFactorValidator.
        Platform of the client to be trusted

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param platform: The platform of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._platform = platform

    @property
    def location(self):
        """
        Gets the location of this MyAuthenticationFactorValidator.
        Location of the trusted client.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The location of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Sets the location of this MyAuthenticationFactorValidator.
        Location of the trusted client.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param location: The location of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._location = location

    @property
    def trusted_token_id(self):
        """
        Gets the trusted_token_id of this MyAuthenticationFactorValidator.
        Trusted token resource identifier.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The trusted_token_id of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._trusted_token_id

    @trusted_token_id.setter
    def trusted_token_id(self, trusted_token_id):
        """
        Sets the trusted_token_id of this MyAuthenticationFactorValidator.
        Trusted token resource identifier.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param trusted_token_id: The trusted_token_id of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._trusted_token_id = trusted_token_id

    @property
    def kmsi_token_id(self):
        """
        Gets the kmsi_token_id of this MyAuthenticationFactorValidator.
        KMSI token resource identifier.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The kmsi_token_id of this MyAuthenticationFactorValidator.
        :rtype: str
        """
        return self._kmsi_token_id

    @kmsi_token_id.setter
    def kmsi_token_id(self, kmsi_token_id):
        """
        Sets the kmsi_token_id of this MyAuthenticationFactorValidator.
        KMSI token resource identifier.

        **SCIM++ Properties:**
         - type: string
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param kmsi_token_id: The kmsi_token_id of this MyAuthenticationFactorValidator.
        :type: str
        """
        self._kmsi_token_id = kmsi_token_id

    @property
    def policy_enabled_second_factors(self):
        """
        Gets the policy_enabled_second_factors of this MyAuthenticationFactorValidator.
        Sign-On Policy dictated allowed second factors.

        **SCIM++ Properties:**
         - type: string
         - multiValued: true
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The policy_enabled_second_factors of this MyAuthenticationFactorValidator.
        :rtype: list[str]
        """
        return self._policy_enabled_second_factors

    @policy_enabled_second_factors.setter
    def policy_enabled_second_factors(self, policy_enabled_second_factors):
        """
        Sets the policy_enabled_second_factors of this MyAuthenticationFactorValidator.
        Sign-On Policy dictated allowed second factors.

        **SCIM++ Properties:**
         - type: string
         - multiValued: true
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param policy_enabled_second_factors: The policy_enabled_second_factors of this MyAuthenticationFactorValidator.
        :type: list[str]
        """
        self._policy_enabled_second_factors = policy_enabled_second_factors

    @property
    def create_trusted_agent(self):
        """
        Gets the create_trusted_agent of this MyAuthenticationFactorValidator.
        Indicates to create trust token.

        **SCIM++ Properties:**
         - type: boolean
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The create_trusted_agent of this MyAuthenticationFactorValidator.
        :rtype: bool
        """
        return self._create_trusted_agent

    @create_trusted_agent.setter
    def create_trusted_agent(self, create_trusted_agent):
        """
        Sets the create_trusted_agent of this MyAuthenticationFactorValidator.
        Indicates to create trust token.

        **SCIM++ Properties:**
         - type: boolean
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param create_trusted_agent: The create_trusted_agent of this MyAuthenticationFactorValidator.
        :type: bool
        """
        self._create_trusted_agent = create_trusted_agent

    @property
    def create_kmsi_token(self):
        """
        Gets the create_kmsi_token of this MyAuthenticationFactorValidator.
        Indicates to create kmsi token.

        **SCIM++ Properties:**
         - type: boolean
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The create_kmsi_token of this MyAuthenticationFactorValidator.
        :rtype: bool
        """
        return self._create_kmsi_token

    @create_kmsi_token.setter
    def create_kmsi_token(self, create_kmsi_token):
        """
        Sets the create_kmsi_token of this MyAuthenticationFactorValidator.
        Indicates to create kmsi token.

        **SCIM++ Properties:**
         - type: boolean
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param create_kmsi_token: The create_kmsi_token of this MyAuthenticationFactorValidator.
        :type: bool
        """
        self._create_kmsi_token = create_kmsi_token

    @property
    def is_acc_rec_enabled(self):
        """
        Gets the is_acc_rec_enabled of this MyAuthenticationFactorValidator.
        Flag indicates whether the factor is enrolled in account recovery. If the value is not provided or false, then it will be treated as MFA factor validation.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The is_acc_rec_enabled of this MyAuthenticationFactorValidator.
        :rtype: bool
        """
        return self._is_acc_rec_enabled

    @is_acc_rec_enabled.setter
    def is_acc_rec_enabled(self, is_acc_rec_enabled):
        """
        Sets the is_acc_rec_enabled of this MyAuthenticationFactorValidator.
        Flag indicates whether the factor is enrolled in account recovery. If the value is not provided or false, then it will be treated as MFA factor validation.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param is_acc_rec_enabled: The is_acc_rec_enabled of this MyAuthenticationFactorValidator.
        :type: bool
        """
        self._is_acc_rec_enabled = is_acc_rec_enabled

    @property
    def policy_trusted_frequency_mins(self):
        """
        Gets the policy_trusted_frequency_mins of this MyAuthenticationFactorValidator.
        Sign-On Policy dictated validity duration for trusted client in Minutes.

        **SCIM++ Properties:**
         - type: integer
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :return: The policy_trusted_frequency_mins of this MyAuthenticationFactorValidator.
        :rtype: int
        """
        return self._policy_trusted_frequency_mins

    @policy_trusted_frequency_mins.setter
    def policy_trusted_frequency_mins(self, policy_trusted_frequency_mins):
        """
        Sets the policy_trusted_frequency_mins of this MyAuthenticationFactorValidator.
        Sign-On Policy dictated validity duration for trusted client in Minutes.

        **SCIM++ Properties:**
         - type: integer
         - multiValued: false
         - required: false
         - mutability: writeOnly
         - returned: never
         - uniqueness: none


        :param policy_trusted_frequency_mins: The policy_trusted_frequency_mins of this MyAuthenticationFactorValidator.
        :type: int
        """
        self._policy_trusted_frequency_mins = policy_trusted_frequency_mins

    @property
    def third_party_factor(self):
        """
        Gets the third_party_factor of this MyAuthenticationFactorValidator.

        :return: The third_party_factor of this MyAuthenticationFactorValidator.
        :rtype: oci.identity_domains.models.MyAuthenticationFactorValidatorThirdPartyFactor
        """
        return self._third_party_factor

    @third_party_factor.setter
    def third_party_factor(self, third_party_factor):
        """
        Sets the third_party_factor of this MyAuthenticationFactorValidator.

        :param third_party_factor: The third_party_factor of this MyAuthenticationFactorValidator.
        :type: oci.identity_domains.models.MyAuthenticationFactorValidatorThirdPartyFactor
        """
        self._third_party_factor = third_party_factor

    @property
    def additional_attributes(self):
        """
        Gets the additional_attributes of this MyAuthenticationFactorValidator.
        Additional attributes which will be sent as part of a push notification

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The additional_attributes of this MyAuthenticationFactorValidator.
        :rtype: list[oci.identity_domains.models.MyAuthenticationFactorValidatorAdditionalAttributes]
        """
        return self._additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes):
        """
        Sets the additional_attributes of this MyAuthenticationFactorValidator.
        Additional attributes which will be sent as part of a push notification

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param additional_attributes: The additional_attributes of this MyAuthenticationFactorValidator.
        :type: list[oci.identity_domains.models.MyAuthenticationFactorValidatorAdditionalAttributes]
        """
        self._additional_attributes = additional_attributes

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
