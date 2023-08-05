# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateGovernanceInstanceConfigurationDetails(object):
    """
    The details of a tenancy-wide configuration for GovernanceInstances to be updated.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateGovernanceInstanceConfigurationDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param sender_info:
            The value to assign to the sender_info property of this UpdateGovernanceInstanceConfigurationDetails.
        :type sender_info: oci.access_governance_cp.models.UpdateSenderConfig

        """
        self.swagger_types = {
            'sender_info': 'UpdateSenderConfig'
        }

        self.attribute_map = {
            'sender_info': 'senderInfo'
        }

        self._sender_info = None

    @property
    def sender_info(self):
        """
        Gets the sender_info of this UpdateGovernanceInstanceConfigurationDetails.

        :return: The sender_info of this UpdateGovernanceInstanceConfigurationDetails.
        :rtype: oci.access_governance_cp.models.UpdateSenderConfig
        """
        return self._sender_info

    @sender_info.setter
    def sender_info(self, sender_info):
        """
        Sets the sender_info of this UpdateGovernanceInstanceConfigurationDetails.

        :param sender_info: The sender_info of this UpdateGovernanceInstanceConfigurationDetails.
        :type: oci.access_governance_cp.models.UpdateSenderConfig
        """
        self._sender_info = sender_info

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
