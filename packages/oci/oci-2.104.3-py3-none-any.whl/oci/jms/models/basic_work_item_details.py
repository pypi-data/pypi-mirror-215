# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .work_item_details import WorkItemDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BasicWorkItemDetails(WorkItemDetails):
    """
    The common work item details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new BasicWorkItemDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.jms.models.BasicWorkItemDetails.kind` attribute
        of this class is ``BASIC`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this BasicWorkItemDetails.
            Allowed values for this property are: "BASIC", "APPLICATION"
        :type kind: str

        :param work_item_type:
            The value to assign to the work_item_type property of this BasicWorkItemDetails.
            Allowed values for this property are: "LCM", "JFR_CAPTURE", "JFR_UPLOAD", "CRYPTO_ANALYSIS", "CRYPTO_ANALYSIS_MERGE", "ADVANCED_USAGE_TRACKING", "PERFORMANCE_TUNING", "JMIGRATE_ANALYSIS"
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
        self._kind = 'BASIC'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
