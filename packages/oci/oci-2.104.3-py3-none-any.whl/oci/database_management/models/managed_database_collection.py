# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ManagedDatabaseCollection(object):
    """
    A collection of Managed Database objects.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ManagedDatabaseCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param items:
            The value to assign to the items property of this ManagedDatabaseCollection.
        :type items: list[oci.database_management.models.ManagedDatabaseSummary]

        """
        self.swagger_types = {
            'items': 'list[ManagedDatabaseSummary]'
        }

        self.attribute_map = {
            'items': 'items'
        }

        self._items = None

    @property
    def items(self):
        """
        **[Required]** Gets the items of this ManagedDatabaseCollection.
        An array of ManagedDatabaseSummary resources.


        :return: The items of this ManagedDatabaseCollection.
        :rtype: list[oci.database_management.models.ManagedDatabaseSummary]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this ManagedDatabaseCollection.
        An array of ManagedDatabaseSummary resources.


        :param items: The items of this ManagedDatabaseCollection.
        :type: list[oci.database_management.models.ManagedDatabaseSummary]
        """
        self._items = items

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
