# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_config_source_details import CreateConfigSourceDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateGitConfigSourceDetails(CreateConfigSourceDetails):
    """
    Creation details for configuration Git information.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateGitConfigSourceDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.resource_manager.models.CreateGitConfigSourceDetails.config_source_type` attribute
        of this class is ``GIT_CONFIG_SOURCE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param config_source_type:
            The value to assign to the config_source_type property of this CreateGitConfigSourceDetails.
        :type config_source_type: str

        :param working_directory:
            The value to assign to the working_directory property of this CreateGitConfigSourceDetails.
        :type working_directory: str

        :param configuration_source_provider_id:
            The value to assign to the configuration_source_provider_id property of this CreateGitConfigSourceDetails.
        :type configuration_source_provider_id: str

        :param repository_url:
            The value to assign to the repository_url property of this CreateGitConfigSourceDetails.
        :type repository_url: str

        :param branch_name:
            The value to assign to the branch_name property of this CreateGitConfigSourceDetails.
        :type branch_name: str

        """
        self.swagger_types = {
            'config_source_type': 'str',
            'working_directory': 'str',
            'configuration_source_provider_id': 'str',
            'repository_url': 'str',
            'branch_name': 'str'
        }

        self.attribute_map = {
            'config_source_type': 'configSourceType',
            'working_directory': 'workingDirectory',
            'configuration_source_provider_id': 'configurationSourceProviderId',
            'repository_url': 'repositoryUrl',
            'branch_name': 'branchName'
        }

        self._config_source_type = None
        self._working_directory = None
        self._configuration_source_provider_id = None
        self._repository_url = None
        self._branch_name = None
        self._config_source_type = 'GIT_CONFIG_SOURCE'

    @property
    def configuration_source_provider_id(self):
        """
        **[Required]** Gets the configuration_source_provider_id of this CreateGitConfigSourceDetails.
        Unique identifier (`OCID`__)
        for the Git configuration source.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The configuration_source_provider_id of this CreateGitConfigSourceDetails.
        :rtype: str
        """
        return self._configuration_source_provider_id

    @configuration_source_provider_id.setter
    def configuration_source_provider_id(self, configuration_source_provider_id):
        """
        Sets the configuration_source_provider_id of this CreateGitConfigSourceDetails.
        Unique identifier (`OCID`__)
        for the Git configuration source.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param configuration_source_provider_id: The configuration_source_provider_id of this CreateGitConfigSourceDetails.
        :type: str
        """
        self._configuration_source_provider_id = configuration_source_provider_id

    @property
    def repository_url(self):
        """
        Gets the repository_url of this CreateGitConfigSourceDetails.
        The URL of the Git repository.


        :return: The repository_url of this CreateGitConfigSourceDetails.
        :rtype: str
        """
        return self._repository_url

    @repository_url.setter
    def repository_url(self, repository_url):
        """
        Sets the repository_url of this CreateGitConfigSourceDetails.
        The URL of the Git repository.


        :param repository_url: The repository_url of this CreateGitConfigSourceDetails.
        :type: str
        """
        self._repository_url = repository_url

    @property
    def branch_name(self):
        """
        Gets the branch_name of this CreateGitConfigSourceDetails.
        The name of the branch within the Git repository.


        :return: The branch_name of this CreateGitConfigSourceDetails.
        :rtype: str
        """
        return self._branch_name

    @branch_name.setter
    def branch_name(self, branch_name):
        """
        Sets the branch_name of this CreateGitConfigSourceDetails.
        The name of the branch within the Git repository.


        :param branch_name: The branch_name of this CreateGitConfigSourceDetails.
        :type: str
        """
        self._branch_name = branch_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
