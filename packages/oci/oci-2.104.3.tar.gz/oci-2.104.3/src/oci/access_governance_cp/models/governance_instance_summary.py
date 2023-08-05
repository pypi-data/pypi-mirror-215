# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GovernanceInstanceSummary(object):
    """
    The summary of an GovernanceInstance.
    """

    #: A constant which can be used with the lifecycle_state property of a GovernanceInstanceSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a GovernanceInstanceSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a GovernanceInstanceSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a GovernanceInstanceSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a GovernanceInstanceSummary.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    #: A constant which can be used with the license_type property of a GovernanceInstanceSummary.
    #: This constant has a value of "NEW_LICENSE"
    LICENSE_TYPE_NEW_LICENSE = "NEW_LICENSE"

    #: A constant which can be used with the license_type property of a GovernanceInstanceSummary.
    #: This constant has a value of "BRING_YOUR_OWN_LICENSE"
    LICENSE_TYPE_BRING_YOUR_OWN_LICENSE = "BRING_YOUR_OWN_LICENSE"

    #: A constant which can be used with the license_type property of a GovernanceInstanceSummary.
    #: This constant has a value of "AG_ORACLE_WORKLOADS"
    LICENSE_TYPE_AG_ORACLE_WORKLOADS = "AG_ORACLE_WORKLOADS"

    #: A constant which can be used with the license_type property of a GovernanceInstanceSummary.
    #: This constant has a value of "AG_OCI"
    LICENSE_TYPE_AG_OCI = "AG_OCI"

    def __init__(self, **kwargs):
        """
        Initializes a new GovernanceInstanceSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this GovernanceInstanceSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this GovernanceInstanceSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this GovernanceInstanceSummary.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this GovernanceInstanceSummary.
        :type compartment_id: str

        :param time_created:
            The value to assign to the time_created property of this GovernanceInstanceSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this GovernanceInstanceSummary.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this GovernanceInstanceSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "DELETING", "DELETED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param license_type:
            The value to assign to the license_type property of this GovernanceInstanceSummary.
            Allowed values for this property are: "NEW_LICENSE", "BRING_YOUR_OWN_LICENSE", "AG_ORACLE_WORKLOADS", "AG_OCI", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type license_type: str

        :param instance_url:
            The value to assign to the instance_url property of this GovernanceInstanceSummary.
        :type instance_url: str

        :param defined_tags:
            The value to assign to the defined_tags property of this GovernanceInstanceSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this GovernanceInstanceSummary.
        :type freeform_tags: dict(str, str)

        :param system_tags:
            The value to assign to the system_tags property of this GovernanceInstanceSummary.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'license_type': 'str',
            'instance_url': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'license_type': 'licenseType',
            'instance_url': 'instanceUrl',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._license_type = None
        self._instance_url = None
        self._defined_tags = None
        self._freeform_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        Gets the id of this GovernanceInstanceSummary.
        The unique OCID of the GovernanceInstance.


        :return: The id of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this GovernanceInstanceSummary.
        The unique OCID of the GovernanceInstance.


        :param id: The id of this GovernanceInstanceSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this GovernanceInstanceSummary.
        The name for the GovernanceInstance.


        :return: The display_name of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this GovernanceInstanceSummary.
        The name for the GovernanceInstance.


        :param display_name: The display_name of this GovernanceInstanceSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this GovernanceInstanceSummary.
        The description of the GovernanceInstance.


        :return: The description of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this GovernanceInstanceSummary.
        The description of the GovernanceInstance.


        :param description: The description of this GovernanceInstanceSummary.
        :type: str
        """
        self._description = description

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this GovernanceInstanceSummary.
        The OCID of the compartment where the GovernanceInstance resides.


        :return: The compartment_id of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this GovernanceInstanceSummary.
        The OCID of the compartment where the GovernanceInstance resides.


        :param compartment_id: The compartment_id of this GovernanceInstanceSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this GovernanceInstanceSummary.
        The time the the GovernanceInstance was created in an RFC3339 formatted datetime string.


        :return: The time_created of this GovernanceInstanceSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this GovernanceInstanceSummary.
        The time the the GovernanceInstance was created in an RFC3339 formatted datetime string.


        :param time_created: The time_created of this GovernanceInstanceSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this GovernanceInstanceSummary.
        The time the GovernanceInstance was updated in an RFC3339 formatted datetime string.


        :return: The time_updated of this GovernanceInstanceSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this GovernanceInstanceSummary.
        The time the GovernanceInstance was updated in an RFC3339 formatted datetime string.


        :param time_updated: The time_updated of this GovernanceInstanceSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this GovernanceInstanceSummary.
        The current state of the GovernanceInstance.

        Allowed values for this property are: "CREATING", "ACTIVE", "DELETING", "DELETED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this GovernanceInstanceSummary.
        The current state of the GovernanceInstance.


        :param lifecycle_state: The lifecycle_state of this GovernanceInstanceSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "DELETING", "DELETED", "NEEDS_ATTENTION"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def license_type(self):
        """
        Gets the license_type of this GovernanceInstanceSummary.
        The licenseType being used.

        Allowed values for this property are: "NEW_LICENSE", "BRING_YOUR_OWN_LICENSE", "AG_ORACLE_WORKLOADS", "AG_OCI", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The license_type of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._license_type

    @license_type.setter
    def license_type(self, license_type):
        """
        Sets the license_type of this GovernanceInstanceSummary.
        The licenseType being used.


        :param license_type: The license_type of this GovernanceInstanceSummary.
        :type: str
        """
        allowed_values = ["NEW_LICENSE", "BRING_YOUR_OWN_LICENSE", "AG_ORACLE_WORKLOADS", "AG_OCI"]
        if not value_allowed_none_or_none_sentinel(license_type, allowed_values):
            license_type = 'UNKNOWN_ENUM_VALUE'
        self._license_type = license_type

    @property
    def instance_url(self):
        """
        Gets the instance_url of this GovernanceInstanceSummary.
        The access URL of the GovernanceInstance.


        :return: The instance_url of this GovernanceInstanceSummary.
        :rtype: str
        """
        return self._instance_url

    @instance_url.setter
    def instance_url(self, instance_url):
        """
        Sets the instance_url of this GovernanceInstanceSummary.
        The access URL of the GovernanceInstance.


        :param instance_url: The instance_url of this GovernanceInstanceSummary.
        :type: str
        """
        self._instance_url = instance_url

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this GovernanceInstanceSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this GovernanceInstanceSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this GovernanceInstanceSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this GovernanceInstanceSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this GovernanceInstanceSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this GovernanceInstanceSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this GovernanceInstanceSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this GovernanceInstanceSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this GovernanceInstanceSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this GovernanceInstanceSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this GovernanceInstanceSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this GovernanceInstanceSummary.
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
