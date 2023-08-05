# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ReplaceCertificateAuthorityResponse(object):
    """
    Information about the replace CA Bundle of the rover node.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ReplaceCertificateAuthorityResponse object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param rover_node_id:
            The value to assign to the rover_node_id property of this ReplaceCertificateAuthorityResponse.
        :type rover_node_id: str

        :param replace_ca_details:
            The value to assign to the replace_ca_details property of this ReplaceCertificateAuthorityResponse.
        :type replace_ca_details: oci.rover.models.ReplaceCaDetails

        """
        self.swagger_types = {
            'rover_node_id': 'str',
            'replace_ca_details': 'ReplaceCaDetails'
        }

        self.attribute_map = {
            'rover_node_id': 'roverNodeId',
            'replace_ca_details': 'replaceCaDetails'
        }

        self._rover_node_id = None
        self._replace_ca_details = None

    @property
    def rover_node_id(self):
        """
        **[Required]** Gets the rover_node_id of this ReplaceCertificateAuthorityResponse.
        rover node ocid


        :return: The rover_node_id of this ReplaceCertificateAuthorityResponse.
        :rtype: str
        """
        return self._rover_node_id

    @rover_node_id.setter
    def rover_node_id(self, rover_node_id):
        """
        Sets the rover_node_id of this ReplaceCertificateAuthorityResponse.
        rover node ocid


        :param rover_node_id: The rover_node_id of this ReplaceCertificateAuthorityResponse.
        :type: str
        """
        self._rover_node_id = rover_node_id

    @property
    def replace_ca_details(self):
        """
        Gets the replace_ca_details of this ReplaceCertificateAuthorityResponse.

        :return: The replace_ca_details of this ReplaceCertificateAuthorityResponse.
        :rtype: oci.rover.models.ReplaceCaDetails
        """
        return self._replace_ca_details

    @replace_ca_details.setter
    def replace_ca_details(self, replace_ca_details):
        """
        Sets the replace_ca_details of this ReplaceCertificateAuthorityResponse.

        :param replace_ca_details: The replace_ca_details of this ReplaceCertificateAuthorityResponse.
        :type: oci.rover.models.ReplaceCaDetails
        """
        self._replace_ca_details = replace_ca_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
