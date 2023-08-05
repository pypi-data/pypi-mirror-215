# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Pool(object):
    """
    A Data Flow pool object.
    """

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "ACCEPTED"
    LIFECYCLE_STATE_ACCEPTED = "ACCEPTED"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "SCHEDULED"
    LIFECYCLE_STATE_SCHEDULED = "SCHEDULED"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "STOPPING"
    LIFECYCLE_STATE_STOPPING = "STOPPING"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "STOPPED"
    LIFECYCLE_STATE_STOPPED = "STOPPED"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a Pool.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new Pool object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this Pool.
        :type compartment_id: str

        :param defined_tags:
            The value to assign to the defined_tags property of this Pool.
        :type defined_tags: dict(str, dict(str, object))

        :param description:
            The value to assign to the description property of this Pool.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this Pool.
        :type display_name: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Pool.
        :type freeform_tags: dict(str, str)

        :param id:
            The value to assign to the id property of this Pool.
        :type id: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this Pool.
        :type lifecycle_details: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Pool.
            Allowed values for this property are: "ACCEPTED", "SCHEDULED", "CREATING", "ACTIVE", "STOPPING", "STOPPED", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param owner_principal_id:
            The value to assign to the owner_principal_id property of this Pool.
        :type owner_principal_id: str

        :param owner_user_name:
            The value to assign to the owner_user_name property of this Pool.
        :type owner_user_name: str

        :param pool_metrics:
            The value to assign to the pool_metrics property of this Pool.
        :type pool_metrics: oci.data_flow.models.PoolMetrics

        :param configurations:
            The value to assign to the configurations property of this Pool.
        :type configurations: list[oci.data_flow.models.PoolConfig]

        :param schedules:
            The value to assign to the schedules property of this Pool.
        :type schedules: list[oci.data_flow.models.PoolSchedule]

        :param idle_timeout_in_minutes:
            The value to assign to the idle_timeout_in_minutes property of this Pool.
        :type idle_timeout_in_minutes: int

        :param time_created:
            The value to assign to the time_created property of this Pool.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this Pool.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'description': 'str',
            'display_name': 'str',
            'freeform_tags': 'dict(str, str)',
            'id': 'str',
            'lifecycle_details': 'str',
            'lifecycle_state': 'str',
            'owner_principal_id': 'str',
            'owner_user_name': 'str',
            'pool_metrics': 'PoolMetrics',
            'configurations': 'list[PoolConfig]',
            'schedules': 'list[PoolSchedule]',
            'idle_timeout_in_minutes': 'int',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'defined_tags': 'definedTags',
            'description': 'description',
            'display_name': 'displayName',
            'freeform_tags': 'freeformTags',
            'id': 'id',
            'lifecycle_details': 'lifecycleDetails',
            'lifecycle_state': 'lifecycleState',
            'owner_principal_id': 'ownerPrincipalId',
            'owner_user_name': 'ownerUserName',
            'pool_metrics': 'poolMetrics',
            'configurations': 'configurations',
            'schedules': 'schedules',
            'idle_timeout_in_minutes': 'idleTimeoutInMinutes',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }

        self._compartment_id = None
        self._defined_tags = None
        self._description = None
        self._display_name = None
        self._freeform_tags = None
        self._id = None
        self._lifecycle_details = None
        self._lifecycle_state = None
        self._owner_principal_id = None
        self._owner_user_name = None
        self._pool_metrics = None
        self._configurations = None
        self._schedules = None
        self._idle_timeout_in_minutes = None
        self._time_created = None
        self._time_updated = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this Pool.
        The OCID of a compartment.


        :return: The compartment_id of this Pool.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this Pool.
        The OCID of a compartment.


        :param compartment_id: The compartment_id of this Pool.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def defined_tags(self):
        """
        **[Required]** Gets the defined_tags of this Pool.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this Pool.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Pool.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this Pool.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def description(self):
        """
        Gets the description of this Pool.
        A user-friendly description. Avoid entering confidential information.


        :return: The description of this Pool.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Pool.
        A user-friendly description. Avoid entering confidential information.


        :param description: The description of this Pool.
        :type: str
        """
        self._description = description

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this Pool.
        A user-friendly name. It does not have to be unique. Avoid entering confidential information.


        :return: The display_name of this Pool.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this Pool.
        A user-friendly name. It does not have to be unique. Avoid entering confidential information.


        :param display_name: The display_name of this Pool.
        :type: str
        """
        self._display_name = display_name

    @property
    def freeform_tags(self):
        """
        **[Required]** Gets the freeform_tags of this Pool.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this Pool.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Pool.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this Pool.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def id(self):
        """
        **[Required]** Gets the id of this Pool.
        The OCID of a pool. Unique Id to indentify a dataflow pool resource.


        :return: The id of this Pool.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Pool.
        The OCID of a pool. Unique Id to indentify a dataflow pool resource.


        :param id: The id of this Pool.
        :type: str
        """
        self._id = id

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this Pool.
        The detailed messages about the lifecycle state.


        :return: The lifecycle_details of this Pool.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this Pool.
        The detailed messages about the lifecycle state.


        :param lifecycle_details: The lifecycle_details of this Pool.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this Pool.
        The current state of this pool.

        Allowed values for this property are: "ACCEPTED", "SCHEDULED", "CREATING", "ACTIVE", "STOPPING", "STOPPED", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Pool.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Pool.
        The current state of this pool.


        :param lifecycle_state: The lifecycle_state of this Pool.
        :type: str
        """
        allowed_values = ["ACCEPTED", "SCHEDULED", "CREATING", "ACTIVE", "STOPPING", "STOPPED", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def owner_principal_id(self):
        """
        **[Required]** Gets the owner_principal_id of this Pool.
        The OCID of the user who created the resource.


        :return: The owner_principal_id of this Pool.
        :rtype: str
        """
        return self._owner_principal_id

    @owner_principal_id.setter
    def owner_principal_id(self, owner_principal_id):
        """
        Sets the owner_principal_id of this Pool.
        The OCID of the user who created the resource.


        :param owner_principal_id: The owner_principal_id of this Pool.
        :type: str
        """
        self._owner_principal_id = owner_principal_id

    @property
    def owner_user_name(self):
        """
        Gets the owner_user_name of this Pool.
        The username of the user who created the resource.  If the username of the owner does not exist,
        `null` will be returned and the caller should refer to the ownerPrincipalId value instead.


        :return: The owner_user_name of this Pool.
        :rtype: str
        """
        return self._owner_user_name

    @owner_user_name.setter
    def owner_user_name(self, owner_user_name):
        """
        Sets the owner_user_name of this Pool.
        The username of the user who created the resource.  If the username of the owner does not exist,
        `null` will be returned and the caller should refer to the ownerPrincipalId value instead.


        :param owner_user_name: The owner_user_name of this Pool.
        :type: str
        """
        self._owner_user_name = owner_user_name

    @property
    def pool_metrics(self):
        """
        Gets the pool_metrics of this Pool.

        :return: The pool_metrics of this Pool.
        :rtype: oci.data_flow.models.PoolMetrics
        """
        return self._pool_metrics

    @pool_metrics.setter
    def pool_metrics(self, pool_metrics):
        """
        Sets the pool_metrics of this Pool.

        :param pool_metrics: The pool_metrics of this Pool.
        :type: oci.data_flow.models.PoolMetrics
        """
        self._pool_metrics = pool_metrics

    @property
    def configurations(self):
        """
        **[Required]** Gets the configurations of this Pool.
        List of PoolConfig items.


        :return: The configurations of this Pool.
        :rtype: list[oci.data_flow.models.PoolConfig]
        """
        return self._configurations

    @configurations.setter
    def configurations(self, configurations):
        """
        Sets the configurations of this Pool.
        List of PoolConfig items.


        :param configurations: The configurations of this Pool.
        :type: list[oci.data_flow.models.PoolConfig]
        """
        self._configurations = configurations

    @property
    def schedules(self):
        """
        Gets the schedules of this Pool.
        A list of schedules for pool to auto start and stop.


        :return: The schedules of this Pool.
        :rtype: list[oci.data_flow.models.PoolSchedule]
        """
        return self._schedules

    @schedules.setter
    def schedules(self, schedules):
        """
        Sets the schedules of this Pool.
        A list of schedules for pool to auto start and stop.


        :param schedules: The schedules of this Pool.
        :type: list[oci.data_flow.models.PoolSchedule]
        """
        self._schedules = schedules

    @property
    def idle_timeout_in_minutes(self):
        """
        Gets the idle_timeout_in_minutes of this Pool.
        Optional timeout value in minutes used to auto stop Pools. A Pool will be auto stopped after inactivity for this amount of time period.
        If value not set, pool will not be auto stopped auto.


        :return: The idle_timeout_in_minutes of this Pool.
        :rtype: int
        """
        return self._idle_timeout_in_minutes

    @idle_timeout_in_minutes.setter
    def idle_timeout_in_minutes(self, idle_timeout_in_minutes):
        """
        Sets the idle_timeout_in_minutes of this Pool.
        Optional timeout value in minutes used to auto stop Pools. A Pool will be auto stopped after inactivity for this amount of time period.
        If value not set, pool will not be auto stopped auto.


        :param idle_timeout_in_minutes: The idle_timeout_in_minutes of this Pool.
        :type: int
        """
        self._idle_timeout_in_minutes = idle_timeout_in_minutes

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this Pool.
        The date and time the resource was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2018-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this Pool.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this Pool.
        The date and time the resource was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2018-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this Pool.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this Pool.
        The date and time the resource was updated, expressed in `RFC 3339`__ timestamp format.
        Example: `2018-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this Pool.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this Pool.
        The date and time the resource was updated, expressed in `RFC 3339`__ timestamp format.
        Example: `2018-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this Pool.
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
