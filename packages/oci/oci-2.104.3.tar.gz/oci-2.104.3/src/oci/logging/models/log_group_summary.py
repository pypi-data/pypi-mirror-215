# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LogGroupSummary(object):
    """
    Log group configuration summary.
    """

    #: A constant which can be used with the lifecycle_state property of a LogGroupSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a LogGroupSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a LogGroupSummary.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a LogGroupSummary.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a LogGroupSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a LogGroupSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new LogGroupSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this LogGroupSummary.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this LogGroupSummary.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this LogGroupSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this LogGroupSummary.
        :type description: str

        :param defined_tags:
            The value to assign to the defined_tags property of this LogGroupSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this LogGroupSummary.
        :type freeform_tags: dict(str, str)

        :param time_created:
            The value to assign to the time_created property of this LogGroupSummary.
        :type time_created: datetime

        :param time_last_modified:
            The value to assign to the time_last_modified property of this LogGroupSummary.
        :type time_last_modified: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this LogGroupSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "INACTIVE", "DELETING", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'time_created': 'datetime',
            'time_last_modified': 'datetime',
            'lifecycle_state': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'time_created': 'timeCreated',
            'time_last_modified': 'timeLastModified',
            'lifecycle_state': 'lifecycleState'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._defined_tags = None
        self._freeform_tags = None
        self._time_created = None
        self._time_last_modified = None
        self._lifecycle_state = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this LogGroupSummary.
        The OCID of the resource.


        :return: The id of this LogGroupSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this LogGroupSummary.
        The OCID of the resource.


        :param id: The id of this LogGroupSummary.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this LogGroupSummary.
        The OCID of the compartment that the resource belongs to.


        :return: The compartment_id of this LogGroupSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this LogGroupSummary.
        The OCID of the compartment that the resource belongs to.


        :param compartment_id: The compartment_id of this LogGroupSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this LogGroupSummary.
        The user-friendly display name. This must be unique within the enclosing resource,
        and it's changeable. Avoid entering confidential information.


        :return: The display_name of this LogGroupSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this LogGroupSummary.
        The user-friendly display name. This must be unique within the enclosing resource,
        and it's changeable. Avoid entering confidential information.


        :param display_name: The display_name of this LogGroupSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this LogGroupSummary.
        Description for this resource.


        :return: The description of this LogGroupSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this LogGroupSummary.
        Description for this resource.


        :param description: The description of this LogGroupSummary.
        :type: str
        """
        self._description = description

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this LogGroupSummary.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this LogGroupSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this LogGroupSummary.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this LogGroupSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this LogGroupSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this LogGroupSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this LogGroupSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this LogGroupSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def time_created(self):
        """
        Gets the time_created of this LogGroupSummary.
        Time the resource was created.


        :return: The time_created of this LogGroupSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this LogGroupSummary.
        Time the resource was created.


        :param time_created: The time_created of this LogGroupSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_last_modified(self):
        """
        Gets the time_last_modified of this LogGroupSummary.
        Time the resource was last modified.


        :return: The time_last_modified of this LogGroupSummary.
        :rtype: datetime
        """
        return self._time_last_modified

    @time_last_modified.setter
    def time_last_modified(self, time_last_modified):
        """
        Sets the time_last_modified of this LogGroupSummary.
        Time the resource was last modified.


        :param time_last_modified: The time_last_modified of this LogGroupSummary.
        :type: datetime
        """
        self._time_last_modified = time_last_modified

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this LogGroupSummary.
        The log group object state.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "INACTIVE", "DELETING", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this LogGroupSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this LogGroupSummary.
        The log group object state.


        :param lifecycle_state: The lifecycle_state of this LogGroupSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "INACTIVE", "DELETING", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
