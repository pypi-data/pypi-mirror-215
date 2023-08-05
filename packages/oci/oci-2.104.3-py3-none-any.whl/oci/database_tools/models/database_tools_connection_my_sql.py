# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .database_tools_connection import DatabaseToolsConnection
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DatabaseToolsConnectionMySql(DatabaseToolsConnection):
    """
    Database Tools connection of a MySQL Server.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DatabaseToolsConnectionMySql object with values from keyword arguments. The default value of the :py:attr:`~oci.database_tools.models.DatabaseToolsConnectionMySql.type` attribute
        of this class is ``MYSQL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DatabaseToolsConnectionMySql.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this DatabaseToolsConnectionMySql.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DatabaseToolsConnectionMySql.
        :type compartment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DatabaseToolsConnectionMySql.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this DatabaseToolsConnectionMySql.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this DatabaseToolsConnectionMySql.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DatabaseToolsConnectionMySql.
        :type time_updated: datetime

        :param defined_tags:
            The value to assign to the defined_tags property of this DatabaseToolsConnectionMySql.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DatabaseToolsConnectionMySql.
        :type freeform_tags: dict(str, str)

        :param system_tags:
            The value to assign to the system_tags property of this DatabaseToolsConnectionMySql.
        :type system_tags: dict(str, dict(str, object))

        :param type:
            The value to assign to the type property of this DatabaseToolsConnectionMySql.
            Allowed values for this property are: "ORACLE_DATABASE", "MYSQL"
        :type type: str

        :param related_resource:
            The value to assign to the related_resource property of this DatabaseToolsConnectionMySql.
        :type related_resource: oci.database_tools.models.DatabaseToolsRelatedResourceMySql

        :param connection_string:
            The value to assign to the connection_string property of this DatabaseToolsConnectionMySql.
        :type connection_string: str

        :param user_name:
            The value to assign to the user_name property of this DatabaseToolsConnectionMySql.
        :type user_name: str

        :param user_password:
            The value to assign to the user_password property of this DatabaseToolsConnectionMySql.
        :type user_password: oci.database_tools.models.DatabaseToolsUserPassword

        :param advanced_properties:
            The value to assign to the advanced_properties property of this DatabaseToolsConnectionMySql.
        :type advanced_properties: dict(str, str)

        :param key_stores:
            The value to assign to the key_stores property of this DatabaseToolsConnectionMySql.
        :type key_stores: list[oci.database_tools.models.DatabaseToolsKeyStoreMySql]

        :param private_endpoint_id:
            The value to assign to the private_endpoint_id property of this DatabaseToolsConnectionMySql.
        :type private_endpoint_id: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'system_tags': 'dict(str, dict(str, object))',
            'type': 'str',
            'related_resource': 'DatabaseToolsRelatedResourceMySql',
            'connection_string': 'str',
            'user_name': 'str',
            'user_password': 'DatabaseToolsUserPassword',
            'advanced_properties': 'dict(str, str)',
            'key_stores': 'list[DatabaseToolsKeyStoreMySql]',
            'private_endpoint_id': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'system_tags': 'systemTags',
            'type': 'type',
            'related_resource': 'relatedResource',
            'connection_string': 'connectionString',
            'user_name': 'userName',
            'user_password': 'userPassword',
            'advanced_properties': 'advancedProperties',
            'key_stores': 'keyStores',
            'private_endpoint_id': 'privateEndpointId'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None
        self._defined_tags = None
        self._freeform_tags = None
        self._system_tags = None
        self._type = None
        self._related_resource = None
        self._connection_string = None
        self._user_name = None
        self._user_password = None
        self._advanced_properties = None
        self._key_stores = None
        self._private_endpoint_id = None
        self._type = 'MYSQL'

    @property
    def related_resource(self):
        """
        Gets the related_resource of this DatabaseToolsConnectionMySql.

        :return: The related_resource of this DatabaseToolsConnectionMySql.
        :rtype: oci.database_tools.models.DatabaseToolsRelatedResourceMySql
        """
        return self._related_resource

    @related_resource.setter
    def related_resource(self, related_resource):
        """
        Sets the related_resource of this DatabaseToolsConnectionMySql.

        :param related_resource: The related_resource of this DatabaseToolsConnectionMySql.
        :type: oci.database_tools.models.DatabaseToolsRelatedResourceMySql
        """
        self._related_resource = related_resource

    @property
    def connection_string(self):
        """
        Gets the connection_string of this DatabaseToolsConnectionMySql.
        The connection string used to connect to the MySQL Server.


        :return: The connection_string of this DatabaseToolsConnectionMySql.
        :rtype: str
        """
        return self._connection_string

    @connection_string.setter
    def connection_string(self, connection_string):
        """
        Sets the connection_string of this DatabaseToolsConnectionMySql.
        The connection string used to connect to the MySQL Server.


        :param connection_string: The connection_string of this DatabaseToolsConnectionMySql.
        :type: str
        """
        self._connection_string = connection_string

    @property
    def user_name(self):
        """
        Gets the user_name of this DatabaseToolsConnectionMySql.
        The user name.


        :return: The user_name of this DatabaseToolsConnectionMySql.
        :rtype: str
        """
        return self._user_name

    @user_name.setter
    def user_name(self, user_name):
        """
        Sets the user_name of this DatabaseToolsConnectionMySql.
        The user name.


        :param user_name: The user_name of this DatabaseToolsConnectionMySql.
        :type: str
        """
        self._user_name = user_name

    @property
    def user_password(self):
        """
        Gets the user_password of this DatabaseToolsConnectionMySql.

        :return: The user_password of this DatabaseToolsConnectionMySql.
        :rtype: oci.database_tools.models.DatabaseToolsUserPassword
        """
        return self._user_password

    @user_password.setter
    def user_password(self, user_password):
        """
        Sets the user_password of this DatabaseToolsConnectionMySql.

        :param user_password: The user_password of this DatabaseToolsConnectionMySql.
        :type: oci.database_tools.models.DatabaseToolsUserPassword
        """
        self._user_password = user_password

    @property
    def advanced_properties(self):
        """
        Gets the advanced_properties of this DatabaseToolsConnectionMySql.
        The advanced connection properties key-value pair (for example, `sslMode`).


        :return: The advanced_properties of this DatabaseToolsConnectionMySql.
        :rtype: dict(str, str)
        """
        return self._advanced_properties

    @advanced_properties.setter
    def advanced_properties(self, advanced_properties):
        """
        Sets the advanced_properties of this DatabaseToolsConnectionMySql.
        The advanced connection properties key-value pair (for example, `sslMode`).


        :param advanced_properties: The advanced_properties of this DatabaseToolsConnectionMySql.
        :type: dict(str, str)
        """
        self._advanced_properties = advanced_properties

    @property
    def key_stores(self):
        """
        Gets the key_stores of this DatabaseToolsConnectionMySql.
        The CA certificate to verify the server's certificate and
        the client private key and associated certificate required for client authentication.


        :return: The key_stores of this DatabaseToolsConnectionMySql.
        :rtype: list[oci.database_tools.models.DatabaseToolsKeyStoreMySql]
        """
        return self._key_stores

    @key_stores.setter
    def key_stores(self, key_stores):
        """
        Sets the key_stores of this DatabaseToolsConnectionMySql.
        The CA certificate to verify the server's certificate and
        the client private key and associated certificate required for client authentication.


        :param key_stores: The key_stores of this DatabaseToolsConnectionMySql.
        :type: list[oci.database_tools.models.DatabaseToolsKeyStoreMySql]
        """
        self._key_stores = key_stores

    @property
    def private_endpoint_id(self):
        """
        Gets the private_endpoint_id of this DatabaseToolsConnectionMySql.
        The `OCID`__ of the Database Tools private endpoint used to access the database in the customer VCN.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The private_endpoint_id of this DatabaseToolsConnectionMySql.
        :rtype: str
        """
        return self._private_endpoint_id

    @private_endpoint_id.setter
    def private_endpoint_id(self, private_endpoint_id):
        """
        Sets the private_endpoint_id of this DatabaseToolsConnectionMySql.
        The `OCID`__ of the Database Tools private endpoint used to access the database in the customer VCN.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param private_endpoint_id: The private_endpoint_id of this DatabaseToolsConnectionMySql.
        :type: str
        """
        self._private_endpoint_id = private_endpoint_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
