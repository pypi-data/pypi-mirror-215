# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VbInstance(object):
    """
    Description of Vb Instance.
    """

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a VbInstance.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the consumption_model property of a VbInstance.
    #: This constant has a value of "UCM"
    CONSUMPTION_MODEL_UCM = "UCM"

    #: A constant which can be used with the consumption_model property of a VbInstance.
    #: This constant has a value of "GOV"
    CONSUMPTION_MODEL_GOV = "GOV"

    #: A constant which can be used with the consumption_model property of a VbInstance.
    #: This constant has a value of "VB4SAAS"
    CONSUMPTION_MODEL_VB4_SAAS = "VB4SAAS"

    def __init__(self, **kwargs):
        """
        Initializes a new VbInstance object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this VbInstance.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this VbInstance.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this VbInstance.
        :type compartment_id: str

        :param time_created:
            The value to assign to the time_created property of this VbInstance.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this VbInstance.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this VbInstance.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param state_message:
            The value to assign to the state_message property of this VbInstance.
        :type state_message: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this VbInstance.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this VbInstance.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this VbInstance.
        :type system_tags: dict(str, dict(str, object))

        :param instance_url:
            The value to assign to the instance_url property of this VbInstance.
        :type instance_url: str

        :param node_count:
            The value to assign to the node_count property of this VbInstance.
        :type node_count: int

        :param is_visual_builder_enabled:
            The value to assign to the is_visual_builder_enabled property of this VbInstance.
        :type is_visual_builder_enabled: bool

        :param custom_endpoint:
            The value to assign to the custom_endpoint property of this VbInstance.
        :type custom_endpoint: oci.visual_builder.models.CustomEndpointDetails

        :param alternate_custom_endpoints:
            The value to assign to the alternate_custom_endpoints property of this VbInstance.
        :type alternate_custom_endpoints: list[oci.visual_builder.models.CustomEndpointDetails]

        :param consumption_model:
            The value to assign to the consumption_model property of this VbInstance.
            Allowed values for this property are: "UCM", "GOV", "VB4SAAS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type consumption_model: str

        :param idcs_info:
            The value to assign to the idcs_info property of this VbInstance.
        :type idcs_info: oci.visual_builder.models.IdcsInfoDetails

        :param attachments:
            The value to assign to the attachments property of this VbInstance.
        :type attachments: list[oci.visual_builder.models.AttachmentDetails]

        :param service_nat_gateway_ip:
            The value to assign to the service_nat_gateway_ip property of this VbInstance.
        :type service_nat_gateway_ip: str

        :param management_nat_gateway_ip:
            The value to assign to the management_nat_gateway_ip property of this VbInstance.
        :type management_nat_gateway_ip: str

        :param service_vcn_id:
            The value to assign to the service_vcn_id property of this VbInstance.
        :type service_vcn_id: str

        :param management_vcn_id:
            The value to assign to the management_vcn_id property of this VbInstance.
        :type management_vcn_id: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'state_message': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'instance_url': 'str',
            'node_count': 'int',
            'is_visual_builder_enabled': 'bool',
            'custom_endpoint': 'CustomEndpointDetails',
            'alternate_custom_endpoints': 'list[CustomEndpointDetails]',
            'consumption_model': 'str',
            'idcs_info': 'IdcsInfoDetails',
            'attachments': 'list[AttachmentDetails]',
            'service_nat_gateway_ip': 'str',
            'management_nat_gateway_ip': 'str',
            'service_vcn_id': 'str',
            'management_vcn_id': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'state_message': 'stateMessage',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'instance_url': 'instanceUrl',
            'node_count': 'nodeCount',
            'is_visual_builder_enabled': 'isVisualBuilderEnabled',
            'custom_endpoint': 'customEndpoint',
            'alternate_custom_endpoints': 'alternateCustomEndpoints',
            'consumption_model': 'consumptionModel',
            'idcs_info': 'idcsInfo',
            'attachments': 'attachments',
            'service_nat_gateway_ip': 'serviceNatGatewayIp',
            'management_nat_gateway_ip': 'managementNatGatewayIp',
            'service_vcn_id': 'serviceVcnId',
            'management_vcn_id': 'managementVcnId'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._state_message = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._instance_url = None
        self._node_count = None
        self._is_visual_builder_enabled = None
        self._custom_endpoint = None
        self._alternate_custom_endpoints = None
        self._consumption_model = None
        self._idcs_info = None
        self._attachments = None
        self._service_nat_gateway_ip = None
        self._management_nat_gateway_ip = None
        self._service_vcn_id = None
        self._management_vcn_id = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this VbInstance.
        Unique identifier that is immutable on creation.


        :return: The id of this VbInstance.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VbInstance.
        Unique identifier that is immutable on creation.


        :param id: The id of this VbInstance.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this VbInstance.
        Vb Instance Identifier, can be renamed.


        :return: The display_name of this VbInstance.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this VbInstance.
        Vb Instance Identifier, can be renamed.


        :param display_name: The display_name of this VbInstance.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this VbInstance.
        Compartment Identifier.


        :return: The compartment_id of this VbInstance.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this VbInstance.
        Compartment Identifier.


        :param compartment_id: The compartment_id of this VbInstance.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_created(self):
        """
        Gets the time_created of this VbInstance.
        The time the the VbInstance was created. An RFC3339 formatted datetime string.


        :return: The time_created of this VbInstance.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this VbInstance.
        The time the the VbInstance was created. An RFC3339 formatted datetime string.


        :param time_created: The time_created of this VbInstance.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this VbInstance.
        The time the VbInstance was updated. An RFC3339 formatted datetime string.


        :return: The time_updated of this VbInstance.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this VbInstance.
        The time the VbInstance was updated. An RFC3339 formatted datetime string.


        :param time_updated: The time_updated of this VbInstance.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this VbInstance.
        The current state of the vb instance.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this VbInstance.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this VbInstance.
        The current state of the vb instance.


        :param lifecycle_state: The lifecycle_state of this VbInstance.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def state_message(self):
        """
        Gets the state_message of this VbInstance.
        An message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :return: The state_message of this VbInstance.
        :rtype: str
        """
        return self._state_message

    @state_message.setter
    def state_message(self, state_message):
        """
        Sets the state_message of this VbInstance.
        An message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :param state_message: The state_message of this VbInstance.
        :type: str
        """
        self._state_message = state_message

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this VbInstance.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this VbInstance.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this VbInstance.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this VbInstance.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this VbInstance.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this VbInstance.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this VbInstance.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this VbInstance.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this VbInstance.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this VbInstance.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this VbInstance.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this VbInstance.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def instance_url(self):
        """
        **[Required]** Gets the instance_url of this VbInstance.
        The Vb Instance URL.


        :return: The instance_url of this VbInstance.
        :rtype: str
        """
        return self._instance_url

    @instance_url.setter
    def instance_url(self, instance_url):
        """
        Sets the instance_url of this VbInstance.
        The Vb Instance URL.


        :param instance_url: The instance_url of this VbInstance.
        :type: str
        """
        self._instance_url = instance_url

    @property
    def node_count(self):
        """
        **[Required]** Gets the node_count of this VbInstance.
        The number of Nodes


        :return: The node_count of this VbInstance.
        :rtype: int
        """
        return self._node_count

    @node_count.setter
    def node_count(self, node_count):
        """
        Sets the node_count of this VbInstance.
        The number of Nodes


        :param node_count: The node_count of this VbInstance.
        :type: int
        """
        self._node_count = node_count

    @property
    def is_visual_builder_enabled(self):
        """
        Gets the is_visual_builder_enabled of this VbInstance.
        Visual Builder is enabled or not.


        :return: The is_visual_builder_enabled of this VbInstance.
        :rtype: bool
        """
        return self._is_visual_builder_enabled

    @is_visual_builder_enabled.setter
    def is_visual_builder_enabled(self, is_visual_builder_enabled):
        """
        Sets the is_visual_builder_enabled of this VbInstance.
        Visual Builder is enabled or not.


        :param is_visual_builder_enabled: The is_visual_builder_enabled of this VbInstance.
        :type: bool
        """
        self._is_visual_builder_enabled = is_visual_builder_enabled

    @property
    def custom_endpoint(self):
        """
        Gets the custom_endpoint of this VbInstance.

        :return: The custom_endpoint of this VbInstance.
        :rtype: oci.visual_builder.models.CustomEndpointDetails
        """
        return self._custom_endpoint

    @custom_endpoint.setter
    def custom_endpoint(self, custom_endpoint):
        """
        Sets the custom_endpoint of this VbInstance.

        :param custom_endpoint: The custom_endpoint of this VbInstance.
        :type: oci.visual_builder.models.CustomEndpointDetails
        """
        self._custom_endpoint = custom_endpoint

    @property
    def alternate_custom_endpoints(self):
        """
        Gets the alternate_custom_endpoints of this VbInstance.
        A list of alternate custom endpoints used for the vb instance URL.


        :return: The alternate_custom_endpoints of this VbInstance.
        :rtype: list[oci.visual_builder.models.CustomEndpointDetails]
        """
        return self._alternate_custom_endpoints

    @alternate_custom_endpoints.setter
    def alternate_custom_endpoints(self, alternate_custom_endpoints):
        """
        Sets the alternate_custom_endpoints of this VbInstance.
        A list of alternate custom endpoints used for the vb instance URL.


        :param alternate_custom_endpoints: The alternate_custom_endpoints of this VbInstance.
        :type: list[oci.visual_builder.models.CustomEndpointDetails]
        """
        self._alternate_custom_endpoints = alternate_custom_endpoints

    @property
    def consumption_model(self):
        """
        Gets the consumption_model of this VbInstance.
        The entitlement used for billing purposes.

        Allowed values for this property are: "UCM", "GOV", "VB4SAAS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The consumption_model of this VbInstance.
        :rtype: str
        """
        return self._consumption_model

    @consumption_model.setter
    def consumption_model(self, consumption_model):
        """
        Sets the consumption_model of this VbInstance.
        The entitlement used for billing purposes.


        :param consumption_model: The consumption_model of this VbInstance.
        :type: str
        """
        allowed_values = ["UCM", "GOV", "VB4SAAS"]
        if not value_allowed_none_or_none_sentinel(consumption_model, allowed_values):
            consumption_model = 'UNKNOWN_ENUM_VALUE'
        self._consumption_model = consumption_model

    @property
    def idcs_info(self):
        """
        Gets the idcs_info of this VbInstance.

        :return: The idcs_info of this VbInstance.
        :rtype: oci.visual_builder.models.IdcsInfoDetails
        """
        return self._idcs_info

    @idcs_info.setter
    def idcs_info(self, idcs_info):
        """
        Sets the idcs_info of this VbInstance.

        :param idcs_info: The idcs_info of this VbInstance.
        :type: oci.visual_builder.models.IdcsInfoDetails
        """
        self._idcs_info = idcs_info

    @property
    def attachments(self):
        """
        Gets the attachments of this VbInstance.
        A list of associated attachments to other services


        :return: The attachments of this VbInstance.
        :rtype: list[oci.visual_builder.models.AttachmentDetails]
        """
        return self._attachments

    @attachments.setter
    def attachments(self, attachments):
        """
        Sets the attachments of this VbInstance.
        A list of associated attachments to other services


        :param attachments: The attachments of this VbInstance.
        :type: list[oci.visual_builder.models.AttachmentDetails]
        """
        self._attachments = attachments

    @property
    def service_nat_gateway_ip(self):
        """
        Gets the service_nat_gateway_ip of this VbInstance.
        The NAT gateway IP address for the VB service VCN


        :return: The service_nat_gateway_ip of this VbInstance.
        :rtype: str
        """
        return self._service_nat_gateway_ip

    @service_nat_gateway_ip.setter
    def service_nat_gateway_ip(self, service_nat_gateway_ip):
        """
        Sets the service_nat_gateway_ip of this VbInstance.
        The NAT gateway IP address for the VB service VCN


        :param service_nat_gateway_ip: The service_nat_gateway_ip of this VbInstance.
        :type: str
        """
        self._service_nat_gateway_ip = service_nat_gateway_ip

    @property
    def management_nat_gateway_ip(self):
        """
        Gets the management_nat_gateway_ip of this VbInstance.
        The NAT gateway IP address for the VB management VCN


        :return: The management_nat_gateway_ip of this VbInstance.
        :rtype: str
        """
        return self._management_nat_gateway_ip

    @management_nat_gateway_ip.setter
    def management_nat_gateway_ip(self, management_nat_gateway_ip):
        """
        Sets the management_nat_gateway_ip of this VbInstance.
        The NAT gateway IP address for the VB management VCN


        :param management_nat_gateway_ip: The management_nat_gateway_ip of this VbInstance.
        :type: str
        """
        self._management_nat_gateway_ip = management_nat_gateway_ip

    @property
    def service_vcn_id(self):
        """
        Gets the service_vcn_id of this VbInstance.
        The Oracle Cloud ID (OCID) of the Visual Builder service VCN


        :return: The service_vcn_id of this VbInstance.
        :rtype: str
        """
        return self._service_vcn_id

    @service_vcn_id.setter
    def service_vcn_id(self, service_vcn_id):
        """
        Sets the service_vcn_id of this VbInstance.
        The Oracle Cloud ID (OCID) of the Visual Builder service VCN


        :param service_vcn_id: The service_vcn_id of this VbInstance.
        :type: str
        """
        self._service_vcn_id = service_vcn_id

    @property
    def management_vcn_id(self):
        """
        Gets the management_vcn_id of this VbInstance.
        The Oracle Cloud ID (OCID) of the Visual Builder management VCN


        :return: The management_vcn_id of this VbInstance.
        :rtype: str
        """
        return self._management_vcn_id

    @management_vcn_id.setter
    def management_vcn_id(self, management_vcn_id):
        """
        Sets the management_vcn_id of this VbInstance.
        The Oracle Cloud ID (OCID) of the Visual Builder management VCN


        :param management_vcn_id: The management_vcn_id of this VbInstance.
        :type: str
        """
        self._management_vcn_id = management_vcn_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
