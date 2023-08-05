# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AnnouncementSummary(object):
    """
    A summary of a announcement on Console Overview page
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AnnouncementSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this AnnouncementSummary.
        :type key: int

        :param summary:
            The value to assign to the summary property of this AnnouncementSummary.
        :type summary: str

        :param url:
            The value to assign to the url property of this AnnouncementSummary.
        :type url: str

        :param time_released:
            The value to assign to the time_released property of this AnnouncementSummary.
        :type time_released: datetime

        """
        self.swagger_types = {
            'key': 'int',
            'summary': 'str',
            'url': 'str',
            'time_released': 'datetime'
        }

        self.attribute_map = {
            'key': 'key',
            'summary': 'summary',
            'url': 'url',
            'time_released': 'timeReleased'
        }

        self._key = None
        self._summary = None
        self._url = None
        self._time_released = None

    @property
    def key(self):
        """
        **[Required]** Gets the key of this AnnouncementSummary.
        Unique id of the announcement


        :return: The key of this AnnouncementSummary.
        :rtype: int
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this AnnouncementSummary.
        Unique id of the announcement


        :param key: The key of this AnnouncementSummary.
        :type: int
        """
        self._key = key

    @property
    def summary(self):
        """
        **[Required]** Gets the summary of this AnnouncementSummary.
        Summary text of the announcement


        :return: The summary of this AnnouncementSummary.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this AnnouncementSummary.
        Summary text of the announcement


        :param summary: The summary of this AnnouncementSummary.
        :type: str
        """
        self._summary = summary

    @property
    def url(self):
        """
        **[Required]** Gets the url of this AnnouncementSummary.
        URL to the announcement web page


        :return: The url of this AnnouncementSummary.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this AnnouncementSummary.
        URL to the announcement web page


        :param url: The url of this AnnouncementSummary.
        :type: str
        """
        self._url = url

    @property
    def time_released(self):
        """
        **[Required]** Gets the time_released of this AnnouncementSummary.
        Date time on which the announcement was released


        :return: The time_released of this AnnouncementSummary.
        :rtype: datetime
        """
        return self._time_released

    @time_released.setter
    def time_released(self, time_released):
        """
        Sets the time_released of this AnnouncementSummary.
        Date time on which the announcement was released


        :param time_released: The time_released of this AnnouncementSummary.
        :type: datetime
        """
        self._time_released = time_released

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
