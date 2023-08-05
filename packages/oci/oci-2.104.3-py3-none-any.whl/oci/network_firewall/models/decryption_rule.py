# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DecryptionRule(object):
    """
    Decryption Rule used in the firewall policy rules.
    A Decryption Rule is used to define which traffic should be decrypted by the firewall, and how it should do so.
    """

    #: A constant which can be used with the action property of a DecryptionRule.
    #: This constant has a value of "NO_DECRYPT"
    ACTION_NO_DECRYPT = "NO_DECRYPT"

    #: A constant which can be used with the action property of a DecryptionRule.
    #: This constant has a value of "DECRYPT"
    ACTION_DECRYPT = "DECRYPT"

    def __init__(self, **kwargs):
        """
        Initializes a new DecryptionRule object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this DecryptionRule.
        :type name: str

        :param condition:
            The value to assign to the condition property of this DecryptionRule.
        :type condition: oci.network_firewall.models.DecryptionRuleMatchCriteria

        :param action:
            The value to assign to the action property of this DecryptionRule.
            Allowed values for this property are: "NO_DECRYPT", "DECRYPT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type action: str

        :param decryption_profile:
            The value to assign to the decryption_profile property of this DecryptionRule.
        :type decryption_profile: str

        :param secret:
            The value to assign to the secret property of this DecryptionRule.
        :type secret: str

        """
        self.swagger_types = {
            'name': 'str',
            'condition': 'DecryptionRuleMatchCriteria',
            'action': 'str',
            'decryption_profile': 'str',
            'secret': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'condition': 'condition',
            'action': 'action',
            'decryption_profile': 'decryptionProfile',
            'secret': 'secret'
        }

        self._name = None
        self._condition = None
        self._action = None
        self._decryption_profile = None
        self._secret = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this DecryptionRule.
        Name for the decryption rule, must be unique within the policy.


        :return: The name of this DecryptionRule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this DecryptionRule.
        Name for the decryption rule, must be unique within the policy.


        :param name: The name of this DecryptionRule.
        :type: str
        """
        self._name = name

    @property
    def condition(self):
        """
        **[Required]** Gets the condition of this DecryptionRule.

        :return: The condition of this DecryptionRule.
        :rtype: oci.network_firewall.models.DecryptionRuleMatchCriteria
        """
        return self._condition

    @condition.setter
    def condition(self, condition):
        """
        Sets the condition of this DecryptionRule.

        :param condition: The condition of this DecryptionRule.
        :type: oci.network_firewall.models.DecryptionRuleMatchCriteria
        """
        self._condition = condition

    @property
    def action(self):
        """
        **[Required]** Gets the action of this DecryptionRule.
        Action:

        * NO_DECRYPT - Matching traffic is not decrypted.
        * DECRYPT - Matching traffic is decrypted with the specified `secret` according to the specified `decryptionProfile`.

        Allowed values for this property are: "NO_DECRYPT", "DECRYPT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The action of this DecryptionRule.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this DecryptionRule.
        Action:

        * NO_DECRYPT - Matching traffic is not decrypted.
        * DECRYPT - Matching traffic is decrypted with the specified `secret` according to the specified `decryptionProfile`.


        :param action: The action of this DecryptionRule.
        :type: str
        """
        allowed_values = ["NO_DECRYPT", "DECRYPT"]
        if not value_allowed_none_or_none_sentinel(action, allowed_values):
            action = 'UNKNOWN_ENUM_VALUE'
        self._action = action

    @property
    def decryption_profile(self):
        """
        Gets the decryption_profile of this DecryptionRule.
        The name of the decryption profile to use.


        :return: The decryption_profile of this DecryptionRule.
        :rtype: str
        """
        return self._decryption_profile

    @decryption_profile.setter
    def decryption_profile(self, decryption_profile):
        """
        Sets the decryption_profile of this DecryptionRule.
        The name of the decryption profile to use.


        :param decryption_profile: The decryption_profile of this DecryptionRule.
        :type: str
        """
        self._decryption_profile = decryption_profile

    @property
    def secret(self):
        """
        Gets the secret of this DecryptionRule.
        The name of a mapped secret. Its `type` must match that of the specified decryption profile.


        :return: The secret of this DecryptionRule.
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """
        Sets the secret of this DecryptionRule.
        The name of a mapped secret. Its `type` must match that of the specified decryption profile.


        :param secret: The secret of this DecryptionRule.
        :type: str
        """
        self._secret = secret

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
