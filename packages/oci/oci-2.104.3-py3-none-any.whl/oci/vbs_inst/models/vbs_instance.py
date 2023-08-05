# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VbsInstance(object):
    """
    Visual Builder Studio service instance
    """

    #: A constant which can be used with the lifecycle_state property of a VbsInstance.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a VbsInstance.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a VbsInstance.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a VbsInstance.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a VbsInstance.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a VbsInstance.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new VbsInstance object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this VbsInstance.
        :type id: str

        :param name:
            The value to assign to the name property of this VbsInstance.
        :type name: str

        :param display_name:
            The value to assign to the display_name property of this VbsInstance.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this VbsInstance.
        :type compartment_id: str

        :param is_resource_usage_agreement_granted:
            The value to assign to the is_resource_usage_agreement_granted property of this VbsInstance.
        :type is_resource_usage_agreement_granted: bool

        :param resource_compartment_id:
            The value to assign to the resource_compartment_id property of this VbsInstance.
        :type resource_compartment_id: str

        :param vbs_access_url:
            The value to assign to the vbs_access_url property of this VbsInstance.
        :type vbs_access_url: str

        :param time_created:
            The value to assign to the time_created property of this VbsInstance.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this VbsInstance.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this VbsInstance.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecyle_details:
            The value to assign to the lifecyle_details property of this VbsInstance.
        :type lifecyle_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this VbsInstance.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this VbsInstance.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this VbsInstance.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'is_resource_usage_agreement_granted': 'bool',
            'resource_compartment_id': 'str',
            'vbs_access_url': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'lifecyle_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'is_resource_usage_agreement_granted': 'isResourceUsageAgreementGranted',
            'resource_compartment_id': 'resourceCompartmentId',
            'vbs_access_url': 'vbsAccessUrl',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'lifecyle_details': 'lifecyleDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._name = None
        self._display_name = None
        self._compartment_id = None
        self._is_resource_usage_agreement_granted = None
        self._resource_compartment_id = None
        self._vbs_access_url = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._lifecyle_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this VbsInstance.
        Unique identifier that is immutable on creation


        :return: The id of this VbsInstance.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VbsInstance.
        Unique identifier that is immutable on creation


        :param id: The id of this VbsInstance.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this VbsInstance.
        Service instance name (unique identifier)


        :return: The name of this VbsInstance.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VbsInstance.
        Service instance name (unique identifier)


        :param name: The name of this VbsInstance.
        :type: str
        """
        self._name = name

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this VbsInstance.
        Service instance display name


        :return: The display_name of this VbsInstance.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this VbsInstance.
        Service instance display name


        :param display_name: The display_name of this VbsInstance.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this VbsInstance.
        Compartment of the service instance


        :return: The compartment_id of this VbsInstance.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this VbsInstance.
        Compartment of the service instance


        :param compartment_id: The compartment_id of this VbsInstance.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def is_resource_usage_agreement_granted(self):
        """
        Gets the is_resource_usage_agreement_granted of this VbsInstance.
        Whether the VBS service instance owner explicitly approved VBS to create and use resources in the customer tenancy


        :return: The is_resource_usage_agreement_granted of this VbsInstance.
        :rtype: bool
        """
        return self._is_resource_usage_agreement_granted

    @is_resource_usage_agreement_granted.setter
    def is_resource_usage_agreement_granted(self, is_resource_usage_agreement_granted):
        """
        Sets the is_resource_usage_agreement_granted of this VbsInstance.
        Whether the VBS service instance owner explicitly approved VBS to create and use resources in the customer tenancy


        :param is_resource_usage_agreement_granted: The is_resource_usage_agreement_granted of this VbsInstance.
        :type: bool
        """
        self._is_resource_usage_agreement_granted = is_resource_usage_agreement_granted

    @property
    def resource_compartment_id(self):
        """
        Gets the resource_compartment_id of this VbsInstance.
        Compartment where VBS may create additional resources for the service instance


        :return: The resource_compartment_id of this VbsInstance.
        :rtype: str
        """
        return self._resource_compartment_id

    @resource_compartment_id.setter
    def resource_compartment_id(self, resource_compartment_id):
        """
        Sets the resource_compartment_id of this VbsInstance.
        Compartment where VBS may create additional resources for the service instance


        :param resource_compartment_id: The resource_compartment_id of this VbsInstance.
        :type: str
        """
        self._resource_compartment_id = resource_compartment_id

    @property
    def vbs_access_url(self):
        """
        Gets the vbs_access_url of this VbsInstance.
        Public web URL for accessing the VBS service instance


        :return: The vbs_access_url of this VbsInstance.
        :rtype: str
        """
        return self._vbs_access_url

    @vbs_access_url.setter
    def vbs_access_url(self, vbs_access_url):
        """
        Sets the vbs_access_url of this VbsInstance.
        Public web URL for accessing the VBS service instance


        :param vbs_access_url: The vbs_access_url of this VbsInstance.
        :type: str
        """
        self._vbs_access_url = vbs_access_url

    @property
    def time_created(self):
        """
        Gets the time_created of this VbsInstance.
        The time the the VbsInstance was created. An RFC3339 formatted datetime string


        :return: The time_created of this VbsInstance.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this VbsInstance.
        The time the the VbsInstance was created. An RFC3339 formatted datetime string


        :param time_created: The time_created of this VbsInstance.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this VbsInstance.
        The time the VbsInstance was updated. An RFC3339 formatted datetime string


        :return: The time_updated of this VbsInstance.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this VbsInstance.
        The time the VbsInstance was updated. An RFC3339 formatted datetime string


        :param time_updated: The time_updated of this VbsInstance.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this VbsInstance.
        The current state of the VbsInstance.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this VbsInstance.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this VbsInstance.
        The current state of the VbsInstance.


        :param lifecycle_state: The lifecycle_state of this VbsInstance.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecyle_details(self):
        """
        Gets the lifecyle_details of this VbsInstance.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :return: The lifecyle_details of this VbsInstance.
        :rtype: str
        """
        return self._lifecyle_details

    @lifecyle_details.setter
    def lifecyle_details(self, lifecyle_details):
        """
        Sets the lifecyle_details of this VbsInstance.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :param lifecyle_details: The lifecyle_details of this VbsInstance.
        :type: str
        """
        self._lifecyle_details = lifecyle_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this VbsInstance.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this VbsInstance.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this VbsInstance.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this VbsInstance.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this VbsInstance.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this VbsInstance.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this VbsInstance.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this VbsInstance.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this VbsInstance.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this VbsInstance.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this VbsInstance.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this VbsInstance.
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
