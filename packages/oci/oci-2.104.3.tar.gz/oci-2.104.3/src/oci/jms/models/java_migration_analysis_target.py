# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class JavaMigrationAnalysisTarget(object):
    """
    The target describes the input data for Java migration analysis.
    A target contains a managed instance, application Installation Key, sourceJdkVersion, and targetJdkVersion.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new JavaMigrationAnalysisTarget object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param managed_instance_id:
            The value to assign to the managed_instance_id property of this JavaMigrationAnalysisTarget.
        :type managed_instance_id: str

        :param application_installation_key:
            The value to assign to the application_installation_key property of this JavaMigrationAnalysisTarget.
        :type application_installation_key: str

        :param source_jdk_version:
            The value to assign to the source_jdk_version property of this JavaMigrationAnalysisTarget.
        :type source_jdk_version: str

        :param target_jdk_version:
            The value to assign to the target_jdk_version property of this JavaMigrationAnalysisTarget.
        :type target_jdk_version: str

        """
        self.swagger_types = {
            'managed_instance_id': 'str',
            'application_installation_key': 'str',
            'source_jdk_version': 'str',
            'target_jdk_version': 'str'
        }

        self.attribute_map = {
            'managed_instance_id': 'managedInstanceId',
            'application_installation_key': 'applicationInstallationKey',
            'source_jdk_version': 'sourceJdkVersion',
            'target_jdk_version': 'targetJdkVersion'
        }

        self._managed_instance_id = None
        self._application_installation_key = None
        self._source_jdk_version = None
        self._target_jdk_version = None

    @property
    def managed_instance_id(self):
        """
        **[Required]** Gets the managed_instance_id of this JavaMigrationAnalysisTarget.
        The OCID of the managed instance that hosts the application for which the Java migration analysis was performed.


        :return: The managed_instance_id of this JavaMigrationAnalysisTarget.
        :rtype: str
        """
        return self._managed_instance_id

    @managed_instance_id.setter
    def managed_instance_id(self, managed_instance_id):
        """
        Sets the managed_instance_id of this JavaMigrationAnalysisTarget.
        The OCID of the managed instance that hosts the application for which the Java migration analysis was performed.


        :param managed_instance_id: The managed_instance_id of this JavaMigrationAnalysisTarget.
        :type: str
        """
        self._managed_instance_id = managed_instance_id

    @property
    def application_installation_key(self):
        """
        **[Required]** Gets the application_installation_key of this JavaMigrationAnalysisTarget.
        The unique key that identifies the application's installation path that is to be used for the Java migration analysis.


        :return: The application_installation_key of this JavaMigrationAnalysisTarget.
        :rtype: str
        """
        return self._application_installation_key

    @application_installation_key.setter
    def application_installation_key(self, application_installation_key):
        """
        Sets the application_installation_key of this JavaMigrationAnalysisTarget.
        The unique key that identifies the application's installation path that is to be used for the Java migration analysis.


        :param application_installation_key: The application_installation_key of this JavaMigrationAnalysisTarget.
        :type: str
        """
        self._application_installation_key = application_installation_key

    @property
    def source_jdk_version(self):
        """
        **[Required]** Gets the source_jdk_version of this JavaMigrationAnalysisTarget.
        The JDK version the application is currently running on.


        :return: The source_jdk_version of this JavaMigrationAnalysisTarget.
        :rtype: str
        """
        return self._source_jdk_version

    @source_jdk_version.setter
    def source_jdk_version(self, source_jdk_version):
        """
        Sets the source_jdk_version of this JavaMigrationAnalysisTarget.
        The JDK version the application is currently running on.


        :param source_jdk_version: The source_jdk_version of this JavaMigrationAnalysisTarget.
        :type: str
        """
        self._source_jdk_version = source_jdk_version

    @property
    def target_jdk_version(self):
        """
        **[Required]** Gets the target_jdk_version of this JavaMigrationAnalysisTarget.
        The JDK version against which the migration analysis was performed to identify effort required to move from source JDK.


        :return: The target_jdk_version of this JavaMigrationAnalysisTarget.
        :rtype: str
        """
        return self._target_jdk_version

    @target_jdk_version.setter
    def target_jdk_version(self, target_jdk_version):
        """
        Sets the target_jdk_version of this JavaMigrationAnalysisTarget.
        The JDK version against which the migration analysis was performed to identify effort required to move from source JDK.


        :param target_jdk_version: The target_jdk_version of this JavaMigrationAnalysisTarget.
        :type: str
        """
        self._target_jdk_version = target_jdk_version

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
