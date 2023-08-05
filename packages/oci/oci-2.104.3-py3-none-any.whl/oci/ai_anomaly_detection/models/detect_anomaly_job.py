# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectAnomalyJob(object):
    """
    Anomaly Job contains information for asynchronous detection of anomalies.
    """

    #: A constant which can be used with the lifecycle_state property of a DetectAnomalyJob.
    #: This constant has a value of "SUCCEEDED"
    LIFECYCLE_STATE_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the lifecycle_state property of a DetectAnomalyJob.
    #: This constant has a value of "PARTIALLY_SUCCEEDED"
    LIFECYCLE_STATE_PARTIALLY_SUCCEEDED = "PARTIALLY_SUCCEEDED"

    #: A constant which can be used with the lifecycle_state property of a DetectAnomalyJob.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a DetectAnomalyJob.
    #: This constant has a value of "ACCEPTED"
    LIFECYCLE_STATE_ACCEPTED = "ACCEPTED"

    #: A constant which can be used with the lifecycle_state property of a DetectAnomalyJob.
    #: This constant has a value of "CANCELED"
    LIFECYCLE_STATE_CANCELED = "CANCELED"

    #: A constant which can be used with the lifecycle_state property of a DetectAnomalyJob.
    #: This constant has a value of "IN_PROGRESS"
    LIFECYCLE_STATE_IN_PROGRESS = "IN_PROGRESS"

    def __init__(self, **kwargs):
        """
        Initializes a new DetectAnomalyJob object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DetectAnomalyJob.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DetectAnomalyJob.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this DetectAnomalyJob.
        :type display_name: str

        :param description:
            The value to assign to the description property of this DetectAnomalyJob.
        :type description: str

        :param model_id:
            The value to assign to the model_id property of this DetectAnomalyJob.
        :type model_id: str

        :param project_id:
            The value to assign to the project_id property of this DetectAnomalyJob.
        :type project_id: str

        :param sensitivity:
            The value to assign to the sensitivity property of this DetectAnomalyJob.
        :type sensitivity: float

        :param are_all_estimates_required:
            The value to assign to the are_all_estimates_required property of this DetectAnomalyJob.
        :type are_all_estimates_required: bool

        :param input_details:
            The value to assign to the input_details property of this DetectAnomalyJob.
        :type input_details: oci.ai_anomaly_detection.models.InputJobDetails

        :param output_details:
            The value to assign to the output_details property of this DetectAnomalyJob.
        :type output_details: oci.ai_anomaly_detection.models.OutputJobDetails

        :param time_accepted:
            The value to assign to the time_accepted property of this DetectAnomalyJob.
        :type time_accepted: datetime

        :param time_started:
            The value to assign to the time_started property of this DetectAnomalyJob.
        :type time_started: datetime

        :param time_finished:
            The value to assign to the time_finished property of this DetectAnomalyJob.
        :type time_finished: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DetectAnomalyJob.
            Allowed values for this property are: "SUCCEEDED", "PARTIALLY_SUCCEEDED", "FAILED", "ACCEPTED", "CANCELED", "IN_PROGRESS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_state_details:
            The value to assign to the lifecycle_state_details property of this DetectAnomalyJob.
        :type lifecycle_state_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DetectAnomalyJob.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DetectAnomalyJob.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this DetectAnomalyJob.
        :type system_tags: dict(str, object)

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'model_id': 'str',
            'project_id': 'str',
            'sensitivity': 'float',
            'are_all_estimates_required': 'bool',
            'input_details': 'InputJobDetails',
            'output_details': 'OutputJobDetails',
            'time_accepted': 'datetime',
            'time_started': 'datetime',
            'time_finished': 'datetime',
            'lifecycle_state': 'str',
            'lifecycle_state_details': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, object)'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'model_id': 'modelId',
            'project_id': 'projectId',
            'sensitivity': 'sensitivity',
            'are_all_estimates_required': 'areAllEstimatesRequired',
            'input_details': 'inputDetails',
            'output_details': 'outputDetails',
            'time_accepted': 'timeAccepted',
            'time_started': 'timeStarted',
            'time_finished': 'timeFinished',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_state_details': 'lifecycleStateDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._model_id = None
        self._project_id = None
        self._sensitivity = None
        self._are_all_estimates_required = None
        self._input_details = None
        self._output_details = None
        self._time_accepted = None
        self._time_started = None
        self._time_finished = None
        self._lifecycle_state = None
        self._lifecycle_state_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this DetectAnomalyJob.
        Id of the job.


        :return: The id of this DetectAnomalyJob.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DetectAnomalyJob.
        Id of the job.


        :param id: The id of this DetectAnomalyJob.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DetectAnomalyJob.
        The OCID of the compartment that starts the job.


        :return: The compartment_id of this DetectAnomalyJob.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DetectAnomalyJob.
        The OCID of the compartment that starts the job.


        :param compartment_id: The compartment_id of this DetectAnomalyJob.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this DetectAnomalyJob.
        Detect anomaly job display name.


        :return: The display_name of this DetectAnomalyJob.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DetectAnomalyJob.
        Detect anomaly job display name.


        :param display_name: The display_name of this DetectAnomalyJob.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this DetectAnomalyJob.
        Detect anomaly job description.


        :return: The description of this DetectAnomalyJob.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DetectAnomalyJob.
        Detect anomaly job description.


        :param description: The description of this DetectAnomalyJob.
        :type: str
        """
        self._description = description

    @property
    def model_id(self):
        """
        **[Required]** Gets the model_id of this DetectAnomalyJob.
        The OCID of the trained model.


        :return: The model_id of this DetectAnomalyJob.
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """
        Sets the model_id of this DetectAnomalyJob.
        The OCID of the trained model.


        :param model_id: The model_id of this DetectAnomalyJob.
        :type: str
        """
        self._model_id = model_id

    @property
    def project_id(self):
        """
        Gets the project_id of this DetectAnomalyJob.
        The OCID of the project.


        :return: The project_id of this DetectAnomalyJob.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """
        Sets the project_id of this DetectAnomalyJob.
        The OCID of the project.


        :param project_id: The project_id of this DetectAnomalyJob.
        :type: str
        """
        self._project_id = project_id

    @property
    def sensitivity(self):
        """
        Gets the sensitivity of this DetectAnomalyJob.
        The value that customer can adjust to control the sensitivity of anomaly detection


        :return: The sensitivity of this DetectAnomalyJob.
        :rtype: float
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, sensitivity):
        """
        Sets the sensitivity of this DetectAnomalyJob.
        The value that customer can adjust to control the sensitivity of anomaly detection


        :param sensitivity: The sensitivity of this DetectAnomalyJob.
        :type: float
        """
        self._sensitivity = sensitivity

    @property
    def are_all_estimates_required(self):
        """
        Gets the are_all_estimates_required of this DetectAnomalyJob.
        Flag to enable the service to return estimates for all data points rather than just the anomalous data points


        :return: The are_all_estimates_required of this DetectAnomalyJob.
        :rtype: bool
        """
        return self._are_all_estimates_required

    @are_all_estimates_required.setter
    def are_all_estimates_required(self, are_all_estimates_required):
        """
        Sets the are_all_estimates_required of this DetectAnomalyJob.
        Flag to enable the service to return estimates for all data points rather than just the anomalous data points


        :param are_all_estimates_required: The are_all_estimates_required of this DetectAnomalyJob.
        :type: bool
        """
        self._are_all_estimates_required = are_all_estimates_required

    @property
    def input_details(self):
        """
        **[Required]** Gets the input_details of this DetectAnomalyJob.

        :return: The input_details of this DetectAnomalyJob.
        :rtype: oci.ai_anomaly_detection.models.InputJobDetails
        """
        return self._input_details

    @input_details.setter
    def input_details(self, input_details):
        """
        Sets the input_details of this DetectAnomalyJob.

        :param input_details: The input_details of this DetectAnomalyJob.
        :type: oci.ai_anomaly_detection.models.InputJobDetails
        """
        self._input_details = input_details

    @property
    def output_details(self):
        """
        **[Required]** Gets the output_details of this DetectAnomalyJob.

        :return: The output_details of this DetectAnomalyJob.
        :rtype: oci.ai_anomaly_detection.models.OutputJobDetails
        """
        return self._output_details

    @output_details.setter
    def output_details(self, output_details):
        """
        Sets the output_details of this DetectAnomalyJob.

        :param output_details: The output_details of this DetectAnomalyJob.
        :type: oci.ai_anomaly_detection.models.OutputJobDetails
        """
        self._output_details = output_details

    @property
    def time_accepted(self):
        """
        **[Required]** Gets the time_accepted of this DetectAnomalyJob.
        Job accepted time


        :return: The time_accepted of this DetectAnomalyJob.
        :rtype: datetime
        """
        return self._time_accepted

    @time_accepted.setter
    def time_accepted(self, time_accepted):
        """
        Sets the time_accepted of this DetectAnomalyJob.
        Job accepted time


        :param time_accepted: The time_accepted of this DetectAnomalyJob.
        :type: datetime
        """
        self._time_accepted = time_accepted

    @property
    def time_started(self):
        """
        Gets the time_started of this DetectAnomalyJob.
        Job started time


        :return: The time_started of this DetectAnomalyJob.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this DetectAnomalyJob.
        Job started time


        :param time_started: The time_started of this DetectAnomalyJob.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        Gets the time_finished of this DetectAnomalyJob.
        Job finished time


        :return: The time_finished of this DetectAnomalyJob.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this DetectAnomalyJob.
        Job finished time


        :param time_finished: The time_finished of this DetectAnomalyJob.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this DetectAnomalyJob.
        The current state of the batch document job.

        Allowed values for this property are: "SUCCEEDED", "PARTIALLY_SUCCEEDED", "FAILED", "ACCEPTED", "CANCELED", "IN_PROGRESS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this DetectAnomalyJob.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DetectAnomalyJob.
        The current state of the batch document job.


        :param lifecycle_state: The lifecycle_state of this DetectAnomalyJob.
        :type: str
        """
        allowed_values = ["SUCCEEDED", "PARTIALLY_SUCCEEDED", "FAILED", "ACCEPTED", "CANCELED", "IN_PROGRESS"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_state_details(self):
        """
        Gets the lifecycle_state_details of this DetectAnomalyJob.
        The current state details of the batch document job.


        :return: The lifecycle_state_details of this DetectAnomalyJob.
        :rtype: str
        """
        return self._lifecycle_state_details

    @lifecycle_state_details.setter
    def lifecycle_state_details(self, lifecycle_state_details):
        """
        Sets the lifecycle_state_details of this DetectAnomalyJob.
        The current state details of the batch document job.


        :param lifecycle_state_details: The lifecycle_state_details of this DetectAnomalyJob.
        :type: str
        """
        self._lifecycle_state_details = lifecycle_state_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DetectAnomalyJob.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this DetectAnomalyJob.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DetectAnomalyJob.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this DetectAnomalyJob.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DetectAnomalyJob.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this DetectAnomalyJob.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DetectAnomalyJob.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this DetectAnomalyJob.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DetectAnomalyJob.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{ \"orcl-cloud\": { \"free-tier-retained\": \"true\" } }`


        :return: The system_tags of this DetectAnomalyJob.
        :rtype: dict(str, object)
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DetectAnomalyJob.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{ \"orcl-cloud\": { \"free-tier-retained\": \"true\" } }`


        :param system_tags: The system_tags of this DetectAnomalyJob.
        :type: dict(str, object)
        """
        self._system_tags = system_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
