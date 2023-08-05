# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectAnomalyJobSummary(object):
    """
    Anomaly Job summary contains minimal information for asynchronous inference of anomalies
    returned in list response.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DetectAnomalyJobSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this DetectAnomalyJobSummary.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this DetectAnomalyJobSummary.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this DetectAnomalyJobSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this DetectAnomalyJobSummary.
        :type description: str

        :param model_id:
            The value to assign to the model_id property of this DetectAnomalyJobSummary.
        :type model_id: str

        :param project_id:
            The value to assign to the project_id property of this DetectAnomalyJobSummary.
        :type project_id: str

        :param time_accepted:
            The value to assign to the time_accepted property of this DetectAnomalyJobSummary.
        :type time_accepted: datetime

        :param time_started:
            The value to assign to the time_started property of this DetectAnomalyJobSummary.
        :type time_started: datetime

        :param time_finished:
            The value to assign to the time_finished property of this DetectAnomalyJobSummary.
        :type time_finished: datetime

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this DetectAnomalyJobSummary.
        :type lifecycle_state: str

        :param lifecycle_state_details:
            The value to assign to the lifecycle_state_details property of this DetectAnomalyJobSummary.
        :type lifecycle_state_details: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this DetectAnomalyJobSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this DetectAnomalyJobSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this DetectAnomalyJobSummary.
        :type system_tags: dict(str, object)

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'model_id': 'str',
            'project_id': 'str',
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
        **[Required]** Gets the id of this DetectAnomalyJobSummary.
        Id of the job.


        :return: The id of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DetectAnomalyJobSummary.
        Id of the job.


        :param id: The id of this DetectAnomalyJobSummary.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DetectAnomalyJobSummary.
        The OCID of the compartment that starts the job.


        :return: The compartment_id of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DetectAnomalyJobSummary.
        The OCID of the compartment that starts the job.


        :param compartment_id: The compartment_id of this DetectAnomalyJobSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        Gets the display_name of this DetectAnomalyJobSummary.
        Detect anomaly job display name.


        :return: The display_name of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this DetectAnomalyJobSummary.
        Detect anomaly job display name.


        :param display_name: The display_name of this DetectAnomalyJobSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this DetectAnomalyJobSummary.
        Detect anomaly job description.


        :return: The description of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DetectAnomalyJobSummary.
        Detect anomaly job description.


        :param description: The description of this DetectAnomalyJobSummary.
        :type: str
        """
        self._description = description

    @property
    def model_id(self):
        """
        **[Required]** Gets the model_id of this DetectAnomalyJobSummary.
        The OCID of the trained model.


        :return: The model_id of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """
        Sets the model_id of this DetectAnomalyJobSummary.
        The OCID of the trained model.


        :param model_id: The model_id of this DetectAnomalyJobSummary.
        :type: str
        """
        self._model_id = model_id

    @property
    def project_id(self):
        """
        Gets the project_id of this DetectAnomalyJobSummary.
        The OCID of the project.


        :return: The project_id of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """
        Sets the project_id of this DetectAnomalyJobSummary.
        The OCID of the project.


        :param project_id: The project_id of this DetectAnomalyJobSummary.
        :type: str
        """
        self._project_id = project_id

    @property
    def time_accepted(self):
        """
        **[Required]** Gets the time_accepted of this DetectAnomalyJobSummary.
        Job accepted time


        :return: The time_accepted of this DetectAnomalyJobSummary.
        :rtype: datetime
        """
        return self._time_accepted

    @time_accepted.setter
    def time_accepted(self, time_accepted):
        """
        Sets the time_accepted of this DetectAnomalyJobSummary.
        Job accepted time


        :param time_accepted: The time_accepted of this DetectAnomalyJobSummary.
        :type: datetime
        """
        self._time_accepted = time_accepted

    @property
    def time_started(self):
        """
        Gets the time_started of this DetectAnomalyJobSummary.
        Job started time


        :return: The time_started of this DetectAnomalyJobSummary.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this DetectAnomalyJobSummary.
        Job started time


        :param time_started: The time_started of this DetectAnomalyJobSummary.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_finished(self):
        """
        Gets the time_finished of this DetectAnomalyJobSummary.
        Job finished time


        :return: The time_finished of this DetectAnomalyJobSummary.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this DetectAnomalyJobSummary.
        Job finished time


        :param time_finished: The time_finished of this DetectAnomalyJobSummary.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this DetectAnomalyJobSummary.
        The current state of the batch document job.


        :return: The lifecycle_state of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this DetectAnomalyJobSummary.
        The current state of the batch document job.


        :param lifecycle_state: The lifecycle_state of this DetectAnomalyJobSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_state_details(self):
        """
        Gets the lifecycle_state_details of this DetectAnomalyJobSummary.
        The current state details of the batch document job.


        :return: The lifecycle_state_details of this DetectAnomalyJobSummary.
        :rtype: str
        """
        return self._lifecycle_state_details

    @lifecycle_state_details.setter
    def lifecycle_state_details(self, lifecycle_state_details):
        """
        Sets the lifecycle_state_details of this DetectAnomalyJobSummary.
        The current state details of the batch document job.


        :param lifecycle_state_details: The lifecycle_state_details of this DetectAnomalyJobSummary.
        :type: str
        """
        self._lifecycle_state_details = lifecycle_state_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this DetectAnomalyJobSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this DetectAnomalyJobSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this DetectAnomalyJobSummary.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this DetectAnomalyJobSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this DetectAnomalyJobSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this DetectAnomalyJobSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this DetectAnomalyJobSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this DetectAnomalyJobSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this DetectAnomalyJobSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{ \"orcl-cloud\": { \"free-tier-retained\": \"true\" } }`


        :return: The system_tags of this DetectAnomalyJobSummary.
        :rtype: dict(str, object)
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this DetectAnomalyJobSummary.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{ \"orcl-cloud\": { \"free-tier-retained\": \"true\" } }`


        :param system_tags: The system_tags of this DetectAnomalyJobSummary.
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
