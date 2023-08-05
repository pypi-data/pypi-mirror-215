# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DeliverArtifact(object):
    """
    Artifact information that need to be pushed to the artifactory stores.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DeliverArtifact object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param artifact_name:
            The value to assign to the artifact_name property of this DeliverArtifact.
        :type artifact_name: str

        :param artifact_id:
            The value to assign to the artifact_id property of this DeliverArtifact.
        :type artifact_id: str

        """
        self.swagger_types = {
            'artifact_name': 'str',
            'artifact_id': 'str'
        }

        self.attribute_map = {
            'artifact_name': 'artifactName',
            'artifact_id': 'artifactId'
        }

        self._artifact_name = None
        self._artifact_id = None

    @property
    def artifact_name(self):
        """
        **[Required]** Gets the artifact_name of this DeliverArtifact.
        Name of the artifact specified in the build_spec.yaml file.


        :return: The artifact_name of this DeliverArtifact.
        :rtype: str
        """
        return self._artifact_name

    @artifact_name.setter
    def artifact_name(self, artifact_name):
        """
        Sets the artifact_name of this DeliverArtifact.
        Name of the artifact specified in the build_spec.yaml file.


        :param artifact_name: The artifact_name of this DeliverArtifact.
        :type: str
        """
        self._artifact_name = artifact_name

    @property
    def artifact_id(self):
        """
        **[Required]** Gets the artifact_id of this DeliverArtifact.
        Artifact identifier that contains the artifact definition.


        :return: The artifact_id of this DeliverArtifact.
        :rtype: str
        """
        return self._artifact_id

    @artifact_id.setter
    def artifact_id(self, artifact_id):
        """
        Sets the artifact_id of this DeliverArtifact.
        Artifact identifier that contains the artifact definition.


        :param artifact_id: The artifact_id of this DeliverArtifact.
        :type: str
        """
        self._artifact_id = artifact_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
