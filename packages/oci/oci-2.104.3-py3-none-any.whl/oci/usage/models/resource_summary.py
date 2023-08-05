# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceSummary(object):
    """
    The details of a resource under a service.
    """

    #: A constant which can be used with the usage_data_type property of a ResourceSummary.
    #: This constant has a value of "INTERVAL"
    USAGE_DATA_TYPE_INTERVAL = "INTERVAL"

    #: A constant which can be used with the usage_data_type property of a ResourceSummary.
    #: This constant has a value of "POINT_DATA"
    USAGE_DATA_TYPE_POINT_DATA = "POINT_DATA"

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param daily_unit_display_name:
            The value to assign to the daily_unit_display_name property of this ResourceSummary.
        :type daily_unit_display_name: str

        :param hourly_unit_display_name:
            The value to assign to the hourly_unit_display_name property of this ResourceSummary.
        :type hourly_unit_display_name: str

        :param raw_unit_display_name:
            The value to assign to the raw_unit_display_name property of this ResourceSummary.
        :type raw_unit_display_name: str

        :param usage_data_type:
            The value to assign to the usage_data_type property of this ResourceSummary.
            Allowed values for this property are: "INTERVAL", "POINT_DATA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type usage_data_type: str

        :param name:
            The value to assign to the name property of this ResourceSummary.
        :type name: str

        :param servicename:
            The value to assign to the servicename property of this ResourceSummary.
        :type servicename: str

        :param description:
            The value to assign to the description property of this ResourceSummary.
        :type description: str

        :param instance_type:
            The value to assign to the instance_type property of this ResourceSummary.
        :type instance_type: str

        :param is_purchased:
            The value to assign to the is_purchased property of this ResourceSummary.
        :type is_purchased: bool

        :param child_resources:
            The value to assign to the child_resources property of this ResourceSummary.
        :type child_resources: list[str]

        :param skus:
            The value to assign to the skus property of this ResourceSummary.
        :type skus: list[oci.usage.models.SkuProducts]

        """
        self.swagger_types = {
            'daily_unit_display_name': 'str',
            'hourly_unit_display_name': 'str',
            'raw_unit_display_name': 'str',
            'usage_data_type': 'str',
            'name': 'str',
            'servicename': 'str',
            'description': 'str',
            'instance_type': 'str',
            'is_purchased': 'bool',
            'child_resources': 'list[str]',
            'skus': 'list[SkuProducts]'
        }

        self.attribute_map = {
            'daily_unit_display_name': 'dailyUnitDisplayName',
            'hourly_unit_display_name': 'hourlyUnitDisplayName',
            'raw_unit_display_name': 'rawUnitDisplayName',
            'usage_data_type': 'usageDataType',
            'name': 'name',
            'servicename': 'servicename',
            'description': 'description',
            'instance_type': 'instanceType',
            'is_purchased': 'isPurchased',
            'child_resources': 'childResources',
            'skus': 'skus'
        }

        self._daily_unit_display_name = None
        self._hourly_unit_display_name = None
        self._raw_unit_display_name = None
        self._usage_data_type = None
        self._name = None
        self._servicename = None
        self._description = None
        self._instance_type = None
        self._is_purchased = None
        self._child_resources = None
        self._skus = None

    @property
    def daily_unit_display_name(self):
        """
        Gets the daily_unit_display_name of this ResourceSummary.
        Units to be used for daily aggregated data.


        :return: The daily_unit_display_name of this ResourceSummary.
        :rtype: str
        """
        return self._daily_unit_display_name

    @daily_unit_display_name.setter
    def daily_unit_display_name(self, daily_unit_display_name):
        """
        Sets the daily_unit_display_name of this ResourceSummary.
        Units to be used for daily aggregated data.


        :param daily_unit_display_name: The daily_unit_display_name of this ResourceSummary.
        :type: str
        """
        self._daily_unit_display_name = daily_unit_display_name

    @property
    def hourly_unit_display_name(self):
        """
        Gets the hourly_unit_display_name of this ResourceSummary.
        Units to be used for hourly aggregated data.


        :return: The hourly_unit_display_name of this ResourceSummary.
        :rtype: str
        """
        return self._hourly_unit_display_name

    @hourly_unit_display_name.setter
    def hourly_unit_display_name(self, hourly_unit_display_name):
        """
        Sets the hourly_unit_display_name of this ResourceSummary.
        Units to be used for hourly aggregated data.


        :param hourly_unit_display_name: The hourly_unit_display_name of this ResourceSummary.
        :type: str
        """
        self._hourly_unit_display_name = hourly_unit_display_name

    @property
    def raw_unit_display_name(self):
        """
        Gets the raw_unit_display_name of this ResourceSummary.
        Default units to use when unspecified.


        :return: The raw_unit_display_name of this ResourceSummary.
        :rtype: str
        """
        return self._raw_unit_display_name

    @raw_unit_display_name.setter
    def raw_unit_display_name(self, raw_unit_display_name):
        """
        Sets the raw_unit_display_name of this ResourceSummary.
        Default units to use when unspecified.


        :param raw_unit_display_name: The raw_unit_display_name of this ResourceSummary.
        :type: str
        """
        self._raw_unit_display_name = raw_unit_display_name

    @property
    def usage_data_type(self):
        """
        Gets the usage_data_type of this ResourceSummary.
        Usage data type of the resource.

        Allowed values for this property are: "INTERVAL", "POINT_DATA", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The usage_data_type of this ResourceSummary.
        :rtype: str
        """
        return self._usage_data_type

    @usage_data_type.setter
    def usage_data_type(self, usage_data_type):
        """
        Sets the usage_data_type of this ResourceSummary.
        Usage data type of the resource.


        :param usage_data_type: The usage_data_type of this ResourceSummary.
        :type: str
        """
        allowed_values = ["INTERVAL", "POINT_DATA"]
        if not value_allowed_none_or_none_sentinel(usage_data_type, allowed_values):
            usage_data_type = 'UNKNOWN_ENUM_VALUE'
        self._usage_data_type = usage_data_type

    @property
    def name(self):
        """
        Gets the name of this ResourceSummary.
        Name of the resource.


        :return: The name of this ResourceSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ResourceSummary.
        Name of the resource.


        :param name: The name of this ResourceSummary.
        :type: str
        """
        self._name = name

    @property
    def servicename(self):
        """
        Gets the servicename of this ResourceSummary.
        Name of the service.


        :return: The servicename of this ResourceSummary.
        :rtype: str
        """
        return self._servicename

    @servicename.setter
    def servicename(self, servicename):
        """
        Sets the servicename of this ResourceSummary.
        Name of the service.


        :param servicename: The servicename of this ResourceSummary.
        :type: str
        """
        self._servicename = servicename

    @property
    def description(self):
        """
        Gets the description of this ResourceSummary.
        Description of the resource.


        :return: The description of this ResourceSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ResourceSummary.
        Description of the resource.


        :param description: The description of this ResourceSummary.
        :type: str
        """
        self._description = description

    @property
    def instance_type(self):
        """
        Gets the instance_type of this ResourceSummary.
        Instance type for the resource.


        :return: The instance_type of this ResourceSummary.
        :rtype: str
        """
        return self._instance_type

    @instance_type.setter
    def instance_type(self, instance_type):
        """
        Sets the instance_type of this ResourceSummary.
        Instance type for the resource.


        :param instance_type: The instance_type of this ResourceSummary.
        :type: str
        """
        self._instance_type = instance_type

    @property
    def is_purchased(self):
        """
        Gets the is_purchased of this ResourceSummary.
        Indicates if the SKU was purchased


        :return: The is_purchased of this ResourceSummary.
        :rtype: bool
        """
        return self._is_purchased

    @is_purchased.setter
    def is_purchased(self, is_purchased):
        """
        Sets the is_purchased of this ResourceSummary.
        Indicates if the SKU was purchased


        :param is_purchased: The is_purchased of this ResourceSummary.
        :type: bool
        """
        self._is_purchased = is_purchased

    @property
    def child_resources(self):
        """
        Gets the child_resources of this ResourceSummary.
        The details of any child resources.


        :return: The child_resources of this ResourceSummary.
        :rtype: list[str]
        """
        return self._child_resources

    @child_resources.setter
    def child_resources(self, child_resources):
        """
        Sets the child_resources of this ResourceSummary.
        The details of any child resources.


        :param child_resources: The child_resources of this ResourceSummary.
        :type: list[str]
        """
        self._child_resources = child_resources

    @property
    def skus(self):
        """
        Gets the skus of this ResourceSummary.
        The details of resource Skus.


        :return: The skus of this ResourceSummary.
        :rtype: list[oci.usage.models.SkuProducts]
        """
        return self._skus

    @skus.setter
    def skus(self, skus):
        """
        Sets the skus of this ResourceSummary.
        The details of resource Skus.


        :param skus: The skus of this ResourceSummary.
        :type: list[oci.usage.models.SkuProducts]
        """
        self._skus = skus

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
