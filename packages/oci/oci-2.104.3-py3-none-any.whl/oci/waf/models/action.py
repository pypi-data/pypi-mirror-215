# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Action(object):
    """
    An object that represents action and its options.
    The action can be terminating, if it stops further execution of rules and modules.
    And non-terminating, if it does not interrupt execution flow.
    """

    #: A constant which can be used with the type property of a Action.
    #: This constant has a value of "CHECK"
    TYPE_CHECK = "CHECK"

    #: A constant which can be used with the type property of a Action.
    #: This constant has a value of "ALLOW"
    TYPE_ALLOW = "ALLOW"

    #: A constant which can be used with the type property of a Action.
    #: This constant has a value of "RETURN_HTTP_RESPONSE"
    TYPE_RETURN_HTTP_RESPONSE = "RETURN_HTTP_RESPONSE"

    def __init__(self, **kwargs):
        """
        Initializes a new Action object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.waf.models.ReturnHttpResponseAction`
        * :class:`~oci.waf.models.AllowAction`
        * :class:`~oci.waf.models.CheckAction`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this Action.
            Allowed values for this property are: "CHECK", "ALLOW", "RETURN_HTTP_RESPONSE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param name:
            The value to assign to the name property of this Action.
        :type name: str

        """
        self.swagger_types = {
            'type': 'str',
            'name': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'name': 'name'
        }

        self._type = None
        self._name = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'RETURN_HTTP_RESPONSE':
            return 'ReturnHttpResponseAction'

        if type == 'ALLOW':
            return 'AllowAction'

        if type == 'CHECK':
            return 'CheckAction'
        else:
            return 'Action'

    @property
    def type(self):
        """
        **[Required]** Gets the type of this Action.
        * **CHECK** is a non-terminating action that does not stop the execution of rules in current module,
          just emits a log message documenting result of rule execution.

        * **ALLOW** is a non-terminating action which upon matching rule skips all remaining rules in the current module.

        * **RETURN_HTTP_RESPONSE** is a terminating action which is executed immediately, returns a defined HTTP response.

        Allowed values for this property are: "CHECK", "ALLOW", "RETURN_HTTP_RESPONSE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this Action.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this Action.
        * **CHECK** is a non-terminating action that does not stop the execution of rules in current module,
          just emits a log message documenting result of rule execution.

        * **ALLOW** is a non-terminating action which upon matching rule skips all remaining rules in the current module.

        * **RETURN_HTTP_RESPONSE** is a terminating action which is executed immediately, returns a defined HTTP response.


        :param type: The type of this Action.
        :type: str
        """
        allowed_values = ["CHECK", "ALLOW", "RETURN_HTTP_RESPONSE"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def name(self):
        """
        **[Required]** Gets the name of this Action.
        Action name. Can be used to reference the action.


        :return: The name of this Action.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Action.
        Action name. Can be used to reference the action.


        :param name: The name of this Action.
        :type: str
        """
        self._name = name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
