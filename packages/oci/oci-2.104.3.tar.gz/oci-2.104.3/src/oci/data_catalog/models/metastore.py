# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Metastore(object):
    """
    A Data Catalog Metastore provides a centralized metastore repository for use by other OCI services.
    """

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a Metastore.
    #: This constant has a value of "MOVING"
    LIFECYCLE_STATE_MOVING = "MOVING"

    def __init__(self, **kwargs):
        """
        Initializes a new Metastore object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Metastore.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this Metastore.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this Metastore.
        :type compartment_id: str

        :param time_created:
            The value to assign to the time_created property of this Metastore.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this Metastore.
        :type time_updated: datetime

        :param default_managed_table_location:
            The value to assign to the default_managed_table_location property of this Metastore.
        :type default_managed_table_location: str

        :param default_external_table_location:
            The value to assign to the default_external_table_location property of this Metastore.
        :type default_external_table_location: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Metastore.
            Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "MOVING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this Metastore.
        :type lifecycle_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Metastore.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this Metastore.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'default_managed_table_location': 'str',
            'default_external_table_location': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'default_managed_table_location': 'defaultManagedTableLocation',
            'default_external_table_location': 'defaultExternalTableLocation',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._time_created = None
        self._time_updated = None
        self._default_managed_table_location = None
        self._default_external_table_location = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this Metastore.
        The metastore's OCID.


        :return: The id of this Metastore.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Metastore.
        The metastore's OCID.


        :param id: The id of this Metastore.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        Gets the display_name of this Metastore.
        Mutable name of the metastore.


        :return: The display_name of this Metastore.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this Metastore.
        Mutable name of the metastore.


        :param display_name: The display_name of this Metastore.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this Metastore.
        OCID of the compartment which holds the metastore.


        :return: The compartment_id of this Metastore.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this Metastore.
        OCID of the compartment which holds the metastore.


        :param compartment_id: The compartment_id of this Metastore.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_created(self):
        """
        Gets the time_created of this Metastore.
        Time at which the metastore was created. An `RFC3339`__ formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this Metastore.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this Metastore.
        Time at which the metastore was created. An `RFC3339`__ formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this Metastore.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this Metastore.
        Time at which the metastore was last modified. An `RFC3339`__ formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_updated of this Metastore.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this Metastore.
        Time at which the metastore was last modified. An `RFC3339`__ formatted datetime string.

        __ https://tools.ietf.org/html/rfc3339


        :param time_updated: The time_updated of this Metastore.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def default_managed_table_location(self):
        """
        **[Required]** Gets the default_managed_table_location of this Metastore.
        Location under which managed tables will be created by default. This references Object Storage
        using an HDFS URI format. Example: oci://bucket@namespace/sub-dir/


        :return: The default_managed_table_location of this Metastore.
        :rtype: str
        """
        return self._default_managed_table_location

    @default_managed_table_location.setter
    def default_managed_table_location(self, default_managed_table_location):
        """
        Sets the default_managed_table_location of this Metastore.
        Location under which managed tables will be created by default. This references Object Storage
        using an HDFS URI format. Example: oci://bucket@namespace/sub-dir/


        :param default_managed_table_location: The default_managed_table_location of this Metastore.
        :type: str
        """
        self._default_managed_table_location = default_managed_table_location

    @property
    def default_external_table_location(self):
        """
        **[Required]** Gets the default_external_table_location of this Metastore.
        Location under which external tables will be created by default. This references Object Storage
        using an HDFS URI format. Example: oci://bucket@namespace/sub-dir/


        :return: The default_external_table_location of this Metastore.
        :rtype: str
        """
        return self._default_external_table_location

    @default_external_table_location.setter
    def default_external_table_location(self, default_external_table_location):
        """
        Sets the default_external_table_location of this Metastore.
        Location under which external tables will be created by default. This references Object Storage
        using an HDFS URI format. Example: oci://bucket@namespace/sub-dir/


        :param default_external_table_location: The default_external_table_location of this Metastore.
        :type: str
        """
        self._default_external_table_location = default_external_table_location

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this Metastore.
        The current state of the metastore.

        Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "MOVING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Metastore.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Metastore.
        The current state of the metastore.


        :param lifecycle_state: The lifecycle_state of this Metastore.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "MOVING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this Metastore.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :return: The lifecycle_details of this Metastore.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this Metastore.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :param lifecycle_details: The lifecycle_details of this Metastore.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this Metastore.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this Metastore.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Metastore.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this Metastore.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this Metastore.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this Metastore.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Metastore.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this Metastore.
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
