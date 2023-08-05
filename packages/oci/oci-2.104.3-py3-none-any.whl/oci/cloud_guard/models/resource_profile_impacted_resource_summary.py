# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceProfileImpactedResourceSummary(object):
    """
    Resource Profile impacted resource summary.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceProfileImpactedResourceSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ResourceProfileImpactedResourceSummary.
        :type id: str

        :param resource_profile_id:
            The value to assign to the resource_profile_id property of this ResourceProfileImpactedResourceSummary.
        :type resource_profile_id: str

        :param problem_id:
            The value to assign to the problem_id property of this ResourceProfileImpactedResourceSummary.
        :type problem_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ResourceProfileImpactedResourceSummary.
        :type compartment_id: str

        :param resource_id:
            The value to assign to the resource_id property of this ResourceProfileImpactedResourceSummary.
        :type resource_id: str

        :param resource_name:
            The value to assign to the resource_name property of this ResourceProfileImpactedResourceSummary.
        :type resource_name: str

        :param resource_type:
            The value to assign to the resource_type property of this ResourceProfileImpactedResourceSummary.
        :type resource_type: str

        :param sighting_type:
            The value to assign to the sighting_type property of this ResourceProfileImpactedResourceSummary.
        :type sighting_type: str

        :param sighting_type_display_name:
            The value to assign to the sighting_type_display_name property of this ResourceProfileImpactedResourceSummary.
        :type sighting_type_display_name: str

        :param region:
            The value to assign to the region property of this ResourceProfileImpactedResourceSummary.
        :type region: str

        :param time_identified:
            The value to assign to the time_identified property of this ResourceProfileImpactedResourceSummary.
        :type time_identified: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'resource_profile_id': 'str',
            'problem_id': 'str',
            'compartment_id': 'str',
            'resource_id': 'str',
            'resource_name': 'str',
            'resource_type': 'str',
            'sighting_type': 'str',
            'sighting_type_display_name': 'str',
            'region': 'str',
            'time_identified': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'resource_profile_id': 'resourceProfileId',
            'problem_id': 'problemId',
            'compartment_id': 'compartmentId',
            'resource_id': 'resourceId',
            'resource_name': 'resourceName',
            'resource_type': 'resourceType',
            'sighting_type': 'sightingType',
            'sighting_type_display_name': 'sightingTypeDisplayName',
            'region': 'region',
            'time_identified': 'timeIdentified'
        }

        self._id = None
        self._resource_profile_id = None
        self._problem_id = None
        self._compartment_id = None
        self._resource_id = None
        self._resource_name = None
        self._resource_type = None
        self._sighting_type = None
        self._sighting_type_display_name = None
        self._region = None
        self._time_identified = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ResourceProfileImpactedResourceSummary.
        Unique identifier for impacted resource


        :return: The id of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ResourceProfileImpactedResourceSummary.
        Unique identifier for impacted resource


        :param id: The id of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._id = id

    @property
    def resource_profile_id(self):
        """
        **[Required]** Gets the resource_profile_id of this ResourceProfileImpactedResourceSummary.
        Resource profile Id associated with the imacted resource


        :return: The resource_profile_id of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._resource_profile_id

    @resource_profile_id.setter
    def resource_profile_id(self, resource_profile_id):
        """
        Sets the resource_profile_id of this ResourceProfileImpactedResourceSummary.
        Resource profile Id associated with the imacted resource


        :param resource_profile_id: The resource_profile_id of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._resource_profile_id = resource_profile_id

    @property
    def problem_id(self):
        """
        Gets the problem_id of this ResourceProfileImpactedResourceSummary.
        Problem Id for impacted resource


        :return: The problem_id of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._problem_id

    @problem_id.setter
    def problem_id(self, problem_id):
        """
        Sets the problem_id of this ResourceProfileImpactedResourceSummary.
        Problem Id for impacted resource


        :param problem_id: The problem_id of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._problem_id = problem_id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ResourceProfileImpactedResourceSummary.
        Compartment Id for impacted resource


        :return: The compartment_id of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ResourceProfileImpactedResourceSummary.
        Compartment Id for impacted resource


        :param compartment_id: The compartment_id of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def resource_id(self):
        """
        **[Required]** Gets the resource_id of this ResourceProfileImpactedResourceSummary.
        Impacted resource Id


        :return: The resource_id of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id):
        """
        Sets the resource_id of this ResourceProfileImpactedResourceSummary.
        Impacted resource Id


        :param resource_id: The resource_id of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._resource_id = resource_id

    @property
    def resource_name(self):
        """
        **[Required]** Gets the resource_name of this ResourceProfileImpactedResourceSummary.
        Resource name


        :return: The resource_name of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._resource_name

    @resource_name.setter
    def resource_name(self, resource_name):
        """
        Sets the resource_name of this ResourceProfileImpactedResourceSummary.
        Resource name


        :param resource_name: The resource_name of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._resource_name = resource_name

    @property
    def resource_type(self):
        """
        **[Required]** Gets the resource_type of this ResourceProfileImpactedResourceSummary.
        Resource type


        :return: The resource_type of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._resource_type

    @resource_type.setter
    def resource_type(self, resource_type):
        """
        Sets the resource_type of this ResourceProfileImpactedResourceSummary.
        Resource type


        :param resource_type: The resource_type of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._resource_type = resource_type

    @property
    def sighting_type(self):
        """
        **[Required]** Gets the sighting_type of this ResourceProfileImpactedResourceSummary.
        Identifier for the sighting type


        :return: The sighting_type of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._sighting_type

    @sighting_type.setter
    def sighting_type(self, sighting_type):
        """
        Sets the sighting_type of this ResourceProfileImpactedResourceSummary.
        Identifier for the sighting type


        :param sighting_type: The sighting_type of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._sighting_type = sighting_type

    @property
    def sighting_type_display_name(self):
        """
        **[Required]** Gets the sighting_type_display_name of this ResourceProfileImpactedResourceSummary.
        Name of the sighting type


        :return: The sighting_type_display_name of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._sighting_type_display_name

    @sighting_type_display_name.setter
    def sighting_type_display_name(self, sighting_type_display_name):
        """
        Sets the sighting_type_display_name of this ResourceProfileImpactedResourceSummary.
        Name of the sighting type


        :param sighting_type_display_name: The sighting_type_display_name of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._sighting_type_display_name = sighting_type_display_name

    @property
    def region(self):
        """
        **[Required]** Gets the region of this ResourceProfileImpactedResourceSummary.
        Region for impacted resource


        :return: The region of this ResourceProfileImpactedResourceSummary.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """
        Sets the region of this ResourceProfileImpactedResourceSummary.
        Region for impacted resource


        :param region: The region of this ResourceProfileImpactedResourceSummary.
        :type: str
        """
        self._region = region

    @property
    def time_identified(self):
        """
        **[Required]** Gets the time_identified of this ResourceProfileImpactedResourceSummary.
        Time when the impacted resource is identified for given resource profile.


        :return: The time_identified of this ResourceProfileImpactedResourceSummary.
        :rtype: datetime
        """
        return self._time_identified

    @time_identified.setter
    def time_identified(self, time_identified):
        """
        Sets the time_identified of this ResourceProfileImpactedResourceSummary.
        Time when the impacted resource is identified for given resource profile.


        :param time_identified: The time_identified of this ResourceProfileImpactedResourceSummary.
        :type: datetime
        """
        self._time_identified = time_identified

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
