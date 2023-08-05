# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddmDbRecommendationCategoryCollection(object):
    """
    List of recommendation categories
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddmDbRecommendationCategoryCollection object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param database_details_items:
            The value to assign to the database_details_items property of this AddmDbRecommendationCategoryCollection.
        :type database_details_items: list[oci.opsi.models.DatabaseDetails]

        :param items:
            The value to assign to the items property of this AddmDbRecommendationCategoryCollection.
        :type items: list[oci.opsi.models.AddmDbRecommendationCategorySummary]

        """
        self.swagger_types = {
            'database_details_items': 'list[DatabaseDetails]',
            'items': 'list[AddmDbRecommendationCategorySummary]'
        }

        self.attribute_map = {
            'database_details_items': 'databaseDetailsItems',
            'items': 'items'
        }

        self._database_details_items = None
        self._items = None

    @property
    def database_details_items(self):
        """
        **[Required]** Gets the database_details_items of this AddmDbRecommendationCategoryCollection.
        List of database details data


        :return: The database_details_items of this AddmDbRecommendationCategoryCollection.
        :rtype: list[oci.opsi.models.DatabaseDetails]
        """
        return self._database_details_items

    @database_details_items.setter
    def database_details_items(self, database_details_items):
        """
        Sets the database_details_items of this AddmDbRecommendationCategoryCollection.
        List of database details data


        :param database_details_items: The database_details_items of this AddmDbRecommendationCategoryCollection.
        :type: list[oci.opsi.models.DatabaseDetails]
        """
        self._database_details_items = database_details_items

    @property
    def items(self):
        """
        **[Required]** Gets the items of this AddmDbRecommendationCategoryCollection.
        List of recommendation categories


        :return: The items of this AddmDbRecommendationCategoryCollection.
        :rtype: list[oci.opsi.models.AddmDbRecommendationCategorySummary]
        """
        return self._items

    @items.setter
    def items(self, items):
        """
        Sets the items of this AddmDbRecommendationCategoryCollection.
        List of recommendation categories


        :param items: The items of this AddmDbRecommendationCategoryCollection.
        :type: list[oci.opsi.models.AddmDbRecommendationCategorySummary]
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
