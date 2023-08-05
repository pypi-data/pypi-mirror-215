# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TargetDatabase(object):
    """
    The details of the Data Safe target database.
    """

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    #: A constant which can be used with the lifecycle_state property of a TargetDatabase.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new TargetDatabase object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this TargetDatabase.
        :type compartment_id: str

        :param id:
            The value to assign to the id property of this TargetDatabase.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this TargetDatabase.
        :type display_name: str

        :param description:
            The value to assign to the description property of this TargetDatabase.
        :type description: str

        :param database_details:
            The value to assign to the database_details property of this TargetDatabase.
        :type database_details: oci.data_safe.models.DatabaseDetails

        :param credentials:
            The value to assign to the credentials property of this TargetDatabase.
        :type credentials: oci.data_safe.models.Credentials

        :param tls_config:
            The value to assign to the tls_config property of this TargetDatabase.
        :type tls_config: oci.data_safe.models.TlsConfig

        :param connection_option:
            The value to assign to the connection_option property of this TargetDatabase.
        :type connection_option: oci.data_safe.models.ConnectionOption

        :param associated_resource_ids:
            The value to assign to the associated_resource_ids property of this TargetDatabase.
        :type associated_resource_ids: list[str]

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this TargetDatabase.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "NEEDS_ATTENTION", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this TargetDatabase.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this TargetDatabase.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this TargetDatabase.
        :type time_updated: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this TargetDatabase.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this TargetDatabase.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this TargetDatabase.
        :type system_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'database_details': 'DatabaseDetails',
            'credentials': 'Credentials',
            'tls_config': 'TlsConfig',
            'connection_option': 'ConnectionOption',
            'associated_resource_ids': 'list[str]',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'database_details': 'databaseDetails',
            'credentials': 'credentials',
            'tls_config': 'tlsConfig',
            'connection_option': 'connectionOption',
            'associated_resource_ids': 'associatedResourceIds',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._compartment_id = None
        self._id = None
        self._display_name = None
        self._description = None
        self._database_details = None
        self._credentials = None
        self._tls_config = None
        self._connection_option = None
        self._associated_resource_ids = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this TargetDatabase.
        The OCID of the compartment which contains the Data Safe target database.


        :return: The compartment_id of this TargetDatabase.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this TargetDatabase.
        The OCID of the compartment which contains the Data Safe target database.


        :param compartment_id: The compartment_id of this TargetDatabase.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def id(self):
        """
        **[Required]** Gets the id of this TargetDatabase.
        The OCID of the Data Safe target database.


        :return: The id of this TargetDatabase.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this TargetDatabase.
        The OCID of the Data Safe target database.


        :param id: The id of this TargetDatabase.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this TargetDatabase.
        The display name of the target database in Data Safe.


        :return: The display_name of this TargetDatabase.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this TargetDatabase.
        The display name of the target database in Data Safe.


        :param display_name: The display_name of this TargetDatabase.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this TargetDatabase.
        The description of the target database in Data Safe.


        :return: The description of this TargetDatabase.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this TargetDatabase.
        The description of the target database in Data Safe.


        :param description: The description of this TargetDatabase.
        :type: str
        """
        self._description = description

    @property
    def database_details(self):
        """
        **[Required]** Gets the database_details of this TargetDatabase.

        :return: The database_details of this TargetDatabase.
        :rtype: oci.data_safe.models.DatabaseDetails
        """
        return self._database_details

    @database_details.setter
    def database_details(self, database_details):
        """
        Sets the database_details of this TargetDatabase.

        :param database_details: The database_details of this TargetDatabase.
        :type: oci.data_safe.models.DatabaseDetails
        """
        self._database_details = database_details

    @property
    def credentials(self):
        """
        Gets the credentials of this TargetDatabase.

        :return: The credentials of this TargetDatabase.
        :rtype: oci.data_safe.models.Credentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this TargetDatabase.

        :param credentials: The credentials of this TargetDatabase.
        :type: oci.data_safe.models.Credentials
        """
        self._credentials = credentials

    @property
    def tls_config(self):
        """
        Gets the tls_config of this TargetDatabase.

        :return: The tls_config of this TargetDatabase.
        :rtype: oci.data_safe.models.TlsConfig
        """
        return self._tls_config

    @tls_config.setter
    def tls_config(self, tls_config):
        """
        Sets the tls_config of this TargetDatabase.

        :param tls_config: The tls_config of this TargetDatabase.
        :type: oci.data_safe.models.TlsConfig
        """
        self._tls_config = tls_config

    @property
    def connection_option(self):
        """
        Gets the connection_option of this TargetDatabase.

        :return: The connection_option of this TargetDatabase.
        :rtype: oci.data_safe.models.ConnectionOption
        """
        return self._connection_option

    @connection_option.setter
    def connection_option(self, connection_option):
        """
        Sets the connection_option of this TargetDatabase.

        :param connection_option: The connection_option of this TargetDatabase.
        :type: oci.data_safe.models.ConnectionOption
        """
        self._connection_option = connection_option

    @property
    def associated_resource_ids(self):
        """
        Gets the associated_resource_ids of this TargetDatabase.
        The OCIDs of associated resources like Database, Data Safe private endpoint etc.


        :return: The associated_resource_ids of this TargetDatabase.
        :rtype: list[str]
        """
        return self._associated_resource_ids

    @associated_resource_ids.setter
    def associated_resource_ids(self, associated_resource_ids):
        """
        Sets the associated_resource_ids of this TargetDatabase.
        The OCIDs of associated resources like Database, Data Safe private endpoint etc.


        :param associated_resource_ids: The associated_resource_ids of this TargetDatabase.
        :type: list[str]
        """
        self._associated_resource_ids = associated_resource_ids

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this TargetDatabase.
        The current state of the target database in Data Safe.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "NEEDS_ATTENTION", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this TargetDatabase.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this TargetDatabase.
        The current state of the target database in Data Safe.


        :param lifecycle_state: The lifecycle_state of this TargetDatabase.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "NEEDS_ATTENTION", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this TargetDatabase.
        Details about the current state of the target database in Data Safe.


        :return: The lifecycle_details of this TargetDatabase.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this TargetDatabase.
        Details about the current state of the target database in Data Safe.


        :param lifecycle_details: The lifecycle_details of this TargetDatabase.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this TargetDatabase.
        The date and time of target database registration and creation in Data Safe.


        :return: The time_created of this TargetDatabase.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this TargetDatabase.
        The date and time of target database registration and creation in Data Safe.


        :param time_created: The time_created of this TargetDatabase.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this TargetDatabase.
        The date and time of the target database update in Data Safe.


        :return: The time_updated of this TargetDatabase.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this TargetDatabase.
        The date and time of the target database update in Data Safe.


        :param time_updated: The time_updated of this TargetDatabase.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this TargetDatabase.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this TargetDatabase.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this TargetDatabase.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this TargetDatabase.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this TargetDatabase.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this TargetDatabase.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this TargetDatabase.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this TargetDatabase.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this TargetDatabase.
        System tags for this resource. Each key is predefined and scoped to a namespace. For more information, see Resource Tags.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this TargetDatabase.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this TargetDatabase.
        System tags for this resource. Each key is predefined and scoped to a namespace. For more information, see Resource Tags.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this TargetDatabase.
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
