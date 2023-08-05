# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .connection import Connection
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MicrosoftSqlserverConnection(Connection):
    """
    Represents the metadata of a Microsoft SQL Server Connection.
    """

    #: A constant which can be used with the technology_type property of a MicrosoftSqlserverConnection.
    #: This constant has a value of "AMAZON_RDS_SQLSERVER"
    TECHNOLOGY_TYPE_AMAZON_RDS_SQLSERVER = "AMAZON_RDS_SQLSERVER"

    #: A constant which can be used with the technology_type property of a MicrosoftSqlserverConnection.
    #: This constant has a value of "AZURE_SQLSERVER_MANAGED_INSTANCE"
    TECHNOLOGY_TYPE_AZURE_SQLSERVER_MANAGED_INSTANCE = "AZURE_SQLSERVER_MANAGED_INSTANCE"

    #: A constant which can be used with the technology_type property of a MicrosoftSqlserverConnection.
    #: This constant has a value of "AZURE_SQLSERVER_NON_MANAGED_INSTANCE"
    TECHNOLOGY_TYPE_AZURE_SQLSERVER_NON_MANAGED_INSTANCE = "AZURE_SQLSERVER_NON_MANAGED_INSTANCE"

    #: A constant which can be used with the technology_type property of a MicrosoftSqlserverConnection.
    #: This constant has a value of "MICROSOFT_SQLSERVER"
    TECHNOLOGY_TYPE_MICROSOFT_SQLSERVER = "MICROSOFT_SQLSERVER"

    #: A constant which can be used with the security_protocol property of a MicrosoftSqlserverConnection.
    #: This constant has a value of "PLAIN"
    SECURITY_PROTOCOL_PLAIN = "PLAIN"

    #: A constant which can be used with the security_protocol property of a MicrosoftSqlserverConnection.
    #: This constant has a value of "TLS"
    SECURITY_PROTOCOL_TLS = "TLS"

    def __init__(self, **kwargs):
        """
        Initializes a new MicrosoftSqlserverConnection object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.MicrosoftSqlserverConnection.connection_type` attribute
        of this class is ``MICROSOFT_SQLSERVER`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this MicrosoftSqlserverConnection.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type connection_type: str

        :param id:
            The value to assign to the id property of this MicrosoftSqlserverConnection.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this MicrosoftSqlserverConnection.
        :type display_name: str

        :param description:
            The value to assign to the description property of this MicrosoftSqlserverConnection.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this MicrosoftSqlserverConnection.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this MicrosoftSqlserverConnection.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this MicrosoftSqlserverConnection.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this MicrosoftSqlserverConnection.
        :type system_tags: dict(str, dict(str, object))

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this MicrosoftSqlserverConnection.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this MicrosoftSqlserverConnection.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this MicrosoftSqlserverConnection.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this MicrosoftSqlserverConnection.
        :type time_updated: datetime

        :param vault_id:
            The value to assign to the vault_id property of this MicrosoftSqlserverConnection.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this MicrosoftSqlserverConnection.
        :type key_id: str

        :param subnet_id:
            The value to assign to the subnet_id property of this MicrosoftSqlserverConnection.
        :type subnet_id: str

        :param ingress_ips:
            The value to assign to the ingress_ips property of this MicrosoftSqlserverConnection.
        :type ingress_ips: list[oci.golden_gate.models.IngressIpDetails]

        :param nsg_ids:
            The value to assign to the nsg_ids property of this MicrosoftSqlserverConnection.
        :type nsg_ids: list[str]

        :param technology_type:
            The value to assign to the technology_type property of this MicrosoftSqlserverConnection.
            Allowed values for this property are: "AMAZON_RDS_SQLSERVER", "AZURE_SQLSERVER_MANAGED_INSTANCE", "AZURE_SQLSERVER_NON_MANAGED_INSTANCE", "MICROSOFT_SQLSERVER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type technology_type: str

        :param username:
            The value to assign to the username property of this MicrosoftSqlserverConnection.
        :type username: str

        :param host:
            The value to assign to the host property of this MicrosoftSqlserverConnection.
        :type host: str

        :param port:
            The value to assign to the port property of this MicrosoftSqlserverConnection.
        :type port: int

        :param database_name:
            The value to assign to the database_name property of this MicrosoftSqlserverConnection.
        :type database_name: str

        :param additional_attributes:
            The value to assign to the additional_attributes property of this MicrosoftSqlserverConnection.
        :type additional_attributes: list[oci.golden_gate.models.NameValuePair]

        :param security_protocol:
            The value to assign to the security_protocol property of this MicrosoftSqlserverConnection.
            Allowed values for this property are: "PLAIN", "TLS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type security_protocol: str

        :param ssl_ca:
            The value to assign to the ssl_ca property of this MicrosoftSqlserverConnection.
        :type ssl_ca: str

        :param should_validate_server_certificate:
            The value to assign to the should_validate_server_certificate property of this MicrosoftSqlserverConnection.
        :type should_validate_server_certificate: bool

        :param private_ip:
            The value to assign to the private_ip property of this MicrosoftSqlserverConnection.
        :type private_ip: str

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
            'username': 'str',
            'host': 'str',
            'port': 'int',
            'database_name': 'str',
            'additional_attributes': 'list[NameValuePair]',
            'security_protocol': 'str',
            'ssl_ca': 'str',
            'should_validate_server_certificate': 'bool',
            'private_ip': 'str'
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
            'username': 'username',
            'host': 'host',
            'port': 'port',
            'database_name': 'databaseName',
            'additional_attributes': 'additionalAttributes',
            'security_protocol': 'securityProtocol',
            'ssl_ca': 'sslCa',
            'should_validate_server_certificate': 'shouldValidateServerCertificate',
            'private_ip': 'privateIp'
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
        self._username = None
        self._host = None
        self._port = None
        self._database_name = None
        self._additional_attributes = None
        self._security_protocol = None
        self._ssl_ca = None
        self._should_validate_server_certificate = None
        self._private_ip = None
        self._connection_type = 'MICROSOFT_SQLSERVER'

    @property
    def technology_type(self):
        """
        **[Required]** Gets the technology_type of this MicrosoftSqlserverConnection.
        The Microsoft SQL Server technology type.

        Allowed values for this property are: "AMAZON_RDS_SQLSERVER", "AZURE_SQLSERVER_MANAGED_INSTANCE", "AZURE_SQLSERVER_NON_MANAGED_INSTANCE", "MICROSOFT_SQLSERVER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The technology_type of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        """
        Sets the technology_type of this MicrosoftSqlserverConnection.
        The Microsoft SQL Server technology type.


        :param technology_type: The technology_type of this MicrosoftSqlserverConnection.
        :type: str
        """
        allowed_values = ["AMAZON_RDS_SQLSERVER", "AZURE_SQLSERVER_MANAGED_INSTANCE", "AZURE_SQLSERVER_NON_MANAGED_INSTANCE", "MICROSOFT_SQLSERVER"]
        if not value_allowed_none_or_none_sentinel(technology_type, allowed_values):
            technology_type = 'UNKNOWN_ENUM_VALUE'
        self._technology_type = technology_type

    @property
    def username(self):
        """
        **[Required]** Gets the username of this MicrosoftSqlserverConnection.
        The username Oracle GoldenGate uses to connect to the Microsoft SQL Server.
        This username must already exist and be available by the Microsoft SQL Server to be connected to.


        :return: The username of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this MicrosoftSqlserverConnection.
        The username Oracle GoldenGate uses to connect to the Microsoft SQL Server.
        This username must already exist and be available by the Microsoft SQL Server to be connected to.


        :param username: The username of this MicrosoftSqlserverConnection.
        :type: str
        """
        self._username = username

    @property
    def host(self):
        """
        **[Required]** Gets the host of this MicrosoftSqlserverConnection.
        The name or address of a host.


        :return: The host of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """
        Sets the host of this MicrosoftSqlserverConnection.
        The name or address of a host.


        :param host: The host of this MicrosoftSqlserverConnection.
        :type: str
        """
        self._host = host

    @property
    def port(self):
        """
        **[Required]** Gets the port of this MicrosoftSqlserverConnection.
        The port of an endpoint usually specified for a connection.


        :return: The port of this MicrosoftSqlserverConnection.
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this MicrosoftSqlserverConnection.
        The port of an endpoint usually specified for a connection.


        :param port: The port of this MicrosoftSqlserverConnection.
        :type: int
        """
        self._port = port

    @property
    def database_name(self):
        """
        **[Required]** Gets the database_name of this MicrosoftSqlserverConnection.
        The name of the database.


        :return: The database_name of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._database_name

    @database_name.setter
    def database_name(self, database_name):
        """
        Sets the database_name of this MicrosoftSqlserverConnection.
        The name of the database.


        :param database_name: The database_name of this MicrosoftSqlserverConnection.
        :type: str
        """
        self._database_name = database_name

    @property
    def additional_attributes(self):
        """
        Gets the additional_attributes of this MicrosoftSqlserverConnection.
        An array of name-value pair attribute entries.
        Used as additional parameters in connection string.


        :return: The additional_attributes of this MicrosoftSqlserverConnection.
        :rtype: list[oci.golden_gate.models.NameValuePair]
        """
        return self._additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes):
        """
        Sets the additional_attributes of this MicrosoftSqlserverConnection.
        An array of name-value pair attribute entries.
        Used as additional parameters in connection string.


        :param additional_attributes: The additional_attributes of this MicrosoftSqlserverConnection.
        :type: list[oci.golden_gate.models.NameValuePair]
        """
        self._additional_attributes = additional_attributes

    @property
    def security_protocol(self):
        """
        **[Required]** Gets the security_protocol of this MicrosoftSqlserverConnection.
        Security Protocol for Microsoft SQL Server.

        Allowed values for this property are: "PLAIN", "TLS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The security_protocol of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._security_protocol

    @security_protocol.setter
    def security_protocol(self, security_protocol):
        """
        Sets the security_protocol of this MicrosoftSqlserverConnection.
        Security Protocol for Microsoft SQL Server.


        :param security_protocol: The security_protocol of this MicrosoftSqlserverConnection.
        :type: str
        """
        allowed_values = ["PLAIN", "TLS"]
        if not value_allowed_none_or_none_sentinel(security_protocol, allowed_values):
            security_protocol = 'UNKNOWN_ENUM_VALUE'
        self._security_protocol = security_protocol

    @property
    def ssl_ca(self):
        """
        Gets the ssl_ca of this MicrosoftSqlserverConnection.
        Database Certificate - The base64 encoded content of pem file
        containing the server public key (for 1-way SSL).


        :return: The ssl_ca of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._ssl_ca

    @ssl_ca.setter
    def ssl_ca(self, ssl_ca):
        """
        Sets the ssl_ca of this MicrosoftSqlserverConnection.
        Database Certificate - The base64 encoded content of pem file
        containing the server public key (for 1-way SSL).


        :param ssl_ca: The ssl_ca of this MicrosoftSqlserverConnection.
        :type: str
        """
        self._ssl_ca = ssl_ca

    @property
    def should_validate_server_certificate(self):
        """
        Gets the should_validate_server_certificate of this MicrosoftSqlserverConnection.
        If set to true, the driver validates the certificate that is sent by the database server.


        :return: The should_validate_server_certificate of this MicrosoftSqlserverConnection.
        :rtype: bool
        """
        return self._should_validate_server_certificate

    @should_validate_server_certificate.setter
    def should_validate_server_certificate(self, should_validate_server_certificate):
        """
        Sets the should_validate_server_certificate of this MicrosoftSqlserverConnection.
        If set to true, the driver validates the certificate that is sent by the database server.


        :param should_validate_server_certificate: The should_validate_server_certificate of this MicrosoftSqlserverConnection.
        :type: bool
        """
        self._should_validate_server_certificate = should_validate_server_certificate

    @property
    def private_ip(self):
        """
        Gets the private_ip of this MicrosoftSqlserverConnection.
        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :return: The private_ip of this MicrosoftSqlserverConnection.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this MicrosoftSqlserverConnection.
        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :param private_ip: The private_ip of this MicrosoftSqlserverConnection.
        :type: str
        """
        self._private_ip = private_ip

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
