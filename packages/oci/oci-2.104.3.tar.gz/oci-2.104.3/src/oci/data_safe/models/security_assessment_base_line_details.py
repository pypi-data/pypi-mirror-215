# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SecurityAssessmentBaseLineDetails(object):
    """
    The details reqired to set baseline assessment.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SecurityAssessmentBaseLineDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param assessment_ids:
            The value to assign to the assessment_ids property of this SecurityAssessmentBaseLineDetails.
        :type assessment_ids: list[str]

        """
        self.swagger_types = {
            'assessment_ids': 'list[str]'
        }

        self.attribute_map = {
            'assessment_ids': 'assessmentIds'
        }

        self._assessment_ids = None

    @property
    def assessment_ids(self):
        """
        Gets the assessment_ids of this SecurityAssessmentBaseLineDetails.
        List of security assessment OCIDs that need to be updated while setting the baseline.


        :return: The assessment_ids of this SecurityAssessmentBaseLineDetails.
        :rtype: list[str]
        """
        return self._assessment_ids

    @assessment_ids.setter
    def assessment_ids(self, assessment_ids):
        """
        Sets the assessment_ids of this SecurityAssessmentBaseLineDetails.
        List of security assessment OCIDs that need to be updated while setting the baseline.


        :param assessment_ids: The assessment_ids of this SecurityAssessmentBaseLineDetails.
        :type: list[str]
        """
        self._assessment_ids = assessment_ids

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
