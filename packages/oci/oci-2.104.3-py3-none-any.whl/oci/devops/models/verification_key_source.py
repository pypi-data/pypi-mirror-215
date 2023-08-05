# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VerificationKeySource(object):
    """
    The source of the verification material.
    """

    #: A constant which can be used with the verification_key_source_type property of a VerificationKeySource.
    #: This constant has a value of "VAULT_SECRET"
    VERIFICATION_KEY_SOURCE_TYPE_VAULT_SECRET = "VAULT_SECRET"

    #: A constant which can be used with the verification_key_source_type property of a VerificationKeySource.
    #: This constant has a value of "INLINE_PUBLIC_KEY"
    VERIFICATION_KEY_SOURCE_TYPE_INLINE_PUBLIC_KEY = "INLINE_PUBLIC_KEY"

    #: A constant which can be used with the verification_key_source_type property of a VerificationKeySource.
    #: This constant has a value of "NONE"
    VERIFICATION_KEY_SOURCE_TYPE_NONE = "NONE"

    def __init__(self, **kwargs):
        """
        Initializes a new VerificationKeySource object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.devops.models.InlinePublicKeyVerificationKeySource`
        * :class:`~oci.devops.models.VaultSecretVerificationKeySource`
        * :class:`~oci.devops.models.NoneVerificationKeySource`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param verification_key_source_type:
            The value to assign to the verification_key_source_type property of this VerificationKeySource.
            Allowed values for this property are: "VAULT_SECRET", "INLINE_PUBLIC_KEY", "NONE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type verification_key_source_type: str

        """
        self.swagger_types = {
            'verification_key_source_type': 'str'
        }

        self.attribute_map = {
            'verification_key_source_type': 'verificationKeySourceType'
        }

        self._verification_key_source_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['verificationKeySourceType']

        if type == 'INLINE_PUBLIC_KEY':
            return 'InlinePublicKeyVerificationKeySource'

        if type == 'VAULT_SECRET':
            return 'VaultSecretVerificationKeySource'

        if type == 'NONE':
            return 'NoneVerificationKeySource'
        else:
            return 'VerificationKeySource'

    @property
    def verification_key_source_type(self):
        """
        **[Required]** Gets the verification_key_source_type of this VerificationKeySource.
        Specifies type of verification material.

        Allowed values for this property are: "VAULT_SECRET", "INLINE_PUBLIC_KEY", "NONE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The verification_key_source_type of this VerificationKeySource.
        :rtype: str
        """
        return self._verification_key_source_type

    @verification_key_source_type.setter
    def verification_key_source_type(self, verification_key_source_type):
        """
        Sets the verification_key_source_type of this VerificationKeySource.
        Specifies type of verification material.


        :param verification_key_source_type: The verification_key_source_type of this VerificationKeySource.
        :type: str
        """
        allowed_values = ["VAULT_SECRET", "INLINE_PUBLIC_KEY", "NONE"]
        if not value_allowed_none_or_none_sentinel(verification_key_source_type, allowed_values):
            verification_key_source_type = 'UNKNOWN_ENUM_VALUE'
        self._verification_key_source_type = verification_key_source_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
