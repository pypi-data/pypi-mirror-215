# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DataSource(object):
    """
    Details of Data source
    """

    #: A constant which can be used with the data_source_feed_provider property of a DataSource.
    #: This constant has a value of "LOGGINGQUERY"
    DATA_SOURCE_FEED_PROVIDER_LOGGINGQUERY = "LOGGINGQUERY"

    #: A constant which can be used with the status property of a DataSource.
    #: This constant has a value of "ENABLED"
    STATUS_ENABLED = "ENABLED"

    #: A constant which can be used with the status property of a DataSource.
    #: This constant has a value of "DISABLED"
    STATUS_DISABLED = "DISABLED"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a DataSource.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new DataSource object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DataSource.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this DataSource.
        :type display_name: str

        :param data_source_feed_provider:
            The value to assign to the data_source_feed_provider property of this DataSource.
            Allowed values for this property are: "LOGGINGQUERY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type data_source_feed_provider: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DataSource.
        :type compartment_id: str

        :param data_source_details:
            The value to assign to the data_source_details property of this DataSource.
        :type data_source_details: oci.cloud_guard.models.DataSourceDetails

        :param time_created:
            The value to assign to the time_created property of this DataSource.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DataSource.
        :type time_updated: datetime

        :param status:
            The value to assign to the status property of this DataSource.
            Allowed values for this property are: "ENABLED", "DISABLED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param data_source_detector_mapping_info:
            The value to assign to the data_source_detector_mapping_info property of this DataSource.
        :type data_source_detector_mapping_info: list[oci.cloud_guard.models.DataSourceMappingInfo]

        :param region_status_detail:
            The value to assign to the region_status_detail property of this DataSource.
        :type region_status_detail: list[oci.cloud_guard.models.RegionStatusDetail]

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DataSource.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DataSource.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DataSource.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this DataSource.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'data_source_feed_provider': 'str',
            'compartment_id': 'str',
            'data_source_details': 'DataSourceDetails',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'status': 'str',
            'data_source_detector_mapping_info': 'list[DataSourceMappingInfo]',
            'region_status_detail': 'list[RegionStatusDetail]',
            'lifecycle_state': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'data_source_feed_provider': 'dataSourceFeedProvider',
            'compartment_id': 'compartmentId',
            'data_source_details': 'dataSourceDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'status': 'status',
            'data_source_detector_mapping_info': 'dataSourceDetectorMappingInfo',
            'region_status_detail': 'regionStatusDetail',
            'lifecycle_state': 'lifecycleState',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._display_name = None
        self._data_source_feed_provider = None
        self._compartment_id = None
        self._data_source_details = None
        self._time_created = None
        self._time_updated = None
        self._status = None
        self._data_source_detector_mapping_info = None
        self._region_status_detail = None
        self._lifecycle_state = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DataSource.
        Ocid for Data source


        :return: The id of this DataSource.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DataSource.
        Ocid for Data source


        :param id: The id of this DataSource.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DataSource.
        DisplayName of Data source.


        :return: The display_name of this DataSource.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DataSource.
        DisplayName of Data source.


        :param display_name: The display_name of this DataSource.
        :type: str
        """
        self._display_name = display_name

    @property
    def data_source_feed_provider(self):
        """
        **[Required]** Gets the data_source_feed_provider of this DataSource.
        Possible type of dataSourceFeed Provider(LoggingQuery)

        Allowed values for this property are: "LOGGINGQUERY", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The data_source_feed_provider of this DataSource.
        :rtype: str
        """
        return self._data_source_feed_provider

    @data_source_feed_provider.setter
    def data_source_feed_provider(self, data_source_feed_provider):
        """
        Sets the data_source_feed_provider of this DataSource.
        Possible type of dataSourceFeed Provider(LoggingQuery)


        :param data_source_feed_provider: The data_source_feed_provider of this DataSource.
        :type: str
        """
        allowed_values = ["LOGGINGQUERY"]
        if not value_allowed_none_or_none_sentinel(data_source_feed_provider, allowed_values):
            data_source_feed_provider = 'UNKNOWN_ENUM_VALUE'
        self._data_source_feed_provider = data_source_feed_provider

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DataSource.
        CompartmentId of Data source.


        :return: The compartment_id of this DataSource.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DataSource.
        CompartmentId of Data source.


        :param compartment_id: The compartment_id of this DataSource.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def data_source_details(self):
        """
        Gets the data_source_details of this DataSource.

        :return: The data_source_details of this DataSource.
        :rtype: oci.cloud_guard.models.DataSourceDetails
        """
        return self._data_source_details

    @data_source_details.setter
    def data_source_details(self, data_source_details):
        """
        Sets the data_source_details of this DataSource.

        :param data_source_details: The data_source_details of this DataSource.
        :type: oci.cloud_guard.models.DataSourceDetails
        """
        self._data_source_details = data_source_details

    @property
    def time_created(self):
        """
        Gets the time_created of this DataSource.
        The date and time the Data source was created. Format defined by RFC3339.


        :return: The time_created of this DataSource.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this DataSource.
        The date and time the Data source was created. Format defined by RFC3339.


        :param time_created: The time_created of this DataSource.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this DataSource.
        The date and time the Data source was updated. Format defined by RFC3339.


        :return: The time_updated of this DataSource.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this DataSource.
        The date and time the Data source was updated. Format defined by RFC3339.


        :param time_updated: The time_updated of this DataSource.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def status(self):
        """
        Gets the status of this DataSource.
        Status of data Source

        Allowed values for this property are: "ENABLED", "DISABLED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this DataSource.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this DataSource.
        Status of data Source


        :param status: The status of this DataSource.
        :type: str
        """
        allowed_values = ["ENABLED", "DISABLED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def data_source_detector_mapping_info(self):
        """
        Gets the data_source_detector_mapping_info of this DataSource.
        Information about the detector recipe and rule attached


        :return: The data_source_detector_mapping_info of this DataSource.
        :rtype: list[oci.cloud_guard.models.DataSourceMappingInfo]
        """
        return self._data_source_detector_mapping_info

    @data_source_detector_mapping_info.setter
    def data_source_detector_mapping_info(self, data_source_detector_mapping_info):
        """
        Sets the data_source_detector_mapping_info of this DataSource.
        Information about the detector recipe and rule attached


        :param data_source_detector_mapping_info: The data_source_detector_mapping_info of this DataSource.
        :type: list[oci.cloud_guard.models.DataSourceMappingInfo]
        """
        self._data_source_detector_mapping_info = data_source_detector_mapping_info

    @property
    def region_status_detail(self):
        """
        Gets the region_status_detail of this DataSource.
        Information about the region and status of query replication


        :return: The region_status_detail of this DataSource.
        :rtype: list[oci.cloud_guard.models.RegionStatusDetail]
        """
        return self._region_status_detail

    @region_status_detail.setter
    def region_status_detail(self, region_status_detail):
        """
        Sets the region_status_detail of this DataSource.
        Information about the region and status of query replication


        :param region_status_detail: The region_status_detail of this DataSource.
        :type: list[oci.cloud_guard.models.RegionStatusDetail]
        """
        self._region_status_detail = region_status_detail

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this DataSource.
        The current state of the resource.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DataSource.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DataSource.
        The current state of the resource.


        :param lifecycle_state: The lifecycle_state of this DataSource.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DataSource.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`

        Avoid entering confidential information.


        :return: The freeform_tags of this DataSource.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DataSource.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`

        Avoid entering confidential information.


        :param freeform_tags: The freeform_tags of this DataSource.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DataSource.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this DataSource.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DataSource.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this DataSource.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DataSource.
        System tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        System tags can be viewed by users, but can only be created by the system.

        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The system_tags of this DataSource.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DataSource.
        System tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        System tags can be viewed by users, but can only be created by the system.

        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param system_tags: The system_tags of this DataSource.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
