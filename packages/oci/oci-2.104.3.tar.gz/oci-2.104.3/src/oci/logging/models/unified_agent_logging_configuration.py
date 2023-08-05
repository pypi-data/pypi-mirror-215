# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .unified_agent_service_configuration_details import UnifiedAgentServiceConfigurationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UnifiedAgentLoggingConfiguration(UnifiedAgentServiceConfigurationDetails):
    """
    Unified Agent logging service configuration object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UnifiedAgentLoggingConfiguration object with values from keyword arguments. The default value of the :py:attr:`~oci.logging.models.UnifiedAgentLoggingConfiguration.configuration_type` attribute
        of this class is ``LOGGING`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param configuration_type:
            The value to assign to the configuration_type property of this UnifiedAgentLoggingConfiguration.
            Allowed values for this property are: "LOGGING"
        :type configuration_type: str

        :param sources:
            The value to assign to the sources property of this UnifiedAgentLoggingConfiguration.
        :type sources: list[oci.logging.models.UnifiedAgentLoggingSource]

        :param destination:
            The value to assign to the destination property of this UnifiedAgentLoggingConfiguration.
        :type destination: oci.logging.models.UnifiedAgentLoggingDestination

        """
        self.swagger_types = {
            'configuration_type': 'str',
            'sources': 'list[UnifiedAgentLoggingSource]',
            'destination': 'UnifiedAgentLoggingDestination'
        }

        self.attribute_map = {
            'configuration_type': 'configurationType',
            'sources': 'sources',
            'destination': 'destination'
        }

        self._configuration_type = None
        self._sources = None
        self._destination = None
        self._configuration_type = 'LOGGING'

    @property
    def sources(self):
        """
        **[Required]** Gets the sources of this UnifiedAgentLoggingConfiguration.
        Logging source object.


        :return: The sources of this UnifiedAgentLoggingConfiguration.
        :rtype: list[oci.logging.models.UnifiedAgentLoggingSource]
        """
        return self._sources

    @sources.setter
    def sources(self, sources):
        """
        Sets the sources of this UnifiedAgentLoggingConfiguration.
        Logging source object.


        :param sources: The sources of this UnifiedAgentLoggingConfiguration.
        :type: list[oci.logging.models.UnifiedAgentLoggingSource]
        """
        self._sources = sources

    @property
    def destination(self):
        """
        **[Required]** Gets the destination of this UnifiedAgentLoggingConfiguration.

        :return: The destination of this UnifiedAgentLoggingConfiguration.
        :rtype: oci.logging.models.UnifiedAgentLoggingDestination
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """
        Sets the destination of this UnifiedAgentLoggingConfiguration.

        :param destination: The destination of this UnifiedAgentLoggingConfiguration.
        :type: oci.logging.models.UnifiedAgentLoggingDestination
        """
        self._destination = destination

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
