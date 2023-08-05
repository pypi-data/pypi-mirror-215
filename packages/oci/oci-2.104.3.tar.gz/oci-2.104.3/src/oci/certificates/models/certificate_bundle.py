# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CertificateBundle(object):
    """
    The contents of the certificate, properties of the certificate (and certificate version), and user-provided contextual metadata for the certificate.
    """

    #: A constant which can be used with the certificate_bundle_type property of a CertificateBundle.
    #: This constant has a value of "CERTIFICATE_CONTENT_PUBLIC_ONLY"
    CERTIFICATE_BUNDLE_TYPE_CERTIFICATE_CONTENT_PUBLIC_ONLY = "CERTIFICATE_CONTENT_PUBLIC_ONLY"

    #: A constant which can be used with the certificate_bundle_type property of a CertificateBundle.
    #: This constant has a value of "CERTIFICATE_CONTENT_WITH_PRIVATE_KEY"
    CERTIFICATE_BUNDLE_TYPE_CERTIFICATE_CONTENT_WITH_PRIVATE_KEY = "CERTIFICATE_CONTENT_WITH_PRIVATE_KEY"

    #: A constant which can be used with the stages property of a CertificateBundle.
    #: This constant has a value of "CURRENT"
    STAGES_CURRENT = "CURRENT"

    #: A constant which can be used with the stages property of a CertificateBundle.
    #: This constant has a value of "PENDING"
    STAGES_PENDING = "PENDING"

    #: A constant which can be used with the stages property of a CertificateBundle.
    #: This constant has a value of "LATEST"
    STAGES_LATEST = "LATEST"

    #: A constant which can be used with the stages property of a CertificateBundle.
    #: This constant has a value of "PREVIOUS"
    STAGES_PREVIOUS = "PREVIOUS"

    #: A constant which can be used with the stages property of a CertificateBundle.
    #: This constant has a value of "DEPRECATED"
    STAGES_DEPRECATED = "DEPRECATED"

    #: A constant which can be used with the stages property of a CertificateBundle.
    #: This constant has a value of "FAILED"
    STAGES_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new CertificateBundle object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.certificates.models.CertificateBundlePublicOnly`
        * :class:`~oci.certificates.models.CertificateBundleWithPrivateKey`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param certificate_bundle_type:
            The value to assign to the certificate_bundle_type property of this CertificateBundle.
            Allowed values for this property are: "CERTIFICATE_CONTENT_PUBLIC_ONLY", "CERTIFICATE_CONTENT_WITH_PRIVATE_KEY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type certificate_bundle_type: str

        :param certificate_id:
            The value to assign to the certificate_id property of this CertificateBundle.
        :type certificate_id: str

        :param certificate_name:
            The value to assign to the certificate_name property of this CertificateBundle.
        :type certificate_name: str

        :param version_number:
            The value to assign to the version_number property of this CertificateBundle.
        :type version_number: int

        :param serial_number:
            The value to assign to the serial_number property of this CertificateBundle.
        :type serial_number: str

        :param certificate_pem:
            The value to assign to the certificate_pem property of this CertificateBundle.
        :type certificate_pem: str

        :param cert_chain_pem:
            The value to assign to the cert_chain_pem property of this CertificateBundle.
        :type cert_chain_pem: str

        :param time_created:
            The value to assign to the time_created property of this CertificateBundle.
        :type time_created: datetime

        :param validity:
            The value to assign to the validity property of this CertificateBundle.
        :type validity: oci.certificates.models.Validity

        :param version_name:
            The value to assign to the version_name property of this CertificateBundle.
        :type version_name: str

        :param stages:
            The value to assign to the stages property of this CertificateBundle.
            Allowed values for items in this list are: "CURRENT", "PENDING", "LATEST", "PREVIOUS", "DEPRECATED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type stages: list[str]

        :param revocation_status:
            The value to assign to the revocation_status property of this CertificateBundle.
        :type revocation_status: oci.certificates.models.RevocationStatus

        """
        self.swagger_types = {
            'certificate_bundle_type': 'str',
            'certificate_id': 'str',
            'certificate_name': 'str',
            'version_number': 'int',
            'serial_number': 'str',
            'certificate_pem': 'str',
            'cert_chain_pem': 'str',
            'time_created': 'datetime',
            'validity': 'Validity',
            'version_name': 'str',
            'stages': 'list[str]',
            'revocation_status': 'RevocationStatus'
        }

        self.attribute_map = {
            'certificate_bundle_type': 'certificateBundleType',
            'certificate_id': 'certificateId',
            'certificate_name': 'certificateName',
            'version_number': 'versionNumber',
            'serial_number': 'serialNumber',
            'certificate_pem': 'certificatePem',
            'cert_chain_pem': 'certChainPem',
            'time_created': 'timeCreated',
            'validity': 'validity',
            'version_name': 'versionName',
            'stages': 'stages',
            'revocation_status': 'revocationStatus'
        }

        self._certificate_bundle_type = None
        self._certificate_id = None
        self._certificate_name = None
        self._version_number = None
        self._serial_number = None
        self._certificate_pem = None
        self._cert_chain_pem = None
        self._time_created = None
        self._validity = None
        self._version_name = None
        self._stages = None
        self._revocation_status = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['certificateBundleType']

        if type == 'CERTIFICATE_CONTENT_PUBLIC_ONLY':
            return 'CertificateBundlePublicOnly'

        if type == 'CERTIFICATE_CONTENT_WITH_PRIVATE_KEY':
            return 'CertificateBundleWithPrivateKey'
        else:
            return 'CertificateBundle'

    @property
    def certificate_bundle_type(self):
        """
        **[Required]** Gets the certificate_bundle_type of this CertificateBundle.
        The type of certificate bundle, which indicates whether the private key fields are included.

        Allowed values for this property are: "CERTIFICATE_CONTENT_PUBLIC_ONLY", "CERTIFICATE_CONTENT_WITH_PRIVATE_KEY", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The certificate_bundle_type of this CertificateBundle.
        :rtype: str
        """
        return self._certificate_bundle_type

    @certificate_bundle_type.setter
    def certificate_bundle_type(self, certificate_bundle_type):
        """
        Sets the certificate_bundle_type of this CertificateBundle.
        The type of certificate bundle, which indicates whether the private key fields are included.


        :param certificate_bundle_type: The certificate_bundle_type of this CertificateBundle.
        :type: str
        """
        allowed_values = ["CERTIFICATE_CONTENT_PUBLIC_ONLY", "CERTIFICATE_CONTENT_WITH_PRIVATE_KEY"]
        if not value_allowed_none_or_none_sentinel(certificate_bundle_type, allowed_values):
            certificate_bundle_type = 'UNKNOWN_ENUM_VALUE'
        self._certificate_bundle_type = certificate_bundle_type

    @property
    def certificate_id(self):
        """
        **[Required]** Gets the certificate_id of this CertificateBundle.
        The OCID of the certificate.


        :return: The certificate_id of this CertificateBundle.
        :rtype: str
        """
        return self._certificate_id

    @certificate_id.setter
    def certificate_id(self, certificate_id):
        """
        Sets the certificate_id of this CertificateBundle.
        The OCID of the certificate.


        :param certificate_id: The certificate_id of this CertificateBundle.
        :type: str
        """
        self._certificate_id = certificate_id

    @property
    def certificate_name(self):
        """
        **[Required]** Gets the certificate_name of this CertificateBundle.
        The name of the certificate.


        :return: The certificate_name of this CertificateBundle.
        :rtype: str
        """
        return self._certificate_name

    @certificate_name.setter
    def certificate_name(self, certificate_name):
        """
        Sets the certificate_name of this CertificateBundle.
        The name of the certificate.


        :param certificate_name: The certificate_name of this CertificateBundle.
        :type: str
        """
        self._certificate_name = certificate_name

    @property
    def version_number(self):
        """
        **[Required]** Gets the version_number of this CertificateBundle.
        The version number of the certificate.


        :return: The version_number of this CertificateBundle.
        :rtype: int
        """
        return self._version_number

    @version_number.setter
    def version_number(self, version_number):
        """
        Sets the version_number of this CertificateBundle.
        The version number of the certificate.


        :param version_number: The version_number of this CertificateBundle.
        :type: int
        """
        self._version_number = version_number

    @property
    def serial_number(self):
        """
        **[Required]** Gets the serial_number of this CertificateBundle.
        A unique certificate identifier used in certificate revocation tracking, formatted as octets.
        Example: `03 AC FC FA CC B3 CB 02 B8 F8 DE F5 85 E7 7B FF`


        :return: The serial_number of this CertificateBundle.
        :rtype: str
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        """
        Sets the serial_number of this CertificateBundle.
        A unique certificate identifier used in certificate revocation tracking, formatted as octets.
        Example: `03 AC FC FA CC B3 CB 02 B8 F8 DE F5 85 E7 7B FF`


        :param serial_number: The serial_number of this CertificateBundle.
        :type: str
        """
        self._serial_number = serial_number

    @property
    def certificate_pem(self):
        """
        Gets the certificate_pem of this CertificateBundle.
        The certificate in PEM format.


        :return: The certificate_pem of this CertificateBundle.
        :rtype: str
        """
        return self._certificate_pem

    @certificate_pem.setter
    def certificate_pem(self, certificate_pem):
        """
        Sets the certificate_pem of this CertificateBundle.
        The certificate in PEM format.


        :param certificate_pem: The certificate_pem of this CertificateBundle.
        :type: str
        """
        self._certificate_pem = certificate_pem

    @property
    def cert_chain_pem(self):
        """
        Gets the cert_chain_pem of this CertificateBundle.
        The certificate chain (in PEM format) for the certificate bundle.


        :return: The cert_chain_pem of this CertificateBundle.
        :rtype: str
        """
        return self._cert_chain_pem

    @cert_chain_pem.setter
    def cert_chain_pem(self, cert_chain_pem):
        """
        Sets the cert_chain_pem of this CertificateBundle.
        The certificate chain (in PEM format) for the certificate bundle.


        :param cert_chain_pem: The cert_chain_pem of this CertificateBundle.
        :type: str
        """
        self._cert_chain_pem = cert_chain_pem

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this CertificateBundle.
        An optional property indicating when the certificate version was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this CertificateBundle.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this CertificateBundle.
        An optional property indicating when the certificate version was created, expressed in `RFC 3339`__ timestamp format.
        Example: `2019-04-03T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this CertificateBundle.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def validity(self):
        """
        **[Required]** Gets the validity of this CertificateBundle.

        :return: The validity of this CertificateBundle.
        :rtype: oci.certificates.models.Validity
        """
        return self._validity

    @validity.setter
    def validity(self, validity):
        """
        Sets the validity of this CertificateBundle.

        :param validity: The validity of this CertificateBundle.
        :type: oci.certificates.models.Validity
        """
        self._validity = validity

    @property
    def version_name(self):
        """
        Gets the version_name of this CertificateBundle.
        The name of the certificate version.


        :return: The version_name of this CertificateBundle.
        :rtype: str
        """
        return self._version_name

    @version_name.setter
    def version_name(self, version_name):
        """
        Sets the version_name of this CertificateBundle.
        The name of the certificate version.


        :param version_name: The version_name of this CertificateBundle.
        :type: str
        """
        self._version_name = version_name

    @property
    def stages(self):
        """
        **[Required]** Gets the stages of this CertificateBundle.
        A list of rotation states for the certificate bundle.

        Allowed values for items in this list are: "CURRENT", "PENDING", "LATEST", "PREVIOUS", "DEPRECATED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The stages of this CertificateBundle.
        :rtype: list[str]
        """
        return self._stages

    @stages.setter
    def stages(self, stages):
        """
        Sets the stages of this CertificateBundle.
        A list of rotation states for the certificate bundle.


        :param stages: The stages of this CertificateBundle.
        :type: list[str]
        """
        allowed_values = ["CURRENT", "PENDING", "LATEST", "PREVIOUS", "DEPRECATED", "FAILED"]
        if stages:
            stages[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in stages]
        self._stages = stages

    @property
    def revocation_status(self):
        """
        Gets the revocation_status of this CertificateBundle.

        :return: The revocation_status of this CertificateBundle.
        :rtype: oci.certificates.models.RevocationStatus
        """
        return self._revocation_status

    @revocation_status.setter
    def revocation_status(self, revocation_status):
        """
        Sets the revocation_status of this CertificateBundle.

        :param revocation_status: The revocation_status of this CertificateBundle.
        :type: oci.certificates.models.RevocationStatus
        """
        self._revocation_status = revocation_status

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
