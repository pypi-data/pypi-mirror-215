# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RenewCertificateResponse(object):
    """
    The information of renewed rover node certificate.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RenewCertificateResponse object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param rover_node_id:
            The value to assign to the rover_node_id property of this RenewCertificateResponse.
        :type rover_node_id: str

        :param certificate_details:
            The value to assign to the certificate_details property of this RenewCertificateResponse.
        :type certificate_details: oci.rover.models.CertificateDetails

        """
        self.swagger_types = {
            'rover_node_id': 'str',
            'certificate_details': 'CertificateDetails'
        }

        self.attribute_map = {
            'rover_node_id': 'roverNodeId',
            'certificate_details': 'certificateDetails'
        }

        self._rover_node_id = None
        self._certificate_details = None

    @property
    def rover_node_id(self):
        """
        **[Required]** Gets the rover_node_id of this RenewCertificateResponse.
        The id of the rover node.


        :return: The rover_node_id of this RenewCertificateResponse.
        :rtype: str
        """
        return self._rover_node_id

    @rover_node_id.setter
    def rover_node_id(self, rover_node_id):
        """
        Sets the rover_node_id of this RenewCertificateResponse.
        The id of the rover node.


        :param rover_node_id: The rover_node_id of this RenewCertificateResponse.
        :type: str
        """
        self._rover_node_id = rover_node_id

    @property
    def certificate_details(self):
        """
        Gets the certificate_details of this RenewCertificateResponse.

        :return: The certificate_details of this RenewCertificateResponse.
        :rtype: oci.rover.models.CertificateDetails
        """
        return self._certificate_details

    @certificate_details.setter
    def certificate_details(self, certificate_details):
        """
        Sets the certificate_details of this RenewCertificateResponse.

        :param certificate_details: The certificate_details of this RenewCertificateResponse.
        :type: oci.rover.models.CertificateDetails
        """
        self._certificate_details = certificate_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
