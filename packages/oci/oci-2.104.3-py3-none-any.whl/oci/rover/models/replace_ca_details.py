# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ReplaceCaDetails(object):
    """
    Information about the detailed CA bundle replacement of the rover node.
    """

    #: A constant which can be used with the cert_key_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "RSA2048"
    CERT_KEY_ALGORITHM_RSA2048 = "RSA2048"

    #: A constant which can be used with the cert_key_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "RSA4096"
    CERT_KEY_ALGORITHM_RSA4096 = "RSA4096"

    #: A constant which can be used with the cert_key_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "ECDSA_P256"
    CERT_KEY_ALGORITHM_ECDSA_P256 = "ECDSA_P256"

    #: A constant which can be used with the cert_key_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "ECDSA_P384"
    CERT_KEY_ALGORITHM_ECDSA_P384 = "ECDSA_P384"

    #: A constant which can be used with the cert_signature_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "SHA256_WITH_RSA"
    CERT_SIGNATURE_ALGORITHM_SHA256_WITH_RSA = "SHA256_WITH_RSA"

    #: A constant which can be used with the cert_signature_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "SHA384_WITH_RSA"
    CERT_SIGNATURE_ALGORITHM_SHA384_WITH_RSA = "SHA384_WITH_RSA"

    #: A constant which can be used with the cert_signature_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "SHA512_WITH_RSA"
    CERT_SIGNATURE_ALGORITHM_SHA512_WITH_RSA = "SHA512_WITH_RSA"

    #: A constant which can be used with the cert_signature_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "SHA256_WITH_ECDSA"
    CERT_SIGNATURE_ALGORITHM_SHA256_WITH_ECDSA = "SHA256_WITH_ECDSA"

    #: A constant which can be used with the cert_signature_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "SHA384_WITH_ECDSA"
    CERT_SIGNATURE_ALGORITHM_SHA384_WITH_ECDSA = "SHA384_WITH_ECDSA"

    #: A constant which can be used with the cert_signature_algorithm property of a ReplaceCaDetails.
    #: This constant has a value of "SHA512_WITH_ECDSA"
    CERT_SIGNATURE_ALGORITHM_SHA512_WITH_ECDSA = "SHA512_WITH_ECDSA"

    def __init__(self, **kwargs):
        """
        Initializes a new ReplaceCaDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param ca_bundle_pem:
            The value to assign to the ca_bundle_pem property of this ReplaceCaDetails.
        :type ca_bundle_pem: str

        :param certificate_max_validity_duration:
            The value to assign to the certificate_max_validity_duration property of this ReplaceCaDetails.
        :type certificate_max_validity_duration: str

        :param cert_key_algorithm:
            The value to assign to the cert_key_algorithm property of this ReplaceCaDetails.
            Allowed values for this property are: "RSA2048", "RSA4096", "ECDSA_P256", "ECDSA_P384", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type cert_key_algorithm: str

        :param cert_signature_algorithm:
            The value to assign to the cert_signature_algorithm property of this ReplaceCaDetails.
            Allowed values for this property are: "SHA256_WITH_RSA", "SHA384_WITH_RSA", "SHA512_WITH_RSA", "SHA256_WITH_ECDSA", "SHA384_WITH_ECDSA", "SHA512_WITH_ECDSA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type cert_signature_algorithm: str

        """
        self.swagger_types = {
            'ca_bundle_pem': 'str',
            'certificate_max_validity_duration': 'str',
            'cert_key_algorithm': 'str',
            'cert_signature_algorithm': 'str'
        }

        self.attribute_map = {
            'ca_bundle_pem': 'caBundlePem',
            'certificate_max_validity_duration': 'certificateMaxValidityDuration',
            'cert_key_algorithm': 'certKeyAlgorithm',
            'cert_signature_algorithm': 'certSignatureAlgorithm'
        }

        self._ca_bundle_pem = None
        self._certificate_max_validity_duration = None
        self._cert_key_algorithm = None
        self._cert_signature_algorithm = None

    @property
    def ca_bundle_pem(self):
        """
        Gets the ca_bundle_pem of this ReplaceCaDetails.
        Plain text certificate chain in PEM format for the subordinate CA associated with given roverNode.


        :return: The ca_bundle_pem of this ReplaceCaDetails.
        :rtype: str
        """
        return self._ca_bundle_pem

    @ca_bundle_pem.setter
    def ca_bundle_pem(self, ca_bundle_pem):
        """
        Sets the ca_bundle_pem of this ReplaceCaDetails.
        Plain text certificate chain in PEM format for the subordinate CA associated with given roverNode.


        :param ca_bundle_pem: The ca_bundle_pem of this ReplaceCaDetails.
        :type: str
        """
        self._ca_bundle_pem = ca_bundle_pem

    @property
    def certificate_max_validity_duration(self):
        """
        Gets the certificate_max_validity_duration of this ReplaceCaDetails.
        Max validity of leaf certificates issued by the CA associated with given node, in days, in ISO 8601 format, example \"P365D\".


        :return: The certificate_max_validity_duration of this ReplaceCaDetails.
        :rtype: str
        """
        return self._certificate_max_validity_duration

    @certificate_max_validity_duration.setter
    def certificate_max_validity_duration(self, certificate_max_validity_duration):
        """
        Sets the certificate_max_validity_duration of this ReplaceCaDetails.
        Max validity of leaf certificates issued by the CA associated with given node, in days, in ISO 8601 format, example \"P365D\".


        :param certificate_max_validity_duration: The certificate_max_validity_duration of this ReplaceCaDetails.
        :type: str
        """
        self._certificate_max_validity_duration = certificate_max_validity_duration

    @property
    def cert_key_algorithm(self):
        """
        Gets the cert_key_algorithm of this ReplaceCaDetails.
        key algorithm for issuing leaf certificate.

        Allowed values for this property are: "RSA2048", "RSA4096", "ECDSA_P256", "ECDSA_P384", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The cert_key_algorithm of this ReplaceCaDetails.
        :rtype: str
        """
        return self._cert_key_algorithm

    @cert_key_algorithm.setter
    def cert_key_algorithm(self, cert_key_algorithm):
        """
        Sets the cert_key_algorithm of this ReplaceCaDetails.
        key algorithm for issuing leaf certificate.


        :param cert_key_algorithm: The cert_key_algorithm of this ReplaceCaDetails.
        :type: str
        """
        allowed_values = ["RSA2048", "RSA4096", "ECDSA_P256", "ECDSA_P384"]
        if not value_allowed_none_or_none_sentinel(cert_key_algorithm, allowed_values):
            cert_key_algorithm = 'UNKNOWN_ENUM_VALUE'
        self._cert_key_algorithm = cert_key_algorithm

    @property
    def cert_signature_algorithm(self):
        """
        Gets the cert_signature_algorithm of this ReplaceCaDetails.
        signature algorithm for issuing leaf certificate.

        Allowed values for this property are: "SHA256_WITH_RSA", "SHA384_WITH_RSA", "SHA512_WITH_RSA", "SHA256_WITH_ECDSA", "SHA384_WITH_ECDSA", "SHA512_WITH_ECDSA", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The cert_signature_algorithm of this ReplaceCaDetails.
        :rtype: str
        """
        return self._cert_signature_algorithm

    @cert_signature_algorithm.setter
    def cert_signature_algorithm(self, cert_signature_algorithm):
        """
        Sets the cert_signature_algorithm of this ReplaceCaDetails.
        signature algorithm for issuing leaf certificate.


        :param cert_signature_algorithm: The cert_signature_algorithm of this ReplaceCaDetails.
        :type: str
        """
        allowed_values = ["SHA256_WITH_RSA", "SHA384_WITH_RSA", "SHA512_WITH_RSA", "SHA256_WITH_ECDSA", "SHA384_WITH_ECDSA", "SHA512_WITH_ECDSA"]
        if not value_allowed_none_or_none_sentinel(cert_signature_algorithm, allowed_values):
            cert_signature_algorithm = 'UNKNOWN_ENUM_VALUE'
        self._cert_signature_algorithm = cert_signature_algorithm

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
