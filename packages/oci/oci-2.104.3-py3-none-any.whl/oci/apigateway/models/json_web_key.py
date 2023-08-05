# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .static_public_key import StaticPublicKey
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class JsonWebKey(StaticPublicKey):
    """
    A JSON Web Key that represents the public key used for verifying the JWT signature.
    """

    #: A constant which can be used with the kty property of a JsonWebKey.
    #: This constant has a value of "RSA"
    KTY_RSA = "RSA"

    #: A constant which can be used with the use property of a JsonWebKey.
    #: This constant has a value of "sig"
    USE_SIG = "sig"

    #: A constant which can be used with the key_ops property of a JsonWebKey.
    #: This constant has a value of "verify"
    KEY_OPS_VERIFY = "verify"

    def __init__(self, **kwargs):
        """
        Initializes a new JsonWebKey object with values from keyword arguments. The default value of the :py:attr:`~oci.apigateway.models.JsonWebKey.format` attribute
        of this class is ``JSON_WEB_KEY`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kid:
            The value to assign to the kid property of this JsonWebKey.
        :type kid: str

        :param format:
            The value to assign to the format property of this JsonWebKey.
            Allowed values for this property are: "JSON_WEB_KEY", "PEM", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type format: str

        :param kty:
            The value to assign to the kty property of this JsonWebKey.
            Allowed values for this property are: "RSA", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type kty: str

        :param use:
            The value to assign to the use property of this JsonWebKey.
            Allowed values for this property are: "sig", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type use: str

        :param key_ops:
            The value to assign to the key_ops property of this JsonWebKey.
            Allowed values for items in this list are: "verify", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type key_ops: list[str]

        :param alg:
            The value to assign to the alg property of this JsonWebKey.
        :type alg: str

        :param n:
            The value to assign to the n property of this JsonWebKey.
        :type n: str

        :param e:
            The value to assign to the e property of this JsonWebKey.
        :type e: str

        """
        self.swagger_types = {
            'kid': 'str',
            'format': 'str',
            'kty': 'str',
            'use': 'str',
            'key_ops': 'list[str]',
            'alg': 'str',
            'n': 'str',
            'e': 'str'
        }

        self.attribute_map = {
            'kid': 'kid',
            'format': 'format',
            'kty': 'kty',
            'use': 'use',
            'key_ops': 'key_ops',
            'alg': 'alg',
            'n': 'n',
            'e': 'e'
        }

        self._kid = None
        self._format = None
        self._kty = None
        self._use = None
        self._key_ops = None
        self._alg = None
        self._n = None
        self._e = None
        self._format = 'JSON_WEB_KEY'

    @property
    def kty(self):
        """
        **[Required]** Gets the kty of this JsonWebKey.
        The key type.

        Allowed values for this property are: "RSA", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The kty of this JsonWebKey.
        :rtype: str
        """
        return self._kty

    @kty.setter
    def kty(self, kty):
        """
        Sets the kty of this JsonWebKey.
        The key type.


        :param kty: The kty of this JsonWebKey.
        :type: str
        """
        allowed_values = ["RSA"]
        if not value_allowed_none_or_none_sentinel(kty, allowed_values):
            kty = 'UNKNOWN_ENUM_VALUE'
        self._kty = kty

    @property
    def use(self):
        """
        Gets the use of this JsonWebKey.
        The intended use of the public key.

        Allowed values for this property are: "sig", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The use of this JsonWebKey.
        :rtype: str
        """
        return self._use

    @use.setter
    def use(self, use):
        """
        Sets the use of this JsonWebKey.
        The intended use of the public key.


        :param use: The use of this JsonWebKey.
        :type: str
        """
        allowed_values = ["sig"]
        if not value_allowed_none_or_none_sentinel(use, allowed_values):
            use = 'UNKNOWN_ENUM_VALUE'
        self._use = use

    @property
    def key_ops(self):
        """
        Gets the key_ops of this JsonWebKey.
        The operations for which this key is to be used.

        Allowed values for items in this list are: "verify", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The key_ops of this JsonWebKey.
        :rtype: list[str]
        """
        return self._key_ops

    @key_ops.setter
    def key_ops(self, key_ops):
        """
        Sets the key_ops of this JsonWebKey.
        The operations for which this key is to be used.


        :param key_ops: The key_ops of this JsonWebKey.
        :type: list[str]
        """
        allowed_values = ["verify"]
        if key_ops:
            key_ops[:] = ['UNKNOWN_ENUM_VALUE' if not value_allowed_none_or_none_sentinel(x, allowed_values) else x for x in key_ops]
        self._key_ops = key_ops

    @property
    def alg(self):
        """
        **[Required]** Gets the alg of this JsonWebKey.
        The algorithm intended for use with this key.


        :return: The alg of this JsonWebKey.
        :rtype: str
        """
        return self._alg

    @alg.setter
    def alg(self, alg):
        """
        Sets the alg of this JsonWebKey.
        The algorithm intended for use with this key.


        :param alg: The alg of this JsonWebKey.
        :type: str
        """
        self._alg = alg

    @property
    def n(self):
        """
        **[Required]** Gets the n of this JsonWebKey.
        The base64 url encoded modulus of the RSA public key represented
        by this key.


        :return: The n of this JsonWebKey.
        :rtype: str
        """
        return self._n

    @n.setter
    def n(self, n):
        """
        Sets the n of this JsonWebKey.
        The base64 url encoded modulus of the RSA public key represented
        by this key.


        :param n: The n of this JsonWebKey.
        :type: str
        """
        self._n = n

    @property
    def e(self):
        """
        **[Required]** Gets the e of this JsonWebKey.
        The base64 url encoded exponent of the RSA public key represented
        by this key.


        :return: The e of this JsonWebKey.
        :rtype: str
        """
        return self._e

    @e.setter
    def e(self, e):
        """
        Sets the e of this JsonWebKey.
        The base64 url encoded exponent of the RSA public key represented
        by this key.


        :param e: The e of this JsonWebKey.
        :type: str
        """
        self._e = e

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
