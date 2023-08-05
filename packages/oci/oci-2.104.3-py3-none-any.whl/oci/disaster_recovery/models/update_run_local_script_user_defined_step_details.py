# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_dr_plan_user_defined_step_details import UpdateDrPlanUserDefinedStepDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateRunLocalScriptUserDefinedStepDetails(UpdateDrPlanUserDefinedStepDetails):
    """
    The details for updating a Run Local Script step.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateRunLocalScriptUserDefinedStepDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.disaster_recovery.models.UpdateRunLocalScriptUserDefinedStepDetails.step_type` attribute
        of this class is ``RUN_LOCAL_SCRIPT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param step_type:
            The value to assign to the step_type property of this UpdateRunLocalScriptUserDefinedStepDetails.
            Allowed values for this property are: "RUN_OBJECTSTORE_SCRIPT_PRECHECK", "RUN_LOCAL_SCRIPT_PRECHECK", "INVOKE_FUNCTION_PRECHECK", "RUN_OBJECTSTORE_SCRIPT", "RUN_LOCAL_SCRIPT", "INVOKE_FUNCTION"
        :type step_type: str

        :param run_on_instance_id:
            The value to assign to the run_on_instance_id property of this UpdateRunLocalScriptUserDefinedStepDetails.
        :type run_on_instance_id: str

        :param script_command:
            The value to assign to the script_command property of this UpdateRunLocalScriptUserDefinedStepDetails.
        :type script_command: str

        :param run_as_user:
            The value to assign to the run_as_user property of this UpdateRunLocalScriptUserDefinedStepDetails.
        :type run_as_user: str

        """
        self.swagger_types = {
            'step_type': 'str',
            'run_on_instance_id': 'str',
            'script_command': 'str',
            'run_as_user': 'str'
        }

        self.attribute_map = {
            'step_type': 'stepType',
            'run_on_instance_id': 'runOnInstanceId',
            'script_command': 'scriptCommand',
            'run_as_user': 'runAsUser'
        }

        self._step_type = None
        self._run_on_instance_id = None
        self._script_command = None
        self._run_as_user = None
        self._step_type = 'RUN_LOCAL_SCRIPT'

    @property
    def run_on_instance_id(self):
        """
        Gets the run_on_instance_id of this UpdateRunLocalScriptUserDefinedStepDetails.
        The OCID of the instance where this script or command should be executed.

        Example: `ocid1.instance.oc1.phx.exampleocid1`


        :return: The run_on_instance_id of this UpdateRunLocalScriptUserDefinedStepDetails.
        :rtype: str
        """
        return self._run_on_instance_id

    @run_on_instance_id.setter
    def run_on_instance_id(self, run_on_instance_id):
        """
        Sets the run_on_instance_id of this UpdateRunLocalScriptUserDefinedStepDetails.
        The OCID of the instance where this script or command should be executed.

        Example: `ocid1.instance.oc1.phx.exampleocid1`


        :param run_on_instance_id: The run_on_instance_id of this UpdateRunLocalScriptUserDefinedStepDetails.
        :type: str
        """
        self._run_on_instance_id = run_on_instance_id

    @property
    def script_command(self):
        """
        Gets the script_command of this UpdateRunLocalScriptUserDefinedStepDetails.
        The script name and arguments.

        Example: `/usr/bin/python3 /home/opc/scripts/my_app_script.py arg1 arg2 arg3`


        :return: The script_command of this UpdateRunLocalScriptUserDefinedStepDetails.
        :rtype: str
        """
        return self._script_command

    @script_command.setter
    def script_command(self, script_command):
        """
        Sets the script_command of this UpdateRunLocalScriptUserDefinedStepDetails.
        The script name and arguments.

        Example: `/usr/bin/python3 /home/opc/scripts/my_app_script.py arg1 arg2 arg3`


        :param script_command: The script_command of this UpdateRunLocalScriptUserDefinedStepDetails.
        :type: str
        """
        self._script_command = script_command

    @property
    def run_as_user(self):
        """
        Gets the run_as_user of this UpdateRunLocalScriptUserDefinedStepDetails.
        The userid on the instance to be used for executing the script or command.

        Example: `opc`


        :return: The run_as_user of this UpdateRunLocalScriptUserDefinedStepDetails.
        :rtype: str
        """
        return self._run_as_user

    @run_as_user.setter
    def run_as_user(self, run_as_user):
        """
        Sets the run_as_user of this UpdateRunLocalScriptUserDefinedStepDetails.
        The userid on the instance to be used for executing the script or command.

        Example: `opc`


        :param run_as_user: The run_as_user of this UpdateRunLocalScriptUserDefinedStepDetails.
        :type: str
        """
        self._run_as_user = run_as_user

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
