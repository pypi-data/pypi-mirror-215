# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class TestBdsObjectStorageConnectionDetails(object):
    """
    Test access to specified Object Storage bucket using the API key.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new TestBdsObjectStorageConnectionDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param object_storage_uri:
            The value to assign to the object_storage_uri property of this TestBdsObjectStorageConnectionDetails.
        :type object_storage_uri: str

        :param passphrase:
            The value to assign to the passphrase property of this TestBdsObjectStorageConnectionDetails.
        :type passphrase: str

        :param object_storage_region:
            The value to assign to the object_storage_region property of this TestBdsObjectStorageConnectionDetails.
        :type object_storage_region: str

        """
        self.swagger_types = {
            'object_storage_uri': 'str',
            'passphrase': 'str',
            'object_storage_region': 'str'
        }

        self.attribute_map = {
            'object_storage_uri': 'objectStorageUri',
            'passphrase': 'passphrase',
            'object_storage_region': 'objectStorageRegion'
        }

        self._object_storage_uri = None
        self._passphrase = None
        self._object_storage_region = None

    @property
    def object_storage_uri(self):
        """
        **[Required]** Gets the object_storage_uri of this TestBdsObjectStorageConnectionDetails.
        An Oracle Cloud Infrastructure URI to which this connection must be attempted. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.


        :return: The object_storage_uri of this TestBdsObjectStorageConnectionDetails.
        :rtype: str
        """
        return self._object_storage_uri

    @object_storage_uri.setter
    def object_storage_uri(self, object_storage_uri):
        """
        Sets the object_storage_uri of this TestBdsObjectStorageConnectionDetails.
        An Oracle Cloud Infrastructure URI to which this connection must be attempted. See https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/hdfsconnector.htm#uriformat.


        :param object_storage_uri: The object_storage_uri of this TestBdsObjectStorageConnectionDetails.
        :type: str
        """
        self._object_storage_uri = object_storage_uri

    @property
    def passphrase(self):
        """
        **[Required]** Gets the passphrase of this TestBdsObjectStorageConnectionDetails.
        Base64 passphrase used to secure the private key which will be created on user behalf.


        :return: The passphrase of this TestBdsObjectStorageConnectionDetails.
        :rtype: str
        """
        return self._passphrase

    @passphrase.setter
    def passphrase(self, passphrase):
        """
        Sets the passphrase of this TestBdsObjectStorageConnectionDetails.
        Base64 passphrase used to secure the private key which will be created on user behalf.


        :param passphrase: The passphrase of this TestBdsObjectStorageConnectionDetails.
        :type: str
        """
        self._passphrase = passphrase

    @property
    def object_storage_region(self):
        """
        Gets the object_storage_region of this TestBdsObjectStorageConnectionDetails.
        The name of the region to establish the Object Storage endpoint. Example us-phoenix-1 .


        :return: The object_storage_region of this TestBdsObjectStorageConnectionDetails.
        :rtype: str
        """
        return self._object_storage_region

    @object_storage_region.setter
    def object_storage_region(self, object_storage_region):
        """
        Sets the object_storage_region of this TestBdsObjectStorageConnectionDetails.
        The name of the region to establish the Object Storage endpoint. Example us-phoenix-1 .


        :param object_storage_region: The object_storage_region of this TestBdsObjectStorageConnectionDetails.
        :type: str
        """
        self._object_storage_region = object_storage_region

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
