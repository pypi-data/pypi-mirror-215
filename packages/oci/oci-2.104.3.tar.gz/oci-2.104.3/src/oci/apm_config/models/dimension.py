# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Dimension(object):
    """
    A dimension is a label that is used to describe or group metrics.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Dimension object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this Dimension.
        :type name: str

        :param value_source:
            The value to assign to the value_source property of this Dimension.
        :type value_source: str

        """
        self.swagger_types = {
            'name': 'str',
            'value_source': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'value_source': 'valueSource'
        }

        self._name = None
        self._value_source = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this Dimension.
        The name of the dimension.


        :return: The name of this Dimension.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Dimension.
        The name of the dimension.


        :param name: The name of this Dimension.
        :type: str
        """
        self._name = name

    @property
    def value_source(self):
        """
        Gets the value_source of this Dimension.
        The source to populate the dimension. This must not be specified.


        :return: The value_source of this Dimension.
        :rtype: str
        """
        return self._value_source

    @value_source.setter
    def value_source(self, value_source):
        """
        Sets the value_source of this Dimension.
        The source to populate the dimension. This must not be specified.


        :param value_source: The value_source of this Dimension.
        :type: str
        """
        self._value_source = value_source

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
