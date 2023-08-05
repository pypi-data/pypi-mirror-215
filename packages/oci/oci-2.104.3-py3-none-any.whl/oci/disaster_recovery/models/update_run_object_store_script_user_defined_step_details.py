# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_dr_plan_user_defined_step_details import UpdateDrPlanUserDefinedStepDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateRunObjectStoreScriptUserDefinedStepDetails(UpdateDrPlanUserDefinedStepDetails):
    """
    The details for updating a Run Object Store Script step.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateRunObjectStoreScriptUserDefinedStepDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.disaster_recovery.models.UpdateRunObjectStoreScriptUserDefinedStepDetails.step_type` attribute
        of this class is ``RUN_OBJECTSTORE_SCRIPT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param step_type:
            The value to assign to the step_type property of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
            Allowed values for this property are: "RUN_OBJECTSTORE_SCRIPT_PRECHECK", "RUN_LOCAL_SCRIPT_PRECHECK", "INVOKE_FUNCTION_PRECHECK", "RUN_OBJECTSTORE_SCRIPT", "RUN_LOCAL_SCRIPT", "INVOKE_FUNCTION"
        :type step_type: str

        :param run_on_instance_id:
            The value to assign to the run_on_instance_id property of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        :type run_on_instance_id: str

        :param object_storage_script_location:
            The value to assign to the object_storage_script_location property of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        :type object_storage_script_location: oci.disaster_recovery.models.UpdateObjectStorageScriptLocationDetails

        """
        self.swagger_types = {
            'step_type': 'str',
            'run_on_instance_id': 'str',
            'object_storage_script_location': 'UpdateObjectStorageScriptLocationDetails'
        }

        self.attribute_map = {
            'step_type': 'stepType',
            'run_on_instance_id': 'runOnInstanceId',
            'object_storage_script_location': 'objectStorageScriptLocation'
        }

        self._step_type = None
        self._run_on_instance_id = None
        self._object_storage_script_location = None
        self._step_type = 'RUN_OBJECTSTORE_SCRIPT'

    @property
    def run_on_instance_id(self):
        """
        Gets the run_on_instance_id of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        The OCID of the instance where this script or command should be executed.


        :return: The run_on_instance_id of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        :rtype: str
        """
        return self._run_on_instance_id

    @run_on_instance_id.setter
    def run_on_instance_id(self, run_on_instance_id):
        """
        Sets the run_on_instance_id of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        The OCID of the instance where this script or command should be executed.


        :param run_on_instance_id: The run_on_instance_id of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        :type: str
        """
        self._run_on_instance_id = run_on_instance_id

    @property
    def object_storage_script_location(self):
        """
        Gets the object_storage_script_location of this UpdateRunObjectStoreScriptUserDefinedStepDetails.

        :return: The object_storage_script_location of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        :rtype: oci.disaster_recovery.models.UpdateObjectStorageScriptLocationDetails
        """
        return self._object_storage_script_location

    @object_storage_script_location.setter
    def object_storage_script_location(self, object_storage_script_location):
        """
        Sets the object_storage_script_location of this UpdateRunObjectStoreScriptUserDefinedStepDetails.

        :param object_storage_script_location: The object_storage_script_location of this UpdateRunObjectStoreScriptUserDefinedStepDetails.
        :type: oci.disaster_recovery.models.UpdateObjectStorageScriptLocationDetails
        """
        self._object_storage_script_location = object_storage_script_location

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
