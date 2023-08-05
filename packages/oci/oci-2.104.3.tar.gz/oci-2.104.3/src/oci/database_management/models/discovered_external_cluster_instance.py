# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .discovered_external_db_system_component import DiscoveredExternalDbSystemComponent
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DiscoveredExternalClusterInstance(DiscoveredExternalDbSystemComponent):
    """
    The details of an external cluster instance discovered in an external DB system discovery run.
    """

    #: A constant which can be used with the node_role property of a DiscoveredExternalClusterInstance.
    #: This constant has a value of "HUB"
    NODE_ROLE_HUB = "HUB"

    #: A constant which can be used with the node_role property of a DiscoveredExternalClusterInstance.
    #: This constant has a value of "LEAF"
    NODE_ROLE_LEAF = "LEAF"

    def __init__(self, **kwargs):
        """
        Initializes a new DiscoveredExternalClusterInstance object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.DiscoveredExternalClusterInstance.component_type` attribute
        of this class is ``CLUSTER_INSTANCE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param component_id:
            The value to assign to the component_id property of this DiscoveredExternalClusterInstance.
        :type component_id: str

        :param display_name:
            The value to assign to the display_name property of this DiscoveredExternalClusterInstance.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this DiscoveredExternalClusterInstance.
        :type component_name: str

        :param component_type:
            The value to assign to the component_type property of this DiscoveredExternalClusterInstance.
            Allowed values for this property are: "ASM", "ASM_INSTANCE", "CLUSTER", "CLUSTER_INSTANCE", "DATABASE", "DATABASE_INSTANCE", "DATABASE_HOME", "DATABASE_NODE", "DBSYSTEM", "LISTENER", "PLUGGABLE_DATABASE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type component_type: str

        :param resource_id:
            The value to assign to the resource_id property of this DiscoveredExternalClusterInstance.
        :type resource_id: str

        :param is_selected_for_monitoring:
            The value to assign to the is_selected_for_monitoring property of this DiscoveredExternalClusterInstance.
        :type is_selected_for_monitoring: bool

        :param status:
            The value to assign to the status property of this DiscoveredExternalClusterInstance.
            Allowed values for this property are: "NEW", "EXISTING", "MARKED_FOR_DELETION", "UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param associated_components:
            The value to assign to the associated_components property of this DiscoveredExternalClusterInstance.
        :type associated_components: list[oci.database_management.models.AssociatedComponent]

        :param host_name:
            The value to assign to the host_name property of this DiscoveredExternalClusterInstance.
        :type host_name: str

        :param cluster_id:
            The value to assign to the cluster_id property of this DiscoveredExternalClusterInstance.
        :type cluster_id: str

        :param node_role:
            The value to assign to the node_role property of this DiscoveredExternalClusterInstance.
            Allowed values for this property are: "HUB", "LEAF", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type node_role: str

        :param crs_base_directory:
            The value to assign to the crs_base_directory property of this DiscoveredExternalClusterInstance.
        :type crs_base_directory: str

        :param adr_home_directory:
            The value to assign to the adr_home_directory property of this DiscoveredExternalClusterInstance.
        :type adr_home_directory: str

        :param connector:
            The value to assign to the connector property of this DiscoveredExternalClusterInstance.
        :type connector: oci.database_management.models.ExternalDbSystemDiscoveryConnector

        """
        self.swagger_types = {
            'component_id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'component_type': 'str',
            'resource_id': 'str',
            'is_selected_for_monitoring': 'bool',
            'status': 'str',
            'associated_components': 'list[AssociatedComponent]',
            'host_name': 'str',
            'cluster_id': 'str',
            'node_role': 'str',
            'crs_base_directory': 'str',
            'adr_home_directory': 'str',
            'connector': 'ExternalDbSystemDiscoveryConnector'
        }

        self.attribute_map = {
            'component_id': 'componentId',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'component_type': 'componentType',
            'resource_id': 'resourceId',
            'is_selected_for_monitoring': 'isSelectedForMonitoring',
            'status': 'status',
            'associated_components': 'associatedComponents',
            'host_name': 'hostName',
            'cluster_id': 'clusterId',
            'node_role': 'nodeRole',
            'crs_base_directory': 'crsBaseDirectory',
            'adr_home_directory': 'adrHomeDirectory',
            'connector': 'connector'
        }

        self._component_id = None
        self._display_name = None
        self._component_name = None
        self._component_type = None
        self._resource_id = None
        self._is_selected_for_monitoring = None
        self._status = None
        self._associated_components = None
        self._host_name = None
        self._cluster_id = None
        self._node_role = None
        self._crs_base_directory = None
        self._adr_home_directory = None
        self._connector = None
        self._component_type = 'CLUSTER_INSTANCE'

    @property
    def host_name(self):
        """
        **[Required]** Gets the host_name of this DiscoveredExternalClusterInstance.
        The name of the host on which the cluster instance is running.


        :return: The host_name of this DiscoveredExternalClusterInstance.
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """
        Sets the host_name of this DiscoveredExternalClusterInstance.
        The name of the host on which the cluster instance is running.


        :param host_name: The host_name of this DiscoveredExternalClusterInstance.
        :type: str
        """
        self._host_name = host_name

    @property
    def cluster_id(self):
        """
        Gets the cluster_id of this DiscoveredExternalClusterInstance.
        The unique identifier of the Oracle cluster.


        :return: The cluster_id of this DiscoveredExternalClusterInstance.
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """
        Sets the cluster_id of this DiscoveredExternalClusterInstance.
        The unique identifier of the Oracle cluster.


        :param cluster_id: The cluster_id of this DiscoveredExternalClusterInstance.
        :type: str
        """
        self._cluster_id = cluster_id

    @property
    def node_role(self):
        """
        Gets the node_role of this DiscoveredExternalClusterInstance.
        The role of the cluster node.

        Allowed values for this property are: "HUB", "LEAF", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The node_role of this DiscoveredExternalClusterInstance.
        :rtype: str
        """
        return self._node_role

    @node_role.setter
    def node_role(self, node_role):
        """
        Sets the node_role of this DiscoveredExternalClusterInstance.
        The role of the cluster node.


        :param node_role: The node_role of this DiscoveredExternalClusterInstance.
        :type: str
        """
        allowed_values = ["HUB", "LEAF"]
        if not value_allowed_none_or_none_sentinel(node_role, allowed_values):
            node_role = 'UNKNOWN_ENUM_VALUE'
        self._node_role = node_role

    @property
    def crs_base_directory(self):
        """
        Gets the crs_base_directory of this DiscoveredExternalClusterInstance.
        The Oracle base location of Cluster Ready Services (CRS).


        :return: The crs_base_directory of this DiscoveredExternalClusterInstance.
        :rtype: str
        """
        return self._crs_base_directory

    @crs_base_directory.setter
    def crs_base_directory(self, crs_base_directory):
        """
        Sets the crs_base_directory of this DiscoveredExternalClusterInstance.
        The Oracle base location of Cluster Ready Services (CRS).


        :param crs_base_directory: The crs_base_directory of this DiscoveredExternalClusterInstance.
        :type: str
        """
        self._crs_base_directory = crs_base_directory

    @property
    def adr_home_directory(self):
        """
        Gets the adr_home_directory of this DiscoveredExternalClusterInstance.
        The Automatic Diagnostic Repository (ADR) home directory for the cluster instance.


        :return: The adr_home_directory of this DiscoveredExternalClusterInstance.
        :rtype: str
        """
        return self._adr_home_directory

    @adr_home_directory.setter
    def adr_home_directory(self, adr_home_directory):
        """
        Sets the adr_home_directory of this DiscoveredExternalClusterInstance.
        The Automatic Diagnostic Repository (ADR) home directory for the cluster instance.


        :param adr_home_directory: The adr_home_directory of this DiscoveredExternalClusterInstance.
        :type: str
        """
        self._adr_home_directory = adr_home_directory

    @property
    def connector(self):
        """
        Gets the connector of this DiscoveredExternalClusterInstance.

        :return: The connector of this DiscoveredExternalClusterInstance.
        :rtype: oci.database_management.models.ExternalDbSystemDiscoveryConnector
        """
        return self._connector

    @connector.setter
    def connector(self, connector):
        """
        Sets the connector of this DiscoveredExternalClusterInstance.

        :param connector: The connector of this DiscoveredExternalClusterInstance.
        :type: oci.database_management.models.ExternalDbSystemDiscoveryConnector
        """
        self._connector = connector

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
