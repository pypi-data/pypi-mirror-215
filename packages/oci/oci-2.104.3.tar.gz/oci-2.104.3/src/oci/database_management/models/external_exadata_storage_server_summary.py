# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .dbm_resource import DbmResource
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalExadataStorageServerSummary(DbmResource):
    """
    The storage server of the Exadata infrastructure.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalExadataStorageServerSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.ExternalExadataStorageServerSummary.resource_type` attribute
        of this class is ``STORAGE_SERVER_SUMMARY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalExadataStorageServerSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalExadataStorageServerSummary.
        :type display_name: str

        :param version:
            The value to assign to the version property of this ExternalExadataStorageServerSummary.
        :type version: str

        :param internal_id:
            The value to assign to the internal_id property of this ExternalExadataStorageServerSummary.
        :type internal_id: str

        :param status:
            The value to assign to the status property of this ExternalExadataStorageServerSummary.
        :type status: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalExadataStorageServerSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this ExternalExadataStorageServerSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalExadataStorageServerSummary.
        :type time_updated: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalExadataStorageServerSummary.
        :type lifecycle_details: str

        :param additional_details:
            The value to assign to the additional_details property of this ExternalExadataStorageServerSummary.
        :type additional_details: dict(str, str)

        :param resource_type:
            The value to assign to the resource_type property of this ExternalExadataStorageServerSummary.
            Allowed values for this property are: "INFRASTRUCTURE_SUMMARY", "INFRASTRUCTURE", "STORAGE_SERVER_SUMMARY", "STORAGE_SERVER", "STORAGE_GRID_SUMMARY", "STORAGE_GRID", "STORAGE_CONNECTOR_SUMMARY", "STORAGE_CONNECTOR", "DATABASE_SYSTEM_SUMMARY", "DATABASE_SUMMARY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_type: str

        :param make_model:
            The value to assign to the make_model property of this ExternalExadataStorageServerSummary.
        :type make_model: str

        :param ip_address:
            The value to assign to the ip_address property of this ExternalExadataStorageServerSummary.
        :type ip_address: str

        :param cpu_count:
            The value to assign to the cpu_count property of this ExternalExadataStorageServerSummary.
        :type cpu_count: float

        :param memory_gb:
            The value to assign to the memory_gb property of this ExternalExadataStorageServerSummary.
        :type memory_gb: float

        :param max_hard_disk_iops:
            The value to assign to the max_hard_disk_iops property of this ExternalExadataStorageServerSummary.
        :type max_hard_disk_iops: int

        :param max_hard_disk_throughput:
            The value to assign to the max_hard_disk_throughput property of this ExternalExadataStorageServerSummary.
        :type max_hard_disk_throughput: int

        :param max_flash_disk_iops:
            The value to assign to the max_flash_disk_iops property of this ExternalExadataStorageServerSummary.
        :type max_flash_disk_iops: int

        :param max_flash_disk_throughput:
            The value to assign to the max_flash_disk_throughput property of this ExternalExadataStorageServerSummary.
        :type max_flash_disk_throughput: int

        :param connector_id:
            The value to assign to the connector_id property of this ExternalExadataStorageServerSummary.
        :type connector_id: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'version': 'str',
            'internal_id': 'str',
            'status': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_details': 'str',
            'additional_details': 'dict(str, str)',
            'resource_type': 'str',
            'make_model': 'str',
            'ip_address': 'str',
            'cpu_count': 'float',
            'memory_gb': 'float',
            'max_hard_disk_iops': 'int',
            'max_hard_disk_throughput': 'int',
            'max_flash_disk_iops': 'int',
            'max_flash_disk_throughput': 'int',
            'connector_id': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'version': 'version',
            'internal_id': 'internalId',
            'status': 'status',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_details': 'lifecycleDetails',
            'additional_details': 'additionalDetails',
            'resource_type': 'resourceType',
            'make_model': 'makeModel',
            'ip_address': 'ipAddress',
            'cpu_count': 'cpuCount',
            'memory_gb': 'memoryGB',
            'max_hard_disk_iops': 'maxHardDiskIOPS',
            'max_hard_disk_throughput': 'maxHardDiskThroughput',
            'max_flash_disk_iops': 'maxFlashDiskIOPS',
            'max_flash_disk_throughput': 'maxFlashDiskThroughput',
            'connector_id': 'connectorId'
        }

        self._id = None
        self._display_name = None
        self._version = None
        self._internal_id = None
        self._status = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_details = None
        self._additional_details = None
        self._resource_type = None
        self._make_model = None
        self._ip_address = None
        self._cpu_count = None
        self._memory_gb = None
        self._max_hard_disk_iops = None
        self._max_hard_disk_throughput = None
        self._max_flash_disk_iops = None
        self._max_flash_disk_throughput = None
        self._connector_id = None
        self._resource_type = 'STORAGE_SERVER_SUMMARY'

    @property
    def make_model(self):
        """
        Gets the make_model of this ExternalExadataStorageServerSummary.
        The make model of the storage server.


        :return: The make_model of this ExternalExadataStorageServerSummary.
        :rtype: str
        """
        return self._make_model

    @make_model.setter
    def make_model(self, make_model):
        """
        Sets the make_model of this ExternalExadataStorageServerSummary.
        The make model of the storage server.


        :param make_model: The make_model of this ExternalExadataStorageServerSummary.
        :type: str
        """
        self._make_model = make_model

    @property
    def ip_address(self):
        """
        Gets the ip_address of this ExternalExadataStorageServerSummary.
        The IP address of the storage server.


        :return: The ip_address of this ExternalExadataStorageServerSummary.
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """
        Sets the ip_address of this ExternalExadataStorageServerSummary.
        The IP address of the storage server.


        :param ip_address: The ip_address of this ExternalExadataStorageServerSummary.
        :type: str
        """
        self._ip_address = ip_address

    @property
    def cpu_count(self):
        """
        Gets the cpu_count of this ExternalExadataStorageServerSummary.
        The CPU count of the storage server


        :return: The cpu_count of this ExternalExadataStorageServerSummary.
        :rtype: float
        """
        return self._cpu_count

    @cpu_count.setter
    def cpu_count(self, cpu_count):
        """
        Sets the cpu_count of this ExternalExadataStorageServerSummary.
        The CPU count of the storage server


        :param cpu_count: The cpu_count of this ExternalExadataStorageServerSummary.
        :type: float
        """
        self._cpu_count = cpu_count

    @property
    def memory_gb(self):
        """
        Gets the memory_gb of this ExternalExadataStorageServerSummary.
        The storage server memory size in GB


        :return: The memory_gb of this ExternalExadataStorageServerSummary.
        :rtype: float
        """
        return self._memory_gb

    @memory_gb.setter
    def memory_gb(self, memory_gb):
        """
        Sets the memory_gb of this ExternalExadataStorageServerSummary.
        The storage server memory size in GB


        :param memory_gb: The memory_gb of this ExternalExadataStorageServerSummary.
        :type: float
        """
        self._memory_gb = memory_gb

    @property
    def max_hard_disk_iops(self):
        """
        Gets the max_hard_disk_iops of this ExternalExadataStorageServerSummary.
        The maximum hard disk IO operations per second of the storage server


        :return: The max_hard_disk_iops of this ExternalExadataStorageServerSummary.
        :rtype: int
        """
        return self._max_hard_disk_iops

    @max_hard_disk_iops.setter
    def max_hard_disk_iops(self, max_hard_disk_iops):
        """
        Sets the max_hard_disk_iops of this ExternalExadataStorageServerSummary.
        The maximum hard disk IO operations per second of the storage server


        :param max_hard_disk_iops: The max_hard_disk_iops of this ExternalExadataStorageServerSummary.
        :type: int
        """
        self._max_hard_disk_iops = max_hard_disk_iops

    @property
    def max_hard_disk_throughput(self):
        """
        Gets the max_hard_disk_throughput of this ExternalExadataStorageServerSummary.
        The maximum hard disk IO throughput in MB/s of the storage server


        :return: The max_hard_disk_throughput of this ExternalExadataStorageServerSummary.
        :rtype: int
        """
        return self._max_hard_disk_throughput

    @max_hard_disk_throughput.setter
    def max_hard_disk_throughput(self, max_hard_disk_throughput):
        """
        Sets the max_hard_disk_throughput of this ExternalExadataStorageServerSummary.
        The maximum hard disk IO throughput in MB/s of the storage server


        :param max_hard_disk_throughput: The max_hard_disk_throughput of this ExternalExadataStorageServerSummary.
        :type: int
        """
        self._max_hard_disk_throughput = max_hard_disk_throughput

    @property
    def max_flash_disk_iops(self):
        """
        Gets the max_flash_disk_iops of this ExternalExadataStorageServerSummary.
        The maximum flash disk IO operations per second of the storage server


        :return: The max_flash_disk_iops of this ExternalExadataStorageServerSummary.
        :rtype: int
        """
        return self._max_flash_disk_iops

    @max_flash_disk_iops.setter
    def max_flash_disk_iops(self, max_flash_disk_iops):
        """
        Sets the max_flash_disk_iops of this ExternalExadataStorageServerSummary.
        The maximum flash disk IO operations per second of the storage server


        :param max_flash_disk_iops: The max_flash_disk_iops of this ExternalExadataStorageServerSummary.
        :type: int
        """
        self._max_flash_disk_iops = max_flash_disk_iops

    @property
    def max_flash_disk_throughput(self):
        """
        Gets the max_flash_disk_throughput of this ExternalExadataStorageServerSummary.
        The maximum flash disk IO throughput in MB/s of the storage server


        :return: The max_flash_disk_throughput of this ExternalExadataStorageServerSummary.
        :rtype: int
        """
        return self._max_flash_disk_throughput

    @max_flash_disk_throughput.setter
    def max_flash_disk_throughput(self, max_flash_disk_throughput):
        """
        Sets the max_flash_disk_throughput of this ExternalExadataStorageServerSummary.
        The maximum flash disk IO throughput in MB/s of the storage server


        :param max_flash_disk_throughput: The max_flash_disk_throughput of this ExternalExadataStorageServerSummary.
        :type: int
        """
        self._max_flash_disk_throughput = max_flash_disk_throughput

    @property
    def connector_id(self):
        """
        Gets the connector_id of this ExternalExadataStorageServerSummary.
        The `OCID`__ of connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The connector_id of this ExternalExadataStorageServerSummary.
        :rtype: str
        """
        return self._connector_id

    @connector_id.setter
    def connector_id(self, connector_id):
        """
        Sets the connector_id of this ExternalExadataStorageServerSummary.
        The `OCID`__ of connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param connector_id: The connector_id of this ExternalExadataStorageServerSummary.
        :type: str
        """
        self._connector_id = connector_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
