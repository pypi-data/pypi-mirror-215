# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_data_asset_details import CreateDataAssetDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateDataAssetFromRest(CreateDataAssetDetails):
    """
    Details to create Rest data asset type.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateDataAssetFromRest object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.CreateDataAssetFromRest.model_type` attribute
        of this class is ``REST_DATA_ASSET`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this CreateDataAssetFromRest.
            Allowed values for this property are: "ORACLE_DATA_ASSET", "ORACLE_OBJECT_STORAGE_DATA_ASSET", "ORACLE_ATP_DATA_ASSET", "ORACLE_ADWC_DATA_ASSET", "MYSQL_DATA_ASSET", "GENERIC_JDBC_DATA_ASSET", "FUSION_APP_DATA_ASSET", "AMAZON_S3_DATA_ASSET", "LAKE_DATA_ASSET", "REST_DATA_ASSET"
        :type model_type: str

        :param key:
            The value to assign to the key property of this CreateDataAssetFromRest.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this CreateDataAssetFromRest.
        :type model_version: str

        :param name:
            The value to assign to the name property of this CreateDataAssetFromRest.
        :type name: str

        :param description:
            The value to assign to the description property of this CreateDataAssetFromRest.
        :type description: str

        :param object_status:
            The value to assign to the object_status property of this CreateDataAssetFromRest.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this CreateDataAssetFromRest.
        :type identifier: str

        :param external_key:
            The value to assign to the external_key property of this CreateDataAssetFromRest.
        :type external_key: str

        :param asset_properties:
            The value to assign to the asset_properties property of this CreateDataAssetFromRest.
        :type asset_properties: dict(str, str)

        :param registry_metadata:
            The value to assign to the registry_metadata property of this CreateDataAssetFromRest.
        :type registry_metadata: oci.data_integration.models.RegistryMetadata

        :param base_url:
            The value to assign to the base_url property of this CreateDataAssetFromRest.
        :type base_url: str

        :param manifest_file_content:
            The value to assign to the manifest_file_content property of this CreateDataAssetFromRest.
        :type manifest_file_content: str

        :param default_connection:
            The value to assign to the default_connection property of this CreateDataAssetFromRest.
        :type default_connection: oci.data_integration.models.CreateConnectionDetails

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'name': 'str',
            'description': 'str',
            'object_status': 'int',
            'identifier': 'str',
            'external_key': 'str',
            'asset_properties': 'dict(str, str)',
            'registry_metadata': 'RegistryMetadata',
            'base_url': 'str',
            'manifest_file_content': 'str',
            'default_connection': 'CreateConnectionDetails'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'name': 'name',
            'description': 'description',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'external_key': 'externalKey',
            'asset_properties': 'assetProperties',
            'registry_metadata': 'registryMetadata',
            'base_url': 'baseUrl',
            'manifest_file_content': 'manifestFileContent',
            'default_connection': 'defaultConnection'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._name = None
        self._description = None
        self._object_status = None
        self._identifier = None
        self._external_key = None
        self._asset_properties = None
        self._registry_metadata = None
        self._base_url = None
        self._manifest_file_content = None
        self._default_connection = None
        self._model_type = 'REST_DATA_ASSET'

    @property
    def base_url(self):
        """
        **[Required]** Gets the base_url of this CreateDataAssetFromRest.
        The base url of the rest server.


        :return: The base_url of this CreateDataAssetFromRest.
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        """
        Sets the base_url of this CreateDataAssetFromRest.
        The base url of the rest server.


        :param base_url: The base_url of this CreateDataAssetFromRest.
        :type: str
        """
        self._base_url = base_url

    @property
    def manifest_file_content(self):
        """
        **[Required]** Gets the manifest_file_content of this CreateDataAssetFromRest.
        The manifest file content of the rest APIs.


        :return: The manifest_file_content of this CreateDataAssetFromRest.
        :rtype: str
        """
        return self._manifest_file_content

    @manifest_file_content.setter
    def manifest_file_content(self, manifest_file_content):
        """
        Sets the manifest_file_content of this CreateDataAssetFromRest.
        The manifest file content of the rest APIs.


        :param manifest_file_content: The manifest_file_content of this CreateDataAssetFromRest.
        :type: str
        """
        self._manifest_file_content = manifest_file_content

    @property
    def default_connection(self):
        """
        **[Required]** Gets the default_connection of this CreateDataAssetFromRest.

        :return: The default_connection of this CreateDataAssetFromRest.
        :rtype: oci.data_integration.models.CreateConnectionDetails
        """
        return self._default_connection

    @default_connection.setter
    def default_connection(self, default_connection):
        """
        Sets the default_connection of this CreateDataAssetFromRest.

        :param default_connection: The default_connection of this CreateDataAssetFromRest.
        :type: oci.data_integration.models.CreateConnectionDetails
        """
        self._default_connection = default_connection

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
