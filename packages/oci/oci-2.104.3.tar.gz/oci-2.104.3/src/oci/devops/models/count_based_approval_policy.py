# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .approval_policy import ApprovalPolicy
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CountBasedApprovalPolicy(ApprovalPolicy):
    """
    Count based stage approval policy.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CountBasedApprovalPolicy object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.CountBasedApprovalPolicy.approval_policy_type` attribute
        of this class is ``COUNT_BASED_APPROVAL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param approval_policy_type:
            The value to assign to the approval_policy_type property of this CountBasedApprovalPolicy.
            Allowed values for this property are: "COUNT_BASED_APPROVAL"
        :type approval_policy_type: str

        :param number_of_approvals_required:
            The value to assign to the number_of_approvals_required property of this CountBasedApprovalPolicy.
        :type number_of_approvals_required: int

        """
        self.swagger_types = {
            'approval_policy_type': 'str',
            'number_of_approvals_required': 'int'
        }

        self.attribute_map = {
            'approval_policy_type': 'approvalPolicyType',
            'number_of_approvals_required': 'numberOfApprovalsRequired'
        }

        self._approval_policy_type = None
        self._number_of_approvals_required = None
        self._approval_policy_type = 'COUNT_BASED_APPROVAL'

    @property
    def number_of_approvals_required(self):
        """
        **[Required]** Gets the number_of_approvals_required of this CountBasedApprovalPolicy.
        A minimum number of approvals required for stage to proceed.


        :return: The number_of_approvals_required of this CountBasedApprovalPolicy.
        :rtype: int
        """
        return self._number_of_approvals_required

    @number_of_approvals_required.setter
    def number_of_approvals_required(self, number_of_approvals_required):
        """
        Sets the number_of_approvals_required of this CountBasedApprovalPolicy.
        A minimum number of approvals required for stage to proceed.


        :param number_of_approvals_required: The number_of_approvals_required of this CountBasedApprovalPolicy.
        :type: int
        """
        self._number_of_approvals_required = number_of_approvals_required

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
