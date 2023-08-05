# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CertificateSubjectName(object):
    """
    The entity to be secured by the certificate.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CertificateSubjectName object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param country:
            The value to assign to the country property of this CertificateSubjectName.
        :type country: str

        :param state_province:
            The value to assign to the state_province property of this CertificateSubjectName.
        :type state_province: str

        :param locality:
            The value to assign to the locality property of this CertificateSubjectName.
        :type locality: str

        :param organization:
            The value to assign to the organization property of this CertificateSubjectName.
        :type organization: str

        :param organizational_unit:
            The value to assign to the organizational_unit property of this CertificateSubjectName.
        :type organizational_unit: str

        :param common_name:
            The value to assign to the common_name property of this CertificateSubjectName.
        :type common_name: str

        :param email_address:
            The value to assign to the email_address property of this CertificateSubjectName.
        :type email_address: str

        """
        self.swagger_types = {
            'country': 'str',
            'state_province': 'str',
            'locality': 'str',
            'organization': 'str',
            'organizational_unit': 'str',
            'common_name': 'str',
            'email_address': 'str'
        }

        self.attribute_map = {
            'country': 'country',
            'state_province': 'stateProvince',
            'locality': 'locality',
            'organization': 'organization',
            'organizational_unit': 'organizationalUnit',
            'common_name': 'commonName',
            'email_address': 'emailAddress'
        }

        self._country = None
        self._state_province = None
        self._locality = None
        self._organization = None
        self._organizational_unit = None
        self._common_name = None
        self._email_address = None

    @property
    def country(self):
        """
        Gets the country of this CertificateSubjectName.
        ISO 3166-1 alpha-2 code of the country where the organization is located. For a list of codes, see `ISO's website`__.

        __ https://www.iso.org/obp/ui/#search/code/


        :return: The country of this CertificateSubjectName.
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """
        Sets the country of this CertificateSubjectName.
        ISO 3166-1 alpha-2 code of the country where the organization is located. For a list of codes, see `ISO's website`__.

        __ https://www.iso.org/obp/ui/#search/code/


        :param country: The country of this CertificateSubjectName.
        :type: str
        """
        self._country = country

    @property
    def state_province(self):
        """
        Gets the state_province of this CertificateSubjectName.
        The province where the organization is located.


        :return: The state_province of this CertificateSubjectName.
        :rtype: str
        """
        return self._state_province

    @state_province.setter
    def state_province(self, state_province):
        """
        Sets the state_province of this CertificateSubjectName.
        The province where the organization is located.


        :param state_province: The state_province of this CertificateSubjectName.
        :type: str
        """
        self._state_province = state_province

    @property
    def locality(self):
        """
        Gets the locality of this CertificateSubjectName.
        The city in which the organization is located.


        :return: The locality of this CertificateSubjectName.
        :rtype: str
        """
        return self._locality

    @locality.setter
    def locality(self, locality):
        """
        Sets the locality of this CertificateSubjectName.
        The city in which the organization is located.


        :param locality: The locality of this CertificateSubjectName.
        :type: str
        """
        self._locality = locality

    @property
    def organization(self):
        """
        Gets the organization of this CertificateSubjectName.
        The organization name.


        :return: The organization of this CertificateSubjectName.
        :rtype: str
        """
        return self._organization

    @organization.setter
    def organization(self, organization):
        """
        Sets the organization of this CertificateSubjectName.
        The organization name.


        :param organization: The organization of this CertificateSubjectName.
        :type: str
        """
        self._organization = organization

    @property
    def organizational_unit(self):
        """
        Gets the organizational_unit of this CertificateSubjectName.
        The field to differentiate between divisions within an organization.


        :return: The organizational_unit of this CertificateSubjectName.
        :rtype: str
        """
        return self._organizational_unit

    @organizational_unit.setter
    def organizational_unit(self, organizational_unit):
        """
        Sets the organizational_unit of this CertificateSubjectName.
        The field to differentiate between divisions within an organization.


        :param organizational_unit: The organizational_unit of this CertificateSubjectName.
        :type: str
        """
        self._organizational_unit = organizational_unit

    @property
    def common_name(self):
        """
        Gets the common_name of this CertificateSubjectName.
        The fully qualified domain name used for DNS lookups of the server.


        :return: The common_name of this CertificateSubjectName.
        :rtype: str
        """
        return self._common_name

    @common_name.setter
    def common_name(self, common_name):
        """
        Sets the common_name of this CertificateSubjectName.
        The fully qualified domain name used for DNS lookups of the server.


        :param common_name: The common_name of this CertificateSubjectName.
        :type: str
        """
        self._common_name = common_name

    @property
    def email_address(self):
        """
        Gets the email_address of this CertificateSubjectName.
        The email address of the server's administrator.


        :return: The email_address of this CertificateSubjectName.
        :rtype: str
        """
        return self._email_address

    @email_address.setter
    def email_address(self, email_address):
        """
        Sets the email_address of this CertificateSubjectName.
        The email address of the server's administrator.


        :param email_address: The email_address of this CertificateSubjectName.
        :type: str
        """
        self._email_address = email_address

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
