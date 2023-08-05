# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateModelDeploymentEnvironmentConfigurationDetails(object):
    """
    The configuration to carry the environment details thats used in Model Deployment update
    """

    #: A constant which can be used with the environment_configuration_type property of a UpdateModelDeploymentEnvironmentConfigurationDetails.
    #: This constant has a value of "DEFAULT"
    ENVIRONMENT_CONFIGURATION_TYPE_DEFAULT = "DEFAULT"

    #: A constant which can be used with the environment_configuration_type property of a UpdateModelDeploymentEnvironmentConfigurationDetails.
    #: This constant has a value of "OCIR_CONTAINER"
    ENVIRONMENT_CONFIGURATION_TYPE_OCIR_CONTAINER = "OCIR_CONTAINER"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateModelDeploymentEnvironmentConfigurationDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.data_science.models.UpdateDefaultModelDeploymentEnvironmentConfigurationDetails`
        * :class:`~oci.data_science.models.UpdateOcirModelDeploymentEnvironmentConfigurationDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param environment_configuration_type:
            The value to assign to the environment_configuration_type property of this UpdateModelDeploymentEnvironmentConfigurationDetails.
            Allowed values for this property are: "DEFAULT", "OCIR_CONTAINER"
        :type environment_configuration_type: str

        """
        self.swagger_types = {
            'environment_configuration_type': 'str'
        }

        self.attribute_map = {
            'environment_configuration_type': 'environmentConfigurationType'
        }

        self._environment_configuration_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['environmentConfigurationType']

        if type == 'DEFAULT':
            return 'UpdateDefaultModelDeploymentEnvironmentConfigurationDetails'

        if type == 'OCIR_CONTAINER':
            return 'UpdateOcirModelDeploymentEnvironmentConfigurationDetails'
        else:
            return 'UpdateModelDeploymentEnvironmentConfigurationDetails'

    @property
    def environment_configuration_type(self):
        """
        **[Required]** Gets the environment_configuration_type of this UpdateModelDeploymentEnvironmentConfigurationDetails.
        The environment configuration type

        Allowed values for this property are: "DEFAULT", "OCIR_CONTAINER"


        :return: The environment_configuration_type of this UpdateModelDeploymentEnvironmentConfigurationDetails.
        :rtype: str
        """
        return self._environment_configuration_type

    @environment_configuration_type.setter
    def environment_configuration_type(self, environment_configuration_type):
        """
        Sets the environment_configuration_type of this UpdateModelDeploymentEnvironmentConfigurationDetails.
        The environment configuration type


        :param environment_configuration_type: The environment_configuration_type of this UpdateModelDeploymentEnvironmentConfigurationDetails.
        :type: str
        """
        allowed_values = ["DEFAULT", "OCIR_CONTAINER"]
        if not value_allowed_none_or_none_sentinel(environment_configuration_type, allowed_values):
            raise ValueError(
                "Invalid value for `environment_configuration_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._environment_configuration_type = environment_configuration_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
