# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RotateCloudAutonomousVmClusterOrdsCertsDetails(object):
    """
    The details for configuring the ORDS certificates on Cloud Autonomous VM Cluster
    """

    #: A constant which can be used with the certificate_generation_type property of a RotateCloudAutonomousVmClusterOrdsCertsDetails.
    #: This constant has a value of "SYSTEM"
    CERTIFICATE_GENERATION_TYPE_SYSTEM = "SYSTEM"

    #: A constant which can be used with the certificate_generation_type property of a RotateCloudAutonomousVmClusterOrdsCertsDetails.
    #: This constant has a value of "BYOC"
    CERTIFICATE_GENERATION_TYPE_BYOC = "BYOC"

    def __init__(self, **kwargs):
        """
        Initializes a new RotateCloudAutonomousVmClusterOrdsCertsDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param certificate_generation_type:
            The value to assign to the certificate_generation_type property of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
            Allowed values for this property are: "SYSTEM", "BYOC"
        :type certificate_generation_type: str

        :param certificate_id:
            The value to assign to the certificate_id property of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type certificate_id: str

        :param certificate_authority_id:
            The value to assign to the certificate_authority_id property of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type certificate_authority_id: str

        :param ca_bundle_id:
            The value to assign to the ca_bundle_id property of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type ca_bundle_id: str

        """
        self.swagger_types = {
            'certificate_generation_type': 'str',
            'certificate_id': 'str',
            'certificate_authority_id': 'str',
            'ca_bundle_id': 'str'
        }

        self.attribute_map = {
            'certificate_generation_type': 'certificateGenerationType',
            'certificate_id': 'certificateId',
            'certificate_authority_id': 'certificateAuthorityId',
            'ca_bundle_id': 'caBundleId'
        }

        self._certificate_generation_type = None
        self._certificate_id = None
        self._certificate_authority_id = None
        self._ca_bundle_id = None

    @property
    def certificate_generation_type(self):
        """
        **[Required]** Gets the certificate_generation_type of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        Specify SYSTEM to use Oracle-managed certificates. Specify BYOC when you want to bring your own certificate.

        Allowed values for this property are: "SYSTEM", "BYOC"


        :return: The certificate_generation_type of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :rtype: str
        """
        return self._certificate_generation_type

    @certificate_generation_type.setter
    def certificate_generation_type(self, certificate_generation_type):
        """
        Sets the certificate_generation_type of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        Specify SYSTEM to use Oracle-managed certificates. Specify BYOC when you want to bring your own certificate.


        :param certificate_generation_type: The certificate_generation_type of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type: str
        """
        allowed_values = ["SYSTEM", "BYOC"]
        if not value_allowed_none_or_none_sentinel(certificate_generation_type, allowed_values):
            raise ValueError(
                "Invalid value for `certificate_generation_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._certificate_generation_type = certificate_generation_type

    @property
    def certificate_id(self):
        """
        Gets the certificate_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        The `OCID`__ of the certificate to use.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The certificate_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :rtype: str
        """
        return self._certificate_id

    @certificate_id.setter
    def certificate_id(self, certificate_id):
        """
        Sets the certificate_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        The `OCID`__ of the certificate to use.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param certificate_id: The certificate_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type: str
        """
        self._certificate_id = certificate_id

    @property
    def certificate_authority_id(self):
        """
        Gets the certificate_authority_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        The `OCID`__ of the certificate authority.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The certificate_authority_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :rtype: str
        """
        return self._certificate_authority_id

    @certificate_authority_id.setter
    def certificate_authority_id(self, certificate_authority_id):
        """
        Sets the certificate_authority_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        The `OCID`__ of the certificate authority.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param certificate_authority_id: The certificate_authority_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type: str
        """
        self._certificate_authority_id = certificate_authority_id

    @property
    def ca_bundle_id(self):
        """
        Gets the ca_bundle_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        The `OCID`__ of the certificate bundle.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The ca_bundle_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :rtype: str
        """
        return self._ca_bundle_id

    @ca_bundle_id.setter
    def ca_bundle_id(self, ca_bundle_id):
        """
        Sets the ca_bundle_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        The `OCID`__ of the certificate bundle.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param ca_bundle_id: The ca_bundle_id of this RotateCloudAutonomousVmClusterOrdsCertsDetails.
        :type: str
        """
        self._ca_bundle_id = ca_bundle_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
