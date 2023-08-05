# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Me(object):
    """
    User Account
    """

    #: A constant which can be used with the idcs_prevented_operations property of a Me.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a Me.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a Me.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "Contractor"
    USER_TYPE_CONTRACTOR = "Contractor"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "Employee"
    USER_TYPE_EMPLOYEE = "Employee"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "Intern"
    USER_TYPE_INTERN = "Intern"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "Temp"
    USER_TYPE_TEMP = "Temp"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "External"
    USER_TYPE_EXTERNAL = "External"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "Service"
    USER_TYPE_SERVICE = "Service"

    #: A constant which can be used with the user_type property of a Me.
    #: This constant has a value of "Generic"
    USER_TYPE_GENERIC = "Generic"

    def __init__(self, **kwargs):
        """
        Initializes a new Me object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Me.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this Me.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this Me.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this Me.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this Me.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this Me.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this Me.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this Me.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this Me.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this Me.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this Me.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this Me.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this Me.
        :type tenancy_ocid: str

        :param external_id:
            The value to assign to the external_id property of this Me.
        :type external_id: str

        :param user_name:
            The value to assign to the user_name property of this Me.
        :type user_name: str

        :param description:
            The value to assign to the description property of this Me.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this Me.
        :type display_name: str

        :param nick_name:
            The value to assign to the nick_name property of this Me.
        :type nick_name: str

        :param profile_url:
            The value to assign to the profile_url property of this Me.
        :type profile_url: str

        :param title:
            The value to assign to the title property of this Me.
        :type title: str

        :param user_type:
            The value to assign to the user_type property of this Me.
            Allowed values for this property are: "Contractor", "Employee", "Intern", "Temp", "External", "Service", "Generic", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type user_type: str

        :param locale:
            The value to assign to the locale property of this Me.
        :type locale: str

        :param preferred_language:
            The value to assign to the preferred_language property of this Me.
        :type preferred_language: str

        :param timezone:
            The value to assign to the timezone property of this Me.
        :type timezone: str

        :param active:
            The value to assign to the active property of this Me.
        :type active: bool

        :param password:
            The value to assign to the password property of this Me.
        :type password: str

        :param name:
            The value to assign to the name property of this Me.
        :type name: oci.identity_domains.models.MeName

        :param emails:
            The value to assign to the emails property of this Me.
        :type emails: list[oci.identity_domains.models.MeEmails]

        :param phone_numbers:
            The value to assign to the phone_numbers property of this Me.
        :type phone_numbers: list[oci.identity_domains.models.MePhoneNumbers]

        :param ims:
            The value to assign to the ims property of this Me.
        :type ims: list[oci.identity_domains.models.MeIms]

        :param photos:
            The value to assign to the photos property of this Me.
        :type photos: list[oci.identity_domains.models.MePhotos]

        :param addresses:
            The value to assign to the addresses property of this Me.
        :type addresses: list[oci.identity_domains.models.Addresses]

        :param groups:
            The value to assign to the groups property of this Me.
        :type groups: list[oci.identity_domains.models.MeGroups]

        :param entitlements:
            The value to assign to the entitlements property of this Me.
        :type entitlements: list[oci.identity_domains.models.MeEntitlements]

        :param roles:
            The value to assign to the roles property of this Me.
        :type roles: list[oci.identity_domains.models.MeRoles]

        :param x509_certificates:
            The value to assign to the x509_certificates property of this Me.
        :type x509_certificates: list[oci.identity_domains.models.MeX509Certificates]

        :param urn_ietf_params_scim_schemas_extension_enterprise2_0_user:
            The value to assign to the urn_ietf_params_scim_schemas_extension_enterprise2_0_user property of this Me.
        :type urn_ietf_params_scim_schemas_extension_enterprise2_0_user: oci.identity_domains.models.ExtensionEnterprise20User

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user: oci.identity_domains.models.ExtensionUserUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user: oci.identity_domains.models.ExtensionPasswordStateUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user: oci.identity_domains.models.ExtensionUserStateUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user: oci.identity_domains.models.ExtensionMeUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user: oci.identity_domains.models.ExtensionPosixUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user: oci.identity_domains.models.ExtensionMfaUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user: oci.identity_domains.models.ExtensionSecurityQuestionsUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user: oci.identity_domains.models.ExtensionSelfRegistrationUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user: oci.identity_domains.models.ExtensionTermsOfUseUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags: oci.identity_domains.models.ExtensionOCITags

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user: oci.identity_domains.models.ExtensionUserCredentialsUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user: oci.identity_domains.models.ExtensionCapabilitiesUser

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user property of this Me.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user: oci.identity_domains.models.ExtensionDbCredentialsUser

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
            'external_id': 'str',
            'user_name': 'str',
            'description': 'str',
            'display_name': 'str',
            'nick_name': 'str',
            'profile_url': 'str',
            'title': 'str',
            'user_type': 'str',
            'locale': 'str',
            'preferred_language': 'str',
            'timezone': 'str',
            'active': 'bool',
            'password': 'str',
            'name': 'MeName',
            'emails': 'list[MeEmails]',
            'phone_numbers': 'list[MePhoneNumbers]',
            'ims': 'list[MeIms]',
            'photos': 'list[MePhotos]',
            'addresses': 'list[Addresses]',
            'groups': 'list[MeGroups]',
            'entitlements': 'list[MeEntitlements]',
            'roles': 'list[MeRoles]',
            'x509_certificates': 'list[MeX509Certificates]',
            'urn_ietf_params_scim_schemas_extension_enterprise2_0_user': 'ExtensionEnterprise20User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user': 'ExtensionUserUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user': 'ExtensionPasswordStateUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user': 'ExtensionUserStateUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user': 'ExtensionMeUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user': 'ExtensionPosixUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user': 'ExtensionMfaUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user': 'ExtensionSecurityQuestionsUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user': 'ExtensionSelfRegistrationUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user': 'ExtensionTermsOfUseUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags': 'ExtensionOCITags',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user': 'ExtensionUserCredentialsUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user': 'ExtensionCapabilitiesUser',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user': 'ExtensionDbCredentialsUser'
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
            'external_id': 'externalId',
            'user_name': 'userName',
            'description': 'description',
            'display_name': 'displayName',
            'nick_name': 'nickName',
            'profile_url': 'profileUrl',
            'title': 'title',
            'user_type': 'userType',
            'locale': 'locale',
            'preferred_language': 'preferredLanguage',
            'timezone': 'timezone',
            'active': 'active',
            'password': 'password',
            'name': 'name',
            'emails': 'emails',
            'phone_numbers': 'phoneNumbers',
            'ims': 'ims',
            'photos': 'photos',
            'addresses': 'addresses',
            'groups': 'groups',
            'entitlements': 'entitlements',
            'roles': 'roles',
            'x509_certificates': 'x509Certificates',
            'urn_ietf_params_scim_schemas_extension_enterprise2_0_user': 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:user:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:passwordState:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:userState:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:me:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:posix:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:mfa:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:securityQuestions:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:selfRegistration:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:termsOfUse:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:OCITags',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:userCredentials:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:capabilities:User',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:dbCredentials:User'
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
        self._external_id = None
        self._user_name = None
        self._description = None
        self._display_name = None
        self._nick_name = None
        self._profile_url = None
        self._title = None
        self._user_type = None
        self._locale = None
        self._preferred_language = None
        self._timezone = None
        self._active = None
        self._password = None
        self._name = None
        self._emails = None
        self._phone_numbers = None
        self._ims = None
        self._photos = None
        self._addresses = None
        self._groups = None
        self._entitlements = None
        self._roles = None
        self._x509_certificates = None
        self._urn_ietf_params_scim_schemas_extension_enterprise2_0_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user = None

    @property
    def id(self):
        """
        Gets the id of this Me.
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


        :return: The id of this Me.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Me.
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


        :param id: The id of this Me.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this Me.
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


        :return: The ocid of this Me.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this Me.
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


        :param ocid: The ocid of this Me.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this Me.
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


        :return: The schemas of this Me.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this Me.
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


        :param schemas: The schemas of this Me.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this Me.

        :return: The meta of this Me.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this Me.

        :param meta: The meta of this Me.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this Me.

        :return: The idcs_created_by of this Me.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this Me.

        :param idcs_created_by: The idcs_created_by of this Me.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this Me.

        :return: The idcs_last_modified_by of this Me.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this Me.

        :param idcs_last_modified_by: The idcs_last_modified_by of this Me.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this Me.
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


        :return: The idcs_prevented_operations of this Me.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this Me.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this Me.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this Me.
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


        :return: The tags of this Me.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this Me.
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


        :param tags: The tags of this Me.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this Me.
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


        :return: The delete_in_progress of this Me.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this Me.
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


        :param delete_in_progress: The delete_in_progress of this Me.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this Me.
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


        :return: The idcs_last_upgraded_in_release of this Me.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this Me.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this Me.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this Me.
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


        :return: The domain_ocid of this Me.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this Me.
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


        :param domain_ocid: The domain_ocid of this Me.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this Me.
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


        :return: The compartment_ocid of this Me.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this Me.
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


        :param compartment_ocid: The compartment_ocid of this Me.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this Me.
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


        :return: The tenancy_ocid of this Me.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this Me.
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


        :param tenancy_ocid: The tenancy_ocid of this Me.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def external_id(self):
        """
        Gets the external_id of this Me.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued by the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeNameMappings: [[columnHeaderName:External Id]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The external_id of this Me.
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """
        Sets the external_id of this Me.
        An identifier for the Resource as defined by the Service Consumer. The externalId may simplify identification of the Resource between Service Consumer and Service Provider by allowing the Consumer to refer to the Resource with its own identifier, obviating the need to store a local mapping between the local identifier of the Resource and the identifier used by the Service Provider. Each Resource MAY include a non-empty externalId value. The value of the externalId attribute is always issued by the Service Consumer and can never be specified by the Service Provider. The Service Provider MUST always interpret the externalId as scoped to the Service Consumer's tenant.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeNameMappings: [[columnHeaderName:External Id]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param external_id: The external_id of this Me.
        :type: str
        """
        self._external_id = external_id

    @property
    def user_name(self):
        """
        **[Required]** Gets the user_name of this Me.
        User name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: User ID
         - idcsCsvAttributeNameMappings: [[columnHeaderName:User Name, deprecatedColumnHeaderName:User ID]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: global


        :return: The user_name of this Me.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this Me.
        User name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: User ID
         - idcsCsvAttributeNameMappings: [[columnHeaderName:User Name, deprecatedColumnHeaderName:User ID]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: always
         - type: string
         - uniqueness: global


        :param user_name: The user_name of this Me.
        :type: str
        """
        self._user_name = user_name

    @property
    def description(self):
        """
        Gets the description of this Me.
        Description of the user

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsPii: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The description of this Me.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Me.
        Description of the user

        **Added In:** 2012271618

        **SCIM++ Properties:**
         - caseExact: false
         - idcsPii: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param description: The description of this Me.
        :type: str
        """
        self._description = description

    @property
    def display_name(self):
        """
        Gets the display_name of this Me.
        Display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Display Name
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Display Name]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display_name of this Me.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this Me.
        Display name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Display Name
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Display Name]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display_name: The display_name of this Me.
        :type: str
        """
        self._display_name = display_name

    @property
    def nick_name(self):
        """
        Gets the nick_name of this Me.
        Nick name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Nick Name
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Nick Name]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The nick_name of this Me.
        :rtype: str
        """
        return self._nick_name

    @nick_name.setter
    def nick_name(self, nick_name):
        """
        Sets the nick_name of this Me.
        Nick name

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Nick Name
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Nick Name]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param nick_name: The nick_name of this Me.
        :type: str
        """
        self._nick_name = nick_name

    @property
    def profile_url(self):
        """
        Gets the profile_url of this Me.
        A fully-qualified URL to a page representing the User's online profile

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Profile URL
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Profile Url]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The profile_url of this Me.
        :rtype: str
        """
        return self._profile_url

    @profile_url.setter
    def profile_url(self, profile_url):
        """
        Sets the profile_url of this Me.
        A fully-qualified URL to a page representing the User's online profile

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Profile URL
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Profile Url]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param profile_url: The profile_url of this Me.
        :type: str
        """
        self._profile_url = profile_url

    @property
    def title(self):
        """
        Gets the title of this Me.
        Title

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Title
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Title]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The title of this Me.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this Me.
        Title

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Title
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Title]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param title: The title of this Me.
        :type: str
        """
        self._title = title

    @property
    def user_type(self):
        """
        Gets the user_type of this Me.
        Used to identify the organization-to-user relationship

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: User Type
         - idcsCsvAttributeNameMappings: [[columnHeaderName:User Type]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "Contractor", "Employee", "Intern", "Temp", "External", "Service", "Generic", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The user_type of this Me.
        :rtype: str
        """
        return self._user_type

    @user_type.setter
    def user_type(self, user_type):
        """
        Sets the user_type of this Me.
        Used to identify the organization-to-user relationship

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: User Type
         - idcsCsvAttributeNameMappings: [[columnHeaderName:User Type]]
         - idcsPii: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param user_type: The user_type of this Me.
        :type: str
        """
        allowed_values = ["Contractor", "Employee", "Intern", "Temp", "External", "Service", "Generic"]
        if not value_allowed_none_or_none_sentinel(user_type, allowed_values):
            user_type = 'UNKNOWN_ENUM_VALUE'
        self._user_type = user_type

    @property
    def locale(self):
        """
        Gets the locale of this Me.
        Used to indicate the User's default location for purposes of localizing items such as currency, date and time format, numerical representations, and so on.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Locale
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Locale]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The locale of this Me.
        :rtype: str
        """
        return self._locale

    @locale.setter
    def locale(self, locale):
        """
        Sets the locale of this Me.
        Used to indicate the User's default location for purposes of localizing items such as currency, date and time format, numerical representations, and so on.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Locale
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Locale]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param locale: The locale of this Me.
        :type: str
        """
        self._locale = locale

    @property
    def preferred_language(self):
        """
        Gets the preferred_language of this Me.
        User's preferred written or spoken language used for localized user interfaces

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Preferred Language
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Preferred Language]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The preferred_language of this Me.
        :rtype: str
        """
        return self._preferred_language

    @preferred_language.setter
    def preferred_language(self, preferred_language):
        """
        Sets the preferred_language of this Me.
        User's preferred written or spoken language used for localized user interfaces

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Preferred Language
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Preferred Language]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param preferred_language: The preferred_language of this Me.
        :type: str
        """
        self._preferred_language = preferred_language

    @property
    def timezone(self):
        """
        Gets the timezone of this Me.
        User's timezone

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCanonicalValueSourceFilter: attrName eq \"timezones\" and attrValues.value eq \"$(timezone)\"
         - idcsCanonicalValueSourceResourceType: AllowedValue
         - idcsCsvAttributeName: TimeZone
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Time Zone, deprecatedColumnHeaderName:TimeZone]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The timezone of this Me.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this Me.
        User's timezone

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCanonicalValueSourceFilter: attrName eq \"timezones\" and attrValues.value eq \"$(timezone)\"
         - idcsCanonicalValueSourceResourceType: AllowedValue
         - idcsCsvAttributeName: TimeZone
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Time Zone, deprecatedColumnHeaderName:TimeZone]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param timezone: The timezone of this Me.
        :type: str
        """
        self._timezone = timezone

    @property
    def active(self):
        """
        Gets the active of this Me.
        User status

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Active
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Active]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The active of this Me.
        :rtype: bool
        """
        return self._active

    @active.setter
    def active(self, active):
        """
        Sets the active of this Me.
        User status

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Active
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Active]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param active: The active of this Me.
        :type: bool
        """
        self._active = active

    @property
    def password(self):
        """
        Gets the password of this Me.
        Password attribute. Max length for password is controlled via Password Policy.

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Password
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Password]]
         - idcsPii: true
         - idcsSearchable: false
         - idcsSensitive: hash
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: string
         - uniqueness: none


        :return: The password of this Me.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this Me.
        Password attribute. Max length for password is controlled via Password Policy.

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Password
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Password]]
         - idcsPii: true
         - idcsSearchable: false
         - idcsSensitive: hash
         - multiValued: false
         - mutability: writeOnly
         - required: false
         - returned: never
         - type: string
         - uniqueness: none


        :param password: The password of this Me.
        :type: str
        """
        self._password = password

    @property
    def name(self):
        """
        **[Required]** Gets the name of this Me.

        :return: The name of this Me.
        :rtype: oci.identity_domains.models.MeName
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Me.

        :param name: The name of this Me.
        :type: oci.identity_domains.models.MeName
        """
        self._name = name

    @property
    def emails(self):
        """
        Gets the emails of this Me.
        A complex attribute representing emails

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Work Email, mapsTo:emails[work].value], [columnHeaderName:Home Email, mapsTo:emails[home].value], [columnHeaderName:Primary Email Type, mapsTo:emails[$(type)].primary], [columnHeaderName:Other Email, mapsTo:emails[other].value], [columnHeaderName:Recovery Email, mapsTo:emails[recovery].value], [columnHeaderName:Work Email Verified, mapsTo:emails[work].verified], [columnHeaderName:Home Email Verified, mapsTo:emails[home].verified], [columnHeaderName:Other Email Verified, mapsTo:emails[other].verified], [columnHeaderName:Recovery Email Verified, mapsTo:emails[recovery].verified]]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The emails of this Me.
        :rtype: list[oci.identity_domains.models.MeEmails]
        """
        return self._emails

    @emails.setter
    def emails(self, emails):
        """
        Sets the emails of this Me.
        A complex attribute representing emails

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Work Email, mapsTo:emails[work].value], [columnHeaderName:Home Email, mapsTo:emails[home].value], [columnHeaderName:Primary Email Type, mapsTo:emails[$(type)].primary], [columnHeaderName:Other Email, mapsTo:emails[other].value], [columnHeaderName:Recovery Email, mapsTo:emails[recovery].value], [columnHeaderName:Work Email Verified, mapsTo:emails[work].verified], [columnHeaderName:Home Email Verified, mapsTo:emails[home].verified], [columnHeaderName:Other Email Verified, mapsTo:emails[other].verified], [columnHeaderName:Recovery Email Verified, mapsTo:emails[recovery].verified]]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param emails: The emails of this Me.
        :type: list[oci.identity_domains.models.MeEmails]
        """
        self._emails = emails

    @property
    def phone_numbers(self):
        """
        Gets the phone_numbers of this Me.
        Phone numbers

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Work Phone, mapsTo:phoneNumbers[work].value], [columnHeaderName:Mobile No, mapsTo:phoneNumbers[mobile].value], [columnHeaderName:Home Phone, mapsTo:phoneNumbers[home].value], [columnHeaderName:Fax, mapsTo:phoneNumbers[fax].value], [columnHeaderName:Pager, mapsTo:phoneNumbers[pager].value], [columnHeaderName:Other Phone, mapsTo:phoneNumbers[other].value], [columnHeaderName:Recovery Phone, mapsTo:phoneNumbers[recovery].value], [columnHeaderName:Primary Phone Type, mapsTo:phoneNumbers[$(type)].primary]]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The phone_numbers of this Me.
        :rtype: list[oci.identity_domains.models.MePhoneNumbers]
        """
        return self._phone_numbers

    @phone_numbers.setter
    def phone_numbers(self, phone_numbers):
        """
        Sets the phone_numbers of this Me.
        Phone numbers

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Work Phone, mapsTo:phoneNumbers[work].value], [columnHeaderName:Mobile No, mapsTo:phoneNumbers[mobile].value], [columnHeaderName:Home Phone, mapsTo:phoneNumbers[home].value], [columnHeaderName:Fax, mapsTo:phoneNumbers[fax].value], [columnHeaderName:Pager, mapsTo:phoneNumbers[pager].value], [columnHeaderName:Other Phone, mapsTo:phoneNumbers[other].value], [columnHeaderName:Recovery Phone, mapsTo:phoneNumbers[recovery].value], [columnHeaderName:Primary Phone Type, mapsTo:phoneNumbers[$(type)].primary]]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param phone_numbers: The phone_numbers of this Me.
        :type: list[oci.identity_domains.models.MePhoneNumbers]
        """
        self._phone_numbers = phone_numbers

    @property
    def ims(self):
        """
        Gets the ims of this Me.
        User's instant messaging addresses

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The ims of this Me.
        :rtype: list[oci.identity_domains.models.MeIms]
        """
        return self._ims

    @ims.setter
    def ims(self, ims):
        """
        Sets the ims of this Me.
        User's instant messaging addresses

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param ims: The ims of this Me.
        :type: list[oci.identity_domains.models.MeIms]
        """
        self._ims = ims

    @property
    def photos(self):
        """
        Gets the photos of this Me.
        URLs of photos for the User

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The photos of this Me.
        :rtype: list[oci.identity_domains.models.MePhotos]
        """
        return self._photos

    @photos.setter
    def photos(self, photos):
        """
        Sets the photos of this Me.
        URLs of photos for the User

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param photos: The photos of this Me.
        :type: list[oci.identity_domains.models.MePhotos]
        """
        self._photos = photos

    @property
    def addresses(self):
        """
        Gets the addresses of this Me.
        A physical mailing address for this User, as described in (address Element). Canonical Type Values of work, home, and other. The value attribute is a complex type with the following sub-attributes.

        **SCIM++ Properties:**
         - idcsCompositeKey: [type]
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Work Address Street, deprecatedColumnHeaderName:Work Street Address, mapsTo:addresses[work].streetAddress], [columnHeaderName:Work Address Locality, deprecatedColumnHeaderName:Work City, mapsTo:addresses[work].locality], [columnHeaderName:Work Address Region, deprecatedColumnHeaderName:Work State, mapsTo:addresses[work].region], [columnHeaderName:Work Address Postal Code, deprecatedColumnHeaderName:Work Postal Code, mapsTo:addresses[work].postalCode], [columnHeaderName:Work Address Country, deprecatedColumnHeaderName:Work Country, mapsTo:addresses[work].country], [columnHeaderName:Work Address Formatted, mapsTo:addresses[work].formatted], [columnHeaderName:Home Address Formatted, mapsTo:addresses[home].formatted], [columnHeaderName:Other Address Formatted, mapsTo:addresses[other].formatted], [columnHeaderName:Home Address Street, mapsTo:addresses[home].streetAddress], [columnHeaderName:Other Address Street, mapsTo:addresses[other].streetAddress], [columnHeaderName:Home Address Locality, mapsTo:addresses[home].locality], [columnHeaderName:Other Address Locality, mapsTo:addresses[other].locality], [columnHeaderName:Home Address Region, mapsTo:addresses[home].region], [columnHeaderName:Other Address Region, mapsTo:addresses[other].region], [columnHeaderName:Home Address Country, mapsTo:addresses[home].country], [columnHeaderName:Other Address Country, mapsTo:addresses[other].country], [columnHeaderName:Home Address Postal Code, mapsTo:addresses[home].postalCode], [columnHeaderName:Other Address Postal Code, mapsTo:addresses[other].postalCode], [columnHeaderName:Primary Address Type, mapsTo:addresses[$(type)].primary]]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The addresses of this Me.
        :rtype: list[oci.identity_domains.models.Addresses]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """
        Sets the addresses of this Me.
        A physical mailing address for this User, as described in (address Element). Canonical Type Values of work, home, and other. The value attribute is a complex type with the following sub-attributes.

        **SCIM++ Properties:**
         - idcsCompositeKey: [type]
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Work Address Street, deprecatedColumnHeaderName:Work Street Address, mapsTo:addresses[work].streetAddress], [columnHeaderName:Work Address Locality, deprecatedColumnHeaderName:Work City, mapsTo:addresses[work].locality], [columnHeaderName:Work Address Region, deprecatedColumnHeaderName:Work State, mapsTo:addresses[work].region], [columnHeaderName:Work Address Postal Code, deprecatedColumnHeaderName:Work Postal Code, mapsTo:addresses[work].postalCode], [columnHeaderName:Work Address Country, deprecatedColumnHeaderName:Work Country, mapsTo:addresses[work].country], [columnHeaderName:Work Address Formatted, mapsTo:addresses[work].formatted], [columnHeaderName:Home Address Formatted, mapsTo:addresses[home].formatted], [columnHeaderName:Other Address Formatted, mapsTo:addresses[other].formatted], [columnHeaderName:Home Address Street, mapsTo:addresses[home].streetAddress], [columnHeaderName:Other Address Street, mapsTo:addresses[other].streetAddress], [columnHeaderName:Home Address Locality, mapsTo:addresses[home].locality], [columnHeaderName:Other Address Locality, mapsTo:addresses[other].locality], [columnHeaderName:Home Address Region, mapsTo:addresses[home].region], [columnHeaderName:Other Address Region, mapsTo:addresses[other].region], [columnHeaderName:Home Address Country, mapsTo:addresses[home].country], [columnHeaderName:Other Address Country, mapsTo:addresses[other].country], [columnHeaderName:Home Address Postal Code, mapsTo:addresses[home].postalCode], [columnHeaderName:Other Address Postal Code, mapsTo:addresses[other].postalCode], [columnHeaderName:Primary Address Type, mapsTo:addresses[$(type)].primary]]
         - idcsPii: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param addresses: The addresses of this Me.
        :type: list[oci.identity_domains.models.Addresses]
        """
        self._addresses = addresses

    @property
    def groups(self):
        """
        Gets the groups of this Me.
        A list of groups that the user belongs to, either thorough direct membership, nested groups, or dynamically calculated

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The groups of this Me.
        :rtype: list[oci.identity_domains.models.MeGroups]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """
        Sets the groups of this Me.
        A list of groups that the user belongs to, either thorough direct membership, nested groups, or dynamically calculated

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param groups: The groups of this Me.
        :type: list[oci.identity_domains.models.MeGroups]
        """
        self._groups = groups

    @property
    def entitlements(self):
        """
        Gets the entitlements of this Me.
        A list of entitlements for the User that represent a thing the User has.

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The entitlements of this Me.
        :rtype: list[oci.identity_domains.models.MeEntitlements]
        """
        return self._entitlements

    @entitlements.setter
    def entitlements(self, entitlements):
        """
        Sets the entitlements of this Me.
        A list of entitlements for the User that represent a thing the User has.

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param entitlements: The entitlements of this Me.
        :type: list[oci.identity_domains.models.MeEntitlements]
        """
        self._entitlements = entitlements

    @property
    def roles(self):
        """
        Gets the roles of this Me.
        A list of roles for the User that collectively represent who the User is; e.g., 'Student', 'Faculty'.

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The roles of this Me.
        :rtype: list[oci.identity_domains.models.MeRoles]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """
        Sets the roles of this Me.
        A list of roles for the User that collectively represent who the User is; e.g., 'Student', 'Faculty'.

        **SCIM++ Properties:**
         - idcsCompositeKey: [value, type]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param roles: The roles of this Me.
        :type: list[oci.identity_domains.models.MeRoles]
        """
        self._roles = roles

    @property
    def x509_certificates(self):
        """
        Gets the x509_certificates of this Me.
        A list of certificates issued to the User.

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :return: The x509_certificates of this Me.
        :rtype: list[oci.identity_domains.models.MeX509Certificates]
        """
        return self._x509_certificates

    @x509_certificates.setter
    def x509_certificates(self, x509_certificates):
        """
        Sets the x509_certificates of this Me.
        A list of certificates issued to the User.

        **SCIM++ Properties:**
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: default
         - type: complex
         - uniqueness: none


        :param x509_certificates: The x509_certificates of this Me.
        :type: list[oci.identity_domains.models.MeX509Certificates]
        """
        self._x509_certificates = x509_certificates

    @property
    def urn_ietf_params_scim_schemas_extension_enterprise2_0_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_extension_enterprise2_0_user of this Me.

        :return: The urn_ietf_params_scim_schemas_extension_enterprise2_0_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionEnterprise20User
        """
        return self._urn_ietf_params_scim_schemas_extension_enterprise2_0_user

    @urn_ietf_params_scim_schemas_extension_enterprise2_0_user.setter
    def urn_ietf_params_scim_schemas_extension_enterprise2_0_user(self, urn_ietf_params_scim_schemas_extension_enterprise2_0_user):
        """
        Sets the urn_ietf_params_scim_schemas_extension_enterprise2_0_user of this Me.

        :param urn_ietf_params_scim_schemas_extension_enterprise2_0_user: The urn_ietf_params_scim_schemas_extension_enterprise2_0_user of this Me.
        :type: oci.identity_domains.models.ExtensionEnterprise20User
        """
        self._urn_ietf_params_scim_schemas_extension_enterprise2_0_user = urn_ietf_params_scim_schemas_extension_enterprise2_0_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionUserUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user of this Me.
        :type: oci.identity_domains.models.ExtensionUserUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_user_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionPasswordStateUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user of this Me.
        :type: oci.identity_domains.models.ExtensionPasswordStateUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_password_state_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionUserStateUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user of this Me.
        :type: oci.identity_domains.models.ExtensionUserStateUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_user_state_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionMeUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user of this Me.
        :type: oci.identity_domains.models.ExtensionMeUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_me_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionPosixUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user of this Me.
        :type: oci.identity_domains.models.ExtensionPosixUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_posix_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionMfaUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user of this Me.
        :type: oci.identity_domains.models.ExtensionMfaUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_mfa_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionSecurityQuestionsUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user of this Me.
        :type: oci.identity_domains.models.ExtensionSecurityQuestionsUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_security_questions_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionSelfRegistrationUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user of this Me.
        :type: oci.identity_domains.models.ExtensionSelfRegistrationUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_self_registration_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionTermsOfUseUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user of this Me.
        :type: oci.identity_domains.models.ExtensionTermsOfUseUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_terms_of_use_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags of this Me.
        :rtype: oci.identity_domains.models.ExtensionOCITags
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags: The urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags of this Me.
        :type: oci.identity_domains.models.ExtensionOCITags
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags = urn_ietf_params_scim_schemas_oracle_idcs_extension_oci_tags

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionUserCredentialsUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user of this Me.
        :type: oci.identity_domains.models.ExtensionUserCredentialsUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_user_credentials_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionCapabilitiesUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user of this Me.
        :type: oci.identity_domains.models.ExtensionCapabilitiesUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_capabilities_user

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user of this Me.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user of this Me.
        :rtype: oci.identity_domains.models.ExtensionDbCredentialsUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user of this Me.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user of this Me.
        :type: oci.identity_domains.models.ExtensionDbCredentialsUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_db_credentials_user

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
