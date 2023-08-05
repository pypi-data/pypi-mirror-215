# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ThinAssociationAuthorizationResponse(object):
    """
    ThinAssociationAuthorizationResponse model.
    """

    #: A constant which can be used with the association_result property of a ThinAssociationAuthorizationResponse.
    #: This constant has a value of "FAIL_UNKNOWN"
    ASSOCIATION_RESULT_FAIL_UNKNOWN = "FAIL_UNKNOWN"

    #: A constant which can be used with the association_result property of a ThinAssociationAuthorizationResponse.
    #: This constant has a value of "FAIL_BAD_REQUEST"
    ASSOCIATION_RESULT_FAIL_BAD_REQUEST = "FAIL_BAD_REQUEST"

    #: A constant which can be used with the association_result property of a ThinAssociationAuthorizationResponse.
    #: This constant has a value of "FAIL_MISSING_ENDORSE"
    ASSOCIATION_RESULT_FAIL_MISSING_ENDORSE = "FAIL_MISSING_ENDORSE"

    #: A constant which can be used with the association_result property of a ThinAssociationAuthorizationResponse.
    #: This constant has a value of "FAIL_MISSING_ADMIT"
    ASSOCIATION_RESULT_FAIL_MISSING_ADMIT = "FAIL_MISSING_ADMIT"

    #: A constant which can be used with the association_result property of a ThinAssociationAuthorizationResponse.
    #: This constant has a value of "SUCCESS"
    ASSOCIATION_RESULT_SUCCESS = "SUCCESS"

    def __init__(self, **kwargs):
        """
        Initializes a new ThinAssociationAuthorizationResponse object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param responses:
            The value to assign to the responses property of this ThinAssociationAuthorizationResponse.
        :type responses: list[oci.identity_data_plane.models.ThinAuthorizationResponse]

        :param association_result:
            The value to assign to the association_result property of this ThinAssociationAuthorizationResponse.
            Allowed values for this property are: "FAIL_UNKNOWN", "FAIL_BAD_REQUEST", "FAIL_MISSING_ENDORSE", "FAIL_MISSING_ADMIT", "SUCCESS"
        :type association_result: str

        :param decision_cache_duration:
            The value to assign to the decision_cache_duration property of this ThinAssociationAuthorizationResponse.
        :type decision_cache_duration: str

        """
        self.swagger_types = {
            'responses': 'list[ThinAuthorizationResponse]',
            'association_result': 'str',
            'decision_cache_duration': 'str'
        }

        self.attribute_map = {
            'responses': 'responses',
            'association_result': 'associationResult',
            'decision_cache_duration': 'decisionCacheDuration'
        }

        self._responses = None
        self._association_result = None
        self._decision_cache_duration = None

    @property
    def responses(self):
        """
        **[Required]** Gets the responses of this ThinAssociationAuthorizationResponse.
        The authorization responses.


        :return: The responses of this ThinAssociationAuthorizationResponse.
        :rtype: list[oci.identity_data_plane.models.ThinAuthorizationResponse]
        """
        return self._responses

    @responses.setter
    def responses(self, responses):
        """
        Sets the responses of this ThinAssociationAuthorizationResponse.
        The authorization responses.


        :param responses: The responses of this ThinAssociationAuthorizationResponse.
        :type: list[oci.identity_data_plane.models.ThinAuthorizationResponse]
        """
        self._responses = responses

    @property
    def association_result(self):
        """
        **[Required]** Gets the association_result of this ThinAssociationAuthorizationResponse.
        The association verification result.

        Allowed values for this property are: "FAIL_UNKNOWN", "FAIL_BAD_REQUEST", "FAIL_MISSING_ENDORSE", "FAIL_MISSING_ADMIT", "SUCCESS"


        :return: The association_result of this ThinAssociationAuthorizationResponse.
        :rtype: str
        """
        return self._association_result

    @association_result.setter
    def association_result(self, association_result):
        """
        Sets the association_result of this ThinAssociationAuthorizationResponse.
        The association verification result.


        :param association_result: The association_result of this ThinAssociationAuthorizationResponse.
        :type: str
        """
        allowed_values = ["FAIL_UNKNOWN", "FAIL_BAD_REQUEST", "FAIL_MISSING_ENDORSE", "FAIL_MISSING_ADMIT", "SUCCESS"]
        if not value_allowed_none_or_none_sentinel(association_result, allowed_values):
            raise ValueError(
                "Invalid value for `association_result`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._association_result = association_result

    @property
    def decision_cache_duration(self):
        """
        Gets the decision_cache_duration of this ThinAssociationAuthorizationResponse.
        The decision cache duration.


        :return: The decision_cache_duration of this ThinAssociationAuthorizationResponse.
        :rtype: str
        """
        return self._decision_cache_duration

    @decision_cache_duration.setter
    def decision_cache_duration(self, decision_cache_duration):
        """
        Sets the decision_cache_duration of this ThinAssociationAuthorizationResponse.
        The decision cache duration.


        :param decision_cache_duration: The decision_cache_duration of this ThinAssociationAuthorizationResponse.
        :type: str
        """
        self._decision_cache_duration = decision_cache_duration

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
