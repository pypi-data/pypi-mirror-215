# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExtensionAdaptiveUser(object):
    """
    This extension defines attributes to manage user's risk score.
    """

    #: A constant which can be used with the risk_level property of a ExtensionAdaptiveUser.
    #: This constant has a value of "LOW"
    RISK_LEVEL_LOW = "LOW"

    #: A constant which can be used with the risk_level property of a ExtensionAdaptiveUser.
    #: This constant has a value of "MEDIUM"
    RISK_LEVEL_MEDIUM = "MEDIUM"

    #: A constant which can be used with the risk_level property of a ExtensionAdaptiveUser.
    #: This constant has a value of "HIGH"
    RISK_LEVEL_HIGH = "HIGH"

    def __init__(self, **kwargs):
        """
        Initializes a new ExtensionAdaptiveUser object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param risk_level:
            The value to assign to the risk_level property of this ExtensionAdaptiveUser.
            Allowed values for this property are: "LOW", "MEDIUM", "HIGH", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type risk_level: str

        :param risk_scores:
            The value to assign to the risk_scores property of this ExtensionAdaptiveUser.
        :type risk_scores: list[oci.identity_domains.models.UserExtRiskScores]

        """
        self.swagger_types = {
            'risk_level': 'str',
            'risk_scores': 'list[UserExtRiskScores]'
        }

        self.attribute_map = {
            'risk_level': 'riskLevel',
            'risk_scores': 'riskScores'
        }

        self._risk_level = None
        self._risk_scores = None

    @property
    def risk_level(self):
        """
        Gets the risk_level of this ExtensionAdaptiveUser.
        Risk Level

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: request
         - type: string
         - uniqueness: none

        Allowed values for this property are: "LOW", "MEDIUM", "HIGH", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The risk_level of this ExtensionAdaptiveUser.
        :rtype: str
        """
        return self._risk_level

    @risk_level.setter
    def risk_level(self, risk_level):
        """
        Sets the risk_level of this ExtensionAdaptiveUser.
        Risk Level

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param risk_level: The risk_level of this ExtensionAdaptiveUser.
        :type: str
        """
        allowed_values = ["LOW", "MEDIUM", "HIGH"]
        if not value_allowed_none_or_none_sentinel(risk_level, allowed_values):
            risk_level = 'UNKNOWN_ENUM_VALUE'
        self._risk_level = risk_level

    @property
    def risk_scores(self):
        """
        Gets the risk_scores of this ExtensionAdaptiveUser.
        The risk score pertaining to the user.

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :return: The risk_scores of this ExtensionAdaptiveUser.
        :rtype: list[oci.identity_domains.models.UserExtRiskScores]
        """
        return self._risk_scores

    @risk_scores.setter
    def risk_scores(self, risk_scores):
        """
        Sets the risk_scores of this ExtensionAdaptiveUser.
        The risk score pertaining to the user.

        **Added In:** 18.1.6

        **SCIM++ Properties:**
         - caseExact: false
         - idcsCompositeKey: [value]
         - multiValued: true
         - mutability: readWrite
         - required: false
         - returned: request
         - type: complex
         - uniqueness: none


        :param risk_scores: The risk_scores of this ExtensionAdaptiveUser.
        :type: list[oci.identity_domains.models.UserExtRiskScores]
        """
        self._risk_scores = risk_scores

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
