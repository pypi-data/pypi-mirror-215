# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddonOptionSummary(object):
    """
    The properties that define addon summary.
    """

    #: A constant which can be used with the lifecycle_state property of a AddonOptionSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a AddonOptionSummary.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    def __init__(self, **kwargs):
        """
        Initializes a new AddonOptionSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this AddonOptionSummary.
        :type name: str

        :param addon_schema_version:
            The value to assign to the addon_schema_version property of this AddonOptionSummary.
        :type addon_schema_version: str

        :param addon_group:
            The value to assign to the addon_group property of this AddonOptionSummary.
        :type addon_group: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this AddonOptionSummary.
            Allowed values for this property are: "ACTIVE", "INACTIVE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param description:
            The value to assign to the description property of this AddonOptionSummary.
        :type description: str

        :param is_essential:
            The value to assign to the is_essential property of this AddonOptionSummary.
        :type is_essential: bool

        :param versions:
            The value to assign to the versions property of this AddonOptionSummary.
        :type versions: list[oci.container_engine.models.AddonVersions]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this AddonOptionSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this AddonOptionSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this AddonOptionSummary.
        :type system_tags: dict(str, dict(str, object))

        :param time_created:
            The value to assign to the time_created property of this AddonOptionSummary.
        :type time_created: datetime

        """
        self.swagger_types = {
            'name': 'str',
            'addon_schema_version': 'str',
            'addon_group': 'str',
            'lifecycle_state': 'str',
            'description': 'str',
            'is_essential': 'bool',
            'versions': 'list[AddonVersions]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'time_created': 'datetime'
        }

        self.attribute_map = {
            'name': 'name',
            'addon_schema_version': 'addonSchemaVersion',
            'addon_group': 'addonGroup',
            'lifecycle_state': 'lifecycleState',
            'description': 'description',
            'is_essential': 'isEssential',
            'versions': 'versions',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'time_created': 'timeCreated'
        }

        self._name = None
        self._addon_schema_version = None
        self._addon_group = None
        self._lifecycle_state = None
        self._description = None
        self._is_essential = None
        self._versions = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._time_created = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this AddonOptionSummary.
        Name of the addon and it would be unique.


        :return: The name of this AddonOptionSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AddonOptionSummary.
        Name of the addon and it would be unique.


        :param name: The name of this AddonOptionSummary.
        :type: str
        """
        self._name = name

    @property
    def addon_schema_version(self):
        """
        Gets the addon_schema_version of this AddonOptionSummary.
        Addon definition schema version to validate addon.


        :return: The addon_schema_version of this AddonOptionSummary.
        :rtype: str
        """
        return self._addon_schema_version

    @addon_schema_version.setter
    def addon_schema_version(self, addon_schema_version):
        """
        Sets the addon_schema_version of this AddonOptionSummary.
        Addon definition schema version to validate addon.


        :param addon_schema_version: The addon_schema_version of this AddonOptionSummary.
        :type: str
        """
        self._addon_schema_version = addon_schema_version

    @property
    def addon_group(self):
        """
        Gets the addon_group of this AddonOptionSummary.
        Addon group info, a namespace concept that groups addons with similar functionalities.


        :return: The addon_group of this AddonOptionSummary.
        :rtype: str
        """
        return self._addon_group

    @addon_group.setter
    def addon_group(self, addon_group):
        """
        Sets the addon_group of this AddonOptionSummary.
        Addon group info, a namespace concept that groups addons with similar functionalities.


        :param addon_group: The addon_group of this AddonOptionSummary.
        :type: str
        """
        self._addon_group = addon_group

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this AddonOptionSummary.
        The life cycle state of the addon.

        Allowed values for this property are: "ACTIVE", "INACTIVE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this AddonOptionSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this AddonOptionSummary.
        The life cycle state of the addon.


        :param lifecycle_state: The lifecycle_state of this AddonOptionSummary.
        :type: str
        """
        allowed_values = ["ACTIVE", "INACTIVE"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def description(self):
        """
        Gets the description of this AddonOptionSummary.
        Description on the addon.


        :return: The description of this AddonOptionSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AddonOptionSummary.
        Description on the addon.


        :param description: The description of this AddonOptionSummary.
        :type: str
        """
        self._description = description

    @property
    def is_essential(self):
        """
        **[Required]** Gets the is_essential of this AddonOptionSummary.
        Is it an essential addon for cluster operation or not.


        :return: The is_essential of this AddonOptionSummary.
        :rtype: bool
        """
        return self._is_essential

    @is_essential.setter
    def is_essential(self, is_essential):
        """
        Sets the is_essential of this AddonOptionSummary.
        Is it an essential addon for cluster operation or not.


        :param is_essential: The is_essential of this AddonOptionSummary.
        :type: bool
        """
        self._is_essential = is_essential

    @property
    def versions(self):
        """
        **[Required]** Gets the versions of this AddonOptionSummary.
        The resources this work request affects.


        :return: The versions of this AddonOptionSummary.
        :rtype: list[oci.container_engine.models.AddonVersions]
        """
        return self._versions

    @versions.setter
    def versions(self, versions):
        """
        Sets the versions of this AddonOptionSummary.
        The resources this work request affects.


        :param versions: The versions of this AddonOptionSummary.
        :type: list[oci.container_engine.models.AddonVersions]
        """
        self._versions = versions

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this AddonOptionSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this AddonOptionSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this AddonOptionSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this AddonOptionSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this AddonOptionSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this AddonOptionSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this AddonOptionSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this AddonOptionSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this AddonOptionSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this AddonOptionSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this AddonOptionSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this AddonOptionSummary.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def time_created(self):
        """
        Gets the time_created of this AddonOptionSummary.
        The time the work request was created.


        :return: The time_created of this AddonOptionSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this AddonOptionSummary.
        The time the work request was created.


        :param time_created: The time_created of this AddonOptionSummary.
        :type: datetime
        """
        self._time_created = time_created

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
