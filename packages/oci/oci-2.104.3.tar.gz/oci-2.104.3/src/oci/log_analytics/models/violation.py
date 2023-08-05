# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Violation(object):
    """
    Violation
    """

    #: A constant which can be used with the rule_type property of a Violation.
    #: This constant has a value of "WARN"
    RULE_TYPE_WARN = "WARN"

    #: A constant which can be used with the rule_type property of a Violation.
    #: This constant has a value of "ERROR"
    RULE_TYPE_ERROR = "ERROR"

    def __init__(self, **kwargs):
        """
        Initializes a new Violation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param indexes:
            The value to assign to the indexes property of this Violation.
        :type indexes: list[oci.log_analytics.models.Indexes]

        :param rule_description:
            The value to assign to the rule_description property of this Violation.
        :type rule_description: str

        :param rule_name:
            The value to assign to the rule_name property of this Violation.
        :type rule_name: str

        :param rule_remediation:
            The value to assign to the rule_remediation property of this Violation.
        :type rule_remediation: str

        :param rule_type:
            The value to assign to the rule_type property of this Violation.
            Allowed values for this property are: "WARN", "ERROR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type rule_type: str

        """
        self.swagger_types = {
            'indexes': 'list[Indexes]',
            'rule_description': 'str',
            'rule_name': 'str',
            'rule_remediation': 'str',
            'rule_type': 'str'
        }

        self.attribute_map = {
            'indexes': 'indexes',
            'rule_description': 'ruleDescription',
            'rule_name': 'ruleName',
            'rule_remediation': 'ruleRemediation',
            'rule_type': 'ruleType'
        }

        self._indexes = None
        self._rule_description = None
        self._rule_name = None
        self._rule_remediation = None
        self._rule_type = None

    @property
    def indexes(self):
        """
        Gets the indexes of this Violation.
        The indices associated with regular expression violations.


        :return: The indexes of this Violation.
        :rtype: list[oci.log_analytics.models.Indexes]
        """
        return self._indexes

    @indexes.setter
    def indexes(self, indexes):
        """
        Sets the indexes of this Violation.
        The indices associated with regular expression violations.


        :param indexes: The indexes of this Violation.
        :type: list[oci.log_analytics.models.Indexes]
        """
        self._indexes = indexes

    @property
    def rule_description(self):
        """
        Gets the rule_description of this Violation.
        The rule description.


        :return: The rule_description of this Violation.
        :rtype: str
        """
        return self._rule_description

    @rule_description.setter
    def rule_description(self, rule_description):
        """
        Sets the rule_description of this Violation.
        The rule description.


        :param rule_description: The rule_description of this Violation.
        :type: str
        """
        self._rule_description = rule_description

    @property
    def rule_name(self):
        """
        Gets the rule_name of this Violation.
        The rule name.


        :return: The rule_name of this Violation.
        :rtype: str
        """
        return self._rule_name

    @rule_name.setter
    def rule_name(self, rule_name):
        """
        Sets the rule_name of this Violation.
        The rule name.


        :param rule_name: The rule_name of this Violation.
        :type: str
        """
        self._rule_name = rule_name

    @property
    def rule_remediation(self):
        """
        Gets the rule_remediation of this Violation.
        The rule remediation.


        :return: The rule_remediation of this Violation.
        :rtype: str
        """
        return self._rule_remediation

    @rule_remediation.setter
    def rule_remediation(self, rule_remediation):
        """
        Sets the rule_remediation of this Violation.
        The rule remediation.


        :param rule_remediation: The rule_remediation of this Violation.
        :type: str
        """
        self._rule_remediation = rule_remediation

    @property
    def rule_type(self):
        """
        Gets the rule_type of this Violation.
        The rule type.  Either WARN or ERROR.

        Allowed values for this property are: "WARN", "ERROR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The rule_type of this Violation.
        :rtype: str
        """
        return self._rule_type

    @rule_type.setter
    def rule_type(self, rule_type):
        """
        Sets the rule_type of this Violation.
        The rule type.  Either WARN or ERROR.


        :param rule_type: The rule_type of this Violation.
        :type: str
        """
        allowed_values = ["WARN", "ERROR"]
        if not value_allowed_none_or_none_sentinel(rule_type, allowed_values):
            rule_type = 'UNKNOWN_ENUM_VALUE'
        self._rule_type = rule_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
