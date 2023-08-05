# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .model_deployment_environment_configuration_details import ModelDeploymentEnvironmentConfigurationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OcirModelDeploymentEnvironmentConfigurationDetails(ModelDeploymentEnvironmentConfigurationDetails):
    """
    The environment configuration details object for OCI Registry
    """

    def __init__(self, **kwargs):
        """
        Initializes a new OcirModelDeploymentEnvironmentConfigurationDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_science.models.OcirModelDeploymentEnvironmentConfigurationDetails.environment_configuration_type` attribute
        of this class is ``OCIR_CONTAINER`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param environment_configuration_type:
            The value to assign to the environment_configuration_type property of this OcirModelDeploymentEnvironmentConfigurationDetails.
            Allowed values for this property are: "DEFAULT", "OCIR_CONTAINER"
        :type environment_configuration_type: str

        :param image:
            The value to assign to the image property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type image: str

        :param image_digest:
            The value to assign to the image_digest property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type image_digest: str

        :param cmd:
            The value to assign to the cmd property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type cmd: list[str]

        :param entrypoint:
            The value to assign to the entrypoint property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type entrypoint: list[str]

        :param server_port:
            The value to assign to the server_port property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type server_port: int

        :param health_check_port:
            The value to assign to the health_check_port property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type health_check_port: int

        :param environment_variables:
            The value to assign to the environment_variables property of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type environment_variables: dict(str, str)

        """
        self.swagger_types = {
            'environment_configuration_type': 'str',
            'image': 'str',
            'image_digest': 'str',
            'cmd': 'list[str]',
            'entrypoint': 'list[str]',
            'server_port': 'int',
            'health_check_port': 'int',
            'environment_variables': 'dict(str, str)'
        }

        self.attribute_map = {
            'environment_configuration_type': 'environmentConfigurationType',
            'image': 'image',
            'image_digest': 'imageDigest',
            'cmd': 'cmd',
            'entrypoint': 'entrypoint',
            'server_port': 'serverPort',
            'health_check_port': 'healthCheckPort',
            'environment_variables': 'environmentVariables'
        }

        self._environment_configuration_type = None
        self._image = None
        self._image_digest = None
        self._cmd = None
        self._entrypoint = None
        self._server_port = None
        self._health_check_port = None
        self._environment_variables = None
        self._environment_configuration_type = 'OCIR_CONTAINER'

    @property
    def image(self):
        """
        **[Required]** Gets the image of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The full path to the Oracle Container Repository (OCIR) registry, image, and tag in a canonical format.
        Acceptable format:
        `<region>.ocir.io/<registry>/<image>:<tag>`
        `<region>.ocir.io/<registry>/<image>:<tag>@digest`


        :return: The image of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the image of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The full path to the Oracle Container Repository (OCIR) registry, image, and tag in a canonical format.
        Acceptable format:
        `<region>.ocir.io/<registry>/<image>:<tag>`
        `<region>.ocir.io/<registry>/<image>:<tag>@digest`


        :param image: The image of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: str
        """
        self._image = image

    @property
    def image_digest(self):
        """
        Gets the image_digest of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The digest of the container image. For example,
        `sha256:881303a6b2738834d795a32b4a98eb0e5e3d1cad590a712d1e04f9b2fa90a030`


        :return: The image_digest of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: str
        """
        return self._image_digest

    @image_digest.setter
    def image_digest(self, image_digest):
        """
        Sets the image_digest of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The digest of the container image. For example,
        `sha256:881303a6b2738834d795a32b4a98eb0e5e3d1cad590a712d1e04f9b2fa90a030`


        :param image_digest: The image_digest of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: str
        """
        self._image_digest = image_digest

    @property
    def cmd(self):
        """
        Gets the cmd of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The container image run `CMD`__ as a list of strings.
        Use `CMD` as arguments to the `ENTRYPOINT` or the only command to run in the absence of an `ENTRYPOINT`.
        The combined size of `CMD` and `ENTRYPOINT` must be less than 2048 bytes.

        __ https://docs.docker.com/engine/reference/builder/#cmd


        :return: The cmd of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: list[str]
        """
        return self._cmd

    @cmd.setter
    def cmd(self, cmd):
        """
        Sets the cmd of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The container image run `CMD`__ as a list of strings.
        Use `CMD` as arguments to the `ENTRYPOINT` or the only command to run in the absence of an `ENTRYPOINT`.
        The combined size of `CMD` and `ENTRYPOINT` must be less than 2048 bytes.

        __ https://docs.docker.com/engine/reference/builder/#cmd


        :param cmd: The cmd of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: list[str]
        """
        self._cmd = cmd

    @property
    def entrypoint(self):
        """
        Gets the entrypoint of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The container image run `ENTRYPOINT`__ as a list of strings.
        Accept the `CMD` as extra arguments.
        The combined size of `CMD` and `ENTRYPOINT` must be less than 2048 bytes.
        More information on how `CMD` and `ENTRYPOINT` interact are `here`__.

        __ https://docs.docker.com/engine/reference/builder/#entrypoint
        __ https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact


        :return: The entrypoint of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: list[str]
        """
        return self._entrypoint

    @entrypoint.setter
    def entrypoint(self, entrypoint):
        """
        Sets the entrypoint of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The container image run `ENTRYPOINT`__ as a list of strings.
        Accept the `CMD` as extra arguments.
        The combined size of `CMD` and `ENTRYPOINT` must be less than 2048 bytes.
        More information on how `CMD` and `ENTRYPOINT` interact are `here`__.

        __ https://docs.docker.com/engine/reference/builder/#entrypoint
        __ https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact


        :param entrypoint: The entrypoint of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: list[str]
        """
        self._entrypoint = entrypoint

    @property
    def server_port(self):
        """
        Gets the server_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The port on which the web server serving the inference is running.
        The port can be anything between `1024` and `65535`. The following ports cannot be used `24224`, `8446`, `8447`.


        :return: The server_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: int
        """
        return self._server_port

    @server_port.setter
    def server_port(self, server_port):
        """
        Sets the server_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The port on which the web server serving the inference is running.
        The port can be anything between `1024` and `65535`. The following ports cannot be used `24224`, `8446`, `8447`.


        :param server_port: The server_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: int
        """
        self._server_port = server_port

    @property
    def health_check_port(self):
        """
        Gets the health_check_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The port on which the container `HEALTHCHECK`__ would listen.
        The port can be anything between `1024` and `65535`. The following ports cannot be used `24224`, `8446`, `8447`.

        __ https://docs.docker.com/engine/reference/builder/#healthcheck


        :return: The health_check_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: int
        """
        return self._health_check_port

    @health_check_port.setter
    def health_check_port(self, health_check_port):
        """
        Sets the health_check_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        The port on which the container `HEALTHCHECK`__ would listen.
        The port can be anything between `1024` and `65535`. The following ports cannot be used `24224`, `8446`, `8447`.

        __ https://docs.docker.com/engine/reference/builder/#healthcheck


        :param health_check_port: The health_check_port of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: int
        """
        self._health_check_port = health_check_port

    @property
    def environment_variables(self):
        """
        Gets the environment_variables of this OcirModelDeploymentEnvironmentConfigurationDetails.
        Environment variables to set for the web server container.
        The size of envVars must be less than 2048 bytes.
        Key should be under 32 characters.
        Key should contain only letters, digits and underscore (_)
        Key should start with a letter.
        Key should have at least 2 characters.
        Key should not end with underscore eg. `TEST_`
        Key if added cannot be empty. Value can be empty.
        No specific size limits on individual Values. But overall environment variables is limited to 2048 bytes.
        Key can't be reserved Model Deployment environment variables.


        :return: The environment_variables of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :rtype: dict(str, str)
        """
        return self._environment_variables

    @environment_variables.setter
    def environment_variables(self, environment_variables):
        """
        Sets the environment_variables of this OcirModelDeploymentEnvironmentConfigurationDetails.
        Environment variables to set for the web server container.
        The size of envVars must be less than 2048 bytes.
        Key should be under 32 characters.
        Key should contain only letters, digits and underscore (_)
        Key should start with a letter.
        Key should have at least 2 characters.
        Key should not end with underscore eg. `TEST_`
        Key if added cannot be empty. Value can be empty.
        No specific size limits on individual Values. But overall environment variables is limited to 2048 bytes.
        Key can't be reserved Model Deployment environment variables.


        :param environment_variables: The environment_variables of this OcirModelDeploymentEnvironmentConfigurationDetails.
        :type: dict(str, str)
        """
        self._environment_variables = environment_variables

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
