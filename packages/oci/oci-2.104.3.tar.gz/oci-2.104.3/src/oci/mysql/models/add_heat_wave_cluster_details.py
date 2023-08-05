# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddHeatWaveClusterDetails(object):
    """
    Details required to add a HeatWave cluster.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddHeatWaveClusterDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param shape_name:
            The value to assign to the shape_name property of this AddHeatWaveClusterDetails.
        :type shape_name: str

        :param cluster_size:
            The value to assign to the cluster_size property of this AddHeatWaveClusterDetails.
        :type cluster_size: int

        :param is_lakehouse_enabled:
            The value to assign to the is_lakehouse_enabled property of this AddHeatWaveClusterDetails.
        :type is_lakehouse_enabled: bool

        """
        self.swagger_types = {
            'shape_name': 'str',
            'cluster_size': 'int',
            'is_lakehouse_enabled': 'bool'
        }

        self.attribute_map = {
            'shape_name': 'shapeName',
            'cluster_size': 'clusterSize',
            'is_lakehouse_enabled': 'isLakehouseEnabled'
        }

        self._shape_name = None
        self._cluster_size = None
        self._is_lakehouse_enabled = None

    @property
    def shape_name(self):
        """
        **[Required]** Gets the shape_name of this AddHeatWaveClusterDetails.
        The shape determines resources to allocate to the HeatWave
        nodes - CPU cores, memory.


        :return: The shape_name of this AddHeatWaveClusterDetails.
        :rtype: str
        """
        return self._shape_name

    @shape_name.setter
    def shape_name(self, shape_name):
        """
        Sets the shape_name of this AddHeatWaveClusterDetails.
        The shape determines resources to allocate to the HeatWave
        nodes - CPU cores, memory.


        :param shape_name: The shape_name of this AddHeatWaveClusterDetails.
        :type: str
        """
        self._shape_name = shape_name

    @property
    def cluster_size(self):
        """
        **[Required]** Gets the cluster_size of this AddHeatWaveClusterDetails.
        The number of analytics-processing nodes provisioned for the
        HeatWave cluster.


        :return: The cluster_size of this AddHeatWaveClusterDetails.
        :rtype: int
        """
        return self._cluster_size

    @cluster_size.setter
    def cluster_size(self, cluster_size):
        """
        Sets the cluster_size of this AddHeatWaveClusterDetails.
        The number of analytics-processing nodes provisioned for the
        HeatWave cluster.


        :param cluster_size: The cluster_size of this AddHeatWaveClusterDetails.
        :type: int
        """
        self._cluster_size = cluster_size

    @property
    def is_lakehouse_enabled(self):
        """
        Gets the is_lakehouse_enabled of this AddHeatWaveClusterDetails.
        Enable/disable Lakehouse for the HeatWave cluster.


        :return: The is_lakehouse_enabled of this AddHeatWaveClusterDetails.
        :rtype: bool
        """
        return self._is_lakehouse_enabled

    @is_lakehouse_enabled.setter
    def is_lakehouse_enabled(self, is_lakehouse_enabled):
        """
        Sets the is_lakehouse_enabled of this AddHeatWaveClusterDetails.
        Enable/disable Lakehouse for the HeatWave cluster.


        :param is_lakehouse_enabled: The is_lakehouse_enabled of this AddHeatWaveClusterDetails.
        :type: bool
        """
        self._is_lakehouse_enabled = is_lakehouse_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
