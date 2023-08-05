# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class WorkItemDetails(object):
    """
    The minimum details of a work item.
    """

    #: A constant which can be used with the kind property of a WorkItemDetails.
    #: This constant has a value of "BASIC"
    KIND_BASIC = "BASIC"

    #: A constant which can be used with the kind property of a WorkItemDetails.
    #: This constant has a value of "APPLICATION"
    KIND_APPLICATION = "APPLICATION"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "LCM"
    WORK_ITEM_TYPE_LCM = "LCM"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "JFR_CAPTURE"
    WORK_ITEM_TYPE_JFR_CAPTURE = "JFR_CAPTURE"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "JFR_UPLOAD"
    WORK_ITEM_TYPE_JFR_UPLOAD = "JFR_UPLOAD"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "CRYPTO_ANALYSIS"
    WORK_ITEM_TYPE_CRYPTO_ANALYSIS = "CRYPTO_ANALYSIS"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "CRYPTO_ANALYSIS_MERGE"
    WORK_ITEM_TYPE_CRYPTO_ANALYSIS_MERGE = "CRYPTO_ANALYSIS_MERGE"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "ADVANCED_USAGE_TRACKING"
    WORK_ITEM_TYPE_ADVANCED_USAGE_TRACKING = "ADVANCED_USAGE_TRACKING"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "PERFORMANCE_TUNING"
    WORK_ITEM_TYPE_PERFORMANCE_TUNING = "PERFORMANCE_TUNING"

    #: A constant which can be used with the work_item_type property of a WorkItemDetails.
    #: This constant has a value of "JMIGRATE_ANALYSIS"
    WORK_ITEM_TYPE_JMIGRATE_ANALYSIS = "JMIGRATE_ANALYSIS"

    def __init__(self, **kwargs):
        """
        Initializes a new WorkItemDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.jms.models.BasicWorkItemDetails`
        * :class:`~oci.jms.models.ApplicationWorkItemDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this WorkItemDetails.
            Allowed values for this property are: "BASIC", "APPLICATION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type kind: str

        :param work_item_type:
            The value to assign to the work_item_type property of this WorkItemDetails.
            Allowed values for this property are: "LCM", "JFR_CAPTURE", "JFR_UPLOAD", "CRYPTO_ANALYSIS", "CRYPTO_ANALYSIS_MERGE", "ADVANCED_USAGE_TRACKING", "PERFORMANCE_TUNING", "JMIGRATE_ANALYSIS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type work_item_type: str

        """
        self.swagger_types = {
            'kind': 'str',
            'work_item_type': 'str'
        }

        self.attribute_map = {
            'kind': 'kind',
            'work_item_type': 'workItemType'
        }

        self._kind = None
        self._work_item_type = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['kind']

        if type == 'BASIC':
            return 'BasicWorkItemDetails'

        if type == 'APPLICATION':
            return 'ApplicationWorkItemDetails'
        else:
            return 'WorkItemDetails'

    @property
    def kind(self):
        """
        **[Required]** Gets the kind of this WorkItemDetails.
        The kind of work item details.

        Allowed values for this property are: "BASIC", "APPLICATION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The kind of this WorkItemDetails.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        Sets the kind of this WorkItemDetails.
        The kind of work item details.


        :param kind: The kind of this WorkItemDetails.
        :type: str
        """
        allowed_values = ["BASIC", "APPLICATION"]
        if not value_allowed_none_or_none_sentinel(kind, allowed_values):
            kind = 'UNKNOWN_ENUM_VALUE'
        self._kind = kind

    @property
    def work_item_type(self):
        """
        Gets the work_item_type of this WorkItemDetails.
        The work item type.

        Allowed values for this property are: "LCM", "JFR_CAPTURE", "JFR_UPLOAD", "CRYPTO_ANALYSIS", "CRYPTO_ANALYSIS_MERGE", "ADVANCED_USAGE_TRACKING", "PERFORMANCE_TUNING", "JMIGRATE_ANALYSIS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The work_item_type of this WorkItemDetails.
        :rtype: str
        """
        return self._work_item_type

    @work_item_type.setter
    def work_item_type(self, work_item_type):
        """
        Sets the work_item_type of this WorkItemDetails.
        The work item type.


        :param work_item_type: The work_item_type of this WorkItemDetails.
        :type: str
        """
        allowed_values = ["LCM", "JFR_CAPTURE", "JFR_UPLOAD", "CRYPTO_ANALYSIS", "CRYPTO_ANALYSIS_MERGE", "ADVANCED_USAGE_TRACKING", "PERFORMANCE_TUNING", "JMIGRATE_ANALYSIS"]
        if not value_allowed_none_or_none_sentinel(work_item_type, allowed_values):
            work_item_type = 'UNKNOWN_ENUM_VALUE'
        self._work_item_type = work_item_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
