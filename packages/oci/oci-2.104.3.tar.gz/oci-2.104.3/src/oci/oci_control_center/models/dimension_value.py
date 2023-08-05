# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DimensionValue(object):
    """
    The dimension value for the given dimension name as key.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DimensionValue object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param dimension_value:
            The value to assign to the dimension_value property of this DimensionValue.
        :type dimension_value: str

        """
        self.swagger_types = {
            'dimension_value': 'str'
        }

        self.attribute_map = {
            'dimension_value': 'dimensionValue'
        }

        self._dimension_value = None

    @property
    def dimension_value(self):
        """
        Gets the dimension_value of this DimensionValue.
        The value of the dimension.


        :return: The dimension_value of this DimensionValue.
        :rtype: str
        """
        return self._dimension_value

    @dimension_value.setter
    def dimension_value(self, dimension_value):
        """
        Sets the dimension_value of this DimensionValue.
        The value of the dimension.


        :param dimension_value: The dimension_value of this DimensionValue.
        :type: str
        """
        self._dimension_value = dimension_value

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
