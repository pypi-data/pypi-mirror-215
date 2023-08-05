# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionGroupGroup(object):
    """
    Idcs Group
    """

    #: A constant which can be used with the creation_mechanism property of a ExtensionGroupGroup.
    #: This constant has a value of "bulk"
    CREATION_MECHANISM_BULK = "bulk"

    #: A constant which can be used with the creation_mechanism property of a ExtensionGroupGroup.
    #: This constant has a value of "api"
    CREATION_MECHANISM_API = "api"

    #: A constant which can be used with the creation_mechanism property of a ExtensionGroupGroup.
    #: This constant has a value of "adsync"
    CREATION_MECHANISM_ADSYNC = "adsync"

    #: A constant which can be used with the creation_mechanism property of a ExtensionGroupGroup.
    #: This constant has a value of "authsync"
    CREATION_MECHANISM_AUTHSYNC = "authsync"

    #: A constant which can be used with the creation_mechanism property of a ExtensionGroupGroup.
    #: This constant has a value of "idcsui"
    CREATION_MECHANISM_IDCSUI = "idcsui"

    #: A constant which can be used with the creation_mechanism property of a ExtensionGroupGroup.
    #: This constant has a value of "import"
    CREATION_MECHANISM_IMPORT = "import"

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionGroupGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param description:
            The value to assign to the description property of this ExtensionGroupGroup.
        :type description: str

        :param creation_mechanism:
            The value to assign to the creation_mechanism property of this ExtensionGroupGroup.
            Allowed values for this property are: "bulk", "api", "adsync", "authsync", "idcsui", "import", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type creation_mechanism: str

        :param password_policy:
            The value to assign to the password_policy property of this ExtensionGroupGroup.
        :type password_policy: oci.identity_domains.models.GroupExtPasswordPolicy

        :param synced_from_app:
            The value to assign to the synced_from_app property of this ExtensionGroupGroup.
        :type synced_from_app: oci.identity_domains.models.GroupExtSyncedFromApp

        :param grants:
            The value to assign to the grants property of this ExtensionGroupGroup.
        :type grants: list[oci.identity_domains.models.GroupExtGrants]

        :param owners:
            The value to assign to the owners property of this ExtensionGroupGroup.
        :type owners: list[oci.identity_domains.models.GroupExtOwners]

        :param app_roles:
            The value to assign to the app_roles property of this ExtensionGroupGroup.
        :type app_roles: list[oci.identity_domains.models.GroupExtAppRoles]

        """
        self.swagger_types = {
            'description': 'str',
            'creation_mechanism': 'str',
            'password_policy': 'GroupExtPasswordPolicy',
            'synced_from_app': 'GroupExtSyncedFromApp',
            'grants': 'list[GroupExtGrants]',
            'owners': 'list[GroupExtOwners]',
            'app_roles': 'list[GroupExtAppRoles]'
        }

        self.attribute_map = {
            'description': 'description',
            'creation_mechanism': 'creationMechanism',
            'password_policy': 'passwordPolicy',
            'synced_from_app': 'syncedFromApp',
            'grants': 'grants',
            'owners': 'owners',
            'app_roles': 'appRoles'
        }

        self._description = None
        self._creation_mechanism = None
        self._password_policy = None
        self._synced_from_app = None
        self._grants = None
        self._owners = None
        self._app_roles = None

    @property
    def description(self):
        """
        Gets the description of this ExtensionGroupGroup.
        Group description

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Description
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Description]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The description of this ExtensionGroupGroup.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ExtensionGroupGroup.
        Group description

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeName: Description
         - idcsCsvAttributeNameMappings: [[columnHeaderName:Description]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param description: The description of this ExtensionGroupGroup.
        :type: str
        """
        self._description = description

    @property
    def creation_mechanism(self):
        """
        Gets the creation_mechanism of this ExtensionGroupGroup.
        Source from which this group got created.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeNameMappings: [[defaultValue:import]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: request
         - type: string
         - uniqueness: none

        Allowed values for this property are: "bulk", "api", "adsync", "authsync", "idcsui", "import", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The creation_mechanism of this ExtensionGroupGroup.
        :rtype: str
        """
        return self._creation_mechanism

    @creation_mechanism.setter
    def creation_mechanism(self, creation_mechanism):
        """
        Sets the creation_mechanism of this ExtensionGroupGroup.
        Source from which this group got created.

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCsvAttributeNameMappings: [[defaultValue:import]]
         - idcsSearchable: true
         - multiValued: false
         - mutability: immutable
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param creation_mechanism: The creation_mechanism of this ExtensionGroupGroup.
        :type: str
        """
        allowed_values = ["bulk", "api", "adsync", "authsync", "idcsui", "import"]
        if not value_allowed_none_or_none_sentinel(creation_mechanism, allowed_values):
            creation_mechanism = 'UNKNOWN_ENUM_VALUE'
        self._creation_mechanism = creation_mechanism

    @property
    def password_policy(self):
        """
        Gets the password_policy of this ExtensionGroupGroup.

        :return: The password_policy of this ExtensionGroupGroup.
        :rtype: oci.identity_domains.models.GroupExtPasswordPolicy
        """
        return self._password_policy

    @password_policy.setter
    def password_policy(self, password_policy):
        """
        Sets the password_policy of this ExtensionGroupGroup.

        :param password_policy: The password_policy of this ExtensionGroupGroup.
        :type: oci.identity_domains.models.GroupExtPasswordPolicy
        """
        self._password_policy = password_policy

    @property
    def synced_from_app(self):
        """
        Gets the synced_from_app of this ExtensionGroupGroup.

        :return: The synced_from_app of this ExtensionGroupGroup.
        :rtype: oci.identity_domains.models.GroupExtSyncedFromApp
        """
        return self._synced_from_app

    @synced_from_app.setter
    def synced_from_app(self, synced_from_app):
        """
        Sets the synced_from_app of this ExtensionGroupGroup.

        :param synced_from_app: The synced_from_app of this ExtensionGroupGroup.
        :type: oci.identity_domains.models.GroupExtSyncedFromApp
        """
        self._synced_from_app = synced_from_app

    @property
    def grants(self):
        """
        Gets the grants of this ExtensionGroupGroup.
        Grants assigned to group

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The grants of this ExtensionGroupGroup.
        :rtype: list[oci.identity_domains.models.GroupExtGrants]
        """
        return self._grants

    @grants.setter
    def grants(self, grants):
        """
        Sets the grants of this ExtensionGroupGroup.
        Grants assigned to group

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param grants: The grants of this ExtensionGroupGroup.
        :type: list[oci.identity_domains.models.GroupExtGrants]
        """
        self._grants = grants

    @property
    def owners(self):
        """
        Gets the owners of this ExtensionGroupGroup.
        Group owners

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value, type]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The owners of this ExtensionGroupGroup.
        :rtype: list[oci.identity_domains.models.GroupExtOwners]
        """
        return self._owners

    @owners.setter
    def owners(self, owners):
        """
        Sets the owners of this ExtensionGroupGroup.
        Group owners

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value, type]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param owners: The owners of this ExtensionGroupGroup.
        :type: list[oci.identity_domains.models.GroupExtOwners]
        """
        self._owners = owners

    @property
    def app_roles(self):
        """
        Gets the app_roles of this ExtensionGroupGroup.
        A list of appRoles that the user belongs to, either thorough direct membership, nested groups, or dynamically calculated

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The app_roles of this ExtensionGroupGroup.
        :rtype: list[oci.identity_domains.models.GroupExtAppRoles]
        """
        return self._app_roles

    @app_roles.setter
    def app_roles(self, app_roles):
        """
        Sets the app_roles of this ExtensionGroupGroup.
        A list of appRoles that the user belongs to, either thorough direct membership, nested groups, or dynamically calculated

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param app_roles: The app_roles of this ExtensionGroupGroup.
        :type: list[oci.identity_domains.models.GroupExtAppRoles]
        """
        self._app_roles = app_roles

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
