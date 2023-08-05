# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalCluster(object):
    """
    The details of an external cluster.
    """

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "NOT_CONNECTED"
    LIFECYCLE_STATE_NOT_CONNECTED = "NOT_CONNECTED"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ExternalCluster.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalCluster object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalCluster.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalCluster.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this ExternalCluster.
        :type component_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalCluster.
        :type compartment_id: str

        :param external_db_system_id:
            The value to assign to the external_db_system_id property of this ExternalCluster.
        :type external_db_system_id: str

        :param external_connector_id:
            The value to assign to the external_connector_id property of this ExternalCluster.
        :type external_connector_id: str

        :param grid_home:
            The value to assign to the grid_home property of this ExternalCluster.
        :type grid_home: str

        :param is_flex_cluster:
            The value to assign to the is_flex_cluster property of this ExternalCluster.
        :type is_flex_cluster: bool

        :param additional_details:
            The value to assign to the additional_details property of this ExternalCluster.
        :type additional_details: dict(str, str)

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalCluster.
            Allowed values for this property are: "CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalCluster.
        :type lifecycle_details: str

        :param network_configurations:
            The value to assign to the network_configurations property of this ExternalCluster.
        :type network_configurations: list[oci.database_management.models.ExternalClusterNetworkConfiguration]

        :param vip_configurations:
            The value to assign to the vip_configurations property of this ExternalCluster.
        :type vip_configurations: list[oci.database_management.models.ExternalClusterVipConfiguration]

        :param scan_configurations:
            The value to assign to the scan_configurations property of this ExternalCluster.
        :type scan_configurations: list[oci.database_management.models.ExternalClusterScanListenerConfiguration]

        :param ocr_file_location:
            The value to assign to the ocr_file_location property of this ExternalCluster.
        :type ocr_file_location: str

        :param time_created:
            The value to assign to the time_created property of this ExternalCluster.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalCluster.
        :type time_updated: datetime

        :param version:
            The value to assign to the version property of this ExternalCluster.
        :type version: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'compartment_id': 'str',
            'external_db_system_id': 'str',
            'external_connector_id': 'str',
            'grid_home': 'str',
            'is_flex_cluster': 'bool',
            'additional_details': 'dict(str, str)',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'network_configurations': 'list[ExternalClusterNetworkConfiguration]',
            'vip_configurations': 'list[ExternalClusterVipConfiguration]',
            'scan_configurations': 'list[ExternalClusterScanListenerConfiguration]',
            'ocr_file_location': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'version': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'compartment_id': 'compartmentId',
            'external_db_system_id': 'externalDbSystemId',
            'external_connector_id': 'externalConnectorId',
            'grid_home': 'gridHome',
            'is_flex_cluster': 'isFlexCluster',
            'additional_details': 'additionalDetails',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'network_configurations': 'networkConfigurations',
            'vip_configurations': 'vipConfigurations',
            'scan_configurations': 'scanConfigurations',
            'ocr_file_location': 'ocrFileLocation',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'version': 'version'
        }

        self._id = None
        self._display_name = None
        self._component_name = None
        self._compartment_id = None
        self._external_db_system_id = None
        self._external_connector_id = None
        self._grid_home = None
        self._is_flex_cluster = None
        self._additional_details = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._network_configurations = None
        self._vip_configurations = None
        self._scan_configurations = None
        self._ocr_file_location = None
        self._time_created = None
        self._time_updated = None
        self._version = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalCluster.
        The `OCID`__ of the external cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalCluster.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalCluster.
        The `OCID`__ of the external cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalCluster.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalCluster.
        The user-friendly name for the external cluster. The name does not have to be unique.


        :return: The display_name of this ExternalCluster.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalCluster.
        The user-friendly name for the external cluster. The name does not have to be unique.


        :param display_name: The display_name of this ExternalCluster.
        :type: str
        """
        self._display_name = display_name

    @property
    def component_name(self):
        """
        **[Required]** Gets the component_name of this ExternalCluster.
        The name of the external cluster.


        :return: The component_name of this ExternalCluster.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """
        Sets the component_name of this ExternalCluster.
        The name of the external cluster.


        :param component_name: The component_name of this ExternalCluster.
        :type: str
        """
        self._component_name = component_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExternalCluster.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalCluster.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalCluster.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalCluster.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def external_db_system_id(self):
        """
        **[Required]** Gets the external_db_system_id of this ExternalCluster.
        The `OCID`__ of the external DB system that the cluster is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_system_id of this ExternalCluster.
        :rtype: str
        """
        return self._external_db_system_id

    @external_db_system_id.setter
    def external_db_system_id(self, external_db_system_id):
        """
        Sets the external_db_system_id of this ExternalCluster.
        The `OCID`__ of the external DB system that the cluster is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_system_id: The external_db_system_id of this ExternalCluster.
        :type: str
        """
        self._external_db_system_id = external_db_system_id

    @property
    def external_connector_id(self):
        """
        Gets the external_connector_id of this ExternalCluster.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_connector_id of this ExternalCluster.
        :rtype: str
        """
        return self._external_connector_id

    @external_connector_id.setter
    def external_connector_id(self, external_connector_id):
        """
        Sets the external_connector_id of this ExternalCluster.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_connector_id: The external_connector_id of this ExternalCluster.
        :type: str
        """
        self._external_connector_id = external_connector_id

    @property
    def grid_home(self):
        """
        Gets the grid_home of this ExternalCluster.
        The directory in which Oracle Grid Infrastructure is installed.


        :return: The grid_home of this ExternalCluster.
        :rtype: str
        """
        return self._grid_home

    @grid_home.setter
    def grid_home(self, grid_home):
        """
        Sets the grid_home of this ExternalCluster.
        The directory in which Oracle Grid Infrastructure is installed.


        :param grid_home: The grid_home of this ExternalCluster.
        :type: str
        """
        self._grid_home = grid_home

    @property
    def is_flex_cluster(self):
        """
        Gets the is_flex_cluster of this ExternalCluster.
        Indicates whether the cluster is Oracle Flex Cluster or not.


        :return: The is_flex_cluster of this ExternalCluster.
        :rtype: bool
        """
        return self._is_flex_cluster

    @is_flex_cluster.setter
    def is_flex_cluster(self, is_flex_cluster):
        """
        Sets the is_flex_cluster of this ExternalCluster.
        Indicates whether the cluster is Oracle Flex Cluster or not.


        :param is_flex_cluster: The is_flex_cluster of this ExternalCluster.
        :type: bool
        """
        self._is_flex_cluster = is_flex_cluster

    @property
    def additional_details(self):
        """
        Gets the additional_details of this ExternalCluster.
        The additional details of the external cluster defined in `{\"key\": \"value\"}` format.
        Example: `{\"bar-key\": \"value\"}`


        :return: The additional_details of this ExternalCluster.
        :rtype: dict(str, str)
        """
        return self._additional_details

    @additional_details.setter
    def additional_details(self, additional_details):
        """
        Sets the additional_details of this ExternalCluster.
        The additional details of the external cluster defined in `{\"key\": \"value\"}` format.
        Example: `{\"bar-key\": \"value\"}`


        :param additional_details: The additional_details of this ExternalCluster.
        :type: dict(str, str)
        """
        self._additional_details = additional_details

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExternalCluster.
        The current lifecycle state of the external cluster.

        Allowed values for this property are: "CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ExternalCluster.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExternalCluster.
        The current lifecycle state of the external cluster.


        :param lifecycle_state: The lifecycle_state of this ExternalCluster.
        :type: str
        """
        allowed_values = ["CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ExternalCluster.
        Additional information about the current lifecycle state.


        :return: The lifecycle_details of this ExternalCluster.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ExternalCluster.
        Additional information about the current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this ExternalCluster.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def network_configurations(self):
        """
        Gets the network_configurations of this ExternalCluster.
        The list of network address configurations of the external cluster.


        :return: The network_configurations of this ExternalCluster.
        :rtype: list[oci.database_management.models.ExternalClusterNetworkConfiguration]
        """
        return self._network_configurations

    @network_configurations.setter
    def network_configurations(self, network_configurations):
        """
        Sets the network_configurations of this ExternalCluster.
        The list of network address configurations of the external cluster.


        :param network_configurations: The network_configurations of this ExternalCluster.
        :type: list[oci.database_management.models.ExternalClusterNetworkConfiguration]
        """
        self._network_configurations = network_configurations

    @property
    def vip_configurations(self):
        """
        Gets the vip_configurations of this ExternalCluster.
        The list of Virtual IP (VIP) configurations of the external cluster.


        :return: The vip_configurations of this ExternalCluster.
        :rtype: list[oci.database_management.models.ExternalClusterVipConfiguration]
        """
        return self._vip_configurations

    @vip_configurations.setter
    def vip_configurations(self, vip_configurations):
        """
        Sets the vip_configurations of this ExternalCluster.
        The list of Virtual IP (VIP) configurations of the external cluster.


        :param vip_configurations: The vip_configurations of this ExternalCluster.
        :type: list[oci.database_management.models.ExternalClusterVipConfiguration]
        """
        self._vip_configurations = vip_configurations

    @property
    def scan_configurations(self):
        """
        Gets the scan_configurations of this ExternalCluster.
        The list of Single Client Access Name (SCAN) configurations of the external cluster.


        :return: The scan_configurations of this ExternalCluster.
        :rtype: list[oci.database_management.models.ExternalClusterScanListenerConfiguration]
        """
        return self._scan_configurations

    @scan_configurations.setter
    def scan_configurations(self, scan_configurations):
        """
        Sets the scan_configurations of this ExternalCluster.
        The list of Single Client Access Name (SCAN) configurations of the external cluster.


        :param scan_configurations: The scan_configurations of this ExternalCluster.
        :type: list[oci.database_management.models.ExternalClusterScanListenerConfiguration]
        """
        self._scan_configurations = scan_configurations

    @property
    def ocr_file_location(self):
        """
        Gets the ocr_file_location of this ExternalCluster.
        The location of the Oracle Cluster Registry (OCR).


        :return: The ocr_file_location of this ExternalCluster.
        :rtype: str
        """
        return self._ocr_file_location

    @ocr_file_location.setter
    def ocr_file_location(self, ocr_file_location):
        """
        Sets the ocr_file_location of this ExternalCluster.
        The location of the Oracle Cluster Registry (OCR).


        :param ocr_file_location: The ocr_file_location of this ExternalCluster.
        :type: str
        """
        self._ocr_file_location = ocr_file_location

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ExternalCluster.
        The date and time the external cluster was created.


        :return: The time_created of this ExternalCluster.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExternalCluster.
        The date and time the external cluster was created.


        :param time_created: The time_created of this ExternalCluster.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this ExternalCluster.
        The date and time the external cluster was last updated.


        :return: The time_updated of this ExternalCluster.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ExternalCluster.
        The date and time the external cluster was last updated.


        :param time_updated: The time_updated of this ExternalCluster.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def version(self):
        """
        Gets the version of this ExternalCluster.
        The cluster version.


        :return: The version of this ExternalCluster.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ExternalCluster.
        The cluster version.


        :param version: The version of this ExternalCluster.
        :type: str
        """
        self._version = version

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
