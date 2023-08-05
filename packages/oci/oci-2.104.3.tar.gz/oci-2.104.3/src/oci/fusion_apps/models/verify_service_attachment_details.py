# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VerifyServiceAttachmentDetails(object):
    """
    Information about the service attachment to be verified.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VerifyServiceAttachmentDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param service_instance_type:
            The value to assign to the service_instance_type property of this VerifyServiceAttachmentDetails.
        :type service_instance_type: str

        :param service_instance_id:
            The value to assign to the service_instance_id property of this VerifyServiceAttachmentDetails.
        :type service_instance_id: str

        """
        self.swagger_types = {
            'service_instance_type': 'str',
            'service_instance_id': 'str'
        }

        self.attribute_map = {
            'service_instance_type': 'serviceInstanceType',
            'service_instance_id': 'serviceInstanceId'
        }

        self._service_instance_type = None
        self._service_instance_id = None

    @property
    def service_instance_type(self):
        """
        **[Required]** Gets the service_instance_type of this VerifyServiceAttachmentDetails.
        Type of the ServiceInstance being attached.


        :return: The service_instance_type of this VerifyServiceAttachmentDetails.
        :rtype: str
        """
        return self._service_instance_type

    @service_instance_type.setter
    def service_instance_type(self, service_instance_type):
        """
        Sets the service_instance_type of this VerifyServiceAttachmentDetails.
        Type of the ServiceInstance being attached.


        :param service_instance_type: The service_instance_type of this VerifyServiceAttachmentDetails.
        :type: str
        """
        self._service_instance_type = service_instance_type

    @property
    def service_instance_id(self):
        """
        **[Required]** Gets the service_instance_id of this VerifyServiceAttachmentDetails.
        The service instance OCID of the instance being attached


        :return: The service_instance_id of this VerifyServiceAttachmentDetails.
        :rtype: str
        """
        return self._service_instance_id

    @service_instance_id.setter
    def service_instance_id(self, service_instance_id):
        """
        Sets the service_instance_id of this VerifyServiceAttachmentDetails.
        The service instance OCID of the instance being attached


        :param service_instance_id: The service_instance_id of this VerifyServiceAttachmentDetails.
        :type: str
        """
        self._service_instance_id = service_instance_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
