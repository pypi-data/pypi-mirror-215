# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class JavaMigrationAnalysisResult(object):
    """
    Result of the Java migration analysis. The analysis result is stored in an Object Storage bucket.
    """

    #: A constant which can be used with the application_execution_type property of a JavaMigrationAnalysisResult.
    #: This constant has a value of "INSTALLED"
    APPLICATION_EXECUTION_TYPE_INSTALLED = "INSTALLED"

    #: A constant which can be used with the application_execution_type property of a JavaMigrationAnalysisResult.
    #: This constant has a value of "DEPLOYED"
    APPLICATION_EXECUTION_TYPE_DEPLOYED = "DEPLOYED"

    def __init__(self, **kwargs):
        """
        Initializes a new JavaMigrationAnalysisResult object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this JavaMigrationAnalysisResult.
        :type id: str

        :param work_request_id:
            The value to assign to the work_request_id property of this JavaMigrationAnalysisResult.
        :type work_request_id: str

        :param fleet_id:
            The value to assign to the fleet_id property of this JavaMigrationAnalysisResult.
        :type fleet_id: str

        :param application_name:
            The value to assign to the application_name property of this JavaMigrationAnalysisResult.
        :type application_name: str

        :param application_path:
            The value to assign to the application_path property of this JavaMigrationAnalysisResult.
        :type application_path: str

        :param application_execution_type:
            The value to assign to the application_execution_type property of this JavaMigrationAnalysisResult.
            Allowed values for this property are: "INSTALLED", "DEPLOYED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type application_execution_type: str

        :param source_jdk_version:
            The value to assign to the source_jdk_version property of this JavaMigrationAnalysisResult.
        :type source_jdk_version: str

        :param target_jdk_version:
            The value to assign to the target_jdk_version property of this JavaMigrationAnalysisResult.
        :type target_jdk_version: str

        :param managed_instance_id:
            The value to assign to the managed_instance_id property of this JavaMigrationAnalysisResult.
        :type managed_instance_id: str

        :param host_name:
            The value to assign to the host_name property of this JavaMigrationAnalysisResult.
        :type host_name: str

        :param time_created:
            The value to assign to the time_created property of this JavaMigrationAnalysisResult.
        :type time_created: datetime

        :param namespace:
            The value to assign to the namespace property of this JavaMigrationAnalysisResult.
        :type namespace: str

        :param bucket_name:
            The value to assign to the bucket_name property of this JavaMigrationAnalysisResult.
        :type bucket_name: str

        :param object_storage_upload_dir_path:
            The value to assign to the object_storage_upload_dir_path property of this JavaMigrationAnalysisResult.
        :type object_storage_upload_dir_path: str

        :param object_list:
            The value to assign to the object_list property of this JavaMigrationAnalysisResult.
        :type object_list: list[str]

        :param metadata:
            The value to assign to the metadata property of this JavaMigrationAnalysisResult.
        :type metadata: str

        """
        self.swagger_types = {
            'id': 'str',
            'work_request_id': 'str',
            'fleet_id': 'str',
            'application_name': 'str',
            'application_path': 'str',
            'application_execution_type': 'str',
            'source_jdk_version': 'str',
            'target_jdk_version': 'str',
            'managed_instance_id': 'str',
            'host_name': 'str',
            'time_created': 'datetime',
            'namespace': 'str',
            'bucket_name': 'str',
            'object_storage_upload_dir_path': 'str',
            'object_list': 'list[str]',
            'metadata': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'work_request_id': 'workRequestId',
            'fleet_id': 'fleetId',
            'application_name': 'applicationName',
            'application_path': 'applicationPath',
            'application_execution_type': 'applicationExecutionType',
            'source_jdk_version': 'sourceJdkVersion',
            'target_jdk_version': 'targetJdkVersion',
            'managed_instance_id': 'managedInstanceId',
            'host_name': 'hostName',
            'time_created': 'timeCreated',
            'namespace': 'namespace',
            'bucket_name': 'bucketName',
            'object_storage_upload_dir_path': 'objectStorageUploadDirPath',
            'object_list': 'objectList',
            'metadata': 'metadata'
        }

        self._id = None
        self._work_request_id = None
        self._fleet_id = None
        self._application_name = None
        self._application_path = None
        self._application_execution_type = None
        self._source_jdk_version = None
        self._target_jdk_version = None
        self._managed_instance_id = None
        self._host_name = None
        self._time_created = None
        self._namespace = None
        self._bucket_name = None
        self._object_storage_upload_dir_path = None
        self._object_list = None
        self._metadata = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this JavaMigrationAnalysisResult.
        The OCID of the migration analysis report.


        :return: The id of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this JavaMigrationAnalysisResult.
        The OCID of the migration analysis report.


        :param id: The id of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._id = id

    @property
    def work_request_id(self):
        """
        Gets the work_request_id of this JavaMigrationAnalysisResult.
        The OCID of the work request of this analysis.


        :return: The work_request_id of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._work_request_id

    @work_request_id.setter
    def work_request_id(self, work_request_id):
        """
        Sets the work_request_id of this JavaMigrationAnalysisResult.
        The OCID of the work request of this analysis.


        :param work_request_id: The work_request_id of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._work_request_id = work_request_id

    @property
    def fleet_id(self):
        """
        **[Required]** Gets the fleet_id of this JavaMigrationAnalysisResult.
        The fleet OCID.


        :return: The fleet_id of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._fleet_id

    @fleet_id.setter
    def fleet_id(self, fleet_id):
        """
        Sets the fleet_id of this JavaMigrationAnalysisResult.
        The fleet OCID.


        :param fleet_id: The fleet_id of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._fleet_id = fleet_id

    @property
    def application_name(self):
        """
        **[Required]** Gets the application_name of this JavaMigrationAnalysisResult.
        The name of the application for which the Java migration analysis was performed.


        :return: The application_name of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._application_name

    @application_name.setter
    def application_name(self, application_name):
        """
        Sets the application_name of this JavaMigrationAnalysisResult.
        The name of the application for which the Java migration analysis was performed.


        :param application_name: The application_name of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._application_name = application_name

    @property
    def application_path(self):
        """
        **[Required]** Gets the application_path of this JavaMigrationAnalysisResult.
        The installation path of the application for which the Java migration analysis was performed.


        :return: The application_path of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._application_path

    @application_path.setter
    def application_path(self, application_path):
        """
        Sets the application_path of this JavaMigrationAnalysisResult.
        The installation path of the application for which the Java migration analysis was performed.


        :param application_path: The application_path of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._application_path = application_path

    @property
    def application_execution_type(self):
        """
        **[Required]** Gets the application_execution_type of this JavaMigrationAnalysisResult.
        Execution type of the application for an application type, such as WAR and EAR, that is deployed or installed.

        Allowed values for this property are: "INSTALLED", "DEPLOYED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The application_execution_type of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._application_execution_type

    @application_execution_type.setter
    def application_execution_type(self, application_execution_type):
        """
        Sets the application_execution_type of this JavaMigrationAnalysisResult.
        Execution type of the application for an application type, such as WAR and EAR, that is deployed or installed.


        :param application_execution_type: The application_execution_type of this JavaMigrationAnalysisResult.
        :type: str
        """
        allowed_values = ["INSTALLED", "DEPLOYED"]
        if not value_allowed_none_or_none_sentinel(application_execution_type, allowed_values):
            application_execution_type = 'UNKNOWN_ENUM_VALUE'
        self._application_execution_type = application_execution_type

    @property
    def source_jdk_version(self):
        """
        **[Required]** Gets the source_jdk_version of this JavaMigrationAnalysisResult.
        The source JDK version of the application that's currently running.


        :return: The source_jdk_version of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._source_jdk_version

    @source_jdk_version.setter
    def source_jdk_version(self, source_jdk_version):
        """
        Sets the source_jdk_version of this JavaMigrationAnalysisResult.
        The source JDK version of the application that's currently running.


        :param source_jdk_version: The source_jdk_version of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._source_jdk_version = source_jdk_version

    @property
    def target_jdk_version(self):
        """
        **[Required]** Gets the target_jdk_version of this JavaMigrationAnalysisResult.
        The target JDK version of the application to be migrated.


        :return: The target_jdk_version of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._target_jdk_version

    @target_jdk_version.setter
    def target_jdk_version(self, target_jdk_version):
        """
        Sets the target_jdk_version of this JavaMigrationAnalysisResult.
        The target JDK version of the application to be migrated.


        :param target_jdk_version: The target_jdk_version of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._target_jdk_version = target_jdk_version

    @property
    def managed_instance_id(self):
        """
        Gets the managed_instance_id of this JavaMigrationAnalysisResult.
        The managed instance OCID.


        :return: The managed_instance_id of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._managed_instance_id

    @managed_instance_id.setter
    def managed_instance_id(self, managed_instance_id):
        """
        Sets the managed_instance_id of this JavaMigrationAnalysisResult.
        The managed instance OCID.


        :param managed_instance_id: The managed_instance_id of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._managed_instance_id = managed_instance_id

    @property
    def host_name(self):
        """
        Gets the host_name of this JavaMigrationAnalysisResult.
        The hostname of the managed instance that hosts the application for which the Java migration analysis was performed.


        :return: The host_name of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """
        Sets the host_name of this JavaMigrationAnalysisResult.
        The hostname of the managed instance that hosts the application for which the Java migration analysis was performed.


        :param host_name: The host_name of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._host_name = host_name

    @property
    def time_created(self):
        """
        Gets the time_created of this JavaMigrationAnalysisResult.
        The time the result is compiled.


        :return: The time_created of this JavaMigrationAnalysisResult.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this JavaMigrationAnalysisResult.
        The time the result is compiled.


        :param time_created: The time_created of this JavaMigrationAnalysisResult.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def namespace(self):
        """
        **[Required]** Gets the namespace of this JavaMigrationAnalysisResult.
        The object storage namespace that contains the results of the migration analysis.


        :return: The namespace of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """
        Sets the namespace of this JavaMigrationAnalysisResult.
        The object storage namespace that contains the results of the migration analysis.


        :param namespace: The namespace of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._namespace = namespace

    @property
    def bucket_name(self):
        """
        **[Required]** Gets the bucket_name of this JavaMigrationAnalysisResult.
        The name of the object storage bucket that contains the results of the migration analysis.


        :return: The bucket_name of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this JavaMigrationAnalysisResult.
        The name of the object storage bucket that contains the results of the migration analysis.


        :param bucket_name: The bucket_name of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._bucket_name = bucket_name

    @property
    def object_storage_upload_dir_path(self):
        """
        **[Required]** Gets the object_storage_upload_dir_path of this JavaMigrationAnalysisResult.
        The directory path of the object storage bucket that contains the results of the migration analysis.


        :return: The object_storage_upload_dir_path of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._object_storage_upload_dir_path

    @object_storage_upload_dir_path.setter
    def object_storage_upload_dir_path(self, object_storage_upload_dir_path):
        """
        Sets the object_storage_upload_dir_path of this JavaMigrationAnalysisResult.
        The directory path of the object storage bucket that contains the results of the migration analysis.


        :param object_storage_upload_dir_path: The object_storage_upload_dir_path of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._object_storage_upload_dir_path = object_storage_upload_dir_path

    @property
    def object_list(self):
        """
        **[Required]** Gets the object_list of this JavaMigrationAnalysisResult.
        The names of the object storage objects that contain the results of the migration analysis.


        :return: The object_list of this JavaMigrationAnalysisResult.
        :rtype: list[str]
        """
        return self._object_list

    @object_list.setter
    def object_list(self, object_list):
        """
        Sets the object_list of this JavaMigrationAnalysisResult.
        The names of the object storage objects that contain the results of the migration analysis.


        :param object_list: The object_list of this JavaMigrationAnalysisResult.
        :type: list[str]
        """
        self._object_list = object_list

    @property
    def metadata(self):
        """
        **[Required]** Gets the metadata of this JavaMigrationAnalysisResult.
        Additional info reserved for future use.


        :return: The metadata of this JavaMigrationAnalysisResult.
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this JavaMigrationAnalysisResult.
        Additional info reserved for future use.


        :param metadata: The metadata of this JavaMigrationAnalysisResult.
        :type: str
        """
        self._metadata = metadata

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
