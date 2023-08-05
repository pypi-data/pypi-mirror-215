# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalDbSystemSummary(object):
    """
    The summary of an external DB system.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalDbSystemSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalDbSystemSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalDbSystemSummary.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalDbSystemSummary.
        :type compartment_id: str

        :param home_directory:
            The value to assign to the home_directory property of this ExternalDbSystemSummary.
        :type home_directory: str

        :param database_management_config:
            The value to assign to the database_management_config property of this ExternalDbSystemSummary.
        :type database_management_config: oci.database_management.models.ExternalDbSystemDatabaseManagementConfigDetails

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalDbSystemSummary.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalDbSystemSummary.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this ExternalDbSystemSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalDbSystemSummary.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'home_directory': 'str',
            'database_management_config': 'ExternalDbSystemDatabaseManagementConfigDetails',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'home_directory': 'homeDirectory',
            'database_management_config': 'databaseManagementConfig',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._home_directory = None
        self._database_management_config = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalDbSystemSummary.
        The `OCID`__ of the external DB system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalDbSystemSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalDbSystemSummary.
        The `OCID`__ of the external DB system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalDbSystemSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalDbSystemSummary.
        The user-friendly name for the DB system. The name does not have to be unique.


        :return: The display_name of this ExternalDbSystemSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalDbSystemSummary.
        The user-friendly name for the DB system. The name does not have to be unique.


        :param display_name: The display_name of this ExternalDbSystemSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExternalDbSystemSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalDbSystemSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalDbSystemSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalDbSystemSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def home_directory(self):
        """
        Gets the home_directory of this ExternalDbSystemSummary.
        The Oracle Grid home directory in case of cluster-based DB system and
        Oracle home directory in case of single instance-based DB system.


        :return: The home_directory of this ExternalDbSystemSummary.
        :rtype: str
        """
        return self._home_directory

    @home_directory.setter
    def home_directory(self, home_directory):
        """
        Sets the home_directory of this ExternalDbSystemSummary.
        The Oracle Grid home directory in case of cluster-based DB system and
        Oracle home directory in case of single instance-based DB system.


        :param home_directory: The home_directory of this ExternalDbSystemSummary.
        :type: str
        """
        self._home_directory = home_directory

    @property
    def database_management_config(self):
        """
        Gets the database_management_config of this ExternalDbSystemSummary.

        :return: The database_management_config of this ExternalDbSystemSummary.
        :rtype: oci.database_management.models.ExternalDbSystemDatabaseManagementConfigDetails
        """
        return self._database_management_config

    @database_management_config.setter
    def database_management_config(self, database_management_config):
        """
        Sets the database_management_config of this ExternalDbSystemSummary.

        :param database_management_config: The database_management_config of this ExternalDbSystemSummary.
        :type: oci.database_management.models.ExternalDbSystemDatabaseManagementConfigDetails
        """
        self._database_management_config = database_management_config

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExternalDbSystemSummary.
        The current lifecycle state of the external DB system resource.


        :return: The lifecycle_state of this ExternalDbSystemSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExternalDbSystemSummary.
        The current lifecycle state of the external DB system resource.


        :param lifecycle_state: The lifecycle_state of this ExternalDbSystemSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ExternalDbSystemSummary.
        Additional information about the current lifecycle state.


        :return: The lifecycle_details of this ExternalDbSystemSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ExternalDbSystemSummary.
        Additional information about the current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this ExternalDbSystemSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ExternalDbSystemSummary.
        The date and time the external DB system was created.


        :return: The time_created of this ExternalDbSystemSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExternalDbSystemSummary.
        The date and time the external DB system was created.


        :param time_created: The time_created of this ExternalDbSystemSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this ExternalDbSystemSummary.
        The date and time the external DB system was last updated.


        :return: The time_updated of this ExternalDbSystemSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ExternalDbSystemSummary.
        The date and time the external DB system was last updated.


        :param time_updated: The time_updated of this ExternalDbSystemSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
