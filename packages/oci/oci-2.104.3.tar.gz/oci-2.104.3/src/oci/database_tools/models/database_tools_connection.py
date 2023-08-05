# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DatabaseToolsConnection(object):
    """
    Description of the Database Tools connection.
    """

    #: A constant which can be used with the lifecycle_state property of a DatabaseToolsConnection.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a DatabaseToolsConnection.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a DatabaseToolsConnection.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a DatabaseToolsConnection.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a DatabaseToolsConnection.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a DatabaseToolsConnection.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the type property of a DatabaseToolsConnection.
    #: This constant has a value of "ORACLE_DATABASE"
    TYPE_ORACLE_DATABASE = "ORACLE_DATABASE"

    #: A constant which can be used with the type property of a DatabaseToolsConnection.
    #: This constant has a value of "MYSQL"
    TYPE_MYSQL = "MYSQL"

    def __init__(self, **kwargs):
        """
        Initializes a new DatabaseToolsConnection object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.database_tools.models.DatabaseToolsConnectionOracleDatabase`
        * :class:`~oci.database_tools.models.DatabaseToolsConnectionMySql`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DatabaseToolsConnection.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this DatabaseToolsConnection.
        :type display_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DatabaseToolsConnection.
        :type compartment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DatabaseToolsConnection.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this DatabaseToolsConnection.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this DatabaseToolsConnection.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this DatabaseToolsConnection.
        :type time_updated: datetime

        :param defined_tags:
            The value to assign to the defined_tags property of this DatabaseToolsConnection.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DatabaseToolsConnection.
        :type freeform_tags: dict(str, str)

        :param system_tags:
            The value to assign to the system_tags property of this DatabaseToolsConnection.
        :type system_tags: dict(str, dict(str, object))

        :param type:
            The value to assign to the type property of this DatabaseToolsConnection.
            Allowed values for this property are: "ORACLE_DATABASE", "MYSQL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'compartment_id': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'system_tags': 'dict(str, dict(str, object))',
            'type': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'compartment_id': 'compartmentId',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'system_tags': 'systemTags',
            'type': 'type'
        }

        self._id = None
        self._display_name = None
        self._compartment_id = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None
        self._defined_tags = None
        self._freeform_tags = None
        self._system_tags = None
        self._type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'ORACLE_DATABASE':
            return 'DatabaseToolsConnectionOracleDatabase'

        if type == 'MYSQL':
            return 'DatabaseToolsConnectionMySql'
        else:
            return 'DatabaseToolsConnection'

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DatabaseToolsConnection.
        The `OCID`__ of the Database Tools connection.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this DatabaseToolsConnection.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DatabaseToolsConnection.
        The `OCID`__ of the Database Tools connection.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this DatabaseToolsConnection.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this DatabaseToolsConnection.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :return: The display_name of this DatabaseToolsConnection.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DatabaseToolsConnection.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :param display_name: The display_name of this DatabaseToolsConnection.
        :type: str
        """
        self._display_name = display_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DatabaseToolsConnection.
        The `OCID`__ of the compartment containing the Database Tools connection.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this DatabaseToolsConnection.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DatabaseToolsConnection.
        The `OCID`__ of the compartment containing the Database Tools connection.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this DatabaseToolsConnection.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this DatabaseToolsConnection.
        The current state of the Database Tools connection.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DatabaseToolsConnection.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DatabaseToolsConnection.
        The current state of the Database Tools connection.


        :param lifecycle_state: The lifecycle_state of this DatabaseToolsConnection.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this DatabaseToolsConnection.
        A message describing the current state in more detail. For example, this message can be used to provide actionable information for a resource in the Failed state.


        :return: The lifecycle_details of this DatabaseToolsConnection.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this DatabaseToolsConnection.
        A message describing the current state in more detail. For example, this message can be used to provide actionable information for a resource in the Failed state.


        :param lifecycle_details: The lifecycle_details of this DatabaseToolsConnection.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this DatabaseToolsConnection.
        The time the Database Tools connection was created. An RFC3339 formatted datetime string.


        :return: The time_created of this DatabaseToolsConnection.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this DatabaseToolsConnection.
        The time the Database Tools connection was created. An RFC3339 formatted datetime string.


        :param time_created: The time_created of this DatabaseToolsConnection.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this DatabaseToolsConnection.
        The time the DatabaseToolsConnection was updated. An RFC3339 formatted datetime string.


        :return: The time_updated of this DatabaseToolsConnection.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this DatabaseToolsConnection.
        The time the DatabaseToolsConnection was updated. An RFC3339 formatted datetime string.


        :param time_updated: The time_updated of this DatabaseToolsConnection.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DatabaseToolsConnection.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this DatabaseToolsConnection.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DatabaseToolsConnection.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this DatabaseToolsConnection.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DatabaseToolsConnection.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this DatabaseToolsConnection.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DatabaseToolsConnection.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this DatabaseToolsConnection.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DatabaseToolsConnection.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this DatabaseToolsConnection.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DatabaseToolsConnection.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this DatabaseToolsConnection.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def type(self):
        """
        **[Required]** Gets the type of this DatabaseToolsConnection.
        The Database Tools connection type.

        Allowed values for this property are: "ORACLE_DATABASE", "MYSQL", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this DatabaseToolsConnection.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this DatabaseToolsConnection.
        The Database Tools connection type.


        :param type: The type of this DatabaseToolsConnection.
        :type: str
        """
        allowed_values = ["ORACLE_DATABASE", "MYSQL"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
