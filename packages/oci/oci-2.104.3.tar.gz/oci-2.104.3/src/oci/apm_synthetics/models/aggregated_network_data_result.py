# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AggregatedNetworkDataResult(object):
    """
    The aggregated network results.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AggregatedNetworkDataResult object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param aggregated_network_data:
            The value to assign to the aggregated_network_data property of this AggregatedNetworkDataResult.
        :type aggregated_network_data: oci.apm_synthetics.models.AggregatedNetworkData

        """
        self.swagger_types = {
            'aggregated_network_data': 'AggregatedNetworkData'
        }

        self.attribute_map = {
            'aggregated_network_data': 'aggregatedNetworkData'
        }

        self._aggregated_network_data = None

    @property
    def aggregated_network_data(self):
        """
        **[Required]** Gets the aggregated_network_data of this AggregatedNetworkDataResult.

        :return: The aggregated_network_data of this AggregatedNetworkDataResult.
        :rtype: oci.apm_synthetics.models.AggregatedNetworkData
        """
        return self._aggregated_network_data

    @aggregated_network_data.setter
    def aggregated_network_data(self, aggregated_network_data):
        """
        Sets the aggregated_network_data of this AggregatedNetworkDataResult.

        :param aggregated_network_data: The aggregated_network_data of this AggregatedNetworkDataResult.
        :type: oci.apm_synthetics.models.AggregatedNetworkData
        """
        self._aggregated_network_data = aggregated_network_data

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
