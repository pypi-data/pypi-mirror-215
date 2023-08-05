# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class HandleAccessRequestDetails(object):
    """
    The details for handling access request.
    """

    #: A constant which can be used with the action property of a HandleAccessRequestDetails.
    #: This constant has a value of "APPROVE"
    ACTION_APPROVE = "APPROVE"

    #: A constant which can be used with the action property of a HandleAccessRequestDetails.
    #: This constant has a value of "DENY"
    ACTION_DENY = "DENY"

    #: A constant which can be used with the action property of a HandleAccessRequestDetails.
    #: This constant has a value of "REVOKE"
    ACTION_REVOKE = "REVOKE"

    #: A constant which can be used with the action property of a HandleAccessRequestDetails.
    #: This constant has a value of "CANCEL"
    ACTION_CANCEL = "CANCEL"

    def __init__(self, **kwargs):
        """
        Initializes a new HandleAccessRequestDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param action:
            The value to assign to the action property of this HandleAccessRequestDetails.
            Allowed values for this property are: "APPROVE", "DENY", "REVOKE", "CANCEL"
        :type action: str

        :param message:
            The value to assign to the message property of this HandleAccessRequestDetails.
        :type message: str

        """
        self.swagger_types = {
            'action': 'str',
            'message': 'str'
        }

        self.attribute_map = {
            'action': 'action',
            'message': 'message'
        }

        self._action = None
        self._message = None

    @property
    def action(self):
        """
        **[Required]** Gets the action of this HandleAccessRequestDetails.
        The action take by persona

        Allowed values for this property are: "APPROVE", "DENY", "REVOKE", "CANCEL"


        :return: The action of this HandleAccessRequestDetails.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this HandleAccessRequestDetails.
        The action take by persona


        :param action: The action of this HandleAccessRequestDetails.
        :type: str
        """
        allowed_values = ["APPROVE", "DENY", "REVOKE", "CANCEL"]
        if not value_allowed_none_or_none_sentinel(action, allowed_values):
            raise ValueError(
                "Invalid value for `action`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._action = action

    @property
    def message(self):
        """
        Gets the message of this HandleAccessRequestDetails.
        Action justification or details.


        :return: The message of this HandleAccessRequestDetails.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this HandleAccessRequestDetails.
        Action justification or details.


        :param message: The message of this HandleAccessRequestDetails.
        :type: str
        """
        self._message = message

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
