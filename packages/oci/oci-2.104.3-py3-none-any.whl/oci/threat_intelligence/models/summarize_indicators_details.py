# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SummarizeIndicatorsDetails(object):
    """
    Query parameters to filter indicators
    """

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "DOMAIN_NAME"
    INDICATOR_TYPE_DOMAIN_NAME = "DOMAIN_NAME"

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "FILE_NAME"
    INDICATOR_TYPE_FILE_NAME = "FILE_NAME"

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "MD5_HASH"
    INDICATOR_TYPE_MD5_HASH = "MD5_HASH"

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "SHA1_HASH"
    INDICATOR_TYPE_SHA1_HASH = "SHA1_HASH"

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "SHA256_HASH"
    INDICATOR_TYPE_SHA256_HASH = "SHA256_HASH"

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "IP_ADDRESS"
    INDICATOR_TYPE_IP_ADDRESS = "IP_ADDRESS"

    #: A constant which can be used with the indicator_type property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "URL"
    INDICATOR_TYPE_URL = "URL"

    #: A constant which can be used with the sort_order property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "ASC"
    SORT_ORDER_ASC = "ASC"

    #: A constant which can be used with the sort_order property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "DESC"
    SORT_ORDER_DESC = "DESC"

    #: A constant which can be used with the sort_by property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "CONFIDENCE"
    SORT_BY_CONFIDENCE = "CONFIDENCE"

    #: A constant which can be used with the sort_by property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "TIMECREATED"
    SORT_BY_TIMECREATED = "TIMECREATED"

    #: A constant which can be used with the sort_by property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "TIMEUPDATED"
    SORT_BY_TIMEUPDATED = "TIMEUPDATED"

    #: A constant which can be used with the sort_by property of a SummarizeIndicatorsDetails.
    #: This constant has a value of "TIMELASTSEEN"
    SORT_BY_TIMELASTSEEN = "TIMELASTSEEN"

    def __init__(self, **kwargs):
        """
        Initializes a new SummarizeIndicatorsDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param indicator_type:
            The value to assign to the indicator_type property of this SummarizeIndicatorsDetails.
            Allowed values for this property are: "DOMAIN_NAME", "FILE_NAME", "MD5_HASH", "SHA1_HASH", "SHA256_HASH", "IP_ADDRESS", "URL"
        :type indicator_type: str

        :param indicator_value:
            The value to assign to the indicator_value property of this SummarizeIndicatorsDetails.
        :type indicator_value: str

        :param threat_types:
            The value to assign to the threat_types property of this SummarizeIndicatorsDetails.
        :type threat_types: list[str]

        :param confidence_greater_than_or_equal_to:
            The value to assign to the confidence_greater_than_or_equal_to property of this SummarizeIndicatorsDetails.
        :type confidence_greater_than_or_equal_to: int

        :param time_updated_greater_than_or_equal_to:
            The value to assign to the time_updated_greater_than_or_equal_to property of this SummarizeIndicatorsDetails.
        :type time_updated_greater_than_or_equal_to: datetime

        :param time_updated_less_than:
            The value to assign to the time_updated_less_than property of this SummarizeIndicatorsDetails.
        :type time_updated_less_than: datetime

        :param time_last_seen_greater_than_or_equal_to:
            The value to assign to the time_last_seen_greater_than_or_equal_to property of this SummarizeIndicatorsDetails.
        :type time_last_seen_greater_than_or_equal_to: datetime

        :param time_last_seen_less_than:
            The value to assign to the time_last_seen_less_than property of this SummarizeIndicatorsDetails.
        :type time_last_seen_less_than: datetime

        :param time_created_greater_than_or_equal_to:
            The value to assign to the time_created_greater_than_or_equal_to property of this SummarizeIndicatorsDetails.
        :type time_created_greater_than_or_equal_to: datetime

        :param time_created_less_than:
            The value to assign to the time_created_less_than property of this SummarizeIndicatorsDetails.
        :type time_created_less_than: datetime

        :param indicator_seen_by:
            The value to assign to the indicator_seen_by property of this SummarizeIndicatorsDetails.
        :type indicator_seen_by: str

        :param malware:
            The value to assign to the malware property of this SummarizeIndicatorsDetails.
        :type malware: str

        :param threat_actor:
            The value to assign to the threat_actor property of this SummarizeIndicatorsDetails.
        :type threat_actor: str

        :param sort_order:
            The value to assign to the sort_order property of this SummarizeIndicatorsDetails.
            Allowed values for this property are: "ASC", "DESC"
        :type sort_order: str

        :param sort_by:
            The value to assign to the sort_by property of this SummarizeIndicatorsDetails.
            Allowed values for this property are: "CONFIDENCE", "TIMECREATED", "TIMEUPDATED", "TIMELASTSEEN"
        :type sort_by: str

        """
        self.swagger_types = {
            'indicator_type': 'str',
            'indicator_value': 'str',
            'threat_types': 'list[str]',
            'confidence_greater_than_or_equal_to': 'int',
            'time_updated_greater_than_or_equal_to': 'datetime',
            'time_updated_less_than': 'datetime',
            'time_last_seen_greater_than_or_equal_to': 'datetime',
            'time_last_seen_less_than': 'datetime',
            'time_created_greater_than_or_equal_to': 'datetime',
            'time_created_less_than': 'datetime',
            'indicator_seen_by': 'str',
            'malware': 'str',
            'threat_actor': 'str',
            'sort_order': 'str',
            'sort_by': 'str'
        }

        self.attribute_map = {
            'indicator_type': 'indicatorType',
            'indicator_value': 'indicatorValue',
            'threat_types': 'threatTypes',
            'confidence_greater_than_or_equal_to': 'confidenceGreaterThanOrEqualTo',
            'time_updated_greater_than_or_equal_to': 'timeUpdatedGreaterThanOrEqualTo',
            'time_updated_less_than': 'timeUpdatedLessThan',
            'time_last_seen_greater_than_or_equal_to': 'timeLastSeenGreaterThanOrEqualTo',
            'time_last_seen_less_than': 'timeLastSeenLessThan',
            'time_created_greater_than_or_equal_to': 'timeCreatedGreaterThanOrEqualTo',
            'time_created_less_than': 'timeCreatedLessThan',
            'indicator_seen_by': 'indicatorSeenBy',
            'malware': 'malware',
            'threat_actor': 'threatActor',
            'sort_order': 'sortOrder',
            'sort_by': 'sortBy'
        }

        self._indicator_type = None
        self._indicator_value = None
        self._threat_types = None
        self._confidence_greater_than_or_equal_to = None
        self._time_updated_greater_than_or_equal_to = None
        self._time_updated_less_than = None
        self._time_last_seen_greater_than_or_equal_to = None
        self._time_last_seen_less_than = None
        self._time_created_greater_than_or_equal_to = None
        self._time_created_less_than = None
        self._indicator_seen_by = None
        self._malware = None
        self._threat_actor = None
        self._sort_order = None
        self._sort_by = None

    @property
    def indicator_type(self):
        """
        Gets the indicator_type of this SummarizeIndicatorsDetails.
        The type of indicator this is

        Allowed values for this property are: "DOMAIN_NAME", "FILE_NAME", "MD5_HASH", "SHA1_HASH", "SHA256_HASH", "IP_ADDRESS", "URL"


        :return: The indicator_type of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._indicator_type

    @indicator_type.setter
    def indicator_type(self, indicator_type):
        """
        Sets the indicator_type of this SummarizeIndicatorsDetails.
        The type of indicator this is


        :param indicator_type: The indicator_type of this SummarizeIndicatorsDetails.
        :type: str
        """
        allowed_values = ["DOMAIN_NAME", "FILE_NAME", "MD5_HASH", "SHA1_HASH", "SHA256_HASH", "IP_ADDRESS", "URL"]
        if not value_allowed_none_or_none_sentinel(indicator_type, allowed_values):
            raise ValueError(
                "Invalid value for `indicator_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._indicator_type = indicator_type

    @property
    def indicator_value(self):
        """
        Gets the indicator_value of this SummarizeIndicatorsDetails.
        The value for the type of indicator this is


        :return: The indicator_value of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._indicator_value

    @indicator_value.setter
    def indicator_value(self, indicator_value):
        """
        Sets the indicator_value of this SummarizeIndicatorsDetails.
        The value for the type of indicator this is


        :param indicator_value: The indicator_value of this SummarizeIndicatorsDetails.
        :type: str
        """
        self._indicator_value = indicator_value

    @property
    def threat_types(self):
        """
        Gets the threat_types of this SummarizeIndicatorsDetails.
        The threat type of entites to be returned.


        :return: The threat_types of this SummarizeIndicatorsDetails.
        :rtype: list[str]
        """
        return self._threat_types

    @threat_types.setter
    def threat_types(self, threat_types):
        """
        Sets the threat_types of this SummarizeIndicatorsDetails.
        The threat type of entites to be returned.


        :param threat_types: The threat_types of this SummarizeIndicatorsDetails.
        :type: list[str]
        """
        self._threat_types = threat_types

    @property
    def confidence_greater_than_or_equal_to(self):
        """
        Gets the confidence_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The minimum level of confidence to return


        :return: The confidence_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :rtype: int
        """
        return self._confidence_greater_than_or_equal_to

    @confidence_greater_than_or_equal_to.setter
    def confidence_greater_than_or_equal_to(self, confidence_greater_than_or_equal_to):
        """
        Sets the confidence_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The minimum level of confidence to return


        :param confidence_greater_than_or_equal_to: The confidence_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :type: int
        """
        self._confidence_greater_than_or_equal_to = confidence_greater_than_or_equal_to

    @property
    def time_updated_greater_than_or_equal_to(self):
        """
        Gets the time_updated_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The oldest update time of entities to be returned.


        :return: The time_updated_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :rtype: datetime
        """
        return self._time_updated_greater_than_or_equal_to

    @time_updated_greater_than_or_equal_to.setter
    def time_updated_greater_than_or_equal_to(self, time_updated_greater_than_or_equal_to):
        """
        Sets the time_updated_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The oldest update time of entities to be returned.


        :param time_updated_greater_than_or_equal_to: The time_updated_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :type: datetime
        """
        self._time_updated_greater_than_or_equal_to = time_updated_greater_than_or_equal_to

    @property
    def time_updated_less_than(self):
        """
        Gets the time_updated_less_than of this SummarizeIndicatorsDetails.
        The newest update time of entities to be returned.


        :return: The time_updated_less_than of this SummarizeIndicatorsDetails.
        :rtype: datetime
        """
        return self._time_updated_less_than

    @time_updated_less_than.setter
    def time_updated_less_than(self, time_updated_less_than):
        """
        Sets the time_updated_less_than of this SummarizeIndicatorsDetails.
        The newest update time of entities to be returned.


        :param time_updated_less_than: The time_updated_less_than of this SummarizeIndicatorsDetails.
        :type: datetime
        """
        self._time_updated_less_than = time_updated_less_than

    @property
    def time_last_seen_greater_than_or_equal_to(self):
        """
        Gets the time_last_seen_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The oldest last seen time of entities to be returned.


        :return: The time_last_seen_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :rtype: datetime
        """
        return self._time_last_seen_greater_than_or_equal_to

    @time_last_seen_greater_than_or_equal_to.setter
    def time_last_seen_greater_than_or_equal_to(self, time_last_seen_greater_than_or_equal_to):
        """
        Sets the time_last_seen_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The oldest last seen time of entities to be returned.


        :param time_last_seen_greater_than_or_equal_to: The time_last_seen_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :type: datetime
        """
        self._time_last_seen_greater_than_or_equal_to = time_last_seen_greater_than_or_equal_to

    @property
    def time_last_seen_less_than(self):
        """
        Gets the time_last_seen_less_than of this SummarizeIndicatorsDetails.
        The newest last seen time of entities to be returned.


        :return: The time_last_seen_less_than of this SummarizeIndicatorsDetails.
        :rtype: datetime
        """
        return self._time_last_seen_less_than

    @time_last_seen_less_than.setter
    def time_last_seen_less_than(self, time_last_seen_less_than):
        """
        Sets the time_last_seen_less_than of this SummarizeIndicatorsDetails.
        The newest last seen time of entities to be returned.


        :param time_last_seen_less_than: The time_last_seen_less_than of this SummarizeIndicatorsDetails.
        :type: datetime
        """
        self._time_last_seen_less_than = time_last_seen_less_than

    @property
    def time_created_greater_than_or_equal_to(self):
        """
        Gets the time_created_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The oldest creation time of entities to be returned.


        :return: The time_created_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :rtype: datetime
        """
        return self._time_created_greater_than_or_equal_to

    @time_created_greater_than_or_equal_to.setter
    def time_created_greater_than_or_equal_to(self, time_created_greater_than_or_equal_to):
        """
        Sets the time_created_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        The oldest creation time of entities to be returned.


        :param time_created_greater_than_or_equal_to: The time_created_greater_than_or_equal_to of this SummarizeIndicatorsDetails.
        :type: datetime
        """
        self._time_created_greater_than_or_equal_to = time_created_greater_than_or_equal_to

    @property
    def time_created_less_than(self):
        """
        Gets the time_created_less_than of this SummarizeIndicatorsDetails.
        The newest creation time of entities to be returned.


        :return: The time_created_less_than of this SummarizeIndicatorsDetails.
        :rtype: datetime
        """
        return self._time_created_less_than

    @time_created_less_than.setter
    def time_created_less_than(self, time_created_less_than):
        """
        Sets the time_created_less_than of this SummarizeIndicatorsDetails.
        The newest creation time of entities to be returned.


        :param time_created_less_than: The time_created_less_than of this SummarizeIndicatorsDetails.
        :type: datetime
        """
        self._time_created_less_than = time_created_less_than

    @property
    def indicator_seen_by(self):
        """
        Gets the indicator_seen_by of this SummarizeIndicatorsDetails.
        Filter to include indicators that have been seen by the provided source.


        :return: The indicator_seen_by of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._indicator_seen_by

    @indicator_seen_by.setter
    def indicator_seen_by(self, indicator_seen_by):
        """
        Sets the indicator_seen_by of this SummarizeIndicatorsDetails.
        Filter to include indicators that have been seen by the provided source.


        :param indicator_seen_by: The indicator_seen_by of this SummarizeIndicatorsDetails.
        :type: str
        """
        self._indicator_seen_by = indicator_seen_by

    @property
    def malware(self):
        """
        Gets the malware of this SummarizeIndicatorsDetails.
        Filter to include indicators associated with the provided malware.


        :return: The malware of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._malware

    @malware.setter
    def malware(self, malware):
        """
        Sets the malware of this SummarizeIndicatorsDetails.
        Filter to include indicators associated with the provided malware.


        :param malware: The malware of this SummarizeIndicatorsDetails.
        :type: str
        """
        self._malware = malware

    @property
    def threat_actor(self):
        """
        Gets the threat_actor of this SummarizeIndicatorsDetails.
        Filter to included indicators associated with the provided threat actor.


        :return: The threat_actor of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._threat_actor

    @threat_actor.setter
    def threat_actor(self, threat_actor):
        """
        Sets the threat_actor of this SummarizeIndicatorsDetails.
        Filter to included indicators associated with the provided threat actor.


        :param threat_actor: The threat_actor of this SummarizeIndicatorsDetails.
        :type: str
        """
        self._threat_actor = threat_actor

    @property
    def sort_order(self):
        """
        Gets the sort_order of this SummarizeIndicatorsDetails.
        The sort order to use, either 'ASC' or 'DESC'.

        Allowed values for this property are: "ASC", "DESC"


        :return: The sort_order of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """
        Sets the sort_order of this SummarizeIndicatorsDetails.
        The sort order to use, either 'ASC' or 'DESC'.


        :param sort_order: The sort_order of this SummarizeIndicatorsDetails.
        :type: str
        """
        allowed_values = ["ASC", "DESC"]
        if not value_allowed_none_or_none_sentinel(sort_order, allowed_values):
            raise ValueError(
                "Invalid value for `sort_order`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._sort_order = sort_order

    @property
    def sort_by(self):
        """
        Gets the sort_by of this SummarizeIndicatorsDetails.
        The field to sort by. Only one field to sort by may be provided

        Allowed values for this property are: "CONFIDENCE", "TIMECREATED", "TIMEUPDATED", "TIMELASTSEEN"


        :return: The sort_by of this SummarizeIndicatorsDetails.
        :rtype: str
        """
        return self._sort_by

    @sort_by.setter
    def sort_by(self, sort_by):
        """
        Sets the sort_by of this SummarizeIndicatorsDetails.
        The field to sort by. Only one field to sort by may be provided


        :param sort_by: The sort_by of this SummarizeIndicatorsDetails.
        :type: str
        """
        allowed_values = ["CONFIDENCE", "TIMECREATED", "TIMEUPDATED", "TIMELASTSEEN"]
        if not value_allowed_none_or_none_sentinel(sort_by, allowed_values):
            raise ValueError(
                "Invalid value for `sort_by`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._sort_by = sort_by

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
