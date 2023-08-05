# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .import_metadata_path import ImportMetadataPath
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ObjectStorageImportMetadataPath(ImportMetadataPath):
    """
    Object Storage details for import metadata path.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ObjectStorageImportMetadataPath object with values from keyword arguments. The default value of the :py:attr:`~oci.data_labeling_service_dataplane.models.ObjectStorageImportMetadataPath.source_type` attribute
        of this class is ``OBJECT_STORAGE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_type:
            The value to assign to the source_type property of this ObjectStorageImportMetadataPath.
            Allowed values for this property are: "OBJECT_STORAGE"
        :type source_type: str

        :param namespace:
            The value to assign to the namespace property of this ObjectStorageImportMetadataPath.
        :type namespace: str

        :param bucket:
            The value to assign to the bucket property of this ObjectStorageImportMetadataPath.
        :type bucket: str

        :param path:
            The value to assign to the path property of this ObjectStorageImportMetadataPath.
        :type path: str

        """
        self.swagger_types = {
            'source_type': 'str',
            'namespace': 'str',
            'bucket': 'str',
            'path': 'str'
        }

        self.attribute_map = {
            'source_type': 'sourceType',
            'namespace': 'namespace',
            'bucket': 'bucket',
            'path': 'path'
        }

        self._source_type = None
        self._namespace = None
        self._bucket = None
        self._path = None
        self._source_type = 'OBJECT_STORAGE'

    @property
    def namespace(self):
        """
        **[Required]** Gets the namespace of this ObjectStorageImportMetadataPath.
        Bucket namespace name


        :return: The namespace of this ObjectStorageImportMetadataPath.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this ObjectStorageImportMetadataPath.
        Bucket namespace name


        :param namespace: The namespace of this ObjectStorageImportMetadataPath.
        :type: str
        """
        self._namespace = namespace

    @property
    def bucket(self):
        """
        **[Required]** Gets the bucket of this ObjectStorageImportMetadataPath.
        Bucket name


        :return: The bucket of this ObjectStorageImportMetadataPath.
        :rtype: str
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """
        Sets the bucket of this ObjectStorageImportMetadataPath.
        Bucket name


        :param bucket: The bucket of this ObjectStorageImportMetadataPath.
        :type: str
        """
        self._bucket = bucket

    @property
    def path(self):
        """
        **[Required]** Gets the path of this ObjectStorageImportMetadataPath.
        Path for the metadata file.


        :return: The path of this ObjectStorageImportMetadataPath.
        :rtype: str
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path of this ObjectStorageImportMetadataPath.
        Path for the metadata file.


        :param path: The path of this ObjectStorageImportMetadataPath.
        :type: str
        """
        self._path = path

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
