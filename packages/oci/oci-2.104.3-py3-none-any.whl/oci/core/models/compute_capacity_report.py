# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ComputeCapacityReport(object):
    """
    A report of the host capacity within an availability domain that is available for you
    to create compute instances. Host capacity is the physical infrastructure that resources such as compute
    instances run on.

    Use the capacity report to determine whether sufficient capacity is available for a shape before
    you create an instance or change the shape of an instance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ComputeCapacityReport object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this ComputeCapacityReport.
        :type compartment_id: str

        :param availability_domain:
            The value to assign to the availability_domain property of this ComputeCapacityReport.
        :type availability_domain: str

        :param shape_availabilities:
            The value to assign to the shape_availabilities property of this ComputeCapacityReport.
        :type shape_availabilities: list[oci.core.models.CapacityReportShapeAvailability]

        :param time_created:
            The value to assign to the time_created property of this ComputeCapacityReport.
        :type time_created: datetime

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'availability_domain': 'str',
            'shape_availabilities': 'list[CapacityReportShapeAvailability]',
            'time_created': 'datetime'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'availability_domain': 'availabilityDomain',
            'shape_availabilities': 'shapeAvailabilities',
            'time_created': 'timeCreated'
        }

        self._compartment_id = None
        self._availability_domain = None
        self._shape_availabilities = None
        self._time_created = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ComputeCapacityReport.
        The `OCID`__ for the compartment. This should always be the root
        compartment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ComputeCapacityReport.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ComputeCapacityReport.
        The `OCID`__ for the compartment. This should always be the root
        compartment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ComputeCapacityReport.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def availability_domain(self):
        """
        **[Required]** Gets the availability_domain of this ComputeCapacityReport.
        The availability domain for the capacity report.

        Example: `Uocm:PHX-AD-1`


        :return: The availability_domain of this ComputeCapacityReport.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this ComputeCapacityReport.
        The availability domain for the capacity report.

        Example: `Uocm:PHX-AD-1`


        :param availability_domain: The availability_domain of this ComputeCapacityReport.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def shape_availabilities(self):
        """
        **[Required]** Gets the shape_availabilities of this ComputeCapacityReport.
        Information about the available capacity for each shape in a capacity report.


        :return: The shape_availabilities of this ComputeCapacityReport.
        :rtype: list[oci.core.models.CapacityReportShapeAvailability]
        """
        return self._shape_availabilities

    @shape_availabilities.setter
    def shape_availabilities(self, shape_availabilities):
        """
        Sets the shape_availabilities of this ComputeCapacityReport.
        Information about the available capacity for each shape in a capacity report.


        :param shape_availabilities: The shape_availabilities of this ComputeCapacityReport.
        :type: list[oci.core.models.CapacityReportShapeAvailability]
        """
        self._shape_availabilities = shape_availabilities

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ComputeCapacityReport.
        The date and time the capacity report was created, in the format defined by
        `RFC3339`__.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this ComputeCapacityReport.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ComputeCapacityReport.
        The date and time the capacity report was created, in the format defined by
        `RFC3339`__.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this ComputeCapacityReport.
        :type: datetime
        """
        self._time_created = time_created

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
