# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddmDbFindingsTimeSeriesSummary(object):
    """
    ADDM findings time series data
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddmDbFindingsTimeSeriesSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AddmDbFindingsTimeSeriesSummary.
        :type id: str

        :param task_id:
            The value to assign to the task_id property of this AddmDbFindingsTimeSeriesSummary.
        :type task_id: int

        :param task_name:
            The value to assign to the task_name property of this AddmDbFindingsTimeSeriesSummary.
        :type task_name: str

        :param finding_id:
            The value to assign to the finding_id property of this AddmDbFindingsTimeSeriesSummary.
        :type finding_id: str

        :param timestamp:
            The value to assign to the timestamp property of this AddmDbFindingsTimeSeriesSummary.
        :type timestamp: datetime

        :param time_analysis_started:
            The value to assign to the time_analysis_started property of this AddmDbFindingsTimeSeriesSummary.
        :type time_analysis_started: datetime

        :param time_analysis_ended:
            The value to assign to the time_analysis_ended property of this AddmDbFindingsTimeSeriesSummary.
        :type time_analysis_ended: datetime

        :param category_name:
            The value to assign to the category_name property of this AddmDbFindingsTimeSeriesSummary.
        :type category_name: str

        :param category_display_name:
            The value to assign to the category_display_name property of this AddmDbFindingsTimeSeriesSummary.
        :type category_display_name: str

        :param name:
            The value to assign to the name property of this AddmDbFindingsTimeSeriesSummary.
        :type name: str

        :param message:
            The value to assign to the message property of this AddmDbFindingsTimeSeriesSummary.
        :type message: str

        :param analysis_db_time_in_secs:
            The value to assign to the analysis_db_time_in_secs property of this AddmDbFindingsTimeSeriesSummary.
        :type analysis_db_time_in_secs: float

        :param analysis_avg_active_sessions:
            The value to assign to the analysis_avg_active_sessions property of this AddmDbFindingsTimeSeriesSummary.
        :type analysis_avg_active_sessions: float

        :param impact_db_time_in_secs:
            The value to assign to the impact_db_time_in_secs property of this AddmDbFindingsTimeSeriesSummary.
        :type impact_db_time_in_secs: float

        :param impact_percent:
            The value to assign to the impact_percent property of this AddmDbFindingsTimeSeriesSummary.
        :type impact_percent: float

        :param impact_avg_active_sessions:
            The value to assign to the impact_avg_active_sessions property of this AddmDbFindingsTimeSeriesSummary.
        :type impact_avg_active_sessions: float

        """
        self.swagger_types = {
            'id': 'str',
            'task_id': 'int',
            'task_name': 'str',
            'finding_id': 'str',
            'timestamp': 'datetime',
            'time_analysis_started': 'datetime',
            'time_analysis_ended': 'datetime',
            'category_name': 'str',
            'category_display_name': 'str',
            'name': 'str',
            'message': 'str',
            'analysis_db_time_in_secs': 'float',
            'analysis_avg_active_sessions': 'float',
            'impact_db_time_in_secs': 'float',
            'impact_percent': 'float',
            'impact_avg_active_sessions': 'float'
        }

        self.attribute_map = {
            'id': 'id',
            'task_id': 'taskId',
            'task_name': 'taskName',
            'finding_id': 'findingId',
            'timestamp': 'timestamp',
            'time_analysis_started': 'timeAnalysisStarted',
            'time_analysis_ended': 'timeAnalysisEnded',
            'category_name': 'categoryName',
            'category_display_name': 'categoryDisplayName',
            'name': 'name',
            'message': 'message',
            'analysis_db_time_in_secs': 'analysisDbTimeInSecs',
            'analysis_avg_active_sessions': 'analysisAvgActiveSessions',
            'impact_db_time_in_secs': 'impactDbTimeInSecs',
            'impact_percent': 'impactPercent',
            'impact_avg_active_sessions': 'impactAvgActiveSessions'
        }

        self._id = None
        self._task_id = None
        self._task_name = None
        self._finding_id = None
        self._timestamp = None
        self._time_analysis_started = None
        self._time_analysis_ended = None
        self._category_name = None
        self._category_display_name = None
        self._name = None
        self._message = None
        self._analysis_db_time_in_secs = None
        self._analysis_avg_active_sessions = None
        self._impact_db_time_in_secs = None
        self._impact_percent = None
        self._impact_avg_active_sessions = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this AddmDbFindingsTimeSeriesSummary.
        The `OCID`__ of the Database insight.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AddmDbFindingsTimeSeriesSummary.
        The `OCID`__ of the Database insight.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._id = id

    @property
    def task_id(self):
        """
        **[Required]** Gets the task_id of this AddmDbFindingsTimeSeriesSummary.
        Unique ADDM task id


        :return: The task_id of this AddmDbFindingsTimeSeriesSummary.
        :rtype: int
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """
        Sets the task_id of this AddmDbFindingsTimeSeriesSummary.
        Unique ADDM task id


        :param task_id: The task_id of this AddmDbFindingsTimeSeriesSummary.
        :type: int
        """
        self._task_id = task_id

    @property
    def task_name(self):
        """
        **[Required]** Gets the task_name of this AddmDbFindingsTimeSeriesSummary.
        ADDM task name


        :return: The task_name of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, task_name):
        """
        Sets the task_name of this AddmDbFindingsTimeSeriesSummary.
        ADDM task name


        :param task_name: The task_name of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._task_name = task_name

    @property
    def finding_id(self):
        """
        **[Required]** Gets the finding_id of this AddmDbFindingsTimeSeriesSummary.
        Unique finding id


        :return: The finding_id of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._finding_id

    @finding_id.setter
    def finding_id(self, finding_id):
        """
        Sets the finding_id of this AddmDbFindingsTimeSeriesSummary.
        Unique finding id


        :param finding_id: The finding_id of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._finding_id = finding_id

    @property
    def timestamp(self):
        """
        **[Required]** Gets the timestamp of this AddmDbFindingsTimeSeriesSummary.
        Timestamp when finding was generated


        :return: The timestamp of this AddmDbFindingsTimeSeriesSummary.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this AddmDbFindingsTimeSeriesSummary.
        Timestamp when finding was generated


        :param timestamp: The timestamp of this AddmDbFindingsTimeSeriesSummary.
        :type: datetime
        """
        self._timestamp = timestamp

    @property
    def time_analysis_started(self):
        """
        Gets the time_analysis_started of this AddmDbFindingsTimeSeriesSummary.
        Start Timestamp of snapshot


        :return: The time_analysis_started of this AddmDbFindingsTimeSeriesSummary.
        :rtype: datetime
        """
        return self._time_analysis_started

    @time_analysis_started.setter
    def time_analysis_started(self, time_analysis_started):
        """
        Sets the time_analysis_started of this AddmDbFindingsTimeSeriesSummary.
        Start Timestamp of snapshot


        :param time_analysis_started: The time_analysis_started of this AddmDbFindingsTimeSeriesSummary.
        :type: datetime
        """
        self._time_analysis_started = time_analysis_started

    @property
    def time_analysis_ended(self):
        """
        Gets the time_analysis_ended of this AddmDbFindingsTimeSeriesSummary.
        End Timestamp of snapshot


        :return: The time_analysis_ended of this AddmDbFindingsTimeSeriesSummary.
        :rtype: datetime
        """
        return self._time_analysis_ended

    @time_analysis_ended.setter
    def time_analysis_ended(self, time_analysis_ended):
        """
        Sets the time_analysis_ended of this AddmDbFindingsTimeSeriesSummary.
        End Timestamp of snapshot


        :param time_analysis_ended: The time_analysis_ended of this AddmDbFindingsTimeSeriesSummary.
        :type: datetime
        """
        self._time_analysis_ended = time_analysis_ended

    @property
    def category_name(self):
        """
        **[Required]** Gets the category_name of this AddmDbFindingsTimeSeriesSummary.
        Category name


        :return: The category_name of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._category_name

    @category_name.setter
    def category_name(self, category_name):
        """
        Sets the category_name of this AddmDbFindingsTimeSeriesSummary.
        Category name


        :param category_name: The category_name of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._category_name = category_name

    @property
    def category_display_name(self):
        """
        **[Required]** Gets the category_display_name of this AddmDbFindingsTimeSeriesSummary.
        Category display name


        :return: The category_display_name of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._category_display_name

    @category_display_name.setter
    def category_display_name(self, category_display_name):
        """
        Sets the category_display_name of this AddmDbFindingsTimeSeriesSummary.
        Category display name


        :param category_display_name: The category_display_name of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._category_display_name = category_display_name

    @property
    def name(self):
        """
        **[Required]** Gets the name of this AddmDbFindingsTimeSeriesSummary.
        Finding name


        :return: The name of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AddmDbFindingsTimeSeriesSummary.
        Finding name


        :param name: The name of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._name = name

    @property
    def message(self):
        """
        **[Required]** Gets the message of this AddmDbFindingsTimeSeriesSummary.
        Finding message


        :return: The message of this AddmDbFindingsTimeSeriesSummary.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this AddmDbFindingsTimeSeriesSummary.
        Finding message


        :param message: The message of this AddmDbFindingsTimeSeriesSummary.
        :type: str
        """
        self._message = message

    @property
    def analysis_db_time_in_secs(self):
        """
        Gets the analysis_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        DB time in seconds for the snapshot


        :return: The analysis_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        :rtype: float
        """
        return self._analysis_db_time_in_secs

    @analysis_db_time_in_secs.setter
    def analysis_db_time_in_secs(self, analysis_db_time_in_secs):
        """
        Sets the analysis_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        DB time in seconds for the snapshot


        :param analysis_db_time_in_secs: The analysis_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        :type: float
        """
        self._analysis_db_time_in_secs = analysis_db_time_in_secs

    @property
    def analysis_avg_active_sessions(self):
        """
        Gets the analysis_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        DB avg active sessions for the snapshot


        :return: The analysis_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        :rtype: float
        """
        return self._analysis_avg_active_sessions

    @analysis_avg_active_sessions.setter
    def analysis_avg_active_sessions(self, analysis_avg_active_sessions):
        """
        Sets the analysis_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        DB avg active sessions for the snapshot


        :param analysis_avg_active_sessions: The analysis_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        :type: float
        """
        self._analysis_avg_active_sessions = analysis_avg_active_sessions

    @property
    def impact_db_time_in_secs(self):
        """
        Gets the impact_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        Impact in seconds


        :return: The impact_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        :rtype: float
        """
        return self._impact_db_time_in_secs

    @impact_db_time_in_secs.setter
    def impact_db_time_in_secs(self, impact_db_time_in_secs):
        """
        Sets the impact_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        Impact in seconds


        :param impact_db_time_in_secs: The impact_db_time_in_secs of this AddmDbFindingsTimeSeriesSummary.
        :type: float
        """
        self._impact_db_time_in_secs = impact_db_time_in_secs

    @property
    def impact_percent(self):
        """
        **[Required]** Gets the impact_percent of this AddmDbFindingsTimeSeriesSummary.
        Impact in terms of percentage of total activity


        :return: The impact_percent of this AddmDbFindingsTimeSeriesSummary.
        :rtype: float
        """
        return self._impact_percent

    @impact_percent.setter
    def impact_percent(self, impact_percent):
        """
        Sets the impact_percent of this AddmDbFindingsTimeSeriesSummary.
        Impact in terms of percentage of total activity


        :param impact_percent: The impact_percent of this AddmDbFindingsTimeSeriesSummary.
        :type: float
        """
        self._impact_percent = impact_percent

    @property
    def impact_avg_active_sessions(self):
        """
        **[Required]** Gets the impact_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        Impact in terms of average active sessions


        :return: The impact_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        :rtype: float
        """
        return self._impact_avg_active_sessions

    @impact_avg_active_sessions.setter
    def impact_avg_active_sessions(self, impact_avg_active_sessions):
        """
        Sets the impact_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        Impact in terms of average active sessions


        :param impact_avg_active_sessions: The impact_avg_active_sessions of this AddmDbFindingsTimeSeriesSummary.
        :type: float
        """
        self._impact_avg_active_sessions = impact_avg_active_sessions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
