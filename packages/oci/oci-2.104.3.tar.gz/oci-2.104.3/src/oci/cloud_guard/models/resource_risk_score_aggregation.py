# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceRiskScoreAggregation(object):
    """
    Risk score of a resource.
    """

    #: A constant which can be used with the risk_level property of a ResourceRiskScoreAggregation.
    #: This constant has a value of "CRITICAL"
    RISK_LEVEL_CRITICAL = "CRITICAL"

    #: A constant which can be used with the risk_level property of a ResourceRiskScoreAggregation.
    #: This constant has a value of "HIGH"
    RISK_LEVEL_HIGH = "HIGH"

    #: A constant which can be used with the risk_level property of a ResourceRiskScoreAggregation.
    #: This constant has a value of "MEDIUM"
    RISK_LEVEL_MEDIUM = "MEDIUM"

    #: A constant which can be used with the risk_level property of a ResourceRiskScoreAggregation.
    #: This constant has a value of "LOW"
    RISK_LEVEL_LOW = "LOW"

    #: A constant which can be used with the risk_level property of a ResourceRiskScoreAggregation.
    #: This constant has a value of "MINOR"
    RISK_LEVEL_MINOR = "MINOR"

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceRiskScoreAggregation object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param tactics:
            The value to assign to the tactics property of this ResourceRiskScoreAggregation.
        :type tactics: list[str]

        :param score_timestamp:
            The value to assign to the score_timestamp property of this ResourceRiskScoreAggregation.
        :type score_timestamp: float

        :param risk_score:
            The value to assign to the risk_score property of this ResourceRiskScoreAggregation.
        :type risk_score: float

        :param risk_level:
            The value to assign to the risk_level property of this ResourceRiskScoreAggregation.
            Allowed values for this property are: "CRITICAL", "HIGH", "MEDIUM", "LOW", "MINOR", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type risk_level: str

        """
        self.swagger_types = {
            'tactics': 'list[str]',
            'score_timestamp': 'float',
            'risk_score': 'float',
            'risk_level': 'str'
        }

        self.attribute_map = {
            'tactics': 'tactics',
            'score_timestamp': 'scoreTimestamp',
            'risk_score': 'riskScore',
            'risk_level': 'riskLevel'
        }

        self._tactics = None
        self._score_timestamp = None
        self._risk_score = None
        self._risk_level = None

    @property
    def tactics(self):
        """
        **[Required]** Gets the tactics of this ResourceRiskScoreAggregation.
        Tactics used for evaluating the risk scrore


        :return: The tactics of this ResourceRiskScoreAggregation.
        :rtype: list[str]
        """
        return self._tactics

    @tactics.setter
    def tactics(self, tactics):
        """
        Sets the tactics of this ResourceRiskScoreAggregation.
        Tactics used for evaluating the risk scrore


        :param tactics: The tactics of this ResourceRiskScoreAggregation.
        :type: list[str]
        """
        self._tactics = tactics

    @property
    def score_timestamp(self):
        """
        **[Required]** Gets the score_timestamp of this ResourceRiskScoreAggregation.
        The date and time for which the score is calculated. Format defined by RFC3339.


        :return: The score_timestamp of this ResourceRiskScoreAggregation.
        :rtype: float
        """
        return self._score_timestamp

    @score_timestamp.setter
    def score_timestamp(self, score_timestamp):
        """
        Sets the score_timestamp of this ResourceRiskScoreAggregation.
        The date and time for which the score is calculated. Format defined by RFC3339.


        :param score_timestamp: The score_timestamp of this ResourceRiskScoreAggregation.
        :type: float
        """
        self._score_timestamp = score_timestamp

    @property
    def risk_score(self):
        """
        **[Required]** Gets the risk_score of this ResourceRiskScoreAggregation.
        Risk Score


        :return: The risk_score of this ResourceRiskScoreAggregation.
        :rtype: float
        """
        return self._risk_score

    @risk_score.setter
    def risk_score(self, risk_score):
        """
        Sets the risk_score of this ResourceRiskScoreAggregation.
        Risk Score


        :param risk_score: The risk_score of this ResourceRiskScoreAggregation.
        :type: float
        """
        self._risk_score = risk_score

    @property
    def risk_level(self):
        """
        **[Required]** Gets the risk_level of this ResourceRiskScoreAggregation.
        The Risk Level

        Allowed values for this property are: "CRITICAL", "HIGH", "MEDIUM", "LOW", "MINOR", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The risk_level of this ResourceRiskScoreAggregation.
        :rtype: str
        """
        return self._risk_level

    @risk_level.setter
    def risk_level(self, risk_level):
        """
        Sets the risk_level of this ResourceRiskScoreAggregation.
        The Risk Level


        :param risk_level: The risk_level of this ResourceRiskScoreAggregation.
        :type: str
        """
        allowed_values = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "MINOR"]
        if not value_allowed_none_or_none_sentinel(risk_level, allowed_values):
            risk_level = 'UNKNOWN_ENUM_VALUE'
        self._risk_level = risk_level

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
