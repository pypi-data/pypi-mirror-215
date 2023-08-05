# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_data_asset_details import UpdateDataAssetDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateDataAssetFromLake(UpdateDataAssetDetails):
    """
    Details for the Lake data asset type.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateDataAssetFromLake object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.UpdateDataAssetFromLake.model_type` attribute
        of this class is ``LAKE_DATA_ASSET`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this UpdateDataAssetFromLake.
            Allowed values for this property are: "ORACLE_DATA_ASSET", "ORACLE_OBJECT_STORAGE_DATA_ASSET", "ORACLE_ATP_DATA_ASSET", "ORACLE_ADWC_DATA_ASSET", "MYSQL_DATA_ASSET", "GENERIC_JDBC_DATA_ASSET", "FUSION_APP_DATA_ASSET", "AMAZON_S3_DATA_ASSET", "LAKE_DATA_ASSET", "REST_DATA_ASSET"
        :type model_type: str

        :param key:
            The value to assign to the key property of this UpdateDataAssetFromLake.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this UpdateDataAssetFromLake.
        :type model_version: str

        :param name:
            The value to assign to the name property of this UpdateDataAssetFromLake.
        :type name: str

        :param description:
            The value to assign to the description property of this UpdateDataAssetFromLake.
        :type description: str

        :param object_status:
            The value to assign to the object_status property of this UpdateDataAssetFromLake.
        :type object_status: int

        :param object_version:
            The value to assign to the object_version property of this UpdateDataAssetFromLake.
        :type object_version: int

        :param identifier:
            The value to assign to the identifier property of this UpdateDataAssetFromLake.
        :type identifier: str

        :param external_key:
            The value to assign to the external_key property of this UpdateDataAssetFromLake.
        :type external_key: str

        :param asset_properties:
            The value to assign to the asset_properties property of this UpdateDataAssetFromLake.
        :type asset_properties: dict(str, str)

        :param registry_metadata:
            The value to assign to the registry_metadata property of this UpdateDataAssetFromLake.
        :type registry_metadata: oci.data_integration.models.RegistryMetadata

        :param lake_id:
            The value to assign to the lake_id property of this UpdateDataAssetFromLake.
        :type lake_id: str

        :param metastore_id:
            The value to assign to the metastore_id property of this UpdateDataAssetFromLake.
        :type metastore_id: str

        :param lake_proxy_endpoint:
            The value to assign to the lake_proxy_endpoint property of this UpdateDataAssetFromLake.
        :type lake_proxy_endpoint: str

        :param default_connection:
            The value to assign to the default_connection property of this UpdateDataAssetFromLake.
        :type default_connection: oci.data_integration.models.UpdateConnectionFromLake

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'name': 'str',
            'description': 'str',
            'object_status': 'int',
            'object_version': 'int',
            'identifier': 'str',
            'external_key': 'str',
            'asset_properties': 'dict(str, str)',
            'registry_metadata': 'RegistryMetadata',
            'lake_id': 'str',
            'metastore_id': 'str',
            'lake_proxy_endpoint': 'str',
            'default_connection': 'UpdateConnectionFromLake'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'name': 'name',
            'description': 'description',
            'object_status': 'objectStatus',
            'object_version': 'objectVersion',
            'identifier': 'identifier',
            'external_key': 'externalKey',
            'asset_properties': 'assetProperties',
            'registry_metadata': 'registryMetadata',
            'lake_id': 'lakeId',
            'metastore_id': 'metastoreId',
            'lake_proxy_endpoint': 'lakeProxyEndpoint',
            'default_connection': 'defaultConnection'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._name = None
        self._description = None
        self._object_status = None
        self._object_version = None
        self._identifier = None
        self._external_key = None
        self._asset_properties = None
        self._registry_metadata = None
        self._lake_id = None
        self._metastore_id = None
        self._lake_proxy_endpoint = None
        self._default_connection = None
        self._model_type = 'LAKE_DATA_ASSET'

    @property
    def lake_id(self):
        """
        **[Required]** Gets the lake_id of this UpdateDataAssetFromLake.
        The Lake Ocid.


        :return: The lake_id of this UpdateDataAssetFromLake.
        :rtype: str
        """
        return self._lake_id

    @lake_id.setter
    def lake_id(self, lake_id):
        """
        Sets the lake_id of this UpdateDataAssetFromLake.
        The Lake Ocid.


        :param lake_id: The lake_id of this UpdateDataAssetFromLake.
        :type: str
        """
        self._lake_id = lake_id

    @property
    def metastore_id(self):
        """
        Gets the metastore_id of this UpdateDataAssetFromLake.
        The metastoreId for the specified Lake Resource.


        :return: The metastore_id of this UpdateDataAssetFromLake.
        :rtype: str
        """
        return self._metastore_id

    @metastore_id.setter
    def metastore_id(self, metastore_id):
        """
        Sets the metastore_id of this UpdateDataAssetFromLake.
        The metastoreId for the specified Lake Resource.


        :param metastore_id: The metastore_id of this UpdateDataAssetFromLake.
        :type: str
        """
        self._metastore_id = metastore_id

    @property
    def lake_proxy_endpoint(self):
        """
        Gets the lake_proxy_endpoint of this UpdateDataAssetFromLake.
        The rangerEndpoint for the specified Lake Resource.


        :return: The lake_proxy_endpoint of this UpdateDataAssetFromLake.
        :rtype: str
        """
        return self._lake_proxy_endpoint

    @lake_proxy_endpoint.setter
    def lake_proxy_endpoint(self, lake_proxy_endpoint):
        """
        Sets the lake_proxy_endpoint of this UpdateDataAssetFromLake.
        The rangerEndpoint for the specified Lake Resource.


        :param lake_proxy_endpoint: The lake_proxy_endpoint of this UpdateDataAssetFromLake.
        :type: str
        """
        self._lake_proxy_endpoint = lake_proxy_endpoint

    @property
    def default_connection(self):
        """
        **[Required]** Gets the default_connection of this UpdateDataAssetFromLake.

        :return: The default_connection of this UpdateDataAssetFromLake.
        :rtype: oci.data_integration.models.UpdateConnectionFromLake
        """
        return self._default_connection

    @default_connection.setter
    def default_connection(self, default_connection):
        """
        Sets the default_connection of this UpdateDataAssetFromLake.

        :param default_connection: The default_connection of this UpdateDataAssetFromLake.
        :type: oci.data_integration.models.UpdateConnectionFromLake
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
