# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .entity_discovered import EntityDiscovered
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalStorageGridDiscoverySummary(EntityDiscovered):
    """
    The Exadata storage server grid.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalStorageGridDiscoverySummary object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.ExternalStorageGridDiscoverySummary.entity_type` attribute
        of this class is ``STORAGE_GRID_DISCOVER_SUMMARY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalStorageGridDiscoverySummary.
        :type id: str

        :param agent_id:
            The value to assign to the agent_id property of this ExternalStorageGridDiscoverySummary.
        :type agent_id: str

        :param connector_id:
            The value to assign to the connector_id property of this ExternalStorageGridDiscoverySummary.
        :type connector_id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalStorageGridDiscoverySummary.
        :type display_name: str

        :param version:
            The value to assign to the version property of this ExternalStorageGridDiscoverySummary.
        :type version: str

        :param internal_id:
            The value to assign to the internal_id property of this ExternalStorageGridDiscoverySummary.
        :type internal_id: str

        :param status:
            The value to assign to the status property of this ExternalStorageGridDiscoverySummary.
        :type status: str

        :param discover_status:
            The value to assign to the discover_status property of this ExternalStorageGridDiscoverySummary.
            Allowed values for this property are: "PREV_DISCOVERED", "NEW_DISCOVERED", "NOT_FOUND", "DISCOVERING"
        :type discover_status: str

        :param discover_error_code:
            The value to assign to the discover_error_code property of this ExternalStorageGridDiscoverySummary.
        :type discover_error_code: str

        :param discover_error_msg:
            The value to assign to the discover_error_msg property of this ExternalStorageGridDiscoverySummary.
        :type discover_error_msg: str

        :param entity_type:
            The value to assign to the entity_type property of this ExternalStorageGridDiscoverySummary.
            Allowed values for this property are: "STORAGE_SERVER_DISCOVER_SUMMARY", "STORAGE_GRID_DISCOVER_SUMMARY", "DATABASE_SYSTEM_DISCOVER_SUMMARY", "INFRASTRUCTURE_DISCOVER_SUMMARY", "INFRASTRUCTURE_DISCOVER"
        :type entity_type: str

        :param count_of_storage_servers_discovered:
            The value to assign to the count_of_storage_servers_discovered property of this ExternalStorageGridDiscoverySummary.
        :type count_of_storage_servers_discovered: int

        """
        self.swagger_types = {
            'id': 'str',
            'agent_id': 'str',
            'connector_id': 'str',
            'display_name': 'str',
            'version': 'str',
            'internal_id': 'str',
            'status': 'str',
            'discover_status': 'str',
            'discover_error_code': 'str',
            'discover_error_msg': 'str',
            'entity_type': 'str',
            'count_of_storage_servers_discovered': 'int'
        }

        self.attribute_map = {
            'id': 'id',
            'agent_id': 'agentId',
            'connector_id': 'connectorId',
            'display_name': 'displayName',
            'version': 'version',
            'internal_id': 'internalId',
            'status': 'status',
            'discover_status': 'discoverStatus',
            'discover_error_code': 'discoverErrorCode',
            'discover_error_msg': 'discoverErrorMsg',
            'entity_type': 'entityType',
            'count_of_storage_servers_discovered': 'countOfStorageServersDiscovered'
        }

        self._id = None
        self._agent_id = None
        self._connector_id = None
        self._display_name = None
        self._version = None
        self._internal_id = None
        self._status = None
        self._discover_status = None
        self._discover_error_code = None
        self._discover_error_msg = None
        self._entity_type = None
        self._count_of_storage_servers_discovered = None
        self._entity_type = 'STORAGE_GRID_DISCOVER_SUMMARY'

    @property
    def count_of_storage_servers_discovered(self):
        """
        Gets the count_of_storage_servers_discovered of this ExternalStorageGridDiscoverySummary.
        The total number of the storage servers discovered.


        :return: The count_of_storage_servers_discovered of this ExternalStorageGridDiscoverySummary.
        :rtype: int
        """
        return self._count_of_storage_servers_discovered

    @count_of_storage_servers_discovered.setter
    def count_of_storage_servers_discovered(self, count_of_storage_servers_discovered):
        """
        Sets the count_of_storage_servers_discovered of this ExternalStorageGridDiscoverySummary.
        The total number of the storage servers discovered.


        :param count_of_storage_servers_discovered: The count_of_storage_servers_discovered of this ExternalStorageGridDiscoverySummary.
        :type: int
        """
        self._count_of_storage_servers_discovered = count_of_storage_servers_discovered

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
