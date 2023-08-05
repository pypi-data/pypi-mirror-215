# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreatePipelineDetails(object):
    """
    The information about new Pipeline.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreatePipelineDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param project_id:
            The value to assign to the project_id property of this CreatePipelineDetails.
        :type project_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreatePipelineDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreatePipelineDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreatePipelineDetails.
        :type description: str

        :param configuration_details:
            The value to assign to the configuration_details property of this CreatePipelineDetails.
        :type configuration_details: oci.data_science.models.PipelineConfigurationDetails

        :param log_configuration_details:
            The value to assign to the log_configuration_details property of this CreatePipelineDetails.
        :type log_configuration_details: oci.data_science.models.PipelineLogConfigurationDetails

        :param infrastructure_configuration_details:
            The value to assign to the infrastructure_configuration_details property of this CreatePipelineDetails.
        :type infrastructure_configuration_details: oci.data_science.models.PipelineInfrastructureConfigurationDetails

        :param step_details:
            The value to assign to the step_details property of this CreatePipelineDetails.
        :type step_details: list[oci.data_science.models.PipelineStepDetails]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreatePipelineDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreatePipelineDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'project_id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'configuration_details': 'PipelineConfigurationDetails',
            'log_configuration_details': 'PipelineLogConfigurationDetails',
            'infrastructure_configuration_details': 'PipelineInfrastructureConfigurationDetails',
            'step_details': 'list[PipelineStepDetails]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'project_id': 'projectId',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'configuration_details': 'configurationDetails',
            'log_configuration_details': 'logConfigurationDetails',
            'infrastructure_configuration_details': 'infrastructureConfigurationDetails',
            'step_details': 'stepDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._project_id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._configuration_details = None
        self._log_configuration_details = None
        self._infrastructure_configuration_details = None
        self._step_details = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def project_id(self):
        """
        **[Required]** Gets the project_id of this CreatePipelineDetails.
        The `OCID`__ of the project to associate the pipeline with.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The project_id of this CreatePipelineDetails.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """
        Sets the project_id of this CreatePipelineDetails.
        The `OCID`__ of the project to associate the pipeline with.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param project_id: The project_id of this CreatePipelineDetails.
        :type: str
        """
        self._project_id = project_id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreatePipelineDetails.
        The `OCID`__ of the compartment where you want to create the pipeline.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreatePipelineDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreatePipelineDetails.
        The `OCID`__ of the compartment where you want to create the pipeline.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreatePipelineDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this CreatePipelineDetails.
        A user-friendly display name for the resource.


        :return: The display_name of this CreatePipelineDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreatePipelineDetails.
        A user-friendly display name for the resource.


        :param display_name: The display_name of this CreatePipelineDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this CreatePipelineDetails.
        A short description of the pipeline.


        :return: The description of this CreatePipelineDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreatePipelineDetails.
        A short description of the pipeline.


        :param description: The description of this CreatePipelineDetails.
        :type: str
        """
        self._description = description

    @property
    def configuration_details(self):
        """
        Gets the configuration_details of this CreatePipelineDetails.

        :return: The configuration_details of this CreatePipelineDetails.
        :rtype: oci.data_science.models.PipelineConfigurationDetails
        """
        return self._configuration_details

    @configuration_details.setter
    def configuration_details(self, configuration_details):
        """
        Sets the configuration_details of this CreatePipelineDetails.

        :param configuration_details: The configuration_details of this CreatePipelineDetails.
        :type: oci.data_science.models.PipelineConfigurationDetails
        """
        self._configuration_details = configuration_details

    @property
    def log_configuration_details(self):
        """
        Gets the log_configuration_details of this CreatePipelineDetails.

        :return: The log_configuration_details of this CreatePipelineDetails.
        :rtype: oci.data_science.models.PipelineLogConfigurationDetails
        """
        return self._log_configuration_details

    @log_configuration_details.setter
    def log_configuration_details(self, log_configuration_details):
        """
        Sets the log_configuration_details of this CreatePipelineDetails.

        :param log_configuration_details: The log_configuration_details of this CreatePipelineDetails.
        :type: oci.data_science.models.PipelineLogConfigurationDetails
        """
        self._log_configuration_details = log_configuration_details

    @property
    def infrastructure_configuration_details(self):
        """
        Gets the infrastructure_configuration_details of this CreatePipelineDetails.

        :return: The infrastructure_configuration_details of this CreatePipelineDetails.
        :rtype: oci.data_science.models.PipelineInfrastructureConfigurationDetails
        """
        return self._infrastructure_configuration_details

    @infrastructure_configuration_details.setter
    def infrastructure_configuration_details(self, infrastructure_configuration_details):
        """
        Sets the infrastructure_configuration_details of this CreatePipelineDetails.

        :param infrastructure_configuration_details: The infrastructure_configuration_details of this CreatePipelineDetails.
        :type: oci.data_science.models.PipelineInfrastructureConfigurationDetails
        """
        self._infrastructure_configuration_details = infrastructure_configuration_details

    @property
    def step_details(self):
        """
        **[Required]** Gets the step_details of this CreatePipelineDetails.
        Array of step details for each step.


        :return: The step_details of this CreatePipelineDetails.
        :rtype: list[oci.data_science.models.PipelineStepDetails]
        """
        return self._step_details

    @step_details.setter
    def step_details(self, step_details):
        """
        Sets the step_details of this CreatePipelineDetails.
        Array of step details for each step.


        :param step_details: The step_details of this CreatePipelineDetails.
        :type: list[oci.data_science.models.PipelineStepDetails]
        """
        self._step_details = step_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreatePipelineDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. See `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreatePipelineDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreatePipelineDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. See `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreatePipelineDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreatePipelineDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. See `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreatePipelineDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreatePipelineDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. See `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreatePipelineDetails.
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
