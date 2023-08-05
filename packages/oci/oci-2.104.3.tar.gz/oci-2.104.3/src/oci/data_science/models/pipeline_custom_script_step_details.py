# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .pipeline_step_details import PipelineStepDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PipelineCustomScriptStepDetails(PipelineStepDetails):
    """
    The type of step where user provides the step artifact to be executed on an execution engine managed by the pipelines service.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PipelineCustomScriptStepDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_science.models.PipelineCustomScriptStepDetails.step_type` attribute
        of this class is ``CUSTOM_SCRIPT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param step_type:
            The value to assign to the step_type property of this PipelineCustomScriptStepDetails.
            Allowed values for this property are: "ML_JOB", "CUSTOM_SCRIPT"
        :type step_type: str

        :param step_name:
            The value to assign to the step_name property of this PipelineCustomScriptStepDetails.
        :type step_name: str

        :param description:
            The value to assign to the description property of this PipelineCustomScriptStepDetails.
        :type description: str

        :param depends_on:
            The value to assign to the depends_on property of this PipelineCustomScriptStepDetails.
        :type depends_on: list[str]

        :param step_configuration_details:
            The value to assign to the step_configuration_details property of this PipelineCustomScriptStepDetails.
        :type step_configuration_details: oci.data_science.models.PipelineStepConfigurationDetails

        :param step_infrastructure_configuration_details:
            The value to assign to the step_infrastructure_configuration_details property of this PipelineCustomScriptStepDetails.
        :type step_infrastructure_configuration_details: oci.data_science.models.PipelineInfrastructureConfigurationDetails

        :param is_artifact_uploaded:
            The value to assign to the is_artifact_uploaded property of this PipelineCustomScriptStepDetails.
        :type is_artifact_uploaded: bool

        """
        self.swagger_types = {
            'step_type': 'str',
            'step_name': 'str',
            'description': 'str',
            'depends_on': 'list[str]',
            'step_configuration_details': 'PipelineStepConfigurationDetails',
            'step_infrastructure_configuration_details': 'PipelineInfrastructureConfigurationDetails',
            'is_artifact_uploaded': 'bool'
        }

        self.attribute_map = {
            'step_type': 'stepType',
            'step_name': 'stepName',
            'description': 'description',
            'depends_on': 'dependsOn',
            'step_configuration_details': 'stepConfigurationDetails',
            'step_infrastructure_configuration_details': 'stepInfrastructureConfigurationDetails',
            'is_artifact_uploaded': 'isArtifactUploaded'
        }

        self._step_type = None
        self._step_name = None
        self._description = None
        self._depends_on = None
        self._step_configuration_details = None
        self._step_infrastructure_configuration_details = None
        self._is_artifact_uploaded = None
        self._step_type = 'CUSTOM_SCRIPT'

    @property
    def step_infrastructure_configuration_details(self):
        """
        Gets the step_infrastructure_configuration_details of this PipelineCustomScriptStepDetails.

        :return: The step_infrastructure_configuration_details of this PipelineCustomScriptStepDetails.
        :rtype: oci.data_science.models.PipelineInfrastructureConfigurationDetails
        """
        return self._step_infrastructure_configuration_details

    @step_infrastructure_configuration_details.setter
    def step_infrastructure_configuration_details(self, step_infrastructure_configuration_details):
        """
        Sets the step_infrastructure_configuration_details of this PipelineCustomScriptStepDetails.

        :param step_infrastructure_configuration_details: The step_infrastructure_configuration_details of this PipelineCustomScriptStepDetails.
        :type: oci.data_science.models.PipelineInfrastructureConfigurationDetails
        """
        self._step_infrastructure_configuration_details = step_infrastructure_configuration_details

    @property
    def is_artifact_uploaded(self):
        """
        Gets the is_artifact_uploaded of this PipelineCustomScriptStepDetails.
        A flag to indicate whether the artifact has been uploaded for this step or not.


        :return: The is_artifact_uploaded of this PipelineCustomScriptStepDetails.
        :rtype: bool
        """
        return self._is_artifact_uploaded

    @is_artifact_uploaded.setter
    def is_artifact_uploaded(self, is_artifact_uploaded):
        """
        Sets the is_artifact_uploaded of this PipelineCustomScriptStepDetails.
        A flag to indicate whether the artifact has been uploaded for this step or not.


        :param is_artifact_uploaded: The is_artifact_uploaded of this PipelineCustomScriptStepDetails.
        :type: bool
        """
        self._is_artifact_uploaded = is_artifact_uploaded

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
