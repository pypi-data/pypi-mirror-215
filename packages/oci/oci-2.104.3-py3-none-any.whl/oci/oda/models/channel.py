# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Channel(object):
    """
    Properties of a Channel.
    """

    #: A constant which can be used with the category property of a Channel.
    #: This constant has a value of "AGENT"
    CATEGORY_AGENT = "AGENT"

    #: A constant which can be used with the category property of a Channel.
    #: This constant has a value of "APPLICATION"
    CATEGORY_APPLICATION = "APPLICATION"

    #: A constant which can be used with the category property of a Channel.
    #: This constant has a value of "BOT"
    CATEGORY_BOT = "BOT"

    #: A constant which can be used with the category property of a Channel.
    #: This constant has a value of "BOT_AS_AGENT"
    CATEGORY_BOT_AS_AGENT = "BOT_AS_AGENT"

    #: A constant which can be used with the category property of a Channel.
    #: This constant has a value of "SYSTEM"
    CATEGORY_SYSTEM = "SYSTEM"

    #: A constant which can be used with the category property of a Channel.
    #: This constant has a value of "EVENT"
    CATEGORY_EVENT = "EVENT"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "ANDROID"
    TYPE_ANDROID = "ANDROID"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "APPEVENT"
    TYPE_APPEVENT = "APPEVENT"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "APPLICATION"
    TYPE_APPLICATION = "APPLICATION"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "CORTANA"
    TYPE_CORTANA = "CORTANA"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "FACEBOOK"
    TYPE_FACEBOOK = "FACEBOOK"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "IOS"
    TYPE_IOS = "IOS"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "MSTEAMS"
    TYPE_MSTEAMS = "MSTEAMS"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "OSS"
    TYPE_OSS = "OSS"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "OSVC"
    TYPE_OSVC = "OSVC"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "SERVICECLOUD"
    TYPE_SERVICECLOUD = "SERVICECLOUD"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "SLACK"
    TYPE_SLACK = "SLACK"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "TEST"
    TYPE_TEST = "TEST"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "TWILIO"
    TYPE_TWILIO = "TWILIO"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "WEB"
    TYPE_WEB = "WEB"

    #: A constant which can be used with the type property of a Channel.
    #: This constant has a value of "WEBHOOK"
    TYPE_WEBHOOK = "WEBHOOK"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a Channel.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new Channel object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.oda.models.AppEventChannel`
        * :class:`~oci.oda.models.FacebookChannel`
        * :class:`~oci.oda.models.WebChannel`
        * :class:`~oci.oda.models.MSTeamsChannel`
        * :class:`~oci.oda.models.TwilioChannel`
        * :class:`~oci.oda.models.OsvcChannel`
        * :class:`~oci.oda.models.AndroidChannel`
        * :class:`~oci.oda.models.OSSChannel`
        * :class:`~oci.oda.models.WebhookChannel`
        * :class:`~oci.oda.models.ApplicationChannel`
        * :class:`~oci.oda.models.SlackChannel`
        * :class:`~oci.oda.models.CortanaChannel`
        * :class:`~oci.oda.models.ServiceCloudChannel`
        * :class:`~oci.oda.models.IosChannel`
        * :class:`~oci.oda.models.TestChannel`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Channel.
        :type id: str

        :param name:
            The value to assign to the name property of this Channel.
        :type name: str

        :param description:
            The value to assign to the description property of this Channel.
        :type description: str

        :param category:
            The value to assign to the category property of this Channel.
            Allowed values for this property are: "AGENT", "APPLICATION", "BOT", "BOT_AS_AGENT", "SYSTEM", "EVENT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type category: str

        :param type:
            The value to assign to the type property of this Channel.
            Allowed values for this property are: "ANDROID", "APPEVENT", "APPLICATION", "CORTANA", "FACEBOOK", "IOS", "MSTEAMS", "OSS", "OSVC", "SERVICECLOUD", "SLACK", "TEST", "TWILIO", "WEB", "WEBHOOK", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param session_expiry_duration_in_milliseconds:
            The value to assign to the session_expiry_duration_in_milliseconds property of this Channel.
        :type session_expiry_duration_in_milliseconds: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Channel.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this Channel.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this Channel.
        :type time_updated: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Channel.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this Channel.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'category': 'str',
            'type': 'str',
            'session_expiry_duration_in_milliseconds': 'int',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'category': 'category',
            'type': 'type',
            'session_expiry_duration_in_milliseconds': 'sessionExpiryDurationInMilliseconds',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._name = None
        self._description = None
        self._category = None
        self._type = None
        self._session_expiry_duration_in_milliseconds = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None
        self._freeform_tags = None
        self._defined_tags = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'APPEVENT':
            return 'AppEventChannel'

        if type == 'FACEBOOK':
            return 'FacebookChannel'

        if type == 'WEB':
            return 'WebChannel'

        if type == 'MSTEAMS':
            return 'MSTeamsChannel'

        if type == 'TWILIO':
            return 'TwilioChannel'

        if type == 'OSVC':
            return 'OsvcChannel'

        if type == 'ANDROID':
            return 'AndroidChannel'

        if type == 'OSS':
            return 'OSSChannel'

        if type == 'WEBHOOK':
            return 'WebhookChannel'

        if type == 'APPLICATION':
            return 'ApplicationChannel'

        if type == 'SLACK':
            return 'SlackChannel'

        if type == 'CORTANA':
            return 'CortanaChannel'

        if type == 'SERVICECLOUD':
            return 'ServiceCloudChannel'

        if type == 'IOS':
            return 'IosChannel'

        if type == 'TEST':
            return 'TestChannel'
        else:
            return 'Channel'

    @property
    def id(self):
        """
        **[Required]** Gets the id of this Channel.
        Unique immutable identifier that was assigned when the Channel was created.


        :return: The id of this Channel.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Channel.
        Unique immutable identifier that was assigned when the Channel was created.


        :param id: The id of this Channel.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """
        **[Required]** Gets the name of this Channel.
        The Channel's name. The name can contain only letters, numbers, periods, and underscores. The name must begin with a letter.


        :return: The name of this Channel.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Channel.
        The Channel's name. The name can contain only letters, numbers, periods, and underscores. The name must begin with a letter.


        :param name: The name of this Channel.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this Channel.
        A short description of the Channel.


        :return: The description of this Channel.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Channel.
        A short description of the Channel.


        :param description: The description of this Channel.
        :type: str
        """
        self._description = description

    @property
    def category(self):
        """
        **[Required]** Gets the category of this Channel.
        The category of the Channel.

        Allowed values for this property are: "AGENT", "APPLICATION", "BOT", "BOT_AS_AGENT", "SYSTEM", "EVENT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The category of this Channel.
        :rtype: str
        """
        return self._category

    @category.setter
    def category(self, category):
        """
        Sets the category of this Channel.
        The category of the Channel.


        :param category: The category of this Channel.
        :type: str
        """
        allowed_values = ["AGENT", "APPLICATION", "BOT", "BOT_AS_AGENT", "SYSTEM", "EVENT"]
        if not value_allowed_none_or_none_sentinel(category, allowed_values):
            category = 'UNKNOWN_ENUM_VALUE'
        self._category = category

    @property
    def type(self):
        """
        **[Required]** Gets the type of this Channel.
        The Channel type.

        Allowed values for this property are: "ANDROID", "APPEVENT", "APPLICATION", "CORTANA", "FACEBOOK", "IOS", "MSTEAMS", "OSS", "OSVC", "SERVICECLOUD", "SLACK", "TEST", "TWILIO", "WEB", "WEBHOOK", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this Channel.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Channel.
        The Channel type.


        :param type: The type of this Channel.
        :type: str
        """
        allowed_values = ["ANDROID", "APPEVENT", "APPLICATION", "CORTANA", "FACEBOOK", "IOS", "MSTEAMS", "OSS", "OSVC", "SERVICECLOUD", "SLACK", "TEST", "TWILIO", "WEB", "WEBHOOK"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def session_expiry_duration_in_milliseconds(self):
        """
        Gets the session_expiry_duration_in_milliseconds of this Channel.
        The number of milliseconds before a session expires.


        :return: The session_expiry_duration_in_milliseconds of this Channel.
        :rtype: int
        """
        return self._session_expiry_duration_in_milliseconds

    @session_expiry_duration_in_milliseconds.setter
    def session_expiry_duration_in_milliseconds(self, session_expiry_duration_in_milliseconds):
        """
        Sets the session_expiry_duration_in_milliseconds of this Channel.
        The number of milliseconds before a session expires.


        :param session_expiry_duration_in_milliseconds: The session_expiry_duration_in_milliseconds of this Channel.
        :type: int
        """
        self._session_expiry_duration_in_milliseconds = session_expiry_duration_in_milliseconds

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this Channel.
        The Channel's current state.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Channel.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Channel.
        The Channel's current state.


        :param lifecycle_state: The lifecycle_state of this Channel.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "INACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this Channel.
        When the resource was created. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_created of this Channel.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this Channel.
        When the resource was created. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_created: The time_created of this Channel.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this Channel.
        When the resource was last updated. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_updated of this Channel.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this Channel.
        When the resource was last updated. A date-time string as described in `RFC 3339`__, section 14.29.

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_updated: The time_updated of this Channel.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this Channel.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this Channel.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Channel.
        Simple key-value pair that is applied without any predefined name, type, or scope.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this Channel.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this Channel.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this Channel.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Channel.
        Usage of predefined tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this Channel.
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
