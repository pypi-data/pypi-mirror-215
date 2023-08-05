# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalAsmDiskGroupSummary(object):
    """
    The summary of an external ASM disk group.
    """

    #: A constant which can be used with the redundancy_type property of a ExternalAsmDiskGroupSummary.
    #: This constant has a value of "EXTEND"
    REDUNDANCY_TYPE_EXTEND = "EXTEND"

    #: A constant which can be used with the redundancy_type property of a ExternalAsmDiskGroupSummary.
    #: This constant has a value of "EXTERN"
    REDUNDANCY_TYPE_EXTERN = "EXTERN"

    #: A constant which can be used with the redundancy_type property of a ExternalAsmDiskGroupSummary.
    #: This constant has a value of "FLEX"
    REDUNDANCY_TYPE_FLEX = "FLEX"

    #: A constant which can be used with the redundancy_type property of a ExternalAsmDiskGroupSummary.
    #: This constant has a value of "HIGH"
    REDUNDANCY_TYPE_HIGH = "HIGH"

    #: A constant which can be used with the redundancy_type property of a ExternalAsmDiskGroupSummary.
    #: This constant has a value of "NORMAL"
    REDUNDANCY_TYPE_NORMAL = "NORMAL"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalAsmDiskGroupSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ExternalAsmDiskGroupSummary.
        :type name: str

        :param mounting_instance_count:
            The value to assign to the mounting_instance_count property of this ExternalAsmDiskGroupSummary.
        :type mounting_instance_count: int

        :param dismounting_instance_count:
            The value to assign to the dismounting_instance_count property of this ExternalAsmDiskGroupSummary.
        :type dismounting_instance_count: int

        :param redundancy_type:
            The value to assign to the redundancy_type property of this ExternalAsmDiskGroupSummary.
            Allowed values for this property are: "EXTEND", "EXTERN", "FLEX", "HIGH", "NORMAL", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type redundancy_type: str

        :param is_sparse:
            The value to assign to the is_sparse property of this ExternalAsmDiskGroupSummary.
        :type is_sparse: bool

        :param databases:
            The value to assign to the databases property of this ExternalAsmDiskGroupSummary.
        :type databases: list[str]

        :param total_size_in_mbs:
            The value to assign to the total_size_in_mbs property of this ExternalAsmDiskGroupSummary.
        :type total_size_in_mbs: int

        :param used_size_in_mbs:
            The value to assign to the used_size_in_mbs property of this ExternalAsmDiskGroupSummary.
        :type used_size_in_mbs: int

        :param used_percent:
            The value to assign to the used_percent property of this ExternalAsmDiskGroupSummary.
        :type used_percent: float

        """
        self.swagger_types = {
            'name': 'str',
            'mounting_instance_count': 'int',
            'dismounting_instance_count': 'int',
            'redundancy_type': 'str',
            'is_sparse': 'bool',
            'databases': 'list[str]',
            'total_size_in_mbs': 'int',
            'used_size_in_mbs': 'int',
            'used_percent': 'float'
        }

        self.attribute_map = {
            'name': 'name',
            'mounting_instance_count': 'mountingInstanceCount',
            'dismounting_instance_count': 'dismountingInstanceCount',
            'redundancy_type': 'redundancyType',
            'is_sparse': 'isSparse',
            'databases': 'databases',
            'total_size_in_mbs': 'totalSizeInMBs',
            'used_size_in_mbs': 'usedSizeInMBs',
            'used_percent': 'usedPercent'
        }

        self._name = None
        self._mounting_instance_count = None
        self._dismounting_instance_count = None
        self._redundancy_type = None
        self._is_sparse = None
        self._databases = None
        self._total_size_in_mbs = None
        self._used_size_in_mbs = None
        self._used_percent = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this ExternalAsmDiskGroupSummary.
        The name of the ASM disk group.


        :return: The name of this ExternalAsmDiskGroupSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ExternalAsmDiskGroupSummary.
        The name of the ASM disk group.


        :param name: The name of this ExternalAsmDiskGroupSummary.
        :type: str
        """
        self._name = name

    @property
    def mounting_instance_count(self):
        """
        Gets the mounting_instance_count of this ExternalAsmDiskGroupSummary.
        The number of ASM instances that have the disk group in mounted state.


        :return: The mounting_instance_count of this ExternalAsmDiskGroupSummary.
        :rtype: int
        """
        return self._mounting_instance_count

    @mounting_instance_count.setter
    def mounting_instance_count(self, mounting_instance_count):
        """
        Sets the mounting_instance_count of this ExternalAsmDiskGroupSummary.
        The number of ASM instances that have the disk group in mounted state.


        :param mounting_instance_count: The mounting_instance_count of this ExternalAsmDiskGroupSummary.
        :type: int
        """
        self._mounting_instance_count = mounting_instance_count

    @property
    def dismounting_instance_count(self):
        """
        Gets the dismounting_instance_count of this ExternalAsmDiskGroupSummary.
        The number of ASM instances that have the disk group in dismounted state.


        :return: The dismounting_instance_count of this ExternalAsmDiskGroupSummary.
        :rtype: int
        """
        return self._dismounting_instance_count

    @dismounting_instance_count.setter
    def dismounting_instance_count(self, dismounting_instance_count):
        """
        Sets the dismounting_instance_count of this ExternalAsmDiskGroupSummary.
        The number of ASM instances that have the disk group in dismounted state.


        :param dismounting_instance_count: The dismounting_instance_count of this ExternalAsmDiskGroupSummary.
        :type: int
        """
        self._dismounting_instance_count = dismounting_instance_count

    @property
    def redundancy_type(self):
        """
        Gets the redundancy_type of this ExternalAsmDiskGroupSummary.
        The redundancy type of the disk group.

        Allowed values for this property are: "EXTEND", "EXTERN", "FLEX", "HIGH", "NORMAL", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The redundancy_type of this ExternalAsmDiskGroupSummary.
        :rtype: str
        """
        return self._redundancy_type

    @redundancy_type.setter
    def redundancy_type(self, redundancy_type):
        """
        Sets the redundancy_type of this ExternalAsmDiskGroupSummary.
        The redundancy type of the disk group.


        :param redundancy_type: The redundancy_type of this ExternalAsmDiskGroupSummary.
        :type: str
        """
        allowed_values = ["EXTEND", "EXTERN", "FLEX", "HIGH", "NORMAL"]
        if not value_allowed_none_or_none_sentinel(redundancy_type, allowed_values):
            redundancy_type = 'UNKNOWN_ENUM_VALUE'
        self._redundancy_type = redundancy_type

    @property
    def is_sparse(self):
        """
        Gets the is_sparse of this ExternalAsmDiskGroupSummary.
        Indicates whether the disk group is a sparse disk group or not.


        :return: The is_sparse of this ExternalAsmDiskGroupSummary.
        :rtype: bool
        """
        return self._is_sparse

    @is_sparse.setter
    def is_sparse(self, is_sparse):
        """
        Sets the is_sparse of this ExternalAsmDiskGroupSummary.
        Indicates whether the disk group is a sparse disk group or not.


        :param is_sparse: The is_sparse of this ExternalAsmDiskGroupSummary.
        :type: bool
        """
        self._is_sparse = is_sparse

    @property
    def databases(self):
        """
        Gets the databases of this ExternalAsmDiskGroupSummary.
        The unique names of the databases using the disk group.


        :return: The databases of this ExternalAsmDiskGroupSummary.
        :rtype: list[str]
        """
        return self._databases

    @databases.setter
    def databases(self, databases):
        """
        Sets the databases of this ExternalAsmDiskGroupSummary.
        The unique names of the databases using the disk group.


        :param databases: The databases of this ExternalAsmDiskGroupSummary.
        :type: list[str]
        """
        self._databases = databases

    @property
    def total_size_in_mbs(self):
        """
        Gets the total_size_in_mbs of this ExternalAsmDiskGroupSummary.
        The total capacity of the disk group (in megabytes).


        :return: The total_size_in_mbs of this ExternalAsmDiskGroupSummary.
        :rtype: int
        """
        return self._total_size_in_mbs

    @total_size_in_mbs.setter
    def total_size_in_mbs(self, total_size_in_mbs):
        """
        Sets the total_size_in_mbs of this ExternalAsmDiskGroupSummary.
        The total capacity of the disk group (in megabytes).


        :param total_size_in_mbs: The total_size_in_mbs of this ExternalAsmDiskGroupSummary.
        :type: int
        """
        self._total_size_in_mbs = total_size_in_mbs

    @property
    def used_size_in_mbs(self):
        """
        Gets the used_size_in_mbs of this ExternalAsmDiskGroupSummary.
        The used capacity of the disk group (in megabytes).


        :return: The used_size_in_mbs of this ExternalAsmDiskGroupSummary.
        :rtype: int
        """
        return self._used_size_in_mbs

    @used_size_in_mbs.setter
    def used_size_in_mbs(self, used_size_in_mbs):
        """
        Sets the used_size_in_mbs of this ExternalAsmDiskGroupSummary.
        The used capacity of the disk group (in megabytes).


        :param used_size_in_mbs: The used_size_in_mbs of this ExternalAsmDiskGroupSummary.
        :type: int
        """
        self._used_size_in_mbs = used_size_in_mbs

    @property
    def used_percent(self):
        """
        Gets the used_percent of this ExternalAsmDiskGroupSummary.
        The percentage of used space in the disk group.


        :return: The used_percent of this ExternalAsmDiskGroupSummary.
        :rtype: float
        """
        return self._used_percent

    @used_percent.setter
    def used_percent(self, used_percent):
        """
        Sets the used_percent of this ExternalAsmDiskGroupSummary.
        The percentage of used space in the disk group.


        :param used_percent: The used_percent of this ExternalAsmDiskGroupSummary.
        :type: float
        """
        self._used_percent = used_percent

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
