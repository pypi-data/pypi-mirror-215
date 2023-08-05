# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ContainerDnsConfig(object):
    """
    DNS settings for containers.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ContainerDnsConfig object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param nameservers:
            The value to assign to the nameservers property of this ContainerDnsConfig.
        :type nameservers: list[str]

        :param searches:
            The value to assign to the searches property of this ContainerDnsConfig.
        :type searches: list[str]

        :param options:
            The value to assign to the options property of this ContainerDnsConfig.
        :type options: list[str]

        """
        self.swagger_types = {
            'nameservers': 'list[str]',
            'searches': 'list[str]',
            'options': 'list[str]'
        }

        self.attribute_map = {
            'nameservers': 'nameservers',
            'searches': 'searches',
            'options': 'options'
        }

        self._nameservers = None
        self._searches = None
        self._options = None

    @property
    def nameservers(self):
        """
        Gets the nameservers of this ContainerDnsConfig.
        Name server IP address


        :return: The nameservers of this ContainerDnsConfig.
        :rtype: list[str]
        """
        return self._nameservers

    @nameservers.setter
    def nameservers(self, nameservers):
        """
        Sets the nameservers of this ContainerDnsConfig.
        Name server IP address


        :param nameservers: The nameservers of this ContainerDnsConfig.
        :type: list[str]
        """
        self._nameservers = nameservers

    @property
    def searches(self):
        """
        Gets the searches of this ContainerDnsConfig.
        Search list for host-name lookup.


        :return: The searches of this ContainerDnsConfig.
        :rtype: list[str]
        """
        return self._searches

    @searches.setter
    def searches(self, searches):
        """
        Sets the searches of this ContainerDnsConfig.
        Search list for host-name lookup.


        :param searches: The searches of this ContainerDnsConfig.
        :type: list[str]
        """
        self._searches = searches

    @property
    def options(self):
        """
        Gets the options of this ContainerDnsConfig.
        Options allows certain internal resolver variables to be modified.


        :return: The options of this ContainerDnsConfig.
        :rtype: list[str]
        """
        return self._options

    @options.setter
    def options(self, options):
        """
        Sets the options of this ContainerDnsConfig.
        Options allows certain internal resolver variables to be modified.


        :param options: The options of this ContainerDnsConfig.
        :type: list[str]
        """
        self._options = options

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
