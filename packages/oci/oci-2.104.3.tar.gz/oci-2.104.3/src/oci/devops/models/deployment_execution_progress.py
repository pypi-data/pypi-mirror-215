# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DeploymentExecutionProgress(object):
    """
    The execution progress details of a deployment.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DeploymentExecutionProgress object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_started:
            The value to assign to the time_started property of this DeploymentExecutionProgress.
        :type time_started: datetime

        :param time_finished:
            The value to assign to the time_finished property of this DeploymentExecutionProgress.
        :type time_finished: datetime

        :param deploy_stage_execution_progress:
            The value to assign to the deploy_stage_execution_progress property of this DeploymentExecutionProgress.
        :type deploy_stage_execution_progress: dict(str, DeployStageExecutionProgress)

        """
        self.swagger_types = {
            'time_started': 'datetime',
            'time_finished': 'datetime',
            'deploy_stage_execution_progress': 'dict(str, DeployStageExecutionProgress)'
        }

        self.attribute_map = {
            'time_started': 'timeStarted',
            'time_finished': 'timeFinished',
            'deploy_stage_execution_progress': 'deployStageExecutionProgress'
        }

        self._time_started = None
        self._time_finished = None
        self._deploy_stage_execution_progress = None

    @property
    def time_started(self):
        """
        Gets the time_started of this DeploymentExecutionProgress.
        Time the deployment is started. Format defined by `RFC3339`__.

        __ https://datatracker.ietf.org/doc/html/rfc3339


        :return: The time_started of this DeploymentExecutionProgress.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this DeploymentExecutionProgress.
        Time the deployment is started. Format defined by `RFC3339`__.

        __ https://datatracker.ietf.org/doc/html/rfc3339


        :param time_started: The time_started of this DeploymentExecutionProgress.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        Gets the time_finished of this DeploymentExecutionProgress.
        Time the deployment is finished. Format defined by `RFC3339`__.

        __ https://datatracker.ietf.org/doc/html/rfc3339


        :return: The time_finished of this DeploymentExecutionProgress.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this DeploymentExecutionProgress.
        Time the deployment is finished. Format defined by `RFC3339`__.

        __ https://datatracker.ietf.org/doc/html/rfc3339


        :param time_finished: The time_finished of this DeploymentExecutionProgress.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def deploy_stage_execution_progress(self):
        """
        Gets the deploy_stage_execution_progress of this DeploymentExecutionProgress.
        Map of stage OCIDs to deploy stage execution progress model.


        :return: The deploy_stage_execution_progress of this DeploymentExecutionProgress.
        :rtype: dict(str, DeployStageExecutionProgress)
        """
        return self._deploy_stage_execution_progress

    @deploy_stage_execution_progress.setter
    def deploy_stage_execution_progress(self, deploy_stage_execution_progress):
        """
        Sets the deploy_stage_execution_progress of this DeploymentExecutionProgress.
        Map of stage OCIDs to deploy stage execution progress model.


        :param deploy_stage_execution_progress: The deploy_stage_execution_progress of this DeploymentExecutionProgress.
        :type: dict(str, DeployStageExecutionProgress)
        """
        self._deploy_stage_execution_progress = deploy_stage_execution_progress

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
