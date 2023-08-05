# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutoUpgradableConfig(object):
    """
    The tenancy-level agent AutoUpgradable configuration.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AutoUpgradableConfig object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_agent_auto_upgradable:
            The value to assign to the is_agent_auto_upgradable property of this AutoUpgradableConfig.
        :type is_agent_auto_upgradable: bool

        """
        self.swagger_types = {
            'is_agent_auto_upgradable': 'bool'
        }

        self.attribute_map = {
            'is_agent_auto_upgradable': 'isAgentAutoUpgradable'
        }

        self._is_agent_auto_upgradable = None

    @property
    def is_agent_auto_upgradable(self):
        """
        **[Required]** Gets the is_agent_auto_upgradable of this AutoUpgradableConfig.
        true if the agents can be upgraded automatically; false if they must be upgraded manually.


        :return: The is_agent_auto_upgradable of this AutoUpgradableConfig.
        :rtype: bool
        """
        return self._is_agent_auto_upgradable

    @is_agent_auto_upgradable.setter
    def is_agent_auto_upgradable(self, is_agent_auto_upgradable):
        """
        Sets the is_agent_auto_upgradable of this AutoUpgradableConfig.
        true if the agents can be upgraded automatically; false if they must be upgraded manually.


        :param is_agent_auto_upgradable: The is_agent_auto_upgradable of this AutoUpgradableConfig.
        :type: bool
        """
        self._is_agent_auto_upgradable = is_agent_auto_upgradable

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
