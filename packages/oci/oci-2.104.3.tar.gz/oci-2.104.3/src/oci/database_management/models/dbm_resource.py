# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DbmResource(object):
    """
    The base exadata resource.
    """

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a DbmResource.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "INFRASTRUCTURE_SUMMARY"
    RESOURCE_TYPE_INFRASTRUCTURE_SUMMARY = "INFRASTRUCTURE_SUMMARY"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "INFRASTRUCTURE"
    RESOURCE_TYPE_INFRASTRUCTURE = "INFRASTRUCTURE"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "STORAGE_SERVER_SUMMARY"
    RESOURCE_TYPE_STORAGE_SERVER_SUMMARY = "STORAGE_SERVER_SUMMARY"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "STORAGE_SERVER"
    RESOURCE_TYPE_STORAGE_SERVER = "STORAGE_SERVER"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "STORAGE_GRID_SUMMARY"
    RESOURCE_TYPE_STORAGE_GRID_SUMMARY = "STORAGE_GRID_SUMMARY"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "STORAGE_GRID"
    RESOURCE_TYPE_STORAGE_GRID = "STORAGE_GRID"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "STORAGE_CONNECTOR_SUMMARY"
    RESOURCE_TYPE_STORAGE_CONNECTOR_SUMMARY = "STORAGE_CONNECTOR_SUMMARY"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "STORAGE_CONNECTOR"
    RESOURCE_TYPE_STORAGE_CONNECTOR = "STORAGE_CONNECTOR"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "DATABASE_SYSTEM_SUMMARY"
    RESOURCE_TYPE_DATABASE_SYSTEM_SUMMARY = "DATABASE_SYSTEM_SUMMARY"

    #: A constant which can be used with the resource_type property of a DbmResource.
    #: This constant has a value of "DATABASE_SUMMARY"
    RESOURCE_TYPE_DATABASE_SUMMARY = "DATABASE_SUMMARY"

    def __init__(self, **kwargs):
        """
        Initializes a new DbmResource object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.database_management.models.ExternalExadataStorageConnector`
        * :class:`~oci.database_management.models.ExternalExadataStorageGridSummary`
        * :class:`~oci.database_management.models.ExternalExadataStorageServer`
        * :class:`~oci.database_management.models.ExternalExadataInfrastructure`
        * :class:`~oci.database_management.models.ExternalExadataStorageGrid`
        * :class:`~oci.database_management.models.ExternalExadataInfrastructureSummary`
        * :class:`~oci.database_management.models.ExternalExadataDatabaseSystemSummary`
        * :class:`~oci.database_management.models.ExternalExadataStorageConnectorSummary`
        * :class:`~oci.database_management.models.ExternalExadataStorageServerSummary`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DbmResource.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this DbmResource.
        :type display_name: str

        :param version:
            The value to assign to the version property of this DbmResource.
        :type version: str

        :param internal_id:
            The value to assign to the internal_id property of this DbmResource.
        :type internal_id: str

        :param status:
            The value to assign to the status property of this DbmResource.
        :type status: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DbmResource.
            Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this DbmResource.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DbmResource.
        :type time_updated: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this DbmResource.
        :type lifecycle_details: str

        :param additional_details:
            The value to assign to the additional_details property of this DbmResource.
        :type additional_details: dict(str, str)

        :param resource_type:
            The value to assign to the resource_type property of this DbmResource.
            Allowed values for this property are: "INFRASTRUCTURE_SUMMARY", "INFRASTRUCTURE", "STORAGE_SERVER_SUMMARY", "STORAGE_SERVER", "STORAGE_GRID_SUMMARY", "STORAGE_GRID", "STORAGE_CONNECTOR_SUMMARY", "STORAGE_CONNECTOR", "DATABASE_SYSTEM_SUMMARY", "DATABASE_SUMMARY"
        :type resource_type: str

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
            'resource_type': 'str'
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
            'resource_type': 'resourceType'
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

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['resourceType']

        if type == 'STORAGE_CONNECTOR':
            return 'ExternalExadataStorageConnector'

        if type == 'STORAGE_GRID_SUMMARY':
            return 'ExternalExadataStorageGridSummary'

        if type == 'STORAGE_SERVER':
            return 'ExternalExadataStorageServer'

        if type == 'INFRASTRUCTURE':
            return 'ExternalExadataInfrastructure'

        if type == 'STORAGE_GRID':
            return 'ExternalExadataStorageGrid'

        if type == 'INFRASTRUCTURE_SUMMARY':
            return 'ExternalExadataInfrastructureSummary'

        if type == 'DATABASE_SYSTEM_SUMMARY':
            return 'ExternalExadataDatabaseSystemSummary'

        if type == 'STORAGE_CONNECTOR_SUMMARY':
            return 'ExternalExadataStorageConnectorSummary'

        if type == 'STORAGE_SERVER_SUMMARY':
            return 'ExternalExadataStorageServerSummary'
        else:
            return 'DbmResource'

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DbmResource.
        The `OCID`__ of the Exadata resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this DbmResource.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DbmResource.
        The `OCID`__ of the Exadata resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this DbmResource.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DbmResource.
        The name of the resource. English letters, numbers, \"-\", \"_\" and \".\" only.


        :return: The display_name of this DbmResource.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DbmResource.
        The name of the resource. English letters, numbers, \"-\", \"_\" and \".\" only.


        :param display_name: The display_name of this DbmResource.
        :type: str
        """
        self._display_name = display_name

    @property
    def version(self):
        """
        Gets the version of this DbmResource.
        The version of the resource.


        :return: The version of this DbmResource.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this DbmResource.
        The version of the resource.


        :param version: The version of this DbmResource.
        :type: str
        """
        self._version = version

    @property
    def internal_id(self):
        """
        Gets the internal_id of this DbmResource.
        The internal ID.


        :return: The internal_id of this DbmResource.
        :rtype: str
        """
        return self._internal_id

    @internal_id.setter
    def internal_id(self, internal_id):
        """
        Sets the internal_id of this DbmResource.
        The internal ID.


        :param internal_id: The internal_id of this DbmResource.
        :type: str
        """
        self._internal_id = internal_id

    @property
    def status(self):
        """
        Gets the status of this DbmResource.
        The status of the entity.


        :return: The status of this DbmResource.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this DbmResource.
        The status of the entity.


        :param status: The status of this DbmResource.
        :type: str
        """
        self._status = status

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this DbmResource.
        The current lifecycle state of the database resource.

        Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"


        :return: The lifecycle_state of this DbmResource.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DbmResource.
        The current lifecycle state of the database resource.


        :param lifecycle_state: The lifecycle_state of this DbmResource.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            raise ValueError(
                "Invalid value for `lifecycle_state`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        Gets the time_created of this DbmResource.
        The timestamp of the creation.


        :return: The time_created of this DbmResource.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this DbmResource.
        The timestamp of the creation.


        :param time_created: The time_created of this DbmResource.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this DbmResource.
        The timestamp of the last update.


        :return: The time_updated of this DbmResource.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this DbmResource.
        The timestamp of the last update.


        :param time_updated: The time_updated of this DbmResource.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this DbmResource.
        The details of the lifecycle state.


        :return: The lifecycle_details of this DbmResource.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this DbmResource.
        The details of the lifecycle state.


        :param lifecycle_details: The lifecycle_details of this DbmResource.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def additional_details(self):
        """
        Gets the additional_details of this DbmResource.
        The additional details of the resource defined in `{\"key\": \"value\"}` format.
        Example: `{\"bar-key\": \"value\"}`


        :return: The additional_details of this DbmResource.
        :rtype: dict(str, str)
        """
        return self._additional_details

    @additional_details.setter
    def additional_details(self, additional_details):
        """
        Sets the additional_details of this DbmResource.
        The additional details of the resource defined in `{\"key\": \"value\"}` format.
        Example: `{\"bar-key\": \"value\"}`


        :param additional_details: The additional_details of this DbmResource.
        :type: dict(str, str)
        """
        self._additional_details = additional_details

    @property
    def resource_type(self):
        """
        **[Required]** Gets the resource_type of this DbmResource.
        The type of resource.

        Allowed values for this property are: "INFRASTRUCTURE_SUMMARY", "INFRASTRUCTURE", "STORAGE_SERVER_SUMMARY", "STORAGE_SERVER", "STORAGE_GRID_SUMMARY", "STORAGE_GRID", "STORAGE_CONNECTOR_SUMMARY", "STORAGE_CONNECTOR", "DATABASE_SYSTEM_SUMMARY", "DATABASE_SUMMARY"


        :return: The resource_type of this DbmResource.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this DbmResource.
        The type of resource.


        :param resource_type: The resource_type of this DbmResource.
        :type: str
        """
        allowed_values = ["INFRASTRUCTURE_SUMMARY", "INFRASTRUCTURE", "STORAGE_SERVER_SUMMARY", "STORAGE_SERVER", "STORAGE_GRID_SUMMARY", "STORAGE_GRID", "STORAGE_CONNECTOR_SUMMARY", "STORAGE_CONNECTOR", "DATABASE_SYSTEM_SUMMARY", "DATABASE_SUMMARY"]
        if not value_allowed_none_or_none_sentinel(resource_type, allowed_values):
            raise ValueError(
                "Invalid value for `resource_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._resource_type = resource_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
