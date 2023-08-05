# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyAuthenticationFactorInitiatorThirdPartyFactor(object):
    """
    User's third-party authentication factor details

    **SCIM++ Properties:**
    - caseExact: false
    - idcsSearchable: false
    - multiValued: false
    - mutability: readWrite
    - required: false
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MyAuthenticationFactorInitiatorThirdPartyFactor object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param third_party_vendor_name:
            The value to assign to the third_party_vendor_name property of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :type third_party_vendor_name: str

        :param third_party_factor_type:
            The value to assign to the third_party_factor_type property of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :type third_party_factor_type: str

        :param third_party_factor_id:
            The value to assign to the third_party_factor_id property of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :type third_party_factor_id: str

        """
        self.swagger_types = {
            'third_party_vendor_name': 'str',
            'third_party_factor_type': 'str',
            'third_party_factor_id': 'str'
        }

        self.attribute_map = {
            'third_party_vendor_name': 'thirdPartyVendorName',
            'third_party_factor_type': 'thirdPartyFactorType',
            'third_party_factor_id': 'thirdPartyFactorId'
        }

        self._third_party_vendor_name = None
        self._third_party_factor_type = None
        self._third_party_factor_id = None

    @property
    def third_party_vendor_name(self):
        """
        **[Required]** Gets the third_party_vendor_name of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        The vendor name of the third party factor

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The third_party_vendor_name of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :rtype: str
        """
        return self._third_party_vendor_name

    @third_party_vendor_name.setter
    def third_party_vendor_name(self, third_party_vendor_name):
        """
        Sets the third_party_vendor_name of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        The vendor name of the third party factor

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param third_party_vendor_name: The third_party_vendor_name of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :type: str
        """
        self._third_party_vendor_name = third_party_vendor_name

    @property
    def third_party_factor_type(self):
        """
        Gets the third_party_factor_type of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        Type of the third party authentication factor

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The third_party_factor_type of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :rtype: str
        """
        return self._third_party_factor_type

    @third_party_factor_type.setter
    def third_party_factor_type(self, third_party_factor_type):
        """
        Sets the third_party_factor_type of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        Type of the third party authentication factor

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param third_party_factor_type: The third_party_factor_type of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :type: str
        """
        self._third_party_factor_type = third_party_factor_type

    @property
    def third_party_factor_id(self):
        """
        Gets the third_party_factor_id of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        Reference to the third party resource

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The third_party_factor_id of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :rtype: str
        """
        return self._third_party_factor_id

    @third_party_factor_id.setter
    def third_party_factor_id(self, third_party_factor_id):
        """
        Sets the third_party_factor_id of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        Reference to the third party resource

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param third_party_factor_id: The third_party_factor_id of this MyAuthenticationFactorInitiatorThirdPartyFactor.
        :type: str
        """
        self._third_party_factor_id = third_party_factor_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
