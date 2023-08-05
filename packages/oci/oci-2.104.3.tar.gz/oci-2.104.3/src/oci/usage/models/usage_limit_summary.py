# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UsageLimitSummary(object):
    """
    Encapsulates a collection of Hard and Soft Limits for a resource within a subscription.
    """

    #: A constant which can be used with the action property of a UsageLimitSummary.
    #: This constant has a value of "QUOTA_BREACH"
    ACTION_QUOTA_BREACH = "QUOTA_BREACH"

    #: A constant which can be used with the action property of a UsageLimitSummary.
    #: This constant has a value of "QUOTA_ALERT"
    ACTION_QUOTA_ALERT = "QUOTA_ALERT"

    #: A constant which can be used with the limit_type property of a UsageLimitSummary.
    #: This constant has a value of "HARD"
    LIMIT_TYPE_HARD = "HARD"

    #: A constant which can be used with the limit_type property of a UsageLimitSummary.
    #: This constant has a value of "SOFT"
    LIMIT_TYPE_SOFT = "SOFT"

    #: A constant which can be used with the value_type property of a UsageLimitSummary.
    #: This constant has a value of "ABSOLUTE"
    VALUE_TYPE_ABSOLUTE = "ABSOLUTE"

    #: A constant which can be used with the value_type property of a UsageLimitSummary.
    #: This constant has a value of "PERCENTAGE"
    VALUE_TYPE_PERCENTAGE = "PERCENTAGE"

    #: A constant which can be used with the lifecycle_state property of a UsageLimitSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    def __init__(self, **kwargs):
        """
        Initializes a new UsageLimitSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_created:
            The value to assign to the time_created property of this UsageLimitSummary.
        :type time_created: datetime

        :param entitlement_id:
            The value to assign to the entitlement_id property of this UsageLimitSummary.
        :type entitlement_id: str

        :param id:
            The value to assign to the id property of this UsageLimitSummary.
        :type id: str

        :param time_modified:
            The value to assign to the time_modified property of this UsageLimitSummary.
        :type time_modified: datetime

        :param resource_name:
            The value to assign to the resource_name property of this UsageLimitSummary.
        :type resource_name: str

        :param service_name:
            The value to assign to the service_name property of this UsageLimitSummary.
        :type service_name: str

        :param limit:
            The value to assign to the limit property of this UsageLimitSummary.
        :type limit: str

        :param created_by:
            The value to assign to the created_by property of this UsageLimitSummary.
        :type created_by: str

        :param modified_by:
            The value to assign to the modified_by property of this UsageLimitSummary.
        :type modified_by: str

        :param action:
            The value to assign to the action property of this UsageLimitSummary.
            Allowed values for this property are: "QUOTA_BREACH", "QUOTA_ALERT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action: str

        :param alert_level:
            The value to assign to the alert_level property of this UsageLimitSummary.
        :type alert_level: float

        :param limit_type:
            The value to assign to the limit_type property of this UsageLimitSummary.
            Allowed values for this property are: "HARD", "SOFT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type limit_type: str

        :param value_type:
            The value to assign to the value_type property of this UsageLimitSummary.
            Allowed values for this property are: "ABSOLUTE", "PERCENTAGE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type value_type: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this UsageLimitSummary.
            Allowed values for this property are: "ACTIVE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param max_hard_limit:
            The value to assign to the max_hard_limit property of this UsageLimitSummary.
        :type max_hard_limit: str

        :param sku_part_id:
            The value to assign to the sku_part_id property of this UsageLimitSummary.
        :type sku_part_id: str

        """
        self.swagger_types = {
            'time_created': 'datetime',
            'entitlement_id': 'str',
            'id': 'str',
            'time_modified': 'datetime',
            'resource_name': 'str',
            'service_name': 'str',
            'limit': 'str',
            'created_by': 'str',
            'modified_by': 'str',
            'action': 'str',
            'alert_level': 'float',
            'limit_type': 'str',
            'value_type': 'str',
            'lifecycle_state': 'str',
            'max_hard_limit': 'str',
            'sku_part_id': 'str'
        }

        self.attribute_map = {
            'time_created': 'timeCreated',
            'entitlement_id': 'entitlementId',
            'id': 'id',
            'time_modified': 'timeModified',
            'resource_name': 'resourceName',
            'service_name': 'serviceName',
            'limit': 'limit',
            'created_by': 'createdBy',
            'modified_by': 'modifiedBy',
            'action': 'action',
            'alert_level': 'alertLevel',
            'limit_type': 'limitType',
            'value_type': 'valueType',
            'lifecycle_state': 'lifecycleState',
            'max_hard_limit': 'maxHardLimit',
            'sku_part_id': 'skuPartId'
        }

        self._time_created = None
        self._entitlement_id = None
        self._id = None
        self._time_modified = None
        self._resource_name = None
        self._service_name = None
        self._limit = None
        self._created_by = None
        self._modified_by = None
        self._action = None
        self._alert_level = None
        self._limit_type = None
        self._value_type = None
        self._lifecycle_state = None
        self._max_hard_limit = None
        self._sku_part_id = None

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this UsageLimitSummary.
        Time when the usage limit was created


        :return: The time_created of this UsageLimitSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this UsageLimitSummary.
        Time when the usage limit was created


        :param time_created: The time_created of this UsageLimitSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def entitlement_id(self):
        """
        **[Required]** Gets the entitlement_id of this UsageLimitSummary.
        Entitlement ID of the usage limit


        :return: The entitlement_id of this UsageLimitSummary.
        :rtype: str
        """
        return self._entitlement_id

    @entitlement_id.setter
    def entitlement_id(self, entitlement_id):
        """
        Sets the entitlement_id of this UsageLimitSummary.
        Entitlement ID of the usage limit


        :param entitlement_id: The entitlement_id of this UsageLimitSummary.
        :type: str
        """
        self._entitlement_id = entitlement_id

    @property
    def id(self):
        """
        **[Required]** Gets the id of this UsageLimitSummary.
        The usage limit ID


        :return: The id of this UsageLimitSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UsageLimitSummary.
        The usage limit ID


        :param id: The id of this UsageLimitSummary.
        :type: str
        """
        self._id = id

    @property
    def time_modified(self):
        """
        **[Required]** Gets the time_modified of this UsageLimitSummary.
        Time when the usage limit was modified


        :return: The time_modified of this UsageLimitSummary.
        :rtype: datetime
        """
        return self._time_modified

    @time_modified.setter
    def time_modified(self, time_modified):
        """
        Sets the time_modified of this UsageLimitSummary.
        Time when the usage limit was modified


        :param time_modified: The time_modified of this UsageLimitSummary.
        :type: datetime
        """
        self._time_modified = time_modified

    @property
    def resource_name(self):
        """
        **[Required]** Gets the resource_name of this UsageLimitSummary.
        The resource for which the limit is defined


        :return: The resource_name of this UsageLimitSummary.
        :rtype: str
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """
        Sets the resource_name of this UsageLimitSummary.
        The resource for which the limit is defined


        :param resource_name: The resource_name of this UsageLimitSummary.
        :type: str
        """
        self._resource_name = resource_name

    @property
    def service_name(self):
        """
        **[Required]** Gets the service_name of this UsageLimitSummary.
        The service for which the limit is defined


        :return: The service_name of this UsageLimitSummary.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this UsageLimitSummary.
        The service for which the limit is defined


        :param service_name: The service_name of this UsageLimitSummary.
        :type: str
        """
        self._service_name = service_name

    @property
    def limit(self):
        """
        **[Required]** Gets the limit of this UsageLimitSummary.
        The limit value


        :return: The limit of this UsageLimitSummary.
        :rtype: str
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """
        Sets the limit of this UsageLimitSummary.
        The limit value


        :param limit: The limit of this UsageLimitSummary.
        :type: str
        """
        self._limit = limit

    @property
    def created_by(self):
        """
        **[Required]** Gets the created_by of this UsageLimitSummary.
        The user who created the limit


        :return: The created_by of this UsageLimitSummary.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this UsageLimitSummary.
        The user who created the limit


        :param created_by: The created_by of this UsageLimitSummary.
        :type: str
        """
        self._created_by = created_by

    @property
    def modified_by(self):
        """
        **[Required]** Gets the modified_by of this UsageLimitSummary.
        The user who modified the limit


        :return: The modified_by of this UsageLimitSummary.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this UsageLimitSummary.
        The user who modified the limit


        :param modified_by: The modified_by of this UsageLimitSummary.
        :type: str
        """
        self._modified_by = modified_by

    @property
    def action(self):
        """
        **[Required]** Gets the action of this UsageLimitSummary.
        The action when usage limit is hit

        Allowed values for this property are: "QUOTA_BREACH", "QUOTA_ALERT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The action of this UsageLimitSummary.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this UsageLimitSummary.
        The action when usage limit is hit


        :param action: The action of this UsageLimitSummary.
        :type: str
        """
        allowed_values = ["QUOTA_BREACH", "QUOTA_ALERT"]
        if not value_allowed_none_or_none_sentinel(action, allowed_values):
            action = 'UNKNOWN_ENUM_VALUE'
        self._action = action

    @property
    def alert_level(self):
        """
        **[Required]** Gets the alert_level of this UsageLimitSummary.
        The alert level of the usage limit


        :return: The alert_level of this UsageLimitSummary.
        :rtype: float
        """
        return self._alert_level

    @alert_level.setter
    def alert_level(self, alert_level):
        """
        Sets the alert_level of this UsageLimitSummary.
        The alert level of the usage limit


        :param alert_level: The alert_level of this UsageLimitSummary.
        :type: float
        """
        self._alert_level = alert_level

    @property
    def limit_type(self):
        """
        **[Required]** Gets the limit_type of this UsageLimitSummary.
        The limit type of the usage limit

        Allowed values for this property are: "HARD", "SOFT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The limit_type of this UsageLimitSummary.
        :rtype: str
        """
        return self._limit_type

    @limit_type.setter
    def limit_type(self, limit_type):
        """
        Sets the limit_type of this UsageLimitSummary.
        The limit type of the usage limit


        :param limit_type: The limit_type of this UsageLimitSummary.
        :type: str
        """
        allowed_values = ["HARD", "SOFT"]
        if not value_allowed_none_or_none_sentinel(limit_type, allowed_values):
            limit_type = 'UNKNOWN_ENUM_VALUE'
        self._limit_type = limit_type

    @property
    def value_type(self):
        """
        **[Required]** Gets the value_type of this UsageLimitSummary.
        The value type of the usage limit

        Allowed values for this property are: "ABSOLUTE", "PERCENTAGE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The value_type of this UsageLimitSummary.
        :rtype: str
        """
        return self._value_type

    @value_type.setter
    def value_type(self, value_type):
        """
        Sets the value_type of this UsageLimitSummary.
        The value type of the usage limit


        :param value_type: The value_type of this UsageLimitSummary.
        :type: str
        """
        allowed_values = ["ABSOLUTE", "PERCENTAGE"]
        if not value_allowed_none_or_none_sentinel(value_type, allowed_values):
            value_type = 'UNKNOWN_ENUM_VALUE'
        self._value_type = value_type

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this UsageLimitSummary.
        The usage limit lifecycle state.

        Allowed values for this property are: "ACTIVE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this UsageLimitSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this UsageLimitSummary.
        The usage limit lifecycle state.


        :param lifecycle_state: The lifecycle_state of this UsageLimitSummary.
        :type: str
        """
        allowed_values = ["ACTIVE"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def max_hard_limit(self):
        """
        Gets the max_hard_limit of this UsageLimitSummary.
        The maximum hard limit set for the usage limit


        :return: The max_hard_limit of this UsageLimitSummary.
        :rtype: str
        """
        return self._max_hard_limit

    @max_hard_limit.setter
    def max_hard_limit(self, max_hard_limit):
        """
        Sets the max_hard_limit of this UsageLimitSummary.
        The maximum hard limit set for the usage limit


        :param max_hard_limit: The max_hard_limit of this UsageLimitSummary.
        :type: str
        """
        self._max_hard_limit = max_hard_limit

    @property
    def sku_part_id(self):
        """
        Gets the sku_part_id of this UsageLimitSummary.
        The SKU for which the usage limit is set


        :return: The sku_part_id of this UsageLimitSummary.
        :rtype: str
        """
        return self._sku_part_id

    @sku_part_id.setter
    def sku_part_id(self, sku_part_id):
        """
        Sets the sku_part_id of this UsageLimitSummary.
        The SKU for which the usage limit is set


        :param sku_part_id: The sku_part_id of this UsageLimitSummary.
        :type: str
        """
        self._sku_part_id = sku_part_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
