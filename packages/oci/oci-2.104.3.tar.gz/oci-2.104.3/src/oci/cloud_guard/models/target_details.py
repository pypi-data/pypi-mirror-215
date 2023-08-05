# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TargetDetails(object):
    """
    Details specific to the target type.
    """

    #: A constant which can be used with the target_resource_type property of a TargetDetails.
    #: This constant has a value of "COMPARTMENT"
    TARGET_RESOURCE_TYPE_COMPARTMENT = "COMPARTMENT"

    #: A constant which can be used with the target_resource_type property of a TargetDetails.
    #: This constant has a value of "ERPCLOUD"
    TARGET_RESOURCE_TYPE_ERPCLOUD = "ERPCLOUD"

    #: A constant which can be used with the target_resource_type property of a TargetDetails.
    #: This constant has a value of "HCMCLOUD"
    TARGET_RESOURCE_TYPE_HCMCLOUD = "HCMCLOUD"

    #: A constant which can be used with the target_resource_type property of a TargetDetails.
    #: This constant has a value of "SECURITY_ZONE"
    TARGET_RESOURCE_TYPE_SECURITY_ZONE = "SECURITY_ZONE"

    def __init__(self, **kwargs):
        """
        Initializes a new TargetDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.cloud_guard.models.SecurityZoneTargetDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param target_resource_type:
            The value to assign to the target_resource_type property of this TargetDetails.
            Allowed values for this property are: "COMPARTMENT", "ERPCLOUD", "HCMCLOUD", "SECURITY_ZONE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type target_resource_type: str

        """
        self.swagger_types = {
            'target_resource_type': 'str'
        }

        self.attribute_map = {
            'target_resource_type': 'targetResourceType'
        }

        self._target_resource_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['targetResourceType']

        if type == 'SECURITY_ZONE':
            return 'SecurityZoneTargetDetails'
        else:
            return 'TargetDetails'

    @property
    def target_resource_type(self):
        """
        **[Required]** Gets the target_resource_type of this TargetDetails.
        Possible type of targets.

        Allowed values for this property are: "COMPARTMENT", "ERPCLOUD", "HCMCLOUD", "SECURITY_ZONE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The target_resource_type of this TargetDetails.
        :rtype: str
        """
        return self._target_resource_type

    @target_resource_type.setter
    def target_resource_type(self, target_resource_type):
        """
        Sets the target_resource_type of this TargetDetails.
        Possible type of targets.


        :param target_resource_type: The target_resource_type of this TargetDetails.
        :type: str
        """
        allowed_values = ["COMPARTMENT", "ERPCLOUD", "HCMCLOUD", "SECURITY_ZONE"]
        if not value_allowed_none_or_none_sentinel(target_resource_type, allowed_values):
            target_resource_type = 'UNKNOWN_ENUM_VALUE'
        self._target_resource_type = target_resource_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
