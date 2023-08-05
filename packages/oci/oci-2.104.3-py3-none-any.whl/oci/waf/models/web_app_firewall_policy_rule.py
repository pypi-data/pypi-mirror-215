# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class WebAppFirewallPolicyRule(object):
    """
    Base schema for WebAppFirewallPolicyRules, including properties common to all of them.
    """

    #: A constant which can be used with the type property of a WebAppFirewallPolicyRule.
    #: This constant has a value of "ACCESS_CONTROL"
    TYPE_ACCESS_CONTROL = "ACCESS_CONTROL"

    #: A constant which can be used with the type property of a WebAppFirewallPolicyRule.
    #: This constant has a value of "PROTECTION"
    TYPE_PROTECTION = "PROTECTION"

    #: A constant which can be used with the type property of a WebAppFirewallPolicyRule.
    #: This constant has a value of "REQUEST_RATE_LIMITING"
    TYPE_REQUEST_RATE_LIMITING = "REQUEST_RATE_LIMITING"

    #: A constant which can be used with the condition_language property of a WebAppFirewallPolicyRule.
    #: This constant has a value of "JMESPATH"
    CONDITION_LANGUAGE_JMESPATH = "JMESPATH"

    def __init__(self, **kwargs):
        """
        Initializes a new WebAppFirewallPolicyRule object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.waf.models.ProtectionRule`
        * :class:`~oci.waf.models.RequestRateLimitingRule`
        * :class:`~oci.waf.models.AccessControlRule`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this WebAppFirewallPolicyRule.
            Allowed values for this property are: "ACCESS_CONTROL", "PROTECTION", "REQUEST_RATE_LIMITING"
        :type type: str

        :param name:
            The value to assign to the name property of this WebAppFirewallPolicyRule.
        :type name: str

        :param condition_language:
            The value to assign to the condition_language property of this WebAppFirewallPolicyRule.
            Allowed values for this property are: "JMESPATH"
        :type condition_language: str

        :param condition:
            The value to assign to the condition property of this WebAppFirewallPolicyRule.
        :type condition: str

        :param action_name:
            The value to assign to the action_name property of this WebAppFirewallPolicyRule.
        :type action_name: str

        """
        self.swagger_types = {
            'type': 'str',
            'name': 'str',
            'condition_language': 'str',
            'condition': 'str',
            'action_name': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'name': 'name',
            'condition_language': 'conditionLanguage',
            'condition': 'condition',
            'action_name': 'actionName'
        }

        self._type = None
        self._name = None
        self._condition_language = None
        self._condition = None
        self._action_name = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['type']

        if type == 'PROTECTION':
            return 'ProtectionRule'

        if type == 'REQUEST_RATE_LIMITING':
            return 'RequestRateLimitingRule'

        if type == 'ACCESS_CONTROL':
            return 'AccessControlRule'
        else:
            return 'WebAppFirewallPolicyRule'

    @property
    def type(self):
        """
        **[Required]** Gets the type of this WebAppFirewallPolicyRule.
        Type of WebAppFirewallPolicyRule.

        Allowed values for this property are: "ACCESS_CONTROL", "PROTECTION", "REQUEST_RATE_LIMITING"


        :return: The type of this WebAppFirewallPolicyRule.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this WebAppFirewallPolicyRule.
        Type of WebAppFirewallPolicyRule.


        :param type: The type of this WebAppFirewallPolicyRule.
        :type: str
        """
        allowed_values = ["ACCESS_CONTROL", "PROTECTION", "REQUEST_RATE_LIMITING"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            raise ValueError(
                "Invalid value for `type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._type = type

    @property
    def name(self):
        """
        **[Required]** Gets the name of this WebAppFirewallPolicyRule.
        Rule name. Must be unique within the module.


        :return: The name of this WebAppFirewallPolicyRule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this WebAppFirewallPolicyRule.
        Rule name. Must be unique within the module.


        :param name: The name of this WebAppFirewallPolicyRule.
        :type: str
        """
        self._name = name

    @property
    def condition_language(self):
        """
        Gets the condition_language of this WebAppFirewallPolicyRule.
        The language used to parse condition from field `condition`. Available languages:

        * **JMESPATH** an extended JMESPath language syntax.

        Allowed values for this property are: "JMESPATH"


        :return: The condition_language of this WebAppFirewallPolicyRule.
        :rtype: str
        """
        return self._condition_language

    @condition_language.setter
    def condition_language(self, condition_language):
        """
        Sets the condition_language of this WebAppFirewallPolicyRule.
        The language used to parse condition from field `condition`. Available languages:

        * **JMESPATH** an extended JMESPath language syntax.


        :param condition_language: The condition_language of this WebAppFirewallPolicyRule.
        :type: str
        """
        allowed_values = ["JMESPATH"]
        if not value_allowed_none_or_none_sentinel(condition_language, allowed_values):
            raise ValueError(
                "Invalid value for `condition_language`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._condition_language = condition_language

    @property
    def condition(self):
        """
        Gets the condition of this WebAppFirewallPolicyRule.
        An expression that determines whether or not the rule action should be executed.


        :return: The condition of this WebAppFirewallPolicyRule.
        :rtype: str
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """
        Sets the condition of this WebAppFirewallPolicyRule.
        An expression that determines whether or not the rule action should be executed.


        :param condition: The condition of this WebAppFirewallPolicyRule.
        :type: str
        """
        self._condition = condition

    @property
    def action_name(self):
        """
        **[Required]** Gets the action_name of this WebAppFirewallPolicyRule.
        References action by name from actions defined in WebAppFirewallPolicy.


        :return: The action_name of this WebAppFirewallPolicyRule.
        :rtype: str
        """
        return self._action_name

    @action_name.setter
    def action_name(self, action_name):
        """
        Sets the action_name of this WebAppFirewallPolicyRule.
        References action by name from actions defined in WebAppFirewallPolicy.


        :param action_name: The action_name of this WebAppFirewallPolicyRule.
        :type: str
        """
        self._action_name = action_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
