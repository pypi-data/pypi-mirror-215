# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DiscoveryJobSummary(object):
    """
    Summary of a discovery job.
    """

    #: A constant which can be used with the lifecycle_state property of a DiscoveryJobSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a DiscoveryJobSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DiscoveryJobSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a DiscoveryJobSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a DiscoveryJobSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a DiscoveryJobSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new DiscoveryJobSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DiscoveryJobSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this DiscoveryJobSummary.
        :type display_name: str

        :param time_started:
            The value to assign to the time_started property of this DiscoveryJobSummary.
        :type time_started: datetime

        :param time_finished:
            The value to assign to the time_finished property of this DiscoveryJobSummary.
        :type time_finished: datetime

        :param sensitive_data_model_id:
            The value to assign to the sensitive_data_model_id property of this DiscoveryJobSummary.
        :type sensitive_data_model_id: str

        :param target_id:
            The value to assign to the target_id property of this DiscoveryJobSummary.
        :type target_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DiscoveryJobSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param discovery_type:
            The value to assign to the discovery_type property of this DiscoveryJobSummary.
        :type discovery_type: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DiscoveryJobSummary.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DiscoveryJobSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DiscoveryJobSummary.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'time_started': 'datetime',
            'time_finished': 'datetime',
            'sensitive_data_model_id': 'str',
            'target_id': 'str',
            'lifecycle_state': 'str',
            'discovery_type': 'str',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'time_started': 'timeStarted',
            'time_finished': 'timeFinished',
            'sensitive_data_model_id': 'sensitiveDataModelId',
            'target_id': 'targetId',
            'lifecycle_state': 'lifecycleState',
            'discovery_type': 'discoveryType',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._display_name = None
        self._time_started = None
        self._time_finished = None
        self._sensitive_data_model_id = None
        self._target_id = None
        self._lifecycle_state = None
        self._discovery_type = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DiscoveryJobSummary.
        The OCID of the discovery job.


        :return: The id of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DiscoveryJobSummary.
        The OCID of the discovery job.


        :param id: The id of this DiscoveryJobSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DiscoveryJobSummary.
        The display name of the discovery job.


        :return: The display_name of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DiscoveryJobSummary.
        The display name of the discovery job.


        :param display_name: The display_name of this DiscoveryJobSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def time_started(self):
        """
        **[Required]** Gets the time_started of this DiscoveryJobSummary.
        The date and time the discovery job started, in the format defined by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_started of this DiscoveryJobSummary.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this DiscoveryJobSummary.
        The date and time the discovery job started, in the format defined by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :param time_started: The time_started of this DiscoveryJobSummary.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        **[Required]** Gets the time_finished of this DiscoveryJobSummary.
        The date and time the discovery job finished, in the format defined by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_finished of this DiscoveryJobSummary.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this DiscoveryJobSummary.
        The date and time the discovery job finished, in the format defined by `RFC3339`__.

        __ https://tools.ietf.org/html/rfc3339


        :param time_finished: The time_finished of this DiscoveryJobSummary.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def sensitive_data_model_id(self):
        """
        **[Required]** Gets the sensitive_data_model_id of this DiscoveryJobSummary.
        The OCID of the sensitive data model associated with the discovery job.


        :return: The sensitive_data_model_id of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._sensitive_data_model_id

    @sensitive_data_model_id.setter
    def sensitive_data_model_id(self, sensitive_data_model_id):
        """
        Sets the sensitive_data_model_id of this DiscoveryJobSummary.
        The OCID of the sensitive data model associated with the discovery job.


        :param sensitive_data_model_id: The sensitive_data_model_id of this DiscoveryJobSummary.
        :type: str
        """
        self._sensitive_data_model_id = sensitive_data_model_id

    @property
    def target_id(self):
        """
        **[Required]** Gets the target_id of this DiscoveryJobSummary.
        The OCID of the target database associated with the discovery job.


        :return: The target_id of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this DiscoveryJobSummary.
        The OCID of the target database associated with the discovery job.


        :param target_id: The target_id of this DiscoveryJobSummary.
        :type: str
        """
        self._target_id = target_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this DiscoveryJobSummary.
        The current state of the discovery job.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DiscoveryJobSummary.
        The current state of the discovery job.


        :param lifecycle_state: The lifecycle_state of this DiscoveryJobSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def discovery_type(self):
        """
        **[Required]** Gets the discovery_type of this DiscoveryJobSummary.
        The type of discovery.


        :return: The discovery_type of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._discovery_type

    @discovery_type.setter
    def discovery_type(self, discovery_type):
        """
        Sets the discovery_type of this DiscoveryJobSummary.
        The type of discovery.


        :param discovery_type: The discovery_type of this DiscoveryJobSummary.
        :type: str
        """
        self._discovery_type = discovery_type

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DiscoveryJobSummary.
        The OCID of the compartment to contain the discovery job.


        :return: The compartment_id of this DiscoveryJobSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DiscoveryJobSummary.
        The OCID of the compartment to contain the discovery job.


        :param compartment_id: The compartment_id of this DiscoveryJobSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DiscoveryJobSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this DiscoveryJobSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DiscoveryJobSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this DiscoveryJobSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DiscoveryJobSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this DiscoveryJobSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DiscoveryJobSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this DiscoveryJobSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
