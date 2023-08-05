# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AwsS3Details(object):
    """
    AWS S3 bucket details used for source Connection resources with RDS_ORACLE type.
    Only supported for source Connection resources with RDS_ORACLE type.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AwsS3Details object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this AwsS3Details.
        :type name: str

        :param region:
            The value to assign to the region property of this AwsS3Details.
        :type region: str

        """
        self.swagger_types = {
            'name': 'str',
            'region': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'region': 'region'
        }

        self._name = None
        self._region = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this AwsS3Details.
        S3 bucket name.


        :return: The name of this AwsS3Details.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AwsS3Details.
        S3 bucket name.


        :param name: The name of this AwsS3Details.
        :type: str
        """
        self._name = name

    @property
    def region(self):
        """
        **[Required]** Gets the region of this AwsS3Details.
        AWS region code where the S3 bucket is located.
        Region code should match the documented available regions:
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions


        :return: The region of this AwsS3Details.
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """
        Sets the region of this AwsS3Details.
        AWS region code where the S3 bucket is located.
        Region code should match the documented available regions:
        https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions


        :param region: The region of this AwsS3Details.
        :type: str
        """
        self._region = region

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
