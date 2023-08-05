# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalDatabaseSummary(object):
    """
    The summary of an external database.
    """

    #: A constant which can be used with the database_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "EXTERNAL_SIDB"
    DATABASE_TYPE_EXTERNAL_SIDB = "EXTERNAL_SIDB"

    #: A constant which can be used with the database_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "EXTERNAL_RAC"
    DATABASE_TYPE_EXTERNAL_RAC = "EXTERNAL_RAC"

    #: A constant which can be used with the database_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "CLOUD_SIDB"
    DATABASE_TYPE_CLOUD_SIDB = "CLOUD_SIDB"

    #: A constant which can be used with the database_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "CLOUD_RAC"
    DATABASE_TYPE_CLOUD_RAC = "CLOUD_RAC"

    #: A constant which can be used with the database_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "SHARED"
    DATABASE_TYPE_SHARED = "SHARED"

    #: A constant which can be used with the database_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "DEDICATED"
    DATABASE_TYPE_DEDICATED = "DEDICATED"

    #: A constant which can be used with the database_sub_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "CDB"
    DATABASE_SUB_TYPE_CDB = "CDB"

    #: A constant which can be used with the database_sub_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "PDB"
    DATABASE_SUB_TYPE_PDB = "PDB"

    #: A constant which can be used with the database_sub_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "NON_CDB"
    DATABASE_SUB_TYPE_NON_CDB = "NON_CDB"

    #: A constant which can be used with the database_sub_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "ACD"
    DATABASE_SUB_TYPE_ACD = "ACD"

    #: A constant which can be used with the database_sub_type property of a ExternalDatabaseSummary.
    #: This constant has a value of "ADB"
    DATABASE_SUB_TYPE_ADB = "ADB"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ExternalDatabaseSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalDatabaseSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalDatabaseSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalDatabaseSummary.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalDatabaseSummary.
        :type compartment_id: str

        :param db_unique_name:
            The value to assign to the db_unique_name property of this ExternalDatabaseSummary.
        :type db_unique_name: str

        :param database_type:
            The value to assign to the database_type property of this ExternalDatabaseSummary.
            Allowed values for this property are: "EXTERNAL_SIDB", "EXTERNAL_RAC", "CLOUD_SIDB", "CLOUD_RAC", "SHARED", "DEDICATED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type database_type: str

        :param database_sub_type:
            The value to assign to the database_sub_type property of this ExternalDatabaseSummary.
            Allowed values for this property are: "CDB", "PDB", "NON_CDB", "ACD", "ADB", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type database_sub_type: str

        :param external_container_database_id:
            The value to assign to the external_container_database_id property of this ExternalDatabaseSummary.
        :type external_container_database_id: str

        :param external_db_home_id:
            The value to assign to the external_db_home_id property of this ExternalDatabaseSummary.
        :type external_db_home_id: str

        :param db_system_info:
            The value to assign to the db_system_info property of this ExternalDatabaseSummary.
        :type db_system_info: oci.database_management.models.ExternalDbSystemBasicInfo

        :param db_management_config:
            The value to assign to the db_management_config property of this ExternalDatabaseSummary.
        :type db_management_config: oci.database_management.models.DatabaseManagementConfig

        :param instance_details:
            The value to assign to the instance_details property of this ExternalDatabaseSummary.
        :type instance_details: list[oci.database_management.models.ExternalDatabaseInstance]

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalDatabaseSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this ExternalDatabaseSummary.
        :type time_created: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'db_unique_name': 'str',
            'database_type': 'str',
            'database_sub_type': 'str',
            'external_container_database_id': 'str',
            'external_db_home_id': 'str',
            'db_system_info': 'ExternalDbSystemBasicInfo',
            'db_management_config': 'DatabaseManagementConfig',
            'instance_details': 'list[ExternalDatabaseInstance]',
            'lifecycle_state': 'str',
            'time_created': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'db_unique_name': 'dbUniqueName',
            'database_type': 'databaseType',
            'database_sub_type': 'databaseSubType',
            'external_container_database_id': 'externalContainerDatabaseId',
            'external_db_home_id': 'externalDbHomeId',
            'db_system_info': 'dbSystemInfo',
            'db_management_config': 'dbManagementConfig',
            'instance_details': 'instanceDetails',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._db_unique_name = None
        self._database_type = None
        self._database_sub_type = None
        self._external_container_database_id = None
        self._external_db_home_id = None
        self._db_system_info = None
        self._db_management_config = None
        self._instance_details = None
        self._lifecycle_state = None
        self._time_created = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalDatabaseSummary.
        The `OCID`__ of the external DB system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalDatabaseSummary.
        The `OCID`__ of the external DB system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalDatabaseSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalDatabaseSummary.
        The user-friendly name for the database. The name does not have to be unique.


        :return: The display_name of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalDatabaseSummary.
        The user-friendly name for the database. The name does not have to be unique.


        :param display_name: The display_name of this ExternalDatabaseSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExternalDatabaseSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalDatabaseSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalDatabaseSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def db_unique_name(self):
        """
        Gets the db_unique_name of this ExternalDatabaseSummary.
        The `DB_UNIQUE_NAME` of the external database.


        :return: The db_unique_name of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._db_unique_name

    @db_unique_name.setter
    def db_unique_name(self, db_unique_name):
        """
        Sets the db_unique_name of this ExternalDatabaseSummary.
        The `DB_UNIQUE_NAME` of the external database.


        :param db_unique_name: The db_unique_name of this ExternalDatabaseSummary.
        :type: str
        """
        self._db_unique_name = db_unique_name

    @property
    def database_type(self):
        """
        Gets the database_type of this ExternalDatabaseSummary.
        The type of Oracle Database installation.

        Allowed values for this property are: "EXTERNAL_SIDB", "EXTERNAL_RAC", "CLOUD_SIDB", "CLOUD_RAC", "SHARED", "DEDICATED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The database_type of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._database_type

    @database_type.setter
    def database_type(self, database_type):
        """
        Sets the database_type of this ExternalDatabaseSummary.
        The type of Oracle Database installation.


        :param database_type: The database_type of this ExternalDatabaseSummary.
        :type: str
        """
        allowed_values = ["EXTERNAL_SIDB", "EXTERNAL_RAC", "CLOUD_SIDB", "CLOUD_RAC", "SHARED", "DEDICATED"]
        if not value_allowed_none_or_none_sentinel(database_type, allowed_values):
            database_type = 'UNKNOWN_ENUM_VALUE'
        self._database_type = database_type

    @property
    def database_sub_type(self):
        """
        Gets the database_sub_type of this ExternalDatabaseSummary.
        The subtype of Oracle Database. Indicates whether the database is a Container Database,
        Pluggable Database, or Non-container Database.

        Allowed values for this property are: "CDB", "PDB", "NON_CDB", "ACD", "ADB", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The database_sub_type of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._database_sub_type

    @database_sub_type.setter
    def database_sub_type(self, database_sub_type):
        """
        Sets the database_sub_type of this ExternalDatabaseSummary.
        The subtype of Oracle Database. Indicates whether the database is a Container Database,
        Pluggable Database, or Non-container Database.


        :param database_sub_type: The database_sub_type of this ExternalDatabaseSummary.
        :type: str
        """
        allowed_values = ["CDB", "PDB", "NON_CDB", "ACD", "ADB"]
        if not value_allowed_none_or_none_sentinel(database_sub_type, allowed_values):
            database_sub_type = 'UNKNOWN_ENUM_VALUE'
        self._database_sub_type = database_sub_type

    @property
    def external_container_database_id(self):
        """
        Gets the external_container_database_id of this ExternalDatabaseSummary.
        The `OCID`__ of the parent Container Database (CDB)
        if this is a Pluggable Database (PDB).

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_container_database_id of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._external_container_database_id

    @external_container_database_id.setter
    def external_container_database_id(self, external_container_database_id):
        """
        Sets the external_container_database_id of this ExternalDatabaseSummary.
        The `OCID`__ of the parent Container Database (CDB)
        if this is a Pluggable Database (PDB).

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_container_database_id: The external_container_database_id of this ExternalDatabaseSummary.
        :type: str
        """
        self._external_container_database_id = external_container_database_id

    @property
    def external_db_home_id(self):
        """
        Gets the external_db_home_id of this ExternalDatabaseSummary.
        The `OCID`__ of the external DB home.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_home_id of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._external_db_home_id

    @external_db_home_id.setter
    def external_db_home_id(self, external_db_home_id):
        """
        Sets the external_db_home_id of this ExternalDatabaseSummary.
        The `OCID`__ of the external DB home.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_home_id: The external_db_home_id of this ExternalDatabaseSummary.
        :type: str
        """
        self._external_db_home_id = external_db_home_id

    @property
    def db_system_info(self):
        """
        Gets the db_system_info of this ExternalDatabaseSummary.

        :return: The db_system_info of this ExternalDatabaseSummary.
        :rtype: oci.database_management.models.ExternalDbSystemBasicInfo
        """
        return self._db_system_info

    @db_system_info.setter
    def db_system_info(self, db_system_info):
        """
        Sets the db_system_info of this ExternalDatabaseSummary.

        :param db_system_info: The db_system_info of this ExternalDatabaseSummary.
        :type: oci.database_management.models.ExternalDbSystemBasicInfo
        """
        self._db_system_info = db_system_info

    @property
    def db_management_config(self):
        """
        Gets the db_management_config of this ExternalDatabaseSummary.

        :return: The db_management_config of this ExternalDatabaseSummary.
        :rtype: oci.database_management.models.DatabaseManagementConfig
        """
        return self._db_management_config

    @db_management_config.setter
    def db_management_config(self, db_management_config):
        """
        Sets the db_management_config of this ExternalDatabaseSummary.

        :param db_management_config: The db_management_config of this ExternalDatabaseSummary.
        :type: oci.database_management.models.DatabaseManagementConfig
        """
        self._db_management_config = db_management_config

    @property
    def instance_details(self):
        """
        Gets the instance_details of this ExternalDatabaseSummary.
        The list of database instances if the database is a RAC database.


        :return: The instance_details of this ExternalDatabaseSummary.
        :rtype: list[oci.database_management.models.ExternalDatabaseInstance]
        """
        return self._instance_details

    @instance_details.setter
    def instance_details(self, instance_details):
        """
        Sets the instance_details of this ExternalDatabaseSummary.
        The list of database instances if the database is a RAC database.


        :param instance_details: The instance_details of this ExternalDatabaseSummary.
        :type: list[oci.database_management.models.ExternalDatabaseInstance]
        """
        self._instance_details = instance_details

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExternalDatabaseSummary.
        The current lifecycle state of the external database resource.

        Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ExternalDatabaseSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExternalDatabaseSummary.
        The current lifecycle state of the external database resource.


        :param lifecycle_state: The lifecycle_state of this ExternalDatabaseSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ExternalDatabaseSummary.
        The date and time the external DB system was created.


        :return: The time_created of this ExternalDatabaseSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExternalDatabaseSummary.
        The date and time the external DB system was created.


        :param time_created: The time_created of this ExternalDatabaseSummary.
        :type: datetime
        """
        self._time_created = time_created

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
