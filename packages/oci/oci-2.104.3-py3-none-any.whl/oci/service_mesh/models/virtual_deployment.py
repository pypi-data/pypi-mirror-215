# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VirtualDeployment(object):
    """
    This resource represents a customer-managed virtual service deployment in the Service Mesh.
    """

    #: A constant which can be used with the lifecycle_state property of a VirtualDeployment.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a VirtualDeployment.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a VirtualDeployment.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a VirtualDeployment.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a VirtualDeployment.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a VirtualDeployment.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new VirtualDeployment object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this VirtualDeployment.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this VirtualDeployment.
        :type compartment_id: str

        :param virtual_service_id:
            The value to assign to the virtual_service_id property of this VirtualDeployment.
        :type virtual_service_id: str

        :param name:
            The value to assign to the name property of this VirtualDeployment.
        :type name: str

        :param description:
            The value to assign to the description property of this VirtualDeployment.
        :type description: str

        :param service_discovery:
            The value to assign to the service_discovery property of this VirtualDeployment.
        :type service_discovery: oci.service_mesh.models.ServiceDiscoveryConfiguration

        :param listeners:
            The value to assign to the listeners property of this VirtualDeployment.
        :type listeners: list[oci.service_mesh.models.VirtualDeploymentListener]

        :param access_logging:
            The value to assign to the access_logging property of this VirtualDeployment.
        :type access_logging: oci.service_mesh.models.AccessLoggingConfiguration

        :param time_created:
            The value to assign to the time_created property of this VirtualDeployment.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this VirtualDeployment.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this VirtualDeployment.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this VirtualDeployment.
        :type lifecycle_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this VirtualDeployment.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this VirtualDeployment.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this VirtualDeployment.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'virtual_service_id': 'str',
            'name': 'str',
            'description': 'str',
            'service_discovery': 'ServiceDiscoveryConfiguration',
            'listeners': 'list[VirtualDeploymentListener]',
            'access_logging': 'AccessLoggingConfiguration',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'virtual_service_id': 'virtualServiceId',
            'name': 'name',
            'description': 'description',
            'service_discovery': 'serviceDiscovery',
            'listeners': 'listeners',
            'access_logging': 'accessLogging',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._compartment_id = None
        self._virtual_service_id = None
        self._name = None
        self._description = None
        self._service_discovery = None
        self._listeners = None
        self._access_logging = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this VirtualDeployment.
        Unique identifier that is immutable on creation.


        :return: The id of this VirtualDeployment.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VirtualDeployment.
        Unique identifier that is immutable on creation.


        :param id: The id of this VirtualDeployment.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this VirtualDeployment.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this VirtualDeployment.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this VirtualDeployment.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this VirtualDeployment.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def virtual_service_id(self):
        """
        **[Required]** Gets the virtual_service_id of this VirtualDeployment.
        The OCID of the virtual service in which this virtual deployment is created.


        :return: The virtual_service_id of this VirtualDeployment.
        :rtype: str
        """
        return self._virtual_service_id

    @virtual_service_id.setter
    def virtual_service_id(self, virtual_service_id):
        """
        Sets the virtual_service_id of this VirtualDeployment.
        The OCID of the virtual service in which this virtual deployment is created.


        :param virtual_service_id: The virtual_service_id of this VirtualDeployment.
        :type: str
        """
        self._virtual_service_id = virtual_service_id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this VirtualDeployment.
        A user-friendly name. The name must be unique within the same virtual service and cannot be changed after creation.
        Avoid entering confidential information.

        Example: `My unique resource name`


        :return: The name of this VirtualDeployment.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VirtualDeployment.
        A user-friendly name. The name must be unique within the same virtual service and cannot be changed after creation.
        Avoid entering confidential information.

        Example: `My unique resource name`


        :param name: The name of this VirtualDeployment.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this VirtualDeployment.
        Description of the resource. It can be changed after creation.
        Avoid entering confidential information.

        Example: `This is my new resource`


        :return: The description of this VirtualDeployment.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this VirtualDeployment.
        Description of the resource. It can be changed after creation.
        Avoid entering confidential information.

        Example: `This is my new resource`


        :param description: The description of this VirtualDeployment.
        :type: str
        """
        self._description = description

    @property
    def service_discovery(self):
        """
        Gets the service_discovery of this VirtualDeployment.

        :return: The service_discovery of this VirtualDeployment.
        :rtype: oci.service_mesh.models.ServiceDiscoveryConfiguration
        """
        return self._service_discovery

    @service_discovery.setter
    def service_discovery(self, service_discovery):
        """
        Sets the service_discovery of this VirtualDeployment.

        :param service_discovery: The service_discovery of this VirtualDeployment.
        :type: oci.service_mesh.models.ServiceDiscoveryConfiguration
        """
        self._service_discovery = service_discovery

    @property
    def listeners(self):
        """
        Gets the listeners of this VirtualDeployment.
        The listeners for the virtual deployment


        :return: The listeners of this VirtualDeployment.
        :rtype: list[oci.service_mesh.models.VirtualDeploymentListener]
        """
        return self._listeners

    @listeners.setter
    def listeners(self, listeners):
        """
        Sets the listeners of this VirtualDeployment.
        The listeners for the virtual deployment


        :param listeners: The listeners of this VirtualDeployment.
        :type: list[oci.service_mesh.models.VirtualDeploymentListener]
        """
        self._listeners = listeners

    @property
    def access_logging(self):
        """
        Gets the access_logging of this VirtualDeployment.

        :return: The access_logging of this VirtualDeployment.
        :rtype: oci.service_mesh.models.AccessLoggingConfiguration
        """
        return self._access_logging

    @access_logging.setter
    def access_logging(self, access_logging):
        """
        Sets the access_logging of this VirtualDeployment.

        :param access_logging: The access_logging of this VirtualDeployment.
        :type: oci.service_mesh.models.AccessLoggingConfiguration
        """
        self._access_logging = access_logging

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this VirtualDeployment.
        The time when this resource was created in an RFC3339 formatted datetime string.


        :return: The time_created of this VirtualDeployment.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this VirtualDeployment.
        The time when this resource was created in an RFC3339 formatted datetime string.


        :param time_created: The time_created of this VirtualDeployment.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this VirtualDeployment.
        The time when this resource was updated in an RFC3339 formatted datetime string.


        :return: The time_updated of this VirtualDeployment.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this VirtualDeployment.
        The time when this resource was updated in an RFC3339 formatted datetime string.


        :param time_updated: The time_updated of this VirtualDeployment.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this VirtualDeployment.
        The current state of the Resource.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this VirtualDeployment.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this VirtualDeployment.
        The current state of the Resource.


        :param lifecycle_state: The lifecycle_state of this VirtualDeployment.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this VirtualDeployment.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in a Failed state.


        :return: The lifecycle_details of this VirtualDeployment.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this VirtualDeployment.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in a Failed state.


        :param lifecycle_details: The lifecycle_details of this VirtualDeployment.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this VirtualDeployment.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this VirtualDeployment.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this VirtualDeployment.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this VirtualDeployment.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this VirtualDeployment.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this VirtualDeployment.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this VirtualDeployment.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this VirtualDeployment.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this VirtualDeployment.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this VirtualDeployment.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this VirtualDeployment.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this VirtualDeployment.
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
