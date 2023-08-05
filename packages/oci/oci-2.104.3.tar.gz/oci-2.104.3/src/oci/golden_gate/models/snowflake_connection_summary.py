# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .connection_summary import ConnectionSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SnowflakeConnectionSummary(ConnectionSummary):
    """
    Summary of the Snowflake Connection.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SnowflakeConnectionSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.SnowflakeConnectionSummary.connection_type` attribute
        of this class is ``SNOWFLAKE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this SnowflakeConnectionSummary.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB"
        :type connection_type: str

        :param id:
            The value to assign to the id property of this SnowflakeConnectionSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this SnowflakeConnectionSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this SnowflakeConnectionSummary.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this SnowflakeConnectionSummary.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this SnowflakeConnectionSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this SnowflakeConnectionSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this SnowflakeConnectionSummary.
        :type system_tags: dict(str, dict(str, object))

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this SnowflakeConnectionSummary.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this SnowflakeConnectionSummary.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this SnowflakeConnectionSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this SnowflakeConnectionSummary.
        :type time_updated: datetime

        :param vault_id:
            The value to assign to the vault_id property of this SnowflakeConnectionSummary.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this SnowflakeConnectionSummary.
        :type key_id: str

        :param subnet_id:
            The value to assign to the subnet_id property of this SnowflakeConnectionSummary.
        :type subnet_id: str

        :param ingress_ips:
            The value to assign to the ingress_ips property of this SnowflakeConnectionSummary.
        :type ingress_ips: list[oci.golden_gate.models.IngressIpDetails]

        :param nsg_ids:
            The value to assign to the nsg_ids property of this SnowflakeConnectionSummary.
        :type nsg_ids: list[str]

        :param technology_type:
            The value to assign to the technology_type property of this SnowflakeConnectionSummary.
        :type technology_type: str

        :param connection_url:
            The value to assign to the connection_url property of this SnowflakeConnectionSummary.
        :type connection_url: str

        :param authentication_type:
            The value to assign to the authentication_type property of this SnowflakeConnectionSummary.
        :type authentication_type: str

        :param username:
            The value to assign to the username property of this SnowflakeConnectionSummary.
        :type username: str

        """
        self.swagger_types = {
            'connection_type': 'str',
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'vault_id': 'str',
            'key_id': 'str',
            'subnet_id': 'str',
            'ingress_ips': 'list[IngressIpDetails]',
            'nsg_ids': 'list[str]',
            'technology_type': 'str',
            'connection_url': 'str',
            'authentication_type': 'str',
            'username': 'str'
        }

        self.attribute_map = {
            'connection_type': 'connectionType',
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'vault_id': 'vaultId',
            'key_id': 'keyId',
            'subnet_id': 'subnetId',
            'ingress_ips': 'ingressIps',
            'nsg_ids': 'nsgIds',
            'technology_type': 'technologyType',
            'connection_url': 'connectionUrl',
            'authentication_type': 'authenticationType',
            'username': 'username'
        }

        self._connection_type = None
        self._id = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None
        self._vault_id = None
        self._key_id = None
        self._subnet_id = None
        self._ingress_ips = None
        self._nsg_ids = None
        self._technology_type = None
        self._connection_url = None
        self._authentication_type = None
        self._username = None
        self._connection_type = 'SNOWFLAKE'

    @property
    def technology_type(self):
        """
        **[Required]** Gets the technology_type of this SnowflakeConnectionSummary.
        The Snowflake technology type.


        :return: The technology_type of this SnowflakeConnectionSummary.
        :rtype: str
        """
        return self._technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        """
        Sets the technology_type of this SnowflakeConnectionSummary.
        The Snowflake technology type.


        :param technology_type: The technology_type of this SnowflakeConnectionSummary.
        :type: str
        """
        self._technology_type = technology_type

    @property
    def connection_url(self):
        """
        **[Required]** Gets the connection_url of this SnowflakeConnectionSummary.
        JDBC connection URL.
        e.g.: 'jdbc:snowflake://<account_name>.snowflakecomputing.com/?warehouse=<warehouse-name>&db=<db-name>'


        :return: The connection_url of this SnowflakeConnectionSummary.
        :rtype: str
        """
        return self._connection_url

    @connection_url.setter
    def connection_url(self, connection_url):
        """
        Sets the connection_url of this SnowflakeConnectionSummary.
        JDBC connection URL.
        e.g.: 'jdbc:snowflake://<account_name>.snowflakecomputing.com/?warehouse=<warehouse-name>&db=<db-name>'


        :param connection_url: The connection_url of this SnowflakeConnectionSummary.
        :type: str
        """
        self._connection_url = connection_url

    @property
    def authentication_type(self):
        """
        **[Required]** Gets the authentication_type of this SnowflakeConnectionSummary.
        Used authentication mechanism to access Snowflake.


        :return: The authentication_type of this SnowflakeConnectionSummary.
        :rtype: str
        """
        return self._authentication_type

    @authentication_type.setter
    def authentication_type(self, authentication_type):
        """
        Sets the authentication_type of this SnowflakeConnectionSummary.
        Used authentication mechanism to access Snowflake.


        :param authentication_type: The authentication_type of this SnowflakeConnectionSummary.
        :type: str
        """
        self._authentication_type = authentication_type

    @property
    def username(self):
        """
        Gets the username of this SnowflakeConnectionSummary.
        The username Oracle GoldenGate uses to connect to Snowflake.
        This username must already exist and be available by Snowflake platform to be connected to.


        :return: The username of this SnowflakeConnectionSummary.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this SnowflakeConnectionSummary.
        The username Oracle GoldenGate uses to connect to Snowflake.
        This username must already exist and be available by Snowflake platform to be connected to.


        :param username: The username of this SnowflakeConnectionSummary.
        :type: str
        """
        self._username = username

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
