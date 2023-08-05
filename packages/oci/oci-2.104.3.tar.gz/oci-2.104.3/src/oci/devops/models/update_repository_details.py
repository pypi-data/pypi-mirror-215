# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateRepositoryDetails(object):
    """
    The information to be updated.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateRepositoryDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this UpdateRepositoryDetails.
        :type name: str

        :param description:
            The value to assign to the description property of this UpdateRepositoryDetails.
        :type description: str

        :param default_branch:
            The value to assign to the default_branch property of this UpdateRepositoryDetails.
        :type default_branch: str

        :param repository_type:
            The value to assign to the repository_type property of this UpdateRepositoryDetails.
        :type repository_type: str

        :param mirror_repository_config:
            The value to assign to the mirror_repository_config property of this UpdateRepositoryDetails.
        :type mirror_repository_config: oci.devops.models.MirrorRepositoryConfig

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateRepositoryDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateRepositoryDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'default_branch': 'str',
            'repository_type': 'str',
            'mirror_repository_config': 'MirrorRepositoryConfig',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'default_branch': 'defaultBranch',
            'repository_type': 'repositoryType',
            'mirror_repository_config': 'mirrorRepositoryConfig',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._name = None
        self._description = None
        self._default_branch = None
        self._repository_type = None
        self._mirror_repository_config = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def name(self):
        """
        Gets the name of this UpdateRepositoryDetails.
        Unique name of a repository.


        :return: The name of this UpdateRepositoryDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this UpdateRepositoryDetails.
        Unique name of a repository.


        :param name: The name of this UpdateRepositoryDetails.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this UpdateRepositoryDetails.
        Details of the repository. Avoid entering confidential information.


        :return: The description of this UpdateRepositoryDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateRepositoryDetails.
        Details of the repository. Avoid entering confidential information.


        :param description: The description of this UpdateRepositoryDetails.
        :type: str
        """
        self._description = description

    @property
    def default_branch(self):
        """
        Gets the default_branch of this UpdateRepositoryDetails.
        The default branch of the repository.


        :return: The default_branch of this UpdateRepositoryDetails.
        :rtype: str
        """
        return self._default_branch

    @default_branch.setter
    def default_branch(self, default_branch):
        """
        Sets the default_branch of this UpdateRepositoryDetails.
        The default branch of the repository.


        :param default_branch: The default_branch of this UpdateRepositoryDetails.
        :type: str
        """
        self._default_branch = default_branch

    @property
    def repository_type(self):
        """
        Gets the repository_type of this UpdateRepositoryDetails.
        Type of repository. Allowed values:
        `MIRRORED`
        `HOSTED`


        :return: The repository_type of this UpdateRepositoryDetails.
        :rtype: str
        """
        return self._repository_type

    @repository_type.setter
    def repository_type(self, repository_type):
        """
        Sets the repository_type of this UpdateRepositoryDetails.
        Type of repository. Allowed values:
        `MIRRORED`
        `HOSTED`


        :param repository_type: The repository_type of this UpdateRepositoryDetails.
        :type: str
        """
        self._repository_type = repository_type

    @property
    def mirror_repository_config(self):
        """
        Gets the mirror_repository_config of this UpdateRepositoryDetails.

        :return: The mirror_repository_config of this UpdateRepositoryDetails.
        :rtype: oci.devops.models.MirrorRepositoryConfig
        """
        return self._mirror_repository_config

    @mirror_repository_config.setter
    def mirror_repository_config(self, mirror_repository_config):
        """
        Sets the mirror_repository_config of this UpdateRepositoryDetails.

        :param mirror_repository_config: The mirror_repository_config of this UpdateRepositoryDetails.
        :type: oci.devops.models.MirrorRepositoryConfig
        """
        self._mirror_repository_config = mirror_repository_config

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateRepositoryDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.  See `Resource Tags`__. Example: `{\"bar-key\": \"value\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateRepositoryDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateRepositoryDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.  See `Resource Tags`__. Example: `{\"bar-key\": \"value\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateRepositoryDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateRepositoryDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. See `Resource Tags`__. Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateRepositoryDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateRepositoryDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. See `Resource Tags`__. Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateRepositoryDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
