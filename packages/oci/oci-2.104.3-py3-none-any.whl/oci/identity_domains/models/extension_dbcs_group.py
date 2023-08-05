# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionDbcsGroup(object):
    """
    Schema for Database Service  Resource
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionDbcsGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param instance_level_schema_names:
            The value to assign to the instance_level_schema_names property of this ExtensionDbcsGroup.
        :type instance_level_schema_names: list[oci.identity_domains.models.GroupExtInstanceLevelSchemaNames]

        :param domain_level_schema_names:
            The value to assign to the domain_level_schema_names property of this ExtensionDbcsGroup.
        :type domain_level_schema_names: list[oci.identity_domains.models.GroupExtDomainLevelSchemaNames]

        :param domain_level_schema:
            The value to assign to the domain_level_schema property of this ExtensionDbcsGroup.
        :type domain_level_schema: str

        :param instance_level_schema:
            The value to assign to the instance_level_schema property of this ExtensionDbcsGroup.
        :type instance_level_schema: str

        """
        self.swagger_types = {
            'instance_level_schema_names': 'list[GroupExtInstanceLevelSchemaNames]',
            'domain_level_schema_names': 'list[GroupExtDomainLevelSchemaNames]',
            'domain_level_schema': 'str',
            'instance_level_schema': 'str'
        }

        self.attribute_map = {
            'instance_level_schema_names': 'instanceLevelSchemaNames',
            'domain_level_schema_names': 'domainLevelSchemaNames',
            'domain_level_schema': 'domainLevelSchema',
            'instance_level_schema': 'instanceLevelSchema'
        }

        self._instance_level_schema_names = None
        self._domain_level_schema_names = None
        self._domain_level_schema = None
        self._instance_level_schema = None

    @property
    def instance_level_schema_names(self):
        """
        Gets the instance_level_schema_names of this ExtensionDbcsGroup.
        DBCS instance-level schema-names. Each schema-name is specific to a DB Instance.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsCompositeKey: [dbInstanceId, schemaName]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex


        :return: The instance_level_schema_names of this ExtensionDbcsGroup.
        :rtype: list[oci.identity_domains.models.GroupExtInstanceLevelSchemaNames]
        """
        return self._instance_level_schema_names

    @instance_level_schema_names.setter
    def instance_level_schema_names(self, instance_level_schema_names):
        """
        Sets the instance_level_schema_names of this ExtensionDbcsGroup.
        DBCS instance-level schema-names. Each schema-name is specific to a DB Instance.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsCompositeKey: [dbInstanceId, schemaName]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex


        :param instance_level_schema_names: The instance_level_schema_names of this ExtensionDbcsGroup.
        :type: list[oci.identity_domains.models.GroupExtInstanceLevelSchemaNames]
        """
        self._instance_level_schema_names = instance_level_schema_names

    @property
    def domain_level_schema_names(self):
        """
        Gets the domain_level_schema_names of this ExtensionDbcsGroup.
        DBCS Domain-level schema-names. Each value is specific to a DB Domain.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsCompositeKey: [domainName, schemaName]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex


        :return: The domain_level_schema_names of this ExtensionDbcsGroup.
        :rtype: list[oci.identity_domains.models.GroupExtDomainLevelSchemaNames]
        """
        return self._domain_level_schema_names

    @domain_level_schema_names.setter
    def domain_level_schema_names(self, domain_level_schema_names):
        """
        Sets the domain_level_schema_names of this ExtensionDbcsGroup.
        DBCS Domain-level schema-names. Each value is specific to a DB Domain.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsCompositeKey: [domainName, schemaName]
         - idcsSearchable: true
         - multiValued: true
         - mutability: readOnly
         - required: false
         - returned: request
         - type: complex


        :param domain_level_schema_names: The domain_level_schema_names of this ExtensionDbcsGroup.
        :type: list[oci.identity_domains.models.GroupExtDomainLevelSchemaNames]
        """
        self._domain_level_schema_names = domain_level_schema_names

    @property
    def domain_level_schema(self):
        """
        Gets the domain_level_schema of this ExtensionDbcsGroup.
        DBCS Domain-level schema-name.  This attribute refers implicitly to a value of 'domainLevelSchemaNames' for a particular DB Domain.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsSensitive: none
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :return: The domain_level_schema of this ExtensionDbcsGroup.
        :rtype: str
        """
        return self._domain_level_schema

    @domain_level_schema.setter
    def domain_level_schema(self, domain_level_schema):
        """
        Sets the domain_level_schema of this ExtensionDbcsGroup.
        DBCS Domain-level schema-name.  This attribute refers implicitly to a value of 'domainLevelSchemaNames' for a particular DB Domain.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsSensitive: none
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param domain_level_schema: The domain_level_schema of this ExtensionDbcsGroup.
        :type: str
        """
        self._domain_level_schema = domain_level_schema

    @property
    def instance_level_schema(self):
        """
        Gets the instance_level_schema of this ExtensionDbcsGroup.
        DBCS instance-level schema-name. This attribute refers implicitly to a value of 'instanceLevelSchemaNames' for a particular DB Instance.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsSensitive: none
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :return: The instance_level_schema of this ExtensionDbcsGroup.
        :rtype: str
        """
        return self._instance_level_schema

    @instance_level_schema.setter
    def instance_level_schema(self, instance_level_schema):
        """
        Sets the instance_level_schema of this ExtensionDbcsGroup.
        DBCS instance-level schema-name. This attribute refers implicitly to a value of 'instanceLevelSchemaNames' for a particular DB Instance.

        **Added In:** 18.2.4

        **SCIM++ Properties:**
         - idcsSearchable: false
         - idcsSensitive: none
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param instance_level_schema: The instance_level_schema of this ExtensionDbcsGroup.
        :type: str
        """
        self._instance_level_schema = instance_level_schema

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
