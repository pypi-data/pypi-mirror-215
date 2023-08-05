# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConsumerGroupPrivilegeSummary(object):
    """
    A summary of consumer group privileges.
    """

    #: A constant which can be used with the grant_option property of a ConsumerGroupPrivilegeSummary.
    #: This constant has a value of "YES"
    GRANT_OPTION_YES = "YES"

    #: A constant which can be used with the grant_option property of a ConsumerGroupPrivilegeSummary.
    #: This constant has a value of "NO"
    GRANT_OPTION_NO = "NO"

    #: A constant which can be used with the initial_group property of a ConsumerGroupPrivilegeSummary.
    #: This constant has a value of "YES"
    INITIAL_GROUP_YES = "YES"

    #: A constant which can be used with the initial_group property of a ConsumerGroupPrivilegeSummary.
    #: This constant has a value of "NO"
    INITIAL_GROUP_NO = "NO"

    def __init__(self, **kwargs):
        """
        Initializes a new ConsumerGroupPrivilegeSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ConsumerGroupPrivilegeSummary.
        :type name: str

        :param grant_option:
            The value to assign to the grant_option property of this ConsumerGroupPrivilegeSummary.
            Allowed values for this property are: "YES", "NO", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type grant_option: str

        :param initial_group:
            The value to assign to the initial_group property of this ConsumerGroupPrivilegeSummary.
            Allowed values for this property are: "YES", "NO", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type initial_group: str

        """
        self.swagger_types = {
            'name': 'str',
            'grant_option': 'str',
            'initial_group': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'grant_option': 'grantOption',
            'initial_group': 'initialGroup'
        }

        self._name = None
        self._grant_option = None
        self._initial_group = None

    @property
    def name(self):
        """
        Gets the name of this ConsumerGroupPrivilegeSummary.
        The name of the granted consumer group privilege.


        :return: The name of this ConsumerGroupPrivilegeSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConsumerGroupPrivilegeSummary.
        The name of the granted consumer group privilege.


        :param name: The name of this ConsumerGroupPrivilegeSummary.
        :type: str
        """
        self._name = name

    @property
    def grant_option(self):
        """
        Gets the grant_option of this ConsumerGroupPrivilegeSummary.
        Indicates whether the privilege is granted with the GRANT option (YES) or not (NO).

        Allowed values for this property are: "YES", "NO", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The grant_option of this ConsumerGroupPrivilegeSummary.
        :rtype: str
        """
        return self._grant_option

    @grant_option.setter
    def grant_option(self, grant_option):
        """
        Sets the grant_option of this ConsumerGroupPrivilegeSummary.
        Indicates whether the privilege is granted with the GRANT option (YES) or not (NO).


        :param grant_option: The grant_option of this ConsumerGroupPrivilegeSummary.
        :type: str
        """
        allowed_values = ["YES", "NO"]
        if not value_allowed_none_or_none_sentinel(grant_option, allowed_values):
            grant_option = 'UNKNOWN_ENUM_VALUE'
        self._grant_option = grant_option

    @property
    def initial_group(self):
        """
        Gets the initial_group of this ConsumerGroupPrivilegeSummary.
        Indicates whether the consumer group is designated as the default for this user or role (YES) or not (NO).

        Allowed values for this property are: "YES", "NO", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The initial_group of this ConsumerGroupPrivilegeSummary.
        :rtype: str
        """
        return self._initial_group

    @initial_group.setter
    def initial_group(self, initial_group):
        """
        Sets the initial_group of this ConsumerGroupPrivilegeSummary.
        Indicates whether the consumer group is designated as the default for this user or role (YES) or not (NO).


        :param initial_group: The initial_group of this ConsumerGroupPrivilegeSummary.
        :type: str
        """
        allowed_values = ["YES", "NO"]
        if not value_allowed_none_or_none_sentinel(initial_group, allowed_values):
            initial_group = 'UNKNOWN_ENUM_VALUE'
        self._initial_group = initial_group

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
