# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_deploy_stage_details import UpdateDeployStageDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateComputeInstanceGroupBlueGreenDeployStageDetails(UpdateDeployStageDetails):
    """
    Specifies the Instance Group Blue-Green deployment stage.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateComputeInstanceGroupBlueGreenDeployStageDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.UpdateComputeInstanceGroupBlueGreenDeployStageDetails.deploy_stage_type` attribute
        of this class is ``COMPUTE_INSTANCE_GROUP_BLUE_GREEN_DEPLOYMENT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param description:
            The value to assign to the description property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type description: str

        :param display_name:
            The value to assign to the display_name property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type display_name: str

        :param deploy_stage_type:
            The value to assign to the deploy_stage_type property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type deploy_stage_type: str

        :param deploy_stage_predecessor_collection:
            The value to assign to the deploy_stage_predecessor_collection property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type deploy_stage_predecessor_collection: oci.devops.models.DeployStagePredecessorCollection

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param deployment_spec_deploy_artifact_id:
            The value to assign to the deployment_spec_deploy_artifact_id property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type deployment_spec_deploy_artifact_id: str

        :param deploy_artifact_ids:
            The value to assign to the deploy_artifact_ids property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type deploy_artifact_ids: list[str]

        :param rollout_policy:
            The value to assign to the rollout_policy property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type rollout_policy: oci.devops.models.ComputeInstanceGroupRolloutPolicy

        :param failure_policy:
            The value to assign to the failure_policy property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type failure_policy: oci.devops.models.ComputeInstanceGroupFailurePolicy

        :param test_load_balancer_config:
            The value to assign to the test_load_balancer_config property of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type test_load_balancer_config: oci.devops.models.LoadBalancerConfig

        """
        self.swagger_types = {
            'description': 'str',
            'display_name': 'str',
            'deploy_stage_type': 'str',
            'deploy_stage_predecessor_collection': 'DeployStagePredecessorCollection',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'deployment_spec_deploy_artifact_id': 'str',
            'deploy_artifact_ids': 'list[str]',
            'rollout_policy': 'ComputeInstanceGroupRolloutPolicy',
            'failure_policy': 'ComputeInstanceGroupFailurePolicy',
            'test_load_balancer_config': 'LoadBalancerConfig'
        }

        self.attribute_map = {
            'description': 'description',
            'display_name': 'displayName',
            'deploy_stage_type': 'deployStageType',
            'deploy_stage_predecessor_collection': 'deployStagePredecessorCollection',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'deployment_spec_deploy_artifact_id': 'deploymentSpecDeployArtifactId',
            'deploy_artifact_ids': 'deployArtifactIds',
            'rollout_policy': 'rolloutPolicy',
            'failure_policy': 'failurePolicy',
            'test_load_balancer_config': 'testLoadBalancerConfig'
        }

        self._description = None
        self._display_name = None
        self._deploy_stage_type = None
        self._deploy_stage_predecessor_collection = None
        self._freeform_tags = None
        self._defined_tags = None
        self._deployment_spec_deploy_artifact_id = None
        self._deploy_artifact_ids = None
        self._rollout_policy = None
        self._failure_policy = None
        self._test_load_balancer_config = None
        self._deploy_stage_type = 'COMPUTE_INSTANCE_GROUP_BLUE_GREEN_DEPLOYMENT'

    @property
    def deployment_spec_deploy_artifact_id(self):
        """
        Gets the deployment_spec_deploy_artifact_id of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        The OCID of the artifact that contains the deployment specification.


        :return: The deployment_spec_deploy_artifact_id of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :rtype: str
        """
        return self._deployment_spec_deploy_artifact_id

    @deployment_spec_deploy_artifact_id.setter
    def deployment_spec_deploy_artifact_id(self, deployment_spec_deploy_artifact_id):
        """
        Sets the deployment_spec_deploy_artifact_id of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        The OCID of the artifact that contains the deployment specification.


        :param deployment_spec_deploy_artifact_id: The deployment_spec_deploy_artifact_id of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type: str
        """
        self._deployment_spec_deploy_artifact_id = deployment_spec_deploy_artifact_id

    @property
    def deploy_artifact_ids(self):
        """
        Gets the deploy_artifact_ids of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        The list of file artifact OCIDs to deploy.


        :return: The deploy_artifact_ids of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :rtype: list[str]
        """
        return self._deploy_artifact_ids

    @deploy_artifact_ids.setter
    def deploy_artifact_ids(self, deploy_artifact_ids):
        """
        Sets the deploy_artifact_ids of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        The list of file artifact OCIDs to deploy.


        :param deploy_artifact_ids: The deploy_artifact_ids of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type: list[str]
        """
        self._deploy_artifact_ids = deploy_artifact_ids

    @property
    def rollout_policy(self):
        """
        Gets the rollout_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.

        :return: The rollout_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :rtype: oci.devops.models.ComputeInstanceGroupRolloutPolicy
        """
        return self._rollout_policy

    @rollout_policy.setter
    def rollout_policy(self, rollout_policy):
        """
        Sets the rollout_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.

        :param rollout_policy: The rollout_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type: oci.devops.models.ComputeInstanceGroupRolloutPolicy
        """
        self._rollout_policy = rollout_policy

    @property
    def failure_policy(self):
        """
        Gets the failure_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.

        :return: The failure_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :rtype: oci.devops.models.ComputeInstanceGroupFailurePolicy
        """
        return self._failure_policy

    @failure_policy.setter
    def failure_policy(self, failure_policy):
        """
        Sets the failure_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.

        :param failure_policy: The failure_policy of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type: oci.devops.models.ComputeInstanceGroupFailurePolicy
        """
        self._failure_policy = failure_policy

    @property
    def test_load_balancer_config(self):
        """
        Gets the test_load_balancer_config of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.

        :return: The test_load_balancer_config of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :rtype: oci.devops.models.LoadBalancerConfig
        """
        return self._test_load_balancer_config

    @test_load_balancer_config.setter
    def test_load_balancer_config(self, test_load_balancer_config):
        """
        Sets the test_load_balancer_config of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.

        :param test_load_balancer_config: The test_load_balancer_config of this UpdateComputeInstanceGroupBlueGreenDeployStageDetails.
        :type: oci.devops.models.LoadBalancerConfig
        """
        self._test_load_balancer_config = test_load_balancer_config

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
