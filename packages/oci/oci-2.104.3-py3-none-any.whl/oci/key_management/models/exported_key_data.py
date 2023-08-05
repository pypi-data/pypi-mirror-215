# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExportedKeyData(object):
    """
    The response to a request to export key material.
    """

    #: A constant which can be used with the algorithm property of a ExportedKeyData.
    #: This constant has a value of "RSA_OAEP_AES_SHA256"
    ALGORITHM_RSA_OAEP_AES_SHA256 = "RSA_OAEP_AES_SHA256"

    #: A constant which can be used with the algorithm property of a ExportedKeyData.
    #: This constant has a value of "RSA_OAEP_SHA256"
    ALGORITHM_RSA_OAEP_SHA256 = "RSA_OAEP_SHA256"

    def __init__(self, **kwargs):
        """
        Initializes a new ExportedKeyData object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key_version_id:
            The value to assign to the key_version_id property of this ExportedKeyData.
        :type key_version_id: str

        :param key_id:
            The value to assign to the key_id property of this ExportedKeyData.
        :type key_id: str

        :param time_created:
            The value to assign to the time_created property of this ExportedKeyData.
        :type time_created: datetime

        :param vault_id:
            The value to assign to the vault_id property of this ExportedKeyData.
        :type vault_id: str

        :param encrypted_key:
            The value to assign to the encrypted_key property of this ExportedKeyData.
        :type encrypted_key: str

        :param algorithm:
            The value to assign to the algorithm property of this ExportedKeyData.
            Allowed values for this property are: "RSA_OAEP_AES_SHA256", "RSA_OAEP_SHA256", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type algorithm: str

        """
        self.swagger_types = {
            'key_version_id': 'str',
            'key_id': 'str',
            'time_created': 'datetime',
            'vault_id': 'str',
            'encrypted_key': 'str',
            'algorithm': 'str'
        }

        self.attribute_map = {
            'key_version_id': 'keyVersionId',
            'key_id': 'keyId',
            'time_created': 'timeCreated',
            'vault_id': 'vaultId',
            'encrypted_key': 'encryptedKey',
            'algorithm': 'algorithm'
        }

        self._key_version_id = None
        self._key_id = None
        self._time_created = None
        self._vault_id = None
        self._encrypted_key = None
        self._algorithm = None

    @property
    def key_version_id(self):
        """
        **[Required]** Gets the key_version_id of this ExportedKeyData.
        The OCID of the key version.


        :return: The key_version_id of this ExportedKeyData.
        :rtype: str
        """
        return self._key_version_id

    @key_version_id.setter
    def key_version_id(self, key_version_id):
        """
        Sets the key_version_id of this ExportedKeyData.
        The OCID of the key version.


        :param key_version_id: The key_version_id of this ExportedKeyData.
        :type: str
        """
        self._key_version_id = key_version_id

    @property
    def key_id(self):
        """
        **[Required]** Gets the key_id of this ExportedKeyData.
        The OCID of the master encryption key associated with this key version.


        :return: The key_id of this ExportedKeyData.
        :rtype: str
        """
        return self._key_id

    @key_id.setter
    def key_id(self, key_id):
        """
        Sets the key_id of this ExportedKeyData.
        The OCID of the master encryption key associated with this key version.


        :param key_id: The key_id of this ExportedKeyData.
        :type: str
        """
        self._key_id = key_id

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ExportedKeyData.
        The date and time this key version was created, expressed in `RFC 3339`__ timestamp format.

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this ExportedKeyData.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExportedKeyData.
        The date and time this key version was created, expressed in `RFC 3339`__ timestamp format.

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this ExportedKeyData.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def vault_id(self):
        """
        **[Required]** Gets the vault_id of this ExportedKeyData.
        The OCID of the vault that contains this key version.


        :return: The vault_id of this ExportedKeyData.
        :rtype: str
        """
        return self._vault_id

    @vault_id.setter
    def vault_id(self, vault_id):
        """
        Sets the vault_id of this ExportedKeyData.
        The OCID of the vault that contains this key version.


        :param vault_id: The vault_id of this ExportedKeyData.
        :type: str
        """
        self._vault_id = vault_id

    @property
    def encrypted_key(self):
        """
        **[Required]** Gets the encrypted_key of this ExportedKeyData.
        The base64-encoded exported key material, which is encrypted by using the public RSA wrapping key specified in the export request.


        :return: The encrypted_key of this ExportedKeyData.
        :rtype: str
        """
        return self._encrypted_key

    @encrypted_key.setter
    def encrypted_key(self, encrypted_key):
        """
        Sets the encrypted_key of this ExportedKeyData.
        The base64-encoded exported key material, which is encrypted by using the public RSA wrapping key specified in the export request.


        :param encrypted_key: The encrypted_key of this ExportedKeyData.
        :type: str
        """
        self._encrypted_key = encrypted_key

    @property
    def algorithm(self):
        """
        **[Required]** Gets the algorithm of this ExportedKeyData.
        The encryption algorithm to use to encrypt exportable key material from a key that persists on the server (as opposed to a key that
        persists on a hardware security module and, therefore, cannot be exported). Specifying RSA_OAEP_AES_SHA256 invokes the RSA AES key
        wrap mechanism, which generates a temporary AES key. The temporary AES key is wrapped by the RSA public wrapping key provided along
        with the request, creating a wrapped temporary AES key. The temporary AES key is also used to wrap the exportable key material. The
        wrapped temporary AES key and the wrapped exportable key material are concatenated, producing concatenated blob output that jointly
        represents them. Specifying RSA_OAEP_SHA256 means that the exportable key material is wrapped by the RSA public wrapping key provided
        along with the request.

        Allowed values for this property are: "RSA_OAEP_AES_SHA256", "RSA_OAEP_SHA256", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The algorithm of this ExportedKeyData.
        :rtype: str
        """
        return self._algorithm

    @algorithm.setter
    def algorithm(self, algorithm):
        """
        Sets the algorithm of this ExportedKeyData.
        The encryption algorithm to use to encrypt exportable key material from a key that persists on the server (as opposed to a key that
        persists on a hardware security module and, therefore, cannot be exported). Specifying RSA_OAEP_AES_SHA256 invokes the RSA AES key
        wrap mechanism, which generates a temporary AES key. The temporary AES key is wrapped by the RSA public wrapping key provided along
        with the request, creating a wrapped temporary AES key. The temporary AES key is also used to wrap the exportable key material. The
        wrapped temporary AES key and the wrapped exportable key material are concatenated, producing concatenated blob output that jointly
        represents them. Specifying RSA_OAEP_SHA256 means that the exportable key material is wrapped by the RSA public wrapping key provided
        along with the request.


        :param algorithm: The algorithm of this ExportedKeyData.
        :type: str
        """
        allowed_values = ["RSA_OAEP_AES_SHA256", "RSA_OAEP_SHA256"]
        if not value_allowed_none_or_none_sentinel(algorithm, allowed_values):
            algorithm = 'UNKNOWN_ENUM_VALUE'
        self._algorithm = algorithm

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
