# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class FleetAgentOsConfiguration(object):
    """
    Management Agent Configuration for list of include/exclude file system paths (specific to operating system).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new FleetAgentOsConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param include_paths:
            The value to assign to the include_paths property of this FleetAgentOsConfiguration.
        :type include_paths: list[str]

        :param exclude_paths:
            The value to assign to the exclude_paths property of this FleetAgentOsConfiguration.
        :type exclude_paths: list[str]

        """
        self.swagger_types = {
            'include_paths': 'list[str]',
            'exclude_paths': 'list[str]'
        }

        self.attribute_map = {
            'include_paths': 'includePaths',
            'exclude_paths': 'excludePaths'
        }

        self._include_paths = None
        self._exclude_paths = None

    @property
    def include_paths(self):
        """
        **[Required]** Gets the include_paths of this FleetAgentOsConfiguration.
        An array of file system paths (environment variables supported).


        :return: The include_paths of this FleetAgentOsConfiguration.
        :rtype: list[str]
        """
        return self._include_paths

    @include_paths.setter
    def include_paths(self, include_paths):
        """
        Sets the include_paths of this FleetAgentOsConfiguration.
        An array of file system paths (environment variables supported).


        :param include_paths: The include_paths of this FleetAgentOsConfiguration.
        :type: list[str]
        """
        self._include_paths = include_paths

    @property
    def exclude_paths(self):
        """
        **[Required]** Gets the exclude_paths of this FleetAgentOsConfiguration.
        An array of file system paths (environment variables supported).


        :return: The exclude_paths of this FleetAgentOsConfiguration.
        :rtype: list[str]
        """
        return self._exclude_paths

    @exclude_paths.setter
    def exclude_paths(self, exclude_paths):
        """
        Sets the exclude_paths of this FleetAgentOsConfiguration.
        An array of file system paths (environment variables supported).


        :param exclude_paths: The exclude_paths of this FleetAgentOsConfiguration.
        :type: list[str]
        """
        self._exclude_paths = exclude_paths

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
