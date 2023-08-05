# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ContainerImage(object):
    """
    Container image metadata.
    """

    #: A constant which can be used with the lifecycle_state property of a ContainerImage.
    #: This constant has a value of "AVAILABLE"
    LIFECYCLE_STATE_AVAILABLE = "AVAILABLE"

    #: A constant which can be used with the lifecycle_state property of a ContainerImage.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ContainerImage.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    def __init__(self, **kwargs):
        """
        Initializes a new ContainerImage object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this ContainerImage.
        :type compartment_id: str

        :param created_by:
            The value to assign to the created_by property of this ContainerImage.
        :type created_by: str

        :param digest:
            The value to assign to the digest property of this ContainerImage.
        :type digest: str

        :param display_name:
            The value to assign to the display_name property of this ContainerImage.
        :type display_name: str

        :param id:
            The value to assign to the id property of this ContainerImage.
        :type id: str

        :param layers:
            The value to assign to the layers property of this ContainerImage.
        :type layers: list[oci.artifacts.models.ContainerImageLayer]

        :param layers_size_in_bytes:
            The value to assign to the layers_size_in_bytes property of this ContainerImage.
        :type layers_size_in_bytes: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ContainerImage.
            Allowed values for this property are: "AVAILABLE", "DELETED", "DELETING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param manifest_size_in_bytes:
            The value to assign to the manifest_size_in_bytes property of this ContainerImage.
        :type manifest_size_in_bytes: int

        :param pull_count:
            The value to assign to the pull_count property of this ContainerImage.
        :type pull_count: int

        :param repository_id:
            The value to assign to the repository_id property of this ContainerImage.
        :type repository_id: str

        :param repository_name:
            The value to assign to the repository_name property of this ContainerImage.
        :type repository_name: str

        :param time_created:
            The value to assign to the time_created property of this ContainerImage.
        :type time_created: datetime

        :param time_last_pulled:
            The value to assign to the time_last_pulled property of this ContainerImage.
        :type time_last_pulled: datetime

        :param version:
            The value to assign to the version property of this ContainerImage.
        :type version: str

        :param versions:
            The value to assign to the versions property of this ContainerImage.
        :type versions: list[oci.artifacts.models.ContainerVersion]

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'created_by': 'str',
            'digest': 'str',
            'display_name': 'str',
            'id': 'str',
            'layers': 'list[ContainerImageLayer]',
            'layers_size_in_bytes': 'int',
            'lifecycle_state': 'str',
            'manifest_size_in_bytes': 'int',
            'pull_count': 'int',
            'repository_id': 'str',
            'repository_name': 'str',
            'time_created': 'datetime',
            'time_last_pulled': 'datetime',
            'version': 'str',
            'versions': 'list[ContainerVersion]'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'created_by': 'createdBy',
            'digest': 'digest',
            'display_name': 'displayName',
            'id': 'id',
            'layers': 'layers',
            'layers_size_in_bytes': 'layersSizeInBytes',
            'lifecycle_state': 'lifecycleState',
            'manifest_size_in_bytes': 'manifestSizeInBytes',
            'pull_count': 'pullCount',
            'repository_id': 'repositoryId',
            'repository_name': 'repositoryName',
            'time_created': 'timeCreated',
            'time_last_pulled': 'timeLastPulled',
            'version': 'version',
            'versions': 'versions'
        }

        self._compartment_id = None
        self._created_by = None
        self._digest = None
        self._display_name = None
        self._id = None
        self._layers = None
        self._layers_size_in_bytes = None
        self._lifecycle_state = None
        self._manifest_size_in_bytes = None
        self._pull_count = None
        self._repository_id = None
        self._repository_name = None
        self._time_created = None
        self._time_last_pulled = None
        self._version = None
        self._versions = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ContainerImage.
        The compartment OCID to which the container image belongs. Inferred from the container repository.


        :return: The compartment_id of this ContainerImage.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ContainerImage.
        The compartment OCID to which the container image belongs. Inferred from the container repository.


        :param compartment_id: The compartment_id of this ContainerImage.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def created_by(self):
        """
        **[Required]** Gets the created_by of this ContainerImage.
        The `OCID`__ of the user or principal that created the resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The created_by of this ContainerImage.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this ContainerImage.
        The `OCID`__ of the user or principal that created the resource.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param created_by: The created_by of this ContainerImage.
        :type: str
        """
        self._created_by = created_by

    @property
    def digest(self):
        """
        **[Required]** Gets the digest of this ContainerImage.
        The container image digest.


        :return: The digest of this ContainerImage.
        :rtype: str
        """
        return self._digest

    @digest.setter
    def digest(self, digest):
        """
        Sets the digest of this ContainerImage.
        The container image digest.


        :param digest: The digest of this ContainerImage.
        :type: str
        """
        self._digest = digest

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ContainerImage.
        The repository name and the most recent version associated with the image.
        If there are no versions associated with the image, then last known version and digest are used instead.
        If the last known version is unavailable, then 'unknown' is used instead of the version.

        Example: `ubuntu:latest` or `ubuntu:latest@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`


        :return: The display_name of this ContainerImage.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ContainerImage.
        The repository name and the most recent version associated with the image.
        If there are no versions associated with the image, then last known version and digest are used instead.
        If the last known version is unavailable, then 'unknown' is used instead of the version.

        Example: `ubuntu:latest` or `ubuntu:latest@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`


        :param display_name: The display_name of this ContainerImage.
        :type: str
        """
        self._display_name = display_name

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ContainerImage.
        The `OCID`__ of the container image.

        Example: `ocid1.containerimage.oc1..exampleuniqueID`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ContainerImage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ContainerImage.
        The `OCID`__ of the container image.

        Example: `ocid1.containerimage.oc1..exampleuniqueID`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ContainerImage.
        :type: str
        """
        self._id = id

    @property
    def layers(self):
        """
        **[Required]** Gets the layers of this ContainerImage.
        Layers of which the image is composed, ordered by the layer digest.


        :return: The layers of this ContainerImage.
        :rtype: list[oci.artifacts.models.ContainerImageLayer]
        """
        return self._layers

    @layers.setter
    def layers(self, layers):
        """
        Sets the layers of this ContainerImage.
        Layers of which the image is composed, ordered by the layer digest.


        :param layers: The layers of this ContainerImage.
        :type: list[oci.artifacts.models.ContainerImageLayer]
        """
        self._layers = layers

    @property
    def layers_size_in_bytes(self):
        """
        **[Required]** Gets the layers_size_in_bytes of this ContainerImage.
        The total size of the container image layers in bytes.


        :return: The layers_size_in_bytes of this ContainerImage.
        :rtype: int
        """
        return self._layers_size_in_bytes

    @layers_size_in_bytes.setter
    def layers_size_in_bytes(self, layers_size_in_bytes):
        """
        Sets the layers_size_in_bytes of this ContainerImage.
        The total size of the container image layers in bytes.


        :param layers_size_in_bytes: The layers_size_in_bytes of this ContainerImage.
        :type: int
        """
        self._layers_size_in_bytes = layers_size_in_bytes

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ContainerImage.
        The current state of the container image.

        Allowed values for this property are: "AVAILABLE", "DELETED", "DELETING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ContainerImage.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ContainerImage.
        The current state of the container image.


        :param lifecycle_state: The lifecycle_state of this ContainerImage.
        :type: str
        """
        allowed_values = ["AVAILABLE", "DELETED", "DELETING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def manifest_size_in_bytes(self):
        """
        **[Required]** Gets the manifest_size_in_bytes of this ContainerImage.
        The size of the container image manifest in bytes.


        :return: The manifest_size_in_bytes of this ContainerImage.
        :rtype: int
        """
        return self._manifest_size_in_bytes

    @manifest_size_in_bytes.setter
    def manifest_size_in_bytes(self, manifest_size_in_bytes):
        """
        Sets the manifest_size_in_bytes of this ContainerImage.
        The size of the container image manifest in bytes.


        :param manifest_size_in_bytes: The manifest_size_in_bytes of this ContainerImage.
        :type: int
        """
        self._manifest_size_in_bytes = manifest_size_in_bytes

    @property
    def pull_count(self):
        """
        **[Required]** Gets the pull_count of this ContainerImage.
        Total number of pulls.


        :return: The pull_count of this ContainerImage.
        :rtype: int
        """
        return self._pull_count

    @pull_count.setter
    def pull_count(self, pull_count):
        """
        Sets the pull_count of this ContainerImage.
        Total number of pulls.


        :param pull_count: The pull_count of this ContainerImage.
        :type: int
        """
        self._pull_count = pull_count

    @property
    def repository_id(self):
        """
        **[Required]** Gets the repository_id of this ContainerImage.
        The `OCID`__ of the container repository.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The repository_id of this ContainerImage.
        :rtype: str
        """
        return self._repository_id

    @repository_id.setter
    def repository_id(self, repository_id):
        """
        Sets the repository_id of this ContainerImage.
        The `OCID`__ of the container repository.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param repository_id: The repository_id of this ContainerImage.
        :type: str
        """
        self._repository_id = repository_id

    @property
    def repository_name(self):
        """
        **[Required]** Gets the repository_name of this ContainerImage.
        The container repository name.


        :return: The repository_name of this ContainerImage.
        :rtype: str
        """
        return self._repository_name

    @repository_name.setter
    def repository_name(self, repository_name):
        """
        Sets the repository_name of this ContainerImage.
        The container repository name.


        :param repository_name: The repository_name of this ContainerImage.
        :type: str
        """
        self._repository_name = repository_name

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ContainerImage.
        An RFC 3339 timestamp indicating when the image was created.


        :return: The time_created of this ContainerImage.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ContainerImage.
        An RFC 3339 timestamp indicating when the image was created.


        :param time_created: The time_created of this ContainerImage.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_last_pulled(self):
        """
        Gets the time_last_pulled of this ContainerImage.
        An RFC 3339 timestamp indicating when the image was last pulled.


        :return: The time_last_pulled of this ContainerImage.
        :rtype: datetime
        """
        return self._time_last_pulled

    @time_last_pulled.setter
    def time_last_pulled(self, time_last_pulled):
        """
        Sets the time_last_pulled of this ContainerImage.
        An RFC 3339 timestamp indicating when the image was last pulled.


        :param time_last_pulled: The time_last_pulled of this ContainerImage.
        :type: datetime
        """
        self._time_last_pulled = time_last_pulled

    @property
    def version(self):
        """
        Gets the version of this ContainerImage.
        The most recent version associated with this image.


        :return: The version of this ContainerImage.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ContainerImage.
        The most recent version associated with this image.


        :param version: The version of this ContainerImage.
        :type: str
        """
        self._version = version

    @property
    def versions(self):
        """
        **[Required]** Gets the versions of this ContainerImage.
        The versions associated with this image.


        :return: The versions of this ContainerImage.
        :rtype: list[oci.artifacts.models.ContainerVersion]
        """
        return self._versions

    @versions.setter
    def versions(self, versions):
        """
        Sets the versions of this ContainerImage.
        The versions associated with this image.


        :param versions: The versions of this ContainerImage.
        :type: list[oci.artifacts.models.ContainerVersion]
        """
        self._versions = versions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
