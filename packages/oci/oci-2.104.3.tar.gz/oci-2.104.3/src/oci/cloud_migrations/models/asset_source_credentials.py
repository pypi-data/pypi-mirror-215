# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AssetSourceCredentials(object):
    """
    Credentials for an asset source.
    """

    #: A constant which can be used with the type property of a AssetSourceCredentials.
    #: This constant has a value of "BASIC"
    TYPE_BASIC = "BASIC"

    def __init__(self, **kwargs):
        """
        Initializes a new AssetSourceCredentials object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this AssetSourceCredentials.
            Allowed values for this property are: "BASIC"
        :type type: str

        :param secret_id:
            The value to assign to the secret_id property of this AssetSourceCredentials.
        :type secret_id: str

        """
        self.swagger_types = {
            'type': 'str',
            'secret_id': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'secret_id': 'secretId'
        }

        self._type = None
        self._secret_id = None

    @property
    def type(self):
        """
        **[Required]** Gets the type of this AssetSourceCredentials.
        Authentication type

        Allowed values for this property are: "BASIC"


        :return: The type of this AssetSourceCredentials.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AssetSourceCredentials.
        Authentication type


        :param type: The type of this AssetSourceCredentials.
        :type: str
        """
        allowed_values = ["BASIC"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            raise ValueError(
                "Invalid value for `type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._type = type

    @property
    def secret_id(self):
        """
        **[Required]** Gets the secret_id of this AssetSourceCredentials.
        The `OCID`__ of the secret in a vault.
        If the the type of the credentials is BASIC`, the secret must contain the username and
        password in JSON format, which is in the form of `{ \"username\": \"<VMwareUser>\", \"password\": \"<VMwarePassword>\" }`.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The secret_id of this AssetSourceCredentials.
        :rtype: str
        """
        return self._secret_id

    @secret_id.setter
    def secret_id(self, secret_id):
        """
        Sets the secret_id of this AssetSourceCredentials.
        The `OCID`__ of the secret in a vault.
        If the the type of the credentials is BASIC`, the secret must contain the username and
        password in JSON format, which is in the form of `{ \"username\": \"<VMwareUser>\", \"password\": \"<VMwarePassword>\" }`.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param secret_id: The secret_id of this AssetSourceCredentials.
        :type: str
        """
        self._secret_id = secret_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
