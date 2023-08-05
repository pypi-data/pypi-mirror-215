# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .verification_key_source import VerificationKeySource
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NoneVerificationKeySource(VerificationKeySource):
    """
    Allows user to opt out of Verification key source
    """

    def __init__(self, **kwargs):
        """
        Initializes a new NoneVerificationKeySource object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.NoneVerificationKeySource.verification_key_source_type` attribute
        of this class is ``NONE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param verification_key_source_type:
            The value to assign to the verification_key_source_type property of this NoneVerificationKeySource.
            Allowed values for this property are: "VAULT_SECRET", "INLINE_PUBLIC_KEY", "NONE"
        :type verification_key_source_type: str

        """
        self.swagger_types = {
            'verification_key_source_type': 'str'
        }

        self.attribute_map = {
            'verification_key_source_type': 'verificationKeySourceType'
        }

        self._verification_key_source_type = None
        self._verification_key_source_type = 'NONE'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
