# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceQuotumCollection(object):
    """
    The quota details of resources under a tenancy.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceQuotumCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param items:
            The value to assign to the items property of this ResourceQuotumCollection.
        :type items: list[oci.usage.models.ResourceQuotumSummary]

        :param is_allowed:
            The value to assign to the is_allowed property of this ResourceQuotumCollection.
        :type is_allowed: bool

        """
        self.swagger_types = {
            'items': 'list[ResourceQuotumSummary]',
            'is_allowed': 'bool'
        }

        self.attribute_map = {
            'items': 'items',
            'is_allowed': 'isAllowed'
        }

        self._items = None
        self._is_allowed = None

    @property
    def items(self):
        """
        **[Required]** Gets the items of this ResourceQuotumCollection.
        The list of resource quota details.


        :return: The items of this ResourceQuotumCollection.
        :rtype: list[oci.usage.models.ResourceQuotumSummary]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this ResourceQuotumCollection.
        The list of resource quota details.


        :param items: The items of this ResourceQuotumCollection.
        :type: list[oci.usage.models.ResourceQuotumSummary]
        """
        self._items = items

    @property
    def is_allowed(self):
        """
        **[Required]** Gets the is_allowed of this ResourceQuotumCollection.
        Used to indicate if further quota consumption isAllowed.


        :return: The is_allowed of this ResourceQuotumCollection.
        :rtype: bool
        """
        return self._is_allowed

    @is_allowed.setter
    def is_allowed(self, is_allowed):
        """
        Sets the is_allowed of this ResourceQuotumCollection.
        Used to indicate if further quota consumption isAllowed.


        :param is_allowed: The is_allowed of this ResourceQuotumCollection.
        :type: bool
        """
        self._is_allowed = is_allowed

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
