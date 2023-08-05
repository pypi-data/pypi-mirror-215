# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_connection_details import UpdateConnectionDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateJavaMessageServiceConnectionDetails(UpdateConnectionDetails):
    """
    The information to update a Java Message Service Connection.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateJavaMessageServiceConnectionDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.UpdateJavaMessageServiceConnectionDetails.connection_type` attribute
        of this class is ``JAVA_MESSAGE_SERVICE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this UpdateJavaMessageServiceConnectionDetails.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB"
        :type connection_type: str

        :param display_name:
            The value to assign to the display_name property of this UpdateJavaMessageServiceConnectionDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateJavaMessageServiceConnectionDetails.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateJavaMessageServiceConnectionDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateJavaMessageServiceConnectionDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param vault_id:
            The value to assign to the vault_id property of this UpdateJavaMessageServiceConnectionDetails.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this UpdateJavaMessageServiceConnectionDetails.
        :type key_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this UpdateJavaMessageServiceConnectionDetails.
        :type nsg_ids: list[str]

        :param should_use_jndi:
            The value to assign to the should_use_jndi property of this UpdateJavaMessageServiceConnectionDetails.
        :type should_use_jndi: bool

        :param jndi_connection_factory:
            The value to assign to the jndi_connection_factory property of this UpdateJavaMessageServiceConnectionDetails.
        :type jndi_connection_factory: str

        :param jndi_provider_url:
            The value to assign to the jndi_provider_url property of this UpdateJavaMessageServiceConnectionDetails.
        :type jndi_provider_url: str

        :param jndi_initial_context_factory:
            The value to assign to the jndi_initial_context_factory property of this UpdateJavaMessageServiceConnectionDetails.
        :type jndi_initial_context_factory: str

        :param jndi_security_principal:
            The value to assign to the jndi_security_principal property of this UpdateJavaMessageServiceConnectionDetails.
        :type jndi_security_principal: str

        :param jndi_security_credentials:
            The value to assign to the jndi_security_credentials property of this UpdateJavaMessageServiceConnectionDetails.
        :type jndi_security_credentials: str

        :param connection_url:
            The value to assign to the connection_url property of this UpdateJavaMessageServiceConnectionDetails.
        :type connection_url: str

        :param connection_factory:
            The value to assign to the connection_factory property of this UpdateJavaMessageServiceConnectionDetails.
        :type connection_factory: str

        :param username:
            The value to assign to the username property of this UpdateJavaMessageServiceConnectionDetails.
        :type username: str

        :param password:
            The value to assign to the password property of this UpdateJavaMessageServiceConnectionDetails.
        :type password: str

        :param private_ip:
            The value to assign to the private_ip property of this UpdateJavaMessageServiceConnectionDetails.
        :type private_ip: str

        """
        self.swagger_types = {
            'connection_type': 'str',
            'display_name': 'str',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'vault_id': 'str',
            'key_id': 'str',
            'nsg_ids': 'list[str]',
            'should_use_jndi': 'bool',
            'jndi_connection_factory': 'str',
            'jndi_provider_url': 'str',
            'jndi_initial_context_factory': 'str',
            'jndi_security_principal': 'str',
            'jndi_security_credentials': 'str',
            'connection_url': 'str',
            'connection_factory': 'str',
            'username': 'str',
            'password': 'str',
            'private_ip': 'str'
        }

        self.attribute_map = {
            'connection_type': 'connectionType',
            'display_name': 'displayName',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'vault_id': 'vaultId',
            'key_id': 'keyId',
            'nsg_ids': 'nsgIds',
            'should_use_jndi': 'shouldUseJndi',
            'jndi_connection_factory': 'jndiConnectionFactory',
            'jndi_provider_url': 'jndiProviderUrl',
            'jndi_initial_context_factory': 'jndiInitialContextFactory',
            'jndi_security_principal': 'jndiSecurityPrincipal',
            'jndi_security_credentials': 'jndiSecurityCredentials',
            'connection_url': 'connectionUrl',
            'connection_factory': 'connectionFactory',
            'username': 'username',
            'password': 'password',
            'private_ip': 'privateIp'
        }

        self._connection_type = None
        self._display_name = None
        self._description = None
        self._freeform_tags = None
        self._defined_tags = None
        self._vault_id = None
        self._key_id = None
        self._nsg_ids = None
        self._should_use_jndi = None
        self._jndi_connection_factory = None
        self._jndi_provider_url = None
        self._jndi_initial_context_factory = None
        self._jndi_security_principal = None
        self._jndi_security_credentials = None
        self._connection_url = None
        self._connection_factory = None
        self._username = None
        self._password = None
        self._private_ip = None
        self._connection_type = 'JAVA_MESSAGE_SERVICE'

    @property
    def should_use_jndi(self):
        """
        Gets the should_use_jndi of this UpdateJavaMessageServiceConnectionDetails.
        If set to true, Java Naming and Directory Interface (JNDI) properties should be provided.


        :return: The should_use_jndi of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: bool
        """
        return self._should_use_jndi

    @should_use_jndi.setter
    def should_use_jndi(self, should_use_jndi):
        """
        Sets the should_use_jndi of this UpdateJavaMessageServiceConnectionDetails.
        If set to true, Java Naming and Directory Interface (JNDI) properties should be provided.


        :param should_use_jndi: The should_use_jndi of this UpdateJavaMessageServiceConnectionDetails.
        :type: bool
        """
        self._should_use_jndi = should_use_jndi

    @property
    def jndi_connection_factory(self):
        """
        Gets the jndi_connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        The Connection Factory can be looked up using this name.
        e.g.: 'ConnectionFactory'


        :return: The jndi_connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_connection_factory

    @jndi_connection_factory.setter
    def jndi_connection_factory(self, jndi_connection_factory):
        """
        Sets the jndi_connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        The Connection Factory can be looked up using this name.
        e.g.: 'ConnectionFactory'


        :param jndi_connection_factory: The jndi_connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_connection_factory = jndi_connection_factory

    @property
    def jndi_provider_url(self):
        """
        Gets the jndi_provider_url of this UpdateJavaMessageServiceConnectionDetails.
        The URL that Java Message Service will use to contact the JNDI provider.
        e.g.: 'tcp://myjms.host.domain:61616?jms.prefetchPolicy.all=1000'


        :return: The jndi_provider_url of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_provider_url

    @jndi_provider_url.setter
    def jndi_provider_url(self, jndi_provider_url):
        """
        Sets the jndi_provider_url of this UpdateJavaMessageServiceConnectionDetails.
        The URL that Java Message Service will use to contact the JNDI provider.
        e.g.: 'tcp://myjms.host.domain:61616?jms.prefetchPolicy.all=1000'


        :param jndi_provider_url: The jndi_provider_url of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_provider_url = jndi_provider_url

    @property
    def jndi_initial_context_factory(self):
        """
        Gets the jndi_initial_context_factory of this UpdateJavaMessageServiceConnectionDetails.
        The implementation of javax.naming.spi.InitialContextFactory interface
        that the client uses to obtain initial naming context.
        e.g.: 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'


        :return: The jndi_initial_context_factory of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_initial_context_factory

    @jndi_initial_context_factory.setter
    def jndi_initial_context_factory(self, jndi_initial_context_factory):
        """
        Sets the jndi_initial_context_factory of this UpdateJavaMessageServiceConnectionDetails.
        The implementation of javax.naming.spi.InitialContextFactory interface
        that the client uses to obtain initial naming context.
        e.g.: 'org.apache.activemq.jndi.ActiveMQInitialContextFactory'


        :param jndi_initial_context_factory: The jndi_initial_context_factory of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_initial_context_factory = jndi_initial_context_factory

    @property
    def jndi_security_principal(self):
        """
        Gets the jndi_security_principal of this UpdateJavaMessageServiceConnectionDetails.
        Specifies the identity of the principal (user) to be authenticated.
        e.g.: 'admin2'


        :return: The jndi_security_principal of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_security_principal

    @jndi_security_principal.setter
    def jndi_security_principal(self, jndi_security_principal):
        """
        Sets the jndi_security_principal of this UpdateJavaMessageServiceConnectionDetails.
        Specifies the identity of the principal (user) to be authenticated.
        e.g.: 'admin2'


        :param jndi_security_principal: The jndi_security_principal of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_security_principal = jndi_security_principal

    @property
    def jndi_security_credentials(self):
        """
        Gets the jndi_security_credentials of this UpdateJavaMessageServiceConnectionDetails.
        The password associated to the principal.


        :return: The jndi_security_credentials of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._jndi_security_credentials

    @jndi_security_credentials.setter
    def jndi_security_credentials(self, jndi_security_credentials):
        """
        Sets the jndi_security_credentials of this UpdateJavaMessageServiceConnectionDetails.
        The password associated to the principal.


        :param jndi_security_credentials: The jndi_security_credentials of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._jndi_security_credentials = jndi_security_credentials

    @property
    def connection_url(self):
        """
        Gets the connection_url of this UpdateJavaMessageServiceConnectionDetails.
        Connectin URL of the Java Message Service, specifying the protocol, host, and port.
        e.g.: 'mq://myjms.host.domain:7676'


        :return: The connection_url of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._connection_url

    @connection_url.setter
    def connection_url(self, connection_url):
        """
        Sets the connection_url of this UpdateJavaMessageServiceConnectionDetails.
        Connectin URL of the Java Message Service, specifying the protocol, host, and port.
        e.g.: 'mq://myjms.host.domain:7676'


        :param connection_url: The connection_url of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._connection_url = connection_url

    @property
    def connection_factory(self):
        """
        Gets the connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        The of Java class implementing javax.jms.ConnectionFactory interface
        supplied by the Java Message Service provider.
        e.g.: 'com.stc.jmsjca.core.JConnectionFactoryXA'


        :return: The connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._connection_factory

    @connection_factory.setter
    def connection_factory(self, connection_factory):
        """
        Sets the connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        The of Java class implementing javax.jms.ConnectionFactory interface
        supplied by the Java Message Service provider.
        e.g.: 'com.stc.jmsjca.core.JConnectionFactoryXA'


        :param connection_factory: The connection_factory of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._connection_factory = connection_factory

    @property
    def username(self):
        """
        Gets the username of this UpdateJavaMessageServiceConnectionDetails.
        The username Oracle GoldenGate uses to connect to the Java Message Service.
        This username must already exist and be available by the Java Message Service to be connected to.


        :return: The username of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this UpdateJavaMessageServiceConnectionDetails.
        The username Oracle GoldenGate uses to connect to the Java Message Service.
        This username must already exist and be available by the Java Message Service to be connected to.


        :param username: The username of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._username = username

    @property
    def password(self):
        """
        Gets the password of this UpdateJavaMessageServiceConnectionDetails.
        The password Oracle GoldenGate uses to connect the associated Java Message Service.


        :return: The password of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this UpdateJavaMessageServiceConnectionDetails.
        The password Oracle GoldenGate uses to connect the associated Java Message Service.


        :param password: The password of this UpdateJavaMessageServiceConnectionDetails.
        :type: str
        """
        self._password = password

    @property
    def private_ip(self):
        """
        Gets the private_ip of this UpdateJavaMessageServiceConnectionDetails.
        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :return: The private_ip of this UpdateJavaMessageServiceConnectionDetails.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this UpdateJavaMessageServiceConnectionDetails.
        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :param private_ip: The private_ip of this UpdateJavaMessageServiceConnectionDetails.
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
