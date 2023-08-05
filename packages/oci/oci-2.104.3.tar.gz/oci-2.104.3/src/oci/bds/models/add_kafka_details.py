# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddKafkaDetails(object):
    """
    The information about the Kafka service to be added.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddKafkaDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param shape:
            The value to assign to the shape property of this AddKafkaDetails.
        :type shape: str

        :param number_of_kafka_nodes:
            The value to assign to the number_of_kafka_nodes property of this AddKafkaDetails.
        :type number_of_kafka_nodes: int

        :param shape_config:
            The value to assign to the shape_config property of this AddKafkaDetails.
        :type shape_config: oci.bds.models.ShapeConfigDetails

        :param block_volume_size_in_gbs:
            The value to assign to the block_volume_size_in_gbs property of this AddKafkaDetails.
        :type block_volume_size_in_gbs: int

        :param cluster_admin_password:
            The value to assign to the cluster_admin_password property of this AddKafkaDetails.
        :type cluster_admin_password: str

        """
        self.swagger_types = {
            'shape': 'str',
            'number_of_kafka_nodes': 'int',
            'shape_config': 'ShapeConfigDetails',
            'block_volume_size_in_gbs': 'int',
            'cluster_admin_password': 'str'
        }

        self.attribute_map = {
            'shape': 'shape',
            'number_of_kafka_nodes': 'numberOfKafkaNodes',
            'shape_config': 'shapeConfig',
            'block_volume_size_in_gbs': 'blockVolumeSizeInGBs',
            'cluster_admin_password': 'clusterAdminPassword'
        }

        self._shape = None
        self._number_of_kafka_nodes = None
        self._shape_config = None
        self._block_volume_size_in_gbs = None
        self._cluster_admin_password = None

    @property
    def shape(self):
        """
        **[Required]** Gets the shape of this AddKafkaDetails.
        Shape of the Kafka broker node.


        :return: The shape of this AddKafkaDetails.
        :rtype: str
        """
        return self._shape

    @shape.setter
    def shape(self, shape):
        """
        Sets the shape of this AddKafkaDetails.
        Shape of the Kafka broker node.


        :param shape: The shape of this AddKafkaDetails.
        :type: str
        """
        self._shape = shape

    @property
    def number_of_kafka_nodes(self):
        """
        **[Required]** Gets the number_of_kafka_nodes of this AddKafkaDetails.
        Number of Kafka nodes for the cluster.


        :return: The number_of_kafka_nodes of this AddKafkaDetails.
        :rtype: int
        """
        return self._number_of_kafka_nodes

    @number_of_kafka_nodes.setter
    def number_of_kafka_nodes(self, number_of_kafka_nodes):
        """
        Sets the number_of_kafka_nodes of this AddKafkaDetails.
        Number of Kafka nodes for the cluster.


        :param number_of_kafka_nodes: The number_of_kafka_nodes of this AddKafkaDetails.
        :type: int
        """
        self._number_of_kafka_nodes = number_of_kafka_nodes

    @property
    def shape_config(self):
        """
        Gets the shape_config of this AddKafkaDetails.

        :return: The shape_config of this AddKafkaDetails.
        :rtype: oci.bds.models.ShapeConfigDetails
        """
        return self._shape_config

    @shape_config.setter
    def shape_config(self, shape_config):
        """
        Sets the shape_config of this AddKafkaDetails.

        :param shape_config: The shape_config of this AddKafkaDetails.
        :type: oci.bds.models.ShapeConfigDetails
        """
        self._shape_config = shape_config

    @property
    def block_volume_size_in_gbs(self):
        """
        Gets the block_volume_size_in_gbs of this AddKafkaDetails.
        The size of block volme in GB to be attached to the given node. All details needed for attaching the block volume are managed by the service itself.


        :return: The block_volume_size_in_gbs of this AddKafkaDetails.
        :rtype: int
        """
        return self._block_volume_size_in_gbs

    @block_volume_size_in_gbs.setter
    def block_volume_size_in_gbs(self, block_volume_size_in_gbs):
        """
        Sets the block_volume_size_in_gbs of this AddKafkaDetails.
        The size of block volme in GB to be attached to the given node. All details needed for attaching the block volume are managed by the service itself.


        :param block_volume_size_in_gbs: The block_volume_size_in_gbs of this AddKafkaDetails.
        :type: int
        """
        self._block_volume_size_in_gbs = block_volume_size_in_gbs

    @property
    def cluster_admin_password(self):
        """
        **[Required]** Gets the cluster_admin_password of this AddKafkaDetails.
        Base-64 encoded password for the cluster admin user.


        :return: The cluster_admin_password of this AddKafkaDetails.
        :rtype: str
        """
        return self._cluster_admin_password

    @cluster_admin_password.setter
    def cluster_admin_password(self, cluster_admin_password):
        """
        Sets the cluster_admin_password of this AddKafkaDetails.
        Base-64 encoded password for the cluster admin user.


        :param cluster_admin_password: The cluster_admin_password of this AddKafkaDetails.
        :type: str
        """
        self._cluster_admin_password = cluster_admin_password

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
