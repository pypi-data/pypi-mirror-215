# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class QueryWorkRequest(object):
    """
    Job details outlining parameters specified when job was submitted.
    """

    #: A constant which can be used with the status property of a QueryWorkRequest.
    #: This constant has a value of "ACCEPTED"
    STATUS_ACCEPTED = "ACCEPTED"

    #: A constant which can be used with the status property of a QueryWorkRequest.
    #: This constant has a value of "CANCELED"
    STATUS_CANCELED = "CANCELED"

    #: A constant which can be used with the status property of a QueryWorkRequest.
    #: This constant has a value of "FAILED"
    STATUS_FAILED = "FAILED"

    #: A constant which can be used with the status property of a QueryWorkRequest.
    #: This constant has a value of "IN_PROGRESS"
    STATUS_IN_PROGRESS = "IN_PROGRESS"

    #: A constant which can be used with the status property of a QueryWorkRequest.
    #: This constant has a value of "SUCCEEDED"
    STATUS_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the operation_type property of a QueryWorkRequest.
    #: This constant has a value of "EXECUTE_QUERY_JOB"
    OPERATION_TYPE_EXECUTE_QUERY_JOB = "EXECUTE_QUERY_JOB"

    #: A constant which can be used with the operation_type property of a QueryWorkRequest.
    #: This constant has a value of "EXECUTE_PURGE_JOB"
    OPERATION_TYPE_EXECUTE_PURGE_JOB = "EXECUTE_PURGE_JOB"

    #: A constant which can be used with the mode property of a QueryWorkRequest.
    #: This constant has a value of "FOREGROUND"
    MODE_FOREGROUND = "FOREGROUND"

    #: A constant which can be used with the mode property of a QueryWorkRequest.
    #: This constant has a value of "BACKGROUND"
    MODE_BACKGROUND = "BACKGROUND"

    #: A constant which can be used with the sub_system property of a QueryWorkRequest.
    #: This constant has a value of "LOG"
    SUB_SYSTEM_LOG = "LOG"

    def __init__(self, **kwargs):
        """
        Initializes a new QueryWorkRequest object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this QueryWorkRequest.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this QueryWorkRequest.
        :type compartment_id: str

        :param time_started:
            The value to assign to the time_started property of this QueryWorkRequest.
        :type time_started: datetime

        :param time_accepted:
            The value to assign to the time_accepted property of this QueryWorkRequest.
        :type time_accepted: datetime

        :param time_finished:
            The value to assign to the time_finished property of this QueryWorkRequest.
        :type time_finished: datetime

        :param time_expires:
            The value to assign to the time_expires property of this QueryWorkRequest.
        :type time_expires: datetime

        :param percent_complete:
            The value to assign to the percent_complete property of this QueryWorkRequest.
        :type percent_complete: int

        :param status:
            The value to assign to the status property of this QueryWorkRequest.
            Allowed values for this property are: "ACCEPTED", "CANCELED", "FAILED", "IN_PROGRESS", "SUCCEEDED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param operation_type:
            The value to assign to the operation_type property of this QueryWorkRequest.
            Allowed values for this property are: "EXECUTE_QUERY_JOB", "EXECUTE_PURGE_JOB", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type operation_type: str

        :param mode:
            The value to assign to the mode property of this QueryWorkRequest.
            Allowed values for this property are: "FOREGROUND", "BACKGROUND", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type mode: str

        :param time_background_at:
            The value to assign to the time_background_at property of this QueryWorkRequest.
        :type time_background_at: datetime

        :param time_filter:
            The value to assign to the time_filter property of this QueryWorkRequest.
        :type time_filter: oci.log_analytics.models.TimeRange

        :param scope_filters:
            The value to assign to the scope_filters property of this QueryWorkRequest.
        :type scope_filters: list[oci.log_analytics.models.ScopeFilter]

        :param sub_system:
            The value to assign to the sub_system property of this QueryWorkRequest.
            Allowed values for this property are: "LOG", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type sub_system: str

        :param display_query_string:
            The value to assign to the display_query_string property of this QueryWorkRequest.
        :type display_query_string: str

        :param internal_query_string:
            The value to assign to the internal_query_string property of this QueryWorkRequest.
        :type internal_query_string: str

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'time_started': 'datetime',
            'time_accepted': 'datetime',
            'time_finished': 'datetime',
            'time_expires': 'datetime',
            'percent_complete': 'int',
            'status': 'str',
            'operation_type': 'str',
            'mode': 'str',
            'time_background_at': 'datetime',
            'time_filter': 'TimeRange',
            'scope_filters': 'list[ScopeFilter]',
            'sub_system': 'str',
            'display_query_string': 'str',
            'internal_query_string': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'time_started': 'timeStarted',
            'time_accepted': 'timeAccepted',
            'time_finished': 'timeFinished',
            'time_expires': 'timeExpires',
            'percent_complete': 'percentComplete',
            'status': 'status',
            'operation_type': 'operationType',
            'mode': 'mode',
            'time_background_at': 'timeBackgroundAt',
            'time_filter': 'timeFilter',
            'scope_filters': 'scopeFilters',
            'sub_system': 'subSystem',
            'display_query_string': 'displayQueryString',
            'internal_query_string': 'internalQueryString'
        }

        self._id = None
        self._compartment_id = None
        self._time_started = None
        self._time_accepted = None
        self._time_finished = None
        self._time_expires = None
        self._percent_complete = None
        self._status = None
        self._operation_type = None
        self._mode = None
        self._time_background_at = None
        self._time_filter = None
        self._scope_filters = None
        self._sub_system = None
        self._display_query_string = None
        self._internal_query_string = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this QueryWorkRequest.
        Unique OCID identifier to reference this query job work Request with.


        :return: The id of this QueryWorkRequest.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this QueryWorkRequest.
        Unique OCID identifier to reference this query job work Request with.


        :param id: The id of this QueryWorkRequest.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this QueryWorkRequest.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this QueryWorkRequest.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this QueryWorkRequest.
        Compartment Identifier `OCID]`__.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this QueryWorkRequest.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def time_started(self):
        """
        **[Required]** Gets the time_started of this QueryWorkRequest.
        When the job was started.


        :return: The time_started of this QueryWorkRequest.
        :rtype: datetime
        """
        return self._time_started

    @time_started.setter
    def time_started(self, time_started):
        """
        Sets the time_started of this QueryWorkRequest.
        When the job was started.


        :param time_started: The time_started of this QueryWorkRequest.
        :type: datetime
        """
        self._time_started = time_started

    @property
    def time_accepted(self):
        """
        Gets the time_accepted of this QueryWorkRequest.
        When the work request was accepted. Should match timeStarted in all cases.


        :return: The time_accepted of this QueryWorkRequest.
        :rtype: datetime
        """
        return self._time_accepted

    @time_accepted.setter
    def time_accepted(self, time_accepted):
        """
        Sets the time_accepted of this QueryWorkRequest.
        When the work request was accepted. Should match timeStarted in all cases.


        :param time_accepted: The time_accepted of this QueryWorkRequest.
        :type: datetime
        """
        self._time_accepted = time_accepted

    @property
    def time_finished(self):
        """
        Gets the time_finished of this QueryWorkRequest.
        When the job finished execution.


        :return: The time_finished of this QueryWorkRequest.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this QueryWorkRequest.
        When the job finished execution.


        :param time_finished: The time_finished of this QueryWorkRequest.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def time_expires(self):
        """
        Gets the time_expires of this QueryWorkRequest.
        When the job will expire.


        :return: The time_expires of this QueryWorkRequest.
        :rtype: datetime
        """
        return self._time_expires

    @time_expires.setter
    def time_expires(self, time_expires):
        """
        Sets the time_expires of this QueryWorkRequest.
        When the job will expire.


        :param time_expires: The time_expires of this QueryWorkRequest.
        :type: datetime
        """
        self._time_expires = time_expires

    @property
    def percent_complete(self):
        """
        Gets the percent_complete of this QueryWorkRequest.
        Percentage progress completion of the query.


        :return: The percent_complete of this QueryWorkRequest.
        :rtype: int
        """
        return self._percent_complete

    @percent_complete.setter
    def percent_complete(self, percent_complete):
        """
        Sets the percent_complete of this QueryWorkRequest.
        Percentage progress completion of the query.


        :param percent_complete: The percent_complete of this QueryWorkRequest.
        :type: int
        """
        self._percent_complete = percent_complete

    @property
    def status(self):
        """
        Gets the status of this QueryWorkRequest.
        Work request status.

        Allowed values for this property are: "ACCEPTED", "CANCELED", "FAILED", "IN_PROGRESS", "SUCCEEDED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this QueryWorkRequest.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this QueryWorkRequest.
        Work request status.


        :param status: The status of this QueryWorkRequest.
        :type: str
        """
        allowed_values = ["ACCEPTED", "CANCELED", "FAILED", "IN_PROGRESS", "SUCCEEDED"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def operation_type(self):
        """
        Gets the operation_type of this QueryWorkRequest.
        Asynchronous action name.

        Allowed values for this property are: "EXECUTE_QUERY_JOB", "EXECUTE_PURGE_JOB", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The operation_type of this QueryWorkRequest.
        :rtype: str
        """
        return self._operation_type

    @operation_type.setter
    def operation_type(self, operation_type):
        """
        Sets the operation_type of this QueryWorkRequest.
        Asynchronous action name.


        :param operation_type: The operation_type of this QueryWorkRequest.
        :type: str
        """
        allowed_values = ["EXECUTE_QUERY_JOB", "EXECUTE_PURGE_JOB"]
        if not value_allowed_none_or_none_sentinel(operation_type, allowed_values):
            operation_type = 'UNKNOWN_ENUM_VALUE'
        self._operation_type = operation_type

    @property
    def mode(self):
        """
        **[Required]** Gets the mode of this QueryWorkRequest.
        Current execution mode for the job.

        Allowed values for this property are: "FOREGROUND", "BACKGROUND", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The mode of this QueryWorkRequest.
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """
        Sets the mode of this QueryWorkRequest.
        Current execution mode for the job.


        :param mode: The mode of this QueryWorkRequest.
        :type: str
        """
        allowed_values = ["FOREGROUND", "BACKGROUND"]
        if not value_allowed_none_or_none_sentinel(mode, allowed_values):
            mode = 'UNKNOWN_ENUM_VALUE'
        self._mode = mode

    @property
    def time_background_at(self):
        """
        Gets the time_background_at of this QueryWorkRequest.
        When the job was put in to the background.


        :return: The time_background_at of this QueryWorkRequest.
        :rtype: datetime
        """
        return self._time_background_at

    @time_background_at.setter
    def time_background_at(self, time_background_at):
        """
        Sets the time_background_at of this QueryWorkRequest.
        When the job was put in to the background.


        :param time_background_at: The time_background_at of this QueryWorkRequest.
        :type: datetime
        """
        self._time_background_at = time_background_at

    @property
    def time_filter(self):
        """
        Gets the time_filter of this QueryWorkRequest.

        :return: The time_filter of this QueryWorkRequest.
        :rtype: oci.log_analytics.models.TimeRange
        """
        return self._time_filter

    @time_filter.setter
    def time_filter(self, time_filter):
        """
        Sets the time_filter of this QueryWorkRequest.

        :param time_filter: The time_filter of this QueryWorkRequest.
        :type: oci.log_analytics.models.TimeRange
        """
        self._time_filter = time_filter

    @property
    def scope_filters(self):
        """
        Gets the scope_filters of this QueryWorkRequest.
        List of filters applied when the query executed.


        :return: The scope_filters of this QueryWorkRequest.
        :rtype: list[oci.log_analytics.models.ScopeFilter]
        """
        return self._scope_filters

    @scope_filters.setter
    def scope_filters(self, scope_filters):
        """
        Sets the scope_filters of this QueryWorkRequest.
        List of filters applied when the query executed.


        :param scope_filters: The scope_filters of this QueryWorkRequest.
        :type: list[oci.log_analytics.models.ScopeFilter]
        """
        self._scope_filters = scope_filters

    @property
    def sub_system(self):
        """
        **[Required]** Gets the sub_system of this QueryWorkRequest.
        Default subsystem to qualify fields with in the queryString if not specified.

        Allowed values for this property are: "LOG", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The sub_system of this QueryWorkRequest.
        :rtype: str
        """
        return self._sub_system

    @sub_system.setter
    def sub_system(self, sub_system):
        """
        Sets the sub_system of this QueryWorkRequest.
        Default subsystem to qualify fields with in the queryString if not specified.


        :param sub_system: The sub_system of this QueryWorkRequest.
        :type: str
        """
        allowed_values = ["LOG"]
        if not value_allowed_none_or_none_sentinel(sub_system, allowed_values):
            sub_system = 'UNKNOWN_ENUM_VALUE'
        self._sub_system = sub_system

    @property
    def display_query_string(self):
        """
        **[Required]** Gets the display_query_string of this QueryWorkRequest.
        Display version of the user speciified queryString.


        :return: The display_query_string of this QueryWorkRequest.
        :rtype: str
        """
        return self._display_query_string

    @display_query_string.setter
    def display_query_string(self, display_query_string):
        """
        Sets the display_query_string of this QueryWorkRequest.
        Display version of the user speciified queryString.


        :param display_query_string: The display_query_string of this QueryWorkRequest.
        :type: str
        """
        self._display_query_string = display_query_string

    @property
    def internal_query_string(self):
        """
        **[Required]** Gets the internal_query_string of this QueryWorkRequest.
        Internal version of the user specified queryString.


        :return: The internal_query_string of this QueryWorkRequest.
        :rtype: str
        """
        return self._internal_query_string

    @internal_query_string.setter
    def internal_query_string(self, internal_query_string):
        """
        Sets the internal_query_string of this QueryWorkRequest.
        Internal version of the user specified queryString.


        :param internal_query_string: The internal_query_string of this QueryWorkRequest.
        :type: str
        """
        self._internal_query_string = internal_query_string

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
