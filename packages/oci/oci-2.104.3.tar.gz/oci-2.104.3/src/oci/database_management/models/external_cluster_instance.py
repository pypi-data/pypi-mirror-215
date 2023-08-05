# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalClusterInstance(object):
    """
    The details of an external cluster instance.
    """

    #: A constant which can be used with the node_role property of a ExternalClusterInstance.
    #: This constant has a value of "HUB"
    NODE_ROLE_HUB = "HUB"

    #: A constant which can be used with the node_role property of a ExternalClusterInstance.
    #: This constant has a value of "LEAF"
    NODE_ROLE_LEAF = "LEAF"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "NOT_CONNECTED"
    LIFECYCLE_STATE_NOT_CONNECTED = "NOT_CONNECTED"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ExternalClusterInstance.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalClusterInstance object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalClusterInstance.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalClusterInstance.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this ExternalClusterInstance.
        :type component_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalClusterInstance.
        :type compartment_id: str

        :param external_cluster_id:
            The value to assign to the external_cluster_id property of this ExternalClusterInstance.
        :type external_cluster_id: str

        :param external_db_system_id:
            The value to assign to the external_db_system_id property of this ExternalClusterInstance.
        :type external_db_system_id: str

        :param external_db_node_id:
            The value to assign to the external_db_node_id property of this ExternalClusterInstance.
        :type external_db_node_id: str

        :param external_connector_id:
            The value to assign to the external_connector_id property of this ExternalClusterInstance.
        :type external_connector_id: str

        :param host_name:
            The value to assign to the host_name property of this ExternalClusterInstance.
        :type host_name: str

        :param node_role:
            The value to assign to the node_role property of this ExternalClusterInstance.
            Allowed values for this property are: "HUB", "LEAF", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type node_role: str

        :param crs_base_directory:
            The value to assign to the crs_base_directory property of this ExternalClusterInstance.
        :type crs_base_directory: str

        :param adr_home_directory:
            The value to assign to the adr_home_directory property of this ExternalClusterInstance.
        :type adr_home_directory: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalClusterInstance.
            Allowed values for this property are: "CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalClusterInstance.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this ExternalClusterInstance.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalClusterInstance.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'compartment_id': 'str',
            'external_cluster_id': 'str',
            'external_db_system_id': 'str',
            'external_db_node_id': 'str',
            'external_connector_id': 'str',
            'host_name': 'str',
            'node_role': 'str',
            'crs_base_directory': 'str',
            'adr_home_directory': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'compartment_id': 'compartmentId',
            'external_cluster_id': 'externalClusterId',
            'external_db_system_id': 'externalDbSystemId',
            'external_db_node_id': 'externalDbNodeId',
            'external_connector_id': 'externalConnectorId',
            'host_name': 'hostName',
            'node_role': 'nodeRole',
            'crs_base_directory': 'crsBaseDirectory',
            'adr_home_directory': 'adrHomeDirectory',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }

        self._id = None
        self._display_name = None
        self._component_name = None
        self._compartment_id = None
        self._external_cluster_id = None
        self._external_db_system_id = None
        self._external_db_node_id = None
        self._external_connector_id = None
        self._host_name = None
        self._node_role = None
        self._crs_base_directory = None
        self._adr_home_directory = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalClusterInstance.
        The `OCID`__ of the external cluster instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalClusterInstance.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalClusterInstance.
        The `OCID`__ of the external cluster instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalClusterInstance.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalClusterInstance.
        The user-friendly name for the cluster instance. The name does not have to be unique.


        :return: The display_name of this ExternalClusterInstance.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalClusterInstance.
        The user-friendly name for the cluster instance. The name does not have to be unique.


        :param display_name: The display_name of this ExternalClusterInstance.
        :type: str
        """
        self._display_name = display_name

    @property
    def component_name(self):
        """
        **[Required]** Gets the component_name of this ExternalClusterInstance.
        The name of the external cluster instance.


        :return: The component_name of this ExternalClusterInstance.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """
        Sets the component_name of this ExternalClusterInstance.
        The name of the external cluster instance.


        :param component_name: The component_name of this ExternalClusterInstance.
        :type: str
        """
        self._component_name = component_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExternalClusterInstance.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalClusterInstance.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalClusterInstance.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalClusterInstance.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def external_cluster_id(self):
        """
        **[Required]** Gets the external_cluster_id of this ExternalClusterInstance.
        The `OCID`__ of the external cluster that the cluster instance belongs to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_cluster_id of this ExternalClusterInstance.
        :rtype: str
        """
        return self._external_cluster_id

    @external_cluster_id.setter
    def external_cluster_id(self, external_cluster_id):
        """
        Sets the external_cluster_id of this ExternalClusterInstance.
        The `OCID`__ of the external cluster that the cluster instance belongs to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_cluster_id: The external_cluster_id of this ExternalClusterInstance.
        :type: str
        """
        self._external_cluster_id = external_cluster_id

    @property
    def external_db_system_id(self):
        """
        **[Required]** Gets the external_db_system_id of this ExternalClusterInstance.
        The `OCID`__ of the external DB system that the cluster instance is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_system_id of this ExternalClusterInstance.
        :rtype: str
        """
        return self._external_db_system_id

    @external_db_system_id.setter
    def external_db_system_id(self, external_db_system_id):
        """
        Sets the external_db_system_id of this ExternalClusterInstance.
        The `OCID`__ of the external DB system that the cluster instance is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_system_id: The external_db_system_id of this ExternalClusterInstance.
        :type: str
        """
        self._external_db_system_id = external_db_system_id

    @property
    def external_db_node_id(self):
        """
        Gets the external_db_node_id of this ExternalClusterInstance.
        The `OCID`__ of the external DB node.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_node_id of this ExternalClusterInstance.
        :rtype: str
        """
        return self._external_db_node_id

    @external_db_node_id.setter
    def external_db_node_id(self, external_db_node_id):
        """
        Sets the external_db_node_id of this ExternalClusterInstance.
        The `OCID`__ of the external DB node.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_node_id: The external_db_node_id of this ExternalClusterInstance.
        :type: str
        """
        self._external_db_node_id = external_db_node_id

    @property
    def external_connector_id(self):
        """
        Gets the external_connector_id of this ExternalClusterInstance.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_connector_id of this ExternalClusterInstance.
        :rtype: str
        """
        return self._external_connector_id

    @external_connector_id.setter
    def external_connector_id(self, external_connector_id):
        """
        Sets the external_connector_id of this ExternalClusterInstance.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_connector_id: The external_connector_id of this ExternalClusterInstance.
        :type: str
        """
        self._external_connector_id = external_connector_id

    @property
    def host_name(self):
        """
        Gets the host_name of this ExternalClusterInstance.
        The name of the host on which the cluster instance is running.


        :return: The host_name of this ExternalClusterInstance.
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """
        Sets the host_name of this ExternalClusterInstance.
        The name of the host on which the cluster instance is running.


        :param host_name: The host_name of this ExternalClusterInstance.
        :type: str
        """
        self._host_name = host_name

    @property
    def node_role(self):
        """
        Gets the node_role of this ExternalClusterInstance.
        The role of the cluster node.

        Allowed values for this property are: "HUB", "LEAF", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The node_role of this ExternalClusterInstance.
        :rtype: str
        """
        return self._node_role

    @node_role.setter
    def node_role(self, node_role):
        """
        Sets the node_role of this ExternalClusterInstance.
        The role of the cluster node.


        :param node_role: The node_role of this ExternalClusterInstance.
        :type: str
        """
        allowed_values = ["HUB", "LEAF"]
        if not value_allowed_none_or_none_sentinel(node_role, allowed_values):
            node_role = 'UNKNOWN_ENUM_VALUE'
        self._node_role = node_role

    @property
    def crs_base_directory(self):
        """
        Gets the crs_base_directory of this ExternalClusterInstance.
        The Oracle base location of Cluster Ready Services (CRS).


        :return: The crs_base_directory of this ExternalClusterInstance.
        :rtype: str
        """
        return self._crs_base_directory

    @crs_base_directory.setter
    def crs_base_directory(self, crs_base_directory):
        """
        Sets the crs_base_directory of this ExternalClusterInstance.
        The Oracle base location of Cluster Ready Services (CRS).


        :param crs_base_directory: The crs_base_directory of this ExternalClusterInstance.
        :type: str
        """
        self._crs_base_directory = crs_base_directory

    @property
    def adr_home_directory(self):
        """
        Gets the adr_home_directory of this ExternalClusterInstance.
        The Automatic Diagnostic Repository (ADR) home directory for the cluster instance.


        :return: The adr_home_directory of this ExternalClusterInstance.
        :rtype: str
        """
        return self._adr_home_directory

    @adr_home_directory.setter
    def adr_home_directory(self, adr_home_directory):
        """
        Sets the adr_home_directory of this ExternalClusterInstance.
        The Automatic Diagnostic Repository (ADR) home directory for the cluster instance.


        :param adr_home_directory: The adr_home_directory of this ExternalClusterInstance.
        :type: str
        """
        self._adr_home_directory = adr_home_directory

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExternalClusterInstance.
        The current lifecycle state of the external cluster instance.

        Allowed values for this property are: "CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ExternalClusterInstance.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExternalClusterInstance.
        The current lifecycle state of the external cluster instance.


        :param lifecycle_state: The lifecycle_state of this ExternalClusterInstance.
        :type: str
        """
        allowed_values = ["CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ExternalClusterInstance.
        Additional information about the current lifecycle state.


        :return: The lifecycle_details of this ExternalClusterInstance.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ExternalClusterInstance.
        Additional information about the current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this ExternalClusterInstance.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        Gets the time_created of this ExternalClusterInstance.
        The date and time the external cluster instance was created.


        :return: The time_created of this ExternalClusterInstance.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExternalClusterInstance.
        The date and time the external cluster instance was created.


        :param time_created: The time_created of this ExternalClusterInstance.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ExternalClusterInstance.
        The date and time the external cluster instance was last updated.


        :return: The time_updated of this ExternalClusterInstance.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ExternalClusterInstance.
        The date and time the external cluster instance was last updated.


        :param time_updated: The time_updated of this ExternalClusterInstance.
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
