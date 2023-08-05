# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DeploymentUpgradeSummary(object):
    """
    Summary of the Deployment Upgrade.
    """

    #: A constant which can be used with the deployment_upgrade_type property of a DeploymentUpgradeSummary.
    #: This constant has a value of "MANUAL"
    DEPLOYMENT_UPGRADE_TYPE_MANUAL = "MANUAL"

    #: A constant which can be used with the deployment_upgrade_type property of a DeploymentUpgradeSummary.
    #: This constant has a value of "AUTOMATIC"
    DEPLOYMENT_UPGRADE_TYPE_AUTOMATIC = "AUTOMATIC"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "IN_PROGRESS"
    LIFECYCLE_STATE_IN_PROGRESS = "IN_PROGRESS"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "CANCELING"
    LIFECYCLE_STATE_CANCELING = "CANCELING"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "CANCELED"
    LIFECYCLE_STATE_CANCELED = "CANCELED"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "SUCCEEDED"
    LIFECYCLE_STATE_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the lifecycle_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "WAITING"
    LIFECYCLE_STATE_WAITING = "WAITING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "RECOVERING"
    LIFECYCLE_SUB_STATE_RECOVERING = "RECOVERING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "STARTING"
    LIFECYCLE_SUB_STATE_STARTING = "STARTING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "STOPPING"
    LIFECYCLE_SUB_STATE_STOPPING = "STOPPING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "MOVING"
    LIFECYCLE_SUB_STATE_MOVING = "MOVING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "UPGRADING"
    LIFECYCLE_SUB_STATE_UPGRADING = "UPGRADING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "RESTORING"
    LIFECYCLE_SUB_STATE_RESTORING = "RESTORING"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "BACKUP_IN_PROGRESS"
    LIFECYCLE_SUB_STATE_BACKUP_IN_PROGRESS = "BACKUP_IN_PROGRESS"

    #: A constant which can be used with the lifecycle_sub_state property of a DeploymentUpgradeSummary.
    #: This constant has a value of "ROLLBACK_IN_PROGRESS"
    LIFECYCLE_SUB_STATE_ROLLBACK_IN_PROGRESS = "ROLLBACK_IN_PROGRESS"

    #: A constant which can be used with the release_type property of a DeploymentUpgradeSummary.
    #: This constant has a value of "MAJOR"
    RELEASE_TYPE_MAJOR = "MAJOR"

    #: A constant which can be used with the release_type property of a DeploymentUpgradeSummary.
    #: This constant has a value of "BUNDLE"
    RELEASE_TYPE_BUNDLE = "BUNDLE"

    #: A constant which can be used with the release_type property of a DeploymentUpgradeSummary.
    #: This constant has a value of "MINOR"
    RELEASE_TYPE_MINOR = "MINOR"

    def __init__(self, **kwargs):
        """
        Initializes a new DeploymentUpgradeSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DeploymentUpgradeSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this DeploymentUpgradeSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this DeploymentUpgradeSummary.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DeploymentUpgradeSummary.
        :type compartment_id: str

        :param deployment_id:
            The value to assign to the deployment_id property of this DeploymentUpgradeSummary.
        :type deployment_id: str

        :param deployment_upgrade_type:
            The value to assign to the deployment_upgrade_type property of this DeploymentUpgradeSummary.
            Allowed values for this property are: "MANUAL", "AUTOMATIC", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type deployment_upgrade_type: str

        :param time_started:
            The value to assign to the time_started property of this DeploymentUpgradeSummary.
        :type time_started: datetime

        :param time_finished:
            The value to assign to the time_finished property of this DeploymentUpgradeSummary.
        :type time_finished: datetime

        :param ogg_version:
            The value to assign to the ogg_version property of this DeploymentUpgradeSummary.
        :type ogg_version: str

        :param time_created:
            The value to assign to the time_created property of this DeploymentUpgradeSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DeploymentUpgradeSummary.
        :type time_updated: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DeploymentUpgradeSummary.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", "IN_PROGRESS", "CANCELING", "CANCELED", "SUCCEEDED", "WAITING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_sub_state:
            The value to assign to the lifecycle_sub_state property of this DeploymentUpgradeSummary.
            Allowed values for this property are: "RECOVERING", "STARTING", "STOPPING", "MOVING", "UPGRADING", "RESTORING", "BACKUP_IN_PROGRESS", "ROLLBACK_IN_PROGRESS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_sub_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this DeploymentUpgradeSummary.
        :type lifecycle_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DeploymentUpgradeSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DeploymentUpgradeSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this DeploymentUpgradeSummary.
        :type system_tags: dict(str, dict(str, object))

        :param previous_ogg_version:
            The value to assign to the previous_ogg_version property of this DeploymentUpgradeSummary.
        :type previous_ogg_version: str

        :param time_schedule:
            The value to assign to the time_schedule property of this DeploymentUpgradeSummary.
        :type time_schedule: datetime

        :param is_snoozed:
            The value to assign to the is_snoozed property of this DeploymentUpgradeSummary.
        :type is_snoozed: bool

        :param time_snoozed_until:
            The value to assign to the time_snoozed_until property of this DeploymentUpgradeSummary.
        :type time_snoozed_until: datetime

        :param time_released:
            The value to assign to the time_released property of this DeploymentUpgradeSummary.
        :type time_released: datetime

        :param release_type:
            The value to assign to the release_type property of this DeploymentUpgradeSummary.
            Allowed values for this property are: "MAJOR", "BUNDLE", "MINOR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type release_type: str

        :param is_security_fix:
            The value to assign to the is_security_fix property of this DeploymentUpgradeSummary.
        :type is_security_fix: bool

        :param is_rollback_allowed:
            The value to assign to the is_rollback_allowed property of this DeploymentUpgradeSummary.
        :type is_rollback_allowed: bool

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'deployment_id': 'str',
            'deployment_upgrade_type': 'str',
            'time_started': 'datetime',
            'time_finished': 'datetime',
            'ogg_version': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_sub_state': 'str',
            'lifecycle_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'previous_ogg_version': 'str',
            'time_schedule': 'datetime',
            'is_snoozed': 'bool',
            'time_snoozed_until': 'datetime',
            'time_released': 'datetime',
            'release_type': 'str',
            'is_security_fix': 'bool',
            'is_rollback_allowed': 'bool'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'deployment_id': 'deploymentId',
            'deployment_upgrade_type': 'deploymentUpgradeType',
            'time_started': 'timeStarted',
            'time_finished': 'timeFinished',
            'ogg_version': 'oggVersion',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_sub_state': 'lifecycleSubState',
            'lifecycle_details': 'lifecycleDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'previous_ogg_version': 'previousOggVersion',
            'time_schedule': 'timeSchedule',
            'is_snoozed': 'isSnoozed',
            'time_snoozed_until': 'timeSnoozedUntil',
            'time_released': 'timeReleased',
            'release_type': 'releaseType',
            'is_security_fix': 'isSecurityFix',
            'is_rollback_allowed': 'isRollbackAllowed'
        }

        self._id = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._deployment_id = None
        self._deployment_upgrade_type = None
        self._time_started = None
        self._time_finished = None
        self._ogg_version = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_state = None
        self._lifecycle_sub_state = None
        self._lifecycle_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._previous_ogg_version = None
        self._time_schedule = None
        self._is_snoozed = None
        self._time_snoozed_until = None
        self._time_released = None
        self._release_type = None
        self._is_security_fix = None
        self._is_rollback_allowed = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DeploymentUpgradeSummary.
        The `OCID`__ of the deployment being referenced.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DeploymentUpgradeSummary.
        The `OCID`__ of the deployment being referenced.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this DeploymentUpgradeSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        Gets the display_name of this DeploymentUpgradeSummary.
        An object's Display Name.


        :return: The display_name of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DeploymentUpgradeSummary.
        An object's Display Name.


        :param display_name: The display_name of this DeploymentUpgradeSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this DeploymentUpgradeSummary.
        Metadata about this specific object.


        :return: The description of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DeploymentUpgradeSummary.
        Metadata about this specific object.


        :param description: The description of this DeploymentUpgradeSummary.
        :type: str
        """
        self._description = description

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DeploymentUpgradeSummary.
        The `OCID`__ of the compartment being referenced.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DeploymentUpgradeSummary.
        The `OCID`__ of the compartment being referenced.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this DeploymentUpgradeSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def deployment_id(self):
        """
        **[Required]** Gets the deployment_id of this DeploymentUpgradeSummary.
        The `OCID`__ of the deployment being referenced.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The deployment_id of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._deployment_id

    @deployment_id.setter
    def deployment_id(self, deployment_id):
        """
        Sets the deployment_id of this DeploymentUpgradeSummary.
        The `OCID`__ of the deployment being referenced.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param deployment_id: The deployment_id of this DeploymentUpgradeSummary.
        :type: str
        """
        self._deployment_id = deployment_id

    @property
    def deployment_upgrade_type(self):
        """
        **[Required]** Gets the deployment_upgrade_type of this DeploymentUpgradeSummary.
        The type of the deployment upgrade: MANUAL or AUTOMATIC

        Allowed values for this property are: "MANUAL", "AUTOMATIC", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The deployment_upgrade_type of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._deployment_upgrade_type

    @deployment_upgrade_type.setter
    def deployment_upgrade_type(self, deployment_upgrade_type):
        """
        Sets the deployment_upgrade_type of this DeploymentUpgradeSummary.
        The type of the deployment upgrade: MANUAL or AUTOMATIC


        :param deployment_upgrade_type: The deployment_upgrade_type of this DeploymentUpgradeSummary.
        :type: str
        """
        allowed_values = ["MANUAL", "AUTOMATIC"]
        if not value_allowed_none_or_none_sentinel(deployment_upgrade_type, allowed_values):
            deployment_upgrade_type = 'UNKNOWN_ENUM_VALUE'
        self._deployment_upgrade_type = deployment_upgrade_type

    @property
    def time_started(self):
        """
        Gets the time_started of this DeploymentUpgradeSummary.
        The date and time the request was started. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_started of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this DeploymentUpgradeSummary.
        The date and time the request was started. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_started: The time_started of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        Gets the time_finished of this DeploymentUpgradeSummary.
        The date and time the request was finished. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_finished of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this DeploymentUpgradeSummary.
        The date and time the request was finished. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_finished: The time_finished of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def ogg_version(self):
        """
        Gets the ogg_version of this DeploymentUpgradeSummary.
        Version of OGG


        :return: The ogg_version of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._ogg_version

    @ogg_version.setter
    def ogg_version(self, ogg_version):
        """
        Sets the ogg_version of this DeploymentUpgradeSummary.
        Version of OGG


        :param ogg_version: The ogg_version of this DeploymentUpgradeSummary.
        :type: str
        """
        self._ogg_version = ogg_version

    @property
    def time_created(self):
        """
        Gets the time_created of this DeploymentUpgradeSummary.
        The time the resource was created. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this DeploymentUpgradeSummary.
        The time the resource was created. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this DeploymentUpgradeSummary.
        The time the resource was last updated. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this DeploymentUpgradeSummary.
        The time the resource was last updated. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this DeploymentUpgradeSummary.
        Possible lifecycle states.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", "IN_PROGRESS", "CANCELING", "CANCELED", "SUCCEEDED", "WAITING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DeploymentUpgradeSummary.
        Possible lifecycle states.


        :param lifecycle_state: The lifecycle_state of this DeploymentUpgradeSummary.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", "IN_PROGRESS", "CANCELING", "CANCELED", "SUCCEEDED", "WAITING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_sub_state(self):
        """
        Gets the lifecycle_sub_state of this DeploymentUpgradeSummary.
        Possible GGS lifecycle sub-states.

        Allowed values for this property are: "RECOVERING", "STARTING", "STOPPING", "MOVING", "UPGRADING", "RESTORING", "BACKUP_IN_PROGRESS", "ROLLBACK_IN_PROGRESS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_sub_state of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._lifecycle_sub_state

    @lifecycle_sub_state.setter
    def lifecycle_sub_state(self, lifecycle_sub_state):
        """
        Sets the lifecycle_sub_state of this DeploymentUpgradeSummary.
        Possible GGS lifecycle sub-states.


        :param lifecycle_sub_state: The lifecycle_sub_state of this DeploymentUpgradeSummary.
        :type: str
        """
        allowed_values = ["RECOVERING", "STARTING", "STOPPING", "MOVING", "UPGRADING", "RESTORING", "BACKUP_IN_PROGRESS", "ROLLBACK_IN_PROGRESS"]
        if not value_allowed_none_or_none_sentinel(lifecycle_sub_state, allowed_values):
            lifecycle_sub_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_sub_state = lifecycle_sub_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this DeploymentUpgradeSummary.
        Describes the object's current state in detail. For example, it can be used to provide
        actionable information for a resource in a Failed state.


        :return: The lifecycle_details of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this DeploymentUpgradeSummary.
        Describes the object's current state in detail. For example, it can be used to provide
        actionable information for a resource in a Failed state.


        :param lifecycle_details: The lifecycle_details of this DeploymentUpgradeSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DeploymentUpgradeSummary.
        A simple key-value pair that is applied without any predefined name, type, or scope. Exists
        for cross-compatibility only.

        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this DeploymentUpgradeSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DeploymentUpgradeSummary.
        A simple key-value pair that is applied without any predefined name, type, or scope. Exists
        for cross-compatibility only.

        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this DeploymentUpgradeSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DeploymentUpgradeSummary.
        Tags defined for this resource. Each key is predefined and scoped to a namespace.

        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this DeploymentUpgradeSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DeploymentUpgradeSummary.
        Tags defined for this resource. Each key is predefined and scoped to a namespace.

        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this DeploymentUpgradeSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DeploymentUpgradeSummary.
        The system tags associated with this resource, if any. The system tags are set by Oracle
        Cloud Infrastructure services. Each key is predefined and scoped to namespaces.  For more
        information, see `Resource Tags`__.

        Example: `{orcl-cloud: {free-tier-retain: true}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The system_tags of this DeploymentUpgradeSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DeploymentUpgradeSummary.
        The system tags associated with this resource, if any. The system tags are set by Oracle
        Cloud Infrastructure services. Each key is predefined and scoped to namespaces.  For more
        information, see `Resource Tags`__.

        Example: `{orcl-cloud: {free-tier-retain: true}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param system_tags: The system_tags of this DeploymentUpgradeSummary.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def previous_ogg_version(self):
        """
        Gets the previous_ogg_version of this DeploymentUpgradeSummary.
        Version of OGG


        :return: The previous_ogg_version of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._previous_ogg_version

    @previous_ogg_version.setter
    def previous_ogg_version(self, previous_ogg_version):
        """
        Sets the previous_ogg_version of this DeploymentUpgradeSummary.
        Version of OGG


        :param previous_ogg_version: The previous_ogg_version of this DeploymentUpgradeSummary.
        :type: str
        """
        self._previous_ogg_version = previous_ogg_version

    @property
    def time_schedule(self):
        """
        Gets the time_schedule of this DeploymentUpgradeSummary.
        The time of upgrade schedule. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_schedule of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_schedule

    @time_schedule.setter
    def time_schedule(self, time_schedule):
        """
        Sets the time_schedule of this DeploymentUpgradeSummary.
        The time of upgrade schedule. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_schedule: The time_schedule of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_schedule = time_schedule

    @property
    def is_snoozed(self):
        """
        Gets the is_snoozed of this DeploymentUpgradeSummary.
        Indicates if upgrade notifications are snoozed or not.


        :return: The is_snoozed of this DeploymentUpgradeSummary.
        :rtype: bool
        """
        return self._is_snoozed

    @is_snoozed.setter
    def is_snoozed(self, is_snoozed):
        """
        Sets the is_snoozed of this DeploymentUpgradeSummary.
        Indicates if upgrade notifications are snoozed or not.


        :param is_snoozed: The is_snoozed of this DeploymentUpgradeSummary.
        :type: bool
        """
        self._is_snoozed = is_snoozed

    @property
    def time_snoozed_until(self):
        """
        Gets the time_snoozed_until of this DeploymentUpgradeSummary.
        The time the upgrade notifications are snoozed until. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_snoozed_until of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_snoozed_until

    @time_snoozed_until.setter
    def time_snoozed_until(self, time_snoozed_until):
        """
        Sets the time_snoozed_until of this DeploymentUpgradeSummary.
        The time the upgrade notifications are snoozed until. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_snoozed_until: The time_snoozed_until of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_snoozed_until = time_snoozed_until

    @property
    def time_released(self):
        """
        Gets the time_released of this DeploymentUpgradeSummary.
        The time the resource was released. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_released of this DeploymentUpgradeSummary.
        :rtype: datetime
        """
        return self._time_released

    @time_released.setter
    def time_released(self, time_released):
        """
        Sets the time_released of this DeploymentUpgradeSummary.
        The time the resource was released. The format is defined by
        `RFC3339`__, such as `2016-08-25T21:10:29.600Z`.

        __ https://tools.ietf.org/html/rfc3339


        :param time_released: The time_released of this DeploymentUpgradeSummary.
        :type: datetime
        """
        self._time_released = time_released

    @property
    def release_type(self):
        """
        Gets the release_type of this DeploymentUpgradeSummary.
        The type of release.

        Allowed values for this property are: "MAJOR", "BUNDLE", "MINOR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The release_type of this DeploymentUpgradeSummary.
        :rtype: str
        """
        return self._release_type

    @release_type.setter
    def release_type(self, release_type):
        """
        Sets the release_type of this DeploymentUpgradeSummary.
        The type of release.


        :param release_type: The release_type of this DeploymentUpgradeSummary.
        :type: str
        """
        allowed_values = ["MAJOR", "BUNDLE", "MINOR"]
        if not value_allowed_none_or_none_sentinel(release_type, allowed_values):
            release_type = 'UNKNOWN_ENUM_VALUE'
        self._release_type = release_type

    @property
    def is_security_fix(self):
        """
        Gets the is_security_fix of this DeploymentUpgradeSummary.
        Indicates if OGG release contains security fix.


        :return: The is_security_fix of this DeploymentUpgradeSummary.
        :rtype: bool
        """
        return self._is_security_fix

    @is_security_fix.setter
    def is_security_fix(self, is_security_fix):
        """
        Sets the is_security_fix of this DeploymentUpgradeSummary.
        Indicates if OGG release contains security fix.


        :param is_security_fix: The is_security_fix of this DeploymentUpgradeSummary.
        :type: bool
        """
        self._is_security_fix = is_security_fix

    @property
    def is_rollback_allowed(self):
        """
        Gets the is_rollback_allowed of this DeploymentUpgradeSummary.
        Indicates if rollback is allowed. In practice only the last upgrade can be rolled back.
        - Manual upgrade is allowed to rollback only until the old version isn't deprecated yet.
        - Automatic upgrade by default is not allowed, unless a serious issue does not justify.


        :return: The is_rollback_allowed of this DeploymentUpgradeSummary.
        :rtype: bool
        """
        return self._is_rollback_allowed

    @is_rollback_allowed.setter
    def is_rollback_allowed(self, is_rollback_allowed):
        """
        Sets the is_rollback_allowed of this DeploymentUpgradeSummary.
        Indicates if rollback is allowed. In practice only the last upgrade can be rolled back.
        - Manual upgrade is allowed to rollback only until the old version isn't deprecated yet.
        - Automatic upgrade by default is not allowed, unless a serious issue does not justify.


        :param is_rollback_allowed: The is_rollback_allowed of this DeploymentUpgradeSummary.
        :type: bool
        """
        self._is_rollback_allowed = is_rollback_allowed

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
