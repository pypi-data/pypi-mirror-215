# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .access_policy_target_details import AccessPolicyTargetDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VirtualServiceAccessPolicyTargetDetails(AccessPolicyTargetDetails):
    """
    Virtual service target which communicates with other virtual services in a mesh.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new VirtualServiceAccessPolicyTargetDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.service_mesh.models.VirtualServiceAccessPolicyTargetDetails.type` attribute
        of this class is ``VIRTUAL_SERVICE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this VirtualServiceAccessPolicyTargetDetails.
            Allowed values for this property are: "ALL_VIRTUAL_SERVICES", "VIRTUAL_SERVICE", "EXTERNAL_SERVICE", "INGRESS_GATEWAY"
        :type type: str

        :param virtual_service_id:
            The value to assign to the virtual_service_id property of this VirtualServiceAccessPolicyTargetDetails.
        :type virtual_service_id: str

        """
        self.swagger_types = {
            'type': 'str',
            'virtual_service_id': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'virtual_service_id': 'virtualServiceId'
        }

        self._type = None
        self._virtual_service_id = None
        self._type = 'VIRTUAL_SERVICE'

    @property
    def virtual_service_id(self):
        """
        **[Required]** Gets the virtual_service_id of this VirtualServiceAccessPolicyTargetDetails.
        The OCID of the virtual service resource.


        :return: The virtual_service_id of this VirtualServiceAccessPolicyTargetDetails.
        :rtype: str
        """
        return self._virtual_service_id

    @virtual_service_id.setter
    def virtual_service_id(self, virtual_service_id):
        """
        Sets the virtual_service_id of this VirtualServiceAccessPolicyTargetDetails.
        The OCID of the virtual service resource.


        :param virtual_service_id: The virtual_service_id of this VirtualServiceAccessPolicyTargetDetails.
        :type: str
        """
        self._virtual_service_id = virtual_service_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
