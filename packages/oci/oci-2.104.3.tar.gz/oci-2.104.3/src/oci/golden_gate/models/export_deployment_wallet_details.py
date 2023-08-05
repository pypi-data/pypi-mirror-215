# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExportDeploymentWalletDetails(object):
    """
    Metadata required to export wallet from deployment
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExportDeploymentWalletDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param vault_id:
            The value to assign to the vault_id property of this ExportDeploymentWalletDetails.
        :type vault_id: str

        :param master_encryption_key_id:
            The value to assign to the master_encryption_key_id property of this ExportDeploymentWalletDetails.
        :type master_encryption_key_id: str

        :param secret_name:
            The value to assign to the secret_name property of this ExportDeploymentWalletDetails.
        :type secret_name: str

        :param description:
            The value to assign to the description property of this ExportDeploymentWalletDetails.
        :type description: str

        """
        self.swagger_types = {
            'vault_id': 'str',
            'master_encryption_key_id': 'str',
            'secret_name': 'str',
            'description': 'str'
        }

        self.attribute_map = {
            'vault_id': 'vaultId',
            'master_encryption_key_id': 'masterEncryptionKeyId',
            'secret_name': 'secretName',
            'description': 'description'
        }

        self._vault_id = None
        self._master_encryption_key_id = None
        self._secret_name = None
        self._description = None

    @property
    def vault_id(self):
        """
        **[Required]** Gets the vault_id of this ExportDeploymentWalletDetails.
        Refers to the customer's vault OCID.
        If provided, it references a vault where GoldenGate can manage secrets. Customers must add policies to permit GoldenGate
        to manage secrets contained within this vault.


        :return: The vault_id of this ExportDeploymentWalletDetails.
        :rtype: str
        """
        return self._vault_id

    @vault_id.setter
    def vault_id(self, vault_id):
        """
        Sets the vault_id of this ExportDeploymentWalletDetails.
        Refers to the customer's vault OCID.
        If provided, it references a vault where GoldenGate can manage secrets. Customers must add policies to permit GoldenGate
        to manage secrets contained within this vault.


        :param vault_id: The vault_id of this ExportDeploymentWalletDetails.
        :type: str
        """
        self._vault_id = vault_id

    @property
    def master_encryption_key_id(self):
        """
        **[Required]** Gets the master_encryption_key_id of this ExportDeploymentWalletDetails.
        Refers to the customer's master key OCID.
        If provided, it references a key to manage secrets. Customers must add policies to permit GoldenGate to use this key.


        :return: The master_encryption_key_id of this ExportDeploymentWalletDetails.
        :rtype: str
        """
        return self._master_encryption_key_id

    @master_encryption_key_id.setter
    def master_encryption_key_id(self, master_encryption_key_id):
        """
        Sets the master_encryption_key_id of this ExportDeploymentWalletDetails.
        Refers to the customer's master key OCID.
        If provided, it references a key to manage secrets. Customers must add policies to permit GoldenGate to use this key.


        :param master_encryption_key_id: The master_encryption_key_id of this ExportDeploymentWalletDetails.
        :type: str
        """
        self._master_encryption_key_id = master_encryption_key_id

    @property
    def secret_name(self):
        """
        **[Required]** Gets the secret_name of this ExportDeploymentWalletDetails.
        Name of the secret with which secret is shown in vault


        :return: The secret_name of this ExportDeploymentWalletDetails.
        :rtype: str
        """
        return self._secret_name

    @secret_name.setter
    def secret_name(self, secret_name):
        """
        Sets the secret_name of this ExportDeploymentWalletDetails.
        Name of the secret with which secret is shown in vault


        :param secret_name: The secret_name of this ExportDeploymentWalletDetails.
        :type: str
        """
        self._secret_name = secret_name

    @property
    def description(self):
        """
        Gets the description of this ExportDeploymentWalletDetails.
        Metadata about this specific object.


        :return: The description of this ExportDeploymentWalletDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ExportDeploymentWalletDetails.
        Metadata about this specific object.


        :param description: The description of this ExportDeploymentWalletDetails.
        :type: str
        """
        self._description = description

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
