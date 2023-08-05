# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .virtual_service_traffic_route_rule_details import VirtualServiceTrafficRouteRuleDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TlsPassthroughVirtualServiceTrafficRouteRuleDetails(VirtualServiceTrafficRouteRuleDetails):
    """
    Rule for routing incoming Virtual Service traffic with TLS_PASSTHROUGH protocol
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TlsPassthroughVirtualServiceTrafficRouteRuleDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.service_mesh.models.TlsPassthroughVirtualServiceTrafficRouteRuleDetails.type` attribute
        of this class is ``TLS_PASSTHROUGH`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this TlsPassthroughVirtualServiceTrafficRouteRuleDetails.
            Allowed values for this property are: "HTTP", "TLS_PASSTHROUGH", "TCP"
        :type type: str

        :param destinations:
            The value to assign to the destinations property of this TlsPassthroughVirtualServiceTrafficRouteRuleDetails.
        :type destinations: list[oci.service_mesh.models.VirtualDeploymentTrafficRuleTargetDetails]

        """
        self.swagger_types = {
            'type': 'str',
            'destinations': 'list[VirtualDeploymentTrafficRuleTargetDetails]'
        }

        self.attribute_map = {
            'type': 'type',
            'destinations': 'destinations'
        }

        self._type = None
        self._destinations = None
        self._type = 'TLS_PASSTHROUGH'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
