# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserCapabilitiesChanger(object):
    """
    User Capabilities Changer
    """

    #: A constant which can be used with the idcs_prevented_operations property of a UserCapabilitiesChanger.
    #: This constant has a value of "replace"
    IDCS_PREVENTED_OPERATIONS_REPLACE = "replace"

    #: A constant which can be used with the idcs_prevented_operations property of a UserCapabilitiesChanger.
    #: This constant has a value of "update"
    IDCS_PREVENTED_OPERATIONS_UPDATE = "update"

    #: A constant which can be used with the idcs_prevented_operations property of a UserCapabilitiesChanger.
    #: This constant has a value of "delete"
    IDCS_PREVENTED_OPERATIONS_DELETE = "delete"

    def __init__(self, **kwargs):
        """
        Initializes a new UserCapabilitiesChanger object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this UserCapabilitiesChanger.
        :type id: str

        :param ocid:
            The value to assign to the ocid property of this UserCapabilitiesChanger.
        :type ocid: str

        :param schemas:
            The value to assign to the schemas property of this UserCapabilitiesChanger.
        :type schemas: list[str]

        :param meta:
            The value to assign to the meta property of this UserCapabilitiesChanger.
        :type meta: oci.identity_domains.models.Meta

        :param idcs_created_by:
            The value to assign to the idcs_created_by property of this UserCapabilitiesChanger.
        :type idcs_created_by: oci.identity_domains.models.IdcsCreatedBy

        :param idcs_last_modified_by:
            The value to assign to the idcs_last_modified_by property of this UserCapabilitiesChanger.
        :type idcs_last_modified_by: oci.identity_domains.models.IdcsLastModifiedBy

        :param idcs_prevented_operations:
            The value to assign to the idcs_prevented_operations property of this UserCapabilitiesChanger.
            Allowed values for items in this list are: "replace", "update", "delete", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type idcs_prevented_operations: list[str]

        :param tags:
            The value to assign to the tags property of this UserCapabilitiesChanger.
        :type tags: list[oci.identity_domains.models.Tags]

        :param delete_in_progress:
            The value to assign to the delete_in_progress property of this UserCapabilitiesChanger.
        :type delete_in_progress: bool

        :param idcs_last_upgraded_in_release:
            The value to assign to the idcs_last_upgraded_in_release property of this UserCapabilitiesChanger.
        :type idcs_last_upgraded_in_release: str

        :param domain_ocid:
            The value to assign to the domain_ocid property of this UserCapabilitiesChanger.
        :type domain_ocid: str

        :param compartment_ocid:
            The value to assign to the compartment_ocid property of this UserCapabilitiesChanger.
        :type compartment_ocid: str

        :param tenancy_ocid:
            The value to assign to the tenancy_ocid property of this UserCapabilitiesChanger.
        :type tenancy_ocid: str

        :param can_use_api_keys:
            The value to assign to the can_use_api_keys property of this UserCapabilitiesChanger.
        :type can_use_api_keys: bool

        :param can_use_auth_tokens:
            The value to assign to the can_use_auth_tokens property of this UserCapabilitiesChanger.
        :type can_use_auth_tokens: bool

        :param can_use_console_password:
            The value to assign to the can_use_console_password property of this UserCapabilitiesChanger.
        :type can_use_console_password: bool

        :param can_use_customer_secret_keys:
            The value to assign to the can_use_customer_secret_keys property of this UserCapabilitiesChanger.
        :type can_use_customer_secret_keys: bool

        :param can_use_o_auth2_client_credentials:
            The value to assign to the can_use_o_auth2_client_credentials property of this UserCapabilitiesChanger.
        :type can_use_o_auth2_client_credentials: bool

        :param can_use_smtp_credentials:
            The value to assign to the can_use_smtp_credentials property of this UserCapabilitiesChanger.
        :type can_use_smtp_credentials: bool

        :param can_use_db_credentials:
            The value to assign to the can_use_db_credentials property of this UserCapabilitiesChanger.
        :type can_use_db_credentials: bool

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user:
            The value to assign to the urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user property of this UserCapabilitiesChanger.
        :type urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user: oci.identity_domains.models.ExtensionSelfChangeUser

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
            'can_use_api_keys': 'bool',
            'can_use_auth_tokens': 'bool',
            'can_use_console_password': 'bool',
            'can_use_customer_secret_keys': 'bool',
            'can_use_o_auth2_client_credentials': 'bool',
            'can_use_smtp_credentials': 'bool',
            'can_use_db_credentials': 'bool',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user': 'ExtensionSelfChangeUser'
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
            'can_use_api_keys': 'canUseApiKeys',
            'can_use_auth_tokens': 'canUseAuthTokens',
            'can_use_console_password': 'canUseConsolePassword',
            'can_use_customer_secret_keys': 'canUseCustomerSecretKeys',
            'can_use_o_auth2_client_credentials': 'canUseOAuth2ClientCredentials',
            'can_use_smtp_credentials': 'canUseSmtpCredentials',
            'can_use_db_credentials': 'canUseDbCredentials',
            'urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user': 'urn:ietf:params:scim:schemas:oracle:idcs:extension:selfChange:User'
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
        self._can_use_api_keys = None
        self._can_use_auth_tokens = None
        self._can_use_console_password = None
        self._can_use_customer_secret_keys = None
        self._can_use_o_auth2_client_credentials = None
        self._can_use_smtp_credentials = None
        self._can_use_db_credentials = None
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user = None

    @property
    def id(self):
        """
        Gets the id of this UserCapabilitiesChanger.
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


        :return: The id of this UserCapabilitiesChanger.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UserCapabilitiesChanger.
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


        :param id: The id of this UserCapabilitiesChanger.
        :type: str
        """
        self._id = id

    @property
    def ocid(self):
        """
        Gets the ocid of this UserCapabilitiesChanger.
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


        :return: The ocid of this UserCapabilitiesChanger.
        :rtype: str
        """
        return self._ocid

    @ocid.setter
    def ocid(self, ocid):
        """
        Sets the ocid of this UserCapabilitiesChanger.
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


        :param ocid: The ocid of this UserCapabilitiesChanger.
        :type: str
        """
        self._ocid = ocid

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this UserCapabilitiesChanger.
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


        :return: The schemas of this UserCapabilitiesChanger.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this UserCapabilitiesChanger.
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


        :param schemas: The schemas of this UserCapabilitiesChanger.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def meta(self):
        """
        Gets the meta of this UserCapabilitiesChanger.

        :return: The meta of this UserCapabilitiesChanger.
        :rtype: oci.identity_domains.models.Meta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """
        Sets the meta of this UserCapabilitiesChanger.

        :param meta: The meta of this UserCapabilitiesChanger.
        :type: oci.identity_domains.models.Meta
        """
        self._meta = meta

    @property
    def idcs_created_by(self):
        """
        Gets the idcs_created_by of this UserCapabilitiesChanger.

        :return: The idcs_created_by of this UserCapabilitiesChanger.
        :rtype: oci.identity_domains.models.IdcsCreatedBy
        """
        return self._idcs_created_by

    @idcs_created_by.setter
    def idcs_created_by(self, idcs_created_by):
        """
        Sets the idcs_created_by of this UserCapabilitiesChanger.

        :param idcs_created_by: The idcs_created_by of this UserCapabilitiesChanger.
        :type: oci.identity_domains.models.IdcsCreatedBy
        """
        self._idcs_created_by = idcs_created_by

    @property
    def idcs_last_modified_by(self):
        """
        Gets the idcs_last_modified_by of this UserCapabilitiesChanger.

        :return: The idcs_last_modified_by of this UserCapabilitiesChanger.
        :rtype: oci.identity_domains.models.IdcsLastModifiedBy
        """
        return self._idcs_last_modified_by

    @idcs_last_modified_by.setter
    def idcs_last_modified_by(self, idcs_last_modified_by):
        """
        Sets the idcs_last_modified_by of this UserCapabilitiesChanger.

        :param idcs_last_modified_by: The idcs_last_modified_by of this UserCapabilitiesChanger.
        :type: oci.identity_domains.models.IdcsLastModifiedBy
        """
        self._idcs_last_modified_by = idcs_last_modified_by

    @property
    def idcs_prevented_operations(self):
        """
        Gets the idcs_prevented_operations of this UserCapabilitiesChanger.
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


        :return: The idcs_prevented_operations of this UserCapabilitiesChanger.
        :rtype: list[str]
        """
        return self._idcs_prevented_operations

    @idcs_prevented_operations.setter
    def idcs_prevented_operations(self, idcs_prevented_operations):
        """
        Sets the idcs_prevented_operations of this UserCapabilitiesChanger.
        Each value of this attribute specifies an operation that only an internal client may perform on this particular resource.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param idcs_prevented_operations: The idcs_prevented_operations of this UserCapabilitiesChanger.
        :type: list[str]
        """
        allowed_values = ["replace", "update", "delete"]
        if idcs_prevented_operations:
            idcs_prevented_operations[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in idcs_prevented_operations]
        self._idcs_prevented_operations = idcs_prevented_operations

    @property
    def tags(self):
        """
        Gets the tags of this UserCapabilitiesChanger.
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


        :return: The tags of this UserCapabilitiesChanger.
        :rtype: list[oci.identity_domains.models.Tags]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this UserCapabilitiesChanger.
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


        :param tags: The tags of this UserCapabilitiesChanger.
        :type: list[oci.identity_domains.models.Tags]
        """
        self._tags = tags

    @property
    def delete_in_progress(self):
        """
        Gets the delete_in_progress of this UserCapabilitiesChanger.
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


        :return: The delete_in_progress of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._delete_in_progress

    @delete_in_progress.setter
    def delete_in_progress(self, delete_in_progress):
        """
        Sets the delete_in_progress of this UserCapabilitiesChanger.
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


        :param delete_in_progress: The delete_in_progress of this UserCapabilitiesChanger.
        :type: bool
        """
        self._delete_in_progress = delete_in_progress

    @property
    def idcs_last_upgraded_in_release(self):
        """
        Gets the idcs_last_upgraded_in_release of this UserCapabilitiesChanger.
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


        :return: The idcs_last_upgraded_in_release of this UserCapabilitiesChanger.
        :rtype: str
        """
        return self._idcs_last_upgraded_in_release

    @idcs_last_upgraded_in_release.setter
    def idcs_last_upgraded_in_release(self, idcs_last_upgraded_in_release):
        """
        Sets the idcs_last_upgraded_in_release of this UserCapabilitiesChanger.
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


        :param idcs_last_upgraded_in_release: The idcs_last_upgraded_in_release of this UserCapabilitiesChanger.
        :type: str
        """
        self._idcs_last_upgraded_in_release = idcs_last_upgraded_in_release

    @property
    def domain_ocid(self):
        """
        Gets the domain_ocid of this UserCapabilitiesChanger.
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


        :return: The domain_ocid of this UserCapabilitiesChanger.
        :rtype: str
        """
        return self._domain_ocid

    @domain_ocid.setter
    def domain_ocid(self, domain_ocid):
        """
        Sets the domain_ocid of this UserCapabilitiesChanger.
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


        :param domain_ocid: The domain_ocid of this UserCapabilitiesChanger.
        :type: str
        """
        self._domain_ocid = domain_ocid

    @property
    def compartment_ocid(self):
        """
        Gets the compartment_ocid of this UserCapabilitiesChanger.
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


        :return: The compartment_ocid of this UserCapabilitiesChanger.
        :rtype: str
        """
        return self._compartment_ocid

    @compartment_ocid.setter
    def compartment_ocid(self, compartment_ocid):
        """
        Sets the compartment_ocid of this UserCapabilitiesChanger.
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


        :param compartment_ocid: The compartment_ocid of this UserCapabilitiesChanger.
        :type: str
        """
        self._compartment_ocid = compartment_ocid

    @property
    def tenancy_ocid(self):
        """
        Gets the tenancy_ocid of this UserCapabilitiesChanger.
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


        :return: The tenancy_ocid of this UserCapabilitiesChanger.
        :rtype: str
        """
        return self._tenancy_ocid

    @tenancy_ocid.setter
    def tenancy_ocid(self, tenancy_ocid):
        """
        Sets the tenancy_ocid of this UserCapabilitiesChanger.
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


        :param tenancy_ocid: The tenancy_ocid of this UserCapabilitiesChanger.
        :type: str
        """
        self._tenancy_ocid = tenancy_ocid

    @property
    def can_use_api_keys(self):
        """
        Gets the can_use_api_keys of this UserCapabilitiesChanger.
        Indicates weather a user can use api keys

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_api_keys of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_api_keys

    @can_use_api_keys.setter
    def can_use_api_keys(self, can_use_api_keys):
        """
        Sets the can_use_api_keys of this UserCapabilitiesChanger.
        Indicates weather a user can use api keys

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_api_keys: The can_use_api_keys of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_api_keys = can_use_api_keys

    @property
    def can_use_auth_tokens(self):
        """
        Gets the can_use_auth_tokens of this UserCapabilitiesChanger.
        Indicates weather a user can use auth tokens

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_auth_tokens of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_auth_tokens

    @can_use_auth_tokens.setter
    def can_use_auth_tokens(self, can_use_auth_tokens):
        """
        Sets the can_use_auth_tokens of this UserCapabilitiesChanger.
        Indicates weather a user can use auth tokens

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_auth_tokens: The can_use_auth_tokens of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_auth_tokens = can_use_auth_tokens

    @property
    def can_use_console_password(self):
        """
        Gets the can_use_console_password of this UserCapabilitiesChanger.
        Indicates weather a user can use console password

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_console_password of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_console_password

    @can_use_console_password.setter
    def can_use_console_password(self, can_use_console_password):
        """
        Sets the can_use_console_password of this UserCapabilitiesChanger.
        Indicates weather a user can use console password

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_console_password: The can_use_console_password of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_console_password = can_use_console_password

    @property
    def can_use_customer_secret_keys(self):
        """
        Gets the can_use_customer_secret_keys of this UserCapabilitiesChanger.
        Indicates weather a user can use customer secret keys

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_customer_secret_keys of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_customer_secret_keys

    @can_use_customer_secret_keys.setter
    def can_use_customer_secret_keys(self, can_use_customer_secret_keys):
        """
        Sets the can_use_customer_secret_keys of this UserCapabilitiesChanger.
        Indicates weather a user can use customer secret keys

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_customer_secret_keys: The can_use_customer_secret_keys of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_customer_secret_keys = can_use_customer_secret_keys

    @property
    def can_use_o_auth2_client_credentials(self):
        """
        Gets the can_use_o_auth2_client_credentials of this UserCapabilitiesChanger.
        Indicates weather a user can use oauth2 client credentials

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_o_auth2_client_credentials of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_o_auth2_client_credentials

    @can_use_o_auth2_client_credentials.setter
    def can_use_o_auth2_client_credentials(self, can_use_o_auth2_client_credentials):
        """
        Sets the can_use_o_auth2_client_credentials of this UserCapabilitiesChanger.
        Indicates weather a user can use oauth2 client credentials

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_o_auth2_client_credentials: The can_use_o_auth2_client_credentials of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_o_auth2_client_credentials = can_use_o_auth2_client_credentials

    @property
    def can_use_smtp_credentials(self):
        """
        Gets the can_use_smtp_credentials of this UserCapabilitiesChanger.
        Indicates weather a user can use smtp credentials

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_smtp_credentials of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_smtp_credentials

    @can_use_smtp_credentials.setter
    def can_use_smtp_credentials(self, can_use_smtp_credentials):
        """
        Sets the can_use_smtp_credentials of this UserCapabilitiesChanger.
        Indicates weather a user can use smtp credentials

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_smtp_credentials: The can_use_smtp_credentials of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_smtp_credentials = can_use_smtp_credentials

    @property
    def can_use_db_credentials(self):
        """
        Gets the can_use_db_credentials of this UserCapabilitiesChanger.
        Indicates weather a user can use db credentials

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The can_use_db_credentials of this UserCapabilitiesChanger.
        :rtype: bool
        """
        return self._can_use_db_credentials

    @can_use_db_credentials.setter
    def can_use_db_credentials(self, can_use_db_credentials):
        """
        Sets the can_use_db_credentials of this UserCapabilitiesChanger.
        Indicates weather a user can use db credentials

        **SCIM++ Properties:**
         - caseExact: false
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param can_use_db_credentials: The can_use_db_credentials of this UserCapabilitiesChanger.
        :type: bool
        """
        self._can_use_db_credentials = can_use_db_credentials

    @property
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user(self):
        """
        Gets the urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user of this UserCapabilitiesChanger.

        :return: The urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user of this UserCapabilitiesChanger.
        :rtype: oci.identity_domains.models.ExtensionSelfChangeUser
        """
        return self._urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user

    @urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user.setter
    def urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user(self, urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user):
        """
        Sets the urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user of this UserCapabilitiesChanger.

        :param urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user: The urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user of this UserCapabilitiesChanger.
        :type: oci.identity_domains.models.ExtensionSelfChangeUser
        """
        self._urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user = urn_ietf_params_scim_schemas_oracle_idcs_extension_self_change_user

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
