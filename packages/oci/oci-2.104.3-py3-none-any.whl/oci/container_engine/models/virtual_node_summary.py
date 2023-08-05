# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VirtualNodeSummary(object):
    """
    The properties that define a virtual node summary.
    """

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodeSummary.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    def __init__(self, **kwargs):
        """
        Initializes a new VirtualNodeSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this VirtualNodeSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this VirtualNodeSummary.
        :type display_name: str

        :param kubernetes_version:
            The value to assign to the kubernetes_version property of this VirtualNodeSummary.
        :type kubernetes_version: str

        :param virtual_node_pool_id:
            The value to assign to the virtual_node_pool_id property of this VirtualNodeSummary.
        :type virtual_node_pool_id: str

        :param availability_domain:
            The value to assign to the availability_domain property of this VirtualNodeSummary.
        :type availability_domain: str

        :param fault_domain:
            The value to assign to the fault_domain property of this VirtualNodeSummary.
        :type fault_domain: str

        :param subnet_id:
            The value to assign to the subnet_id property of this VirtualNodeSummary.
        :type subnet_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this VirtualNodeSummary.
        :type nsg_ids: list[str]

        :param private_ip:
            The value to assign to the private_ip property of this VirtualNodeSummary.
        :type private_ip: str

        :param virtual_node_error:
            The value to assign to the virtual_node_error property of this VirtualNodeSummary.
        :type virtual_node_error: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this VirtualNodeSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this VirtualNodeSummary.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this VirtualNodeSummary.
        :type time_created: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this VirtualNodeSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this VirtualNodeSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this VirtualNodeSummary.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'kubernetes_version': 'str',
            'virtual_node_pool_id': 'str',
            'availability_domain': 'str',
            'fault_domain': 'str',
            'subnet_id': 'str',
            'nsg_ids': 'list[str]',
            'private_ip': 'str',
            'virtual_node_error': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'kubernetes_version': 'kubernetesVersion',
            'virtual_node_pool_id': 'virtualNodePoolId',
            'availability_domain': 'availabilityDomain',
            'fault_domain': 'faultDomain',
            'subnet_id': 'subnetId',
            'nsg_ids': 'nsgIds',
            'private_ip': 'privateIp',
            'virtual_node_error': 'virtualNodeError',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._display_name = None
        self._kubernetes_version = None
        self._virtual_node_pool_id = None
        self._availability_domain = None
        self._fault_domain = None
        self._subnet_id = None
        self._nsg_ids = None
        self._private_ip = None
        self._virtual_node_error = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this VirtualNodeSummary.
        The ocid of the virtual node.


        :return: The id of this VirtualNodeSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VirtualNodeSummary.
        The ocid of the virtual node.


        :param id: The id of this VirtualNodeSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this VirtualNodeSummary.
        The name of the virtual node.


        :return: The display_name of this VirtualNodeSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this VirtualNodeSummary.
        The name of the virtual node.


        :param display_name: The display_name of this VirtualNodeSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def kubernetes_version(self):
        """
        Gets the kubernetes_version of this VirtualNodeSummary.
        The version of Kubernetes this virtual node is running.


        :return: The kubernetes_version of this VirtualNodeSummary.
        :rtype: str
        """
        return self._kubernetes_version

    @kubernetes_version.setter
    def kubernetes_version(self, kubernetes_version):
        """
        Sets the kubernetes_version of this VirtualNodeSummary.
        The version of Kubernetes this virtual node is running.


        :param kubernetes_version: The kubernetes_version of this VirtualNodeSummary.
        :type: str
        """
        self._kubernetes_version = kubernetes_version

    @property
    def virtual_node_pool_id(self):
        """
        **[Required]** Gets the virtual_node_pool_id of this VirtualNodeSummary.
        The ocid of the virtual node pool this virtual node belongs to.


        :return: The virtual_node_pool_id of this VirtualNodeSummary.
        :rtype: str
        """
        return self._virtual_node_pool_id

    @virtual_node_pool_id.setter
    def virtual_node_pool_id(self, virtual_node_pool_id):
        """
        Sets the virtual_node_pool_id of this VirtualNodeSummary.
        The ocid of the virtual node pool this virtual node belongs to.


        :param virtual_node_pool_id: The virtual_node_pool_id of this VirtualNodeSummary.
        :type: str
        """
        self._virtual_node_pool_id = virtual_node_pool_id

    @property
    def availability_domain(self):
        """
        Gets the availability_domain of this VirtualNodeSummary.
        The name of the availability domain in which this virtual node is placed


        :return: The availability_domain of this VirtualNodeSummary.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this VirtualNodeSummary.
        The name of the availability domain in which this virtual node is placed


        :param availability_domain: The availability_domain of this VirtualNodeSummary.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def fault_domain(self):
        """
        Gets the fault_domain of this VirtualNodeSummary.
        The fault domain of this virtual node.


        :return: The fault_domain of this VirtualNodeSummary.
        :rtype: str
        """
        return self._fault_domain

    @fault_domain.setter
    def fault_domain(self, fault_domain):
        """
        Sets the fault_domain of this VirtualNodeSummary.
        The fault domain of this virtual node.


        :param fault_domain: The fault_domain of this VirtualNodeSummary.
        :type: str
        """
        self._fault_domain = fault_domain

    @property
    def subnet_id(self):
        """
        Gets the subnet_id of this VirtualNodeSummary.
        The OCID of the subnet in which this Virtual Node is placed.


        :return: The subnet_id of this VirtualNodeSummary.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this VirtualNodeSummary.
        The OCID of the subnet in which this Virtual Node is placed.


        :param subnet_id: The subnet_id of this VirtualNodeSummary.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this VirtualNodeSummary.
        NSG Ids applied to virtual node vnic.


        :return: The nsg_ids of this VirtualNodeSummary.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this VirtualNodeSummary.
        NSG Ids applied to virtual node vnic.


        :param nsg_ids: The nsg_ids of this VirtualNodeSummary.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    @property
    def private_ip(self):
        """
        Gets the private_ip of this VirtualNodeSummary.
        The private IP address of this Virtual Node.


        :return: The private_ip of this VirtualNodeSummary.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this VirtualNodeSummary.
        The private IP address of this Virtual Node.


        :param private_ip: The private_ip of this VirtualNodeSummary.
        :type: str
        """
        self._private_ip = private_ip

    @property
    def virtual_node_error(self):
        """
        Gets the virtual_node_error of this VirtualNodeSummary.
        An error that may be associated with the virtual node.


        :return: The virtual_node_error of this VirtualNodeSummary.
        :rtype: str
        """
        return self._virtual_node_error

    @virtual_node_error.setter
    def virtual_node_error(self, virtual_node_error):
        """
        Sets the virtual_node_error of this VirtualNodeSummary.
        An error that may be associated with the virtual node.


        :param virtual_node_error: The virtual_node_error of this VirtualNodeSummary.
        :type: str
        """
        self._virtual_node_error = virtual_node_error

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this VirtualNodeSummary.
        The state of the Virtual Node.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this VirtualNodeSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this VirtualNodeSummary.
        The state of the Virtual Node.


        :param lifecycle_state: The lifecycle_state of this VirtualNodeSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this VirtualNodeSummary.
        Details about the state of the Virtual Node.


        :return: The lifecycle_details of this VirtualNodeSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this VirtualNodeSummary.
        Details about the state of the Virtual Node.


        :param lifecycle_details: The lifecycle_details of this VirtualNodeSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        Gets the time_created of this VirtualNodeSummary.
        The time at which the virtual node was created.


        :return: The time_created of this VirtualNodeSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this VirtualNodeSummary.
        The time at which the virtual node was created.


        :param time_created: The time_created of this VirtualNodeSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this VirtualNodeSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this VirtualNodeSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this VirtualNodeSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this VirtualNodeSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this VirtualNodeSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this VirtualNodeSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this VirtualNodeSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this VirtualNodeSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this VirtualNodeSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this VirtualNodeSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this VirtualNodeSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this VirtualNodeSummary.
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
