# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExadataInfrastructureUnAllocatedResources(object):
    """
    Un allocated resources details of the Exadata Cloud@Customer infrastructure. Applies to Exadata Cloud@Customer instances only.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExadataInfrastructureUnAllocatedResources object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExadataInfrastructureUnAllocatedResources.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExadataInfrastructureUnAllocatedResources.
        :type display_name: str

        :param local_storage_in_gbs:
            The value to assign to the local_storage_in_gbs property of this ExadataInfrastructureUnAllocatedResources.
        :type local_storage_in_gbs: int

        :param ocpus:
            The value to assign to the ocpus property of this ExadataInfrastructureUnAllocatedResources.
        :type ocpus: int

        :param memory_in_gbs:
            The value to assign to the memory_in_gbs property of this ExadataInfrastructureUnAllocatedResources.
        :type memory_in_gbs: int

        :param exadata_storage_in_tbs:
            The value to assign to the exadata_storage_in_tbs property of this ExadataInfrastructureUnAllocatedResources.
        :type exadata_storage_in_tbs: float

        :param autonomous_vm_clusters:
            The value to assign to the autonomous_vm_clusters property of this ExadataInfrastructureUnAllocatedResources.
        :type autonomous_vm_clusters: list[oci.database.models.AutonomousVmClusterResourceDetails]

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'local_storage_in_gbs': 'int',
            'ocpus': 'int',
            'memory_in_gbs': 'int',
            'exadata_storage_in_tbs': 'float',
            'autonomous_vm_clusters': 'list[AutonomousVmClusterResourceDetails]'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'local_storage_in_gbs': 'localStorageInGbs',
            'ocpus': 'ocpus',
            'memory_in_gbs': 'memoryInGBs',
            'exadata_storage_in_tbs': 'exadataStorageInTBs',
            'autonomous_vm_clusters': 'autonomousVmClusters'
        }

        self._id = None
        self._display_name = None
        self._local_storage_in_gbs = None
        self._ocpus = None
        self._memory_in_gbs = None
        self._exadata_storage_in_tbs = None
        self._autonomous_vm_clusters = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExadataInfrastructureUnAllocatedResources.
        The `OCID`__ of the Exadata infrastructure.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExadataInfrastructureUnAllocatedResources.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExadataInfrastructureUnAllocatedResources.
        The `OCID`__ of the Exadata infrastructure.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExadataInfrastructureUnAllocatedResources.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExadataInfrastructureUnAllocatedResources.
        The user-friendly name for the Exadata Cloud@Customer infrastructure. The name does not need to be unique.


        :return: The display_name of this ExadataInfrastructureUnAllocatedResources.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExadataInfrastructureUnAllocatedResources.
        The user-friendly name for the Exadata Cloud@Customer infrastructure. The name does not need to be unique.


        :param display_name: The display_name of this ExadataInfrastructureUnAllocatedResources.
        :type: str
        """
        self._display_name = display_name

    @property
    def local_storage_in_gbs(self):
        """
        Gets the local_storage_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        The minimum amount of un allocated storage that is available across all nodes in the infrastructure.


        :return: The local_storage_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        :rtype: int
        """
        return self._local_storage_in_gbs

    @local_storage_in_gbs.setter
    def local_storage_in_gbs(self, local_storage_in_gbs):
        """
        Sets the local_storage_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        The minimum amount of un allocated storage that is available across all nodes in the infrastructure.


        :param local_storage_in_gbs: The local_storage_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        :type: int
        """
        self._local_storage_in_gbs = local_storage_in_gbs

    @property
    def ocpus(self):
        """
        Gets the ocpus of this ExadataInfrastructureUnAllocatedResources.
        The minimum amount of un allocated ocpus that is available across all nodes in the infrastructure.


        :return: The ocpus of this ExadataInfrastructureUnAllocatedResources.
        :rtype: int
        """
        return self._ocpus

    @ocpus.setter
    def ocpus(self, ocpus):
        """
        Sets the ocpus of this ExadataInfrastructureUnAllocatedResources.
        The minimum amount of un allocated ocpus that is available across all nodes in the infrastructure.


        :param ocpus: The ocpus of this ExadataInfrastructureUnAllocatedResources.
        :type: int
        """
        self._ocpus = ocpus

    @property
    def memory_in_gbs(self):
        """
        Gets the memory_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        The minimum amount of un allocated memory that is available across all nodes in the infrastructure.


        :return: The memory_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        :rtype: int
        """
        return self._memory_in_gbs

    @memory_in_gbs.setter
    def memory_in_gbs(self, memory_in_gbs):
        """
        Sets the memory_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        The minimum amount of un allocated memory that is available across all nodes in the infrastructure.


        :param memory_in_gbs: The memory_in_gbs of this ExadataInfrastructureUnAllocatedResources.
        :type: int
        """
        self._memory_in_gbs = memory_in_gbs

    @property
    def exadata_storage_in_tbs(self):
        """
        Gets the exadata_storage_in_tbs of this ExadataInfrastructureUnAllocatedResources.
        Total unallocated exadata storage in the infrastructure in TBs.


        :return: The exadata_storage_in_tbs of this ExadataInfrastructureUnAllocatedResources.
        :rtype: float
        """
        return self._exadata_storage_in_tbs

    @exadata_storage_in_tbs.setter
    def exadata_storage_in_tbs(self, exadata_storage_in_tbs):
        """
        Sets the exadata_storage_in_tbs of this ExadataInfrastructureUnAllocatedResources.
        Total unallocated exadata storage in the infrastructure in TBs.


        :param exadata_storage_in_tbs: The exadata_storage_in_tbs of this ExadataInfrastructureUnAllocatedResources.
        :type: float
        """
        self._exadata_storage_in_tbs = exadata_storage_in_tbs

    @property
    def autonomous_vm_clusters(self):
        """
        Gets the autonomous_vm_clusters of this ExadataInfrastructureUnAllocatedResources.
        The list of Autonomous VM Clusters on the Infra and their associated unallocated resources details


        :return: The autonomous_vm_clusters of this ExadataInfrastructureUnAllocatedResources.
        :rtype: list[oci.database.models.AutonomousVmClusterResourceDetails]
        """
        return self._autonomous_vm_clusters

    @autonomous_vm_clusters.setter
    def autonomous_vm_clusters(self, autonomous_vm_clusters):
        """
        Sets the autonomous_vm_clusters of this ExadataInfrastructureUnAllocatedResources.
        The list of Autonomous VM Clusters on the Infra and their associated unallocated resources details


        :param autonomous_vm_clusters: The autonomous_vm_clusters of this ExadataInfrastructureUnAllocatedResources.
        :type: list[oci.database.models.AutonomousVmClusterResourceDetails]
        """
        self._autonomous_vm_clusters = autonomous_vm_clusters

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
