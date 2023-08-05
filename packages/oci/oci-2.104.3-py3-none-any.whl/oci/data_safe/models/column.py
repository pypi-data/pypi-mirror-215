# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Column(object):
    """
    The description of the column.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Column object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this Column.
        :type display_name: str

        :param field_name:
            The value to assign to the field_name property of this Column.
        :type field_name: str

        :param data_type:
            The value to assign to the data_type property of this Column.
        :type data_type: str

        :param is_hidden:
            The value to assign to the is_hidden property of this Column.
        :type is_hidden: bool

        :param display_order:
            The value to assign to the display_order property of this Column.
        :type display_order: int

        """
        self.swagger_types = {
            'display_name': 'str',
            'field_name': 'str',
            'data_type': 'str',
            'is_hidden': 'bool',
            'display_order': 'int'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'field_name': 'fieldName',
            'data_type': 'dataType',
            'is_hidden': 'isHidden',
            'display_order': 'displayOrder'
        }

        self._display_name = None
        self._field_name = None
        self._data_type = None
        self._is_hidden = None
        self._display_order = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this Column.
        Name of the column displayed on UI.


        :return: The display_name of this Column.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this Column.
        Name of the column displayed on UI.


        :param display_name: The display_name of this Column.
        :type: str
        """
        self._display_name = display_name

    @property
    def field_name(self):
        """
        **[Required]** Gets the field_name of this Column.
        Specifies the corresponding field name in the data source.


        :return: The field_name of this Column.
        :rtype: str
        """
        return self._field_name

    @field_name.setter
    def field_name(self, field_name):
        """
        Sets the field_name of this Column.
        Specifies the corresponding field name in the data source.


        :param field_name: The field_name of this Column.
        :type: str
        """
        self._field_name = field_name

    @property
    def data_type(self):
        """
        Gets the data_type of this Column.
        Specifies the data type of the column.


        :return: The data_type of this Column.
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """
        Sets the data_type of this Column.
        Specifies the data type of the column.


        :param data_type: The data_type of this Column.
        :type: str
        """
        self._data_type = data_type

    @property
    def is_hidden(self):
        """
        **[Required]** Gets the is_hidden of this Column.
        Indicates if the column is hidden. Values can either be 'true' or 'false'.


        :return: The is_hidden of this Column.
        :rtype: bool
        """
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, is_hidden):
        """
        Sets the is_hidden of this Column.
        Indicates if the column is hidden. Values can either be 'true' or 'false'.


        :param is_hidden: The is_hidden of this Column.
        :type: bool
        """
        self._is_hidden = is_hidden

    @property
    def display_order(self):
        """
        **[Required]** Gets the display_order of this Column.
        Specifies the display order of the column.


        :return: The display_order of this Column.
        :rtype: int
        """
        return self._display_order

    @display_order.setter
    def display_order(self, display_order):
        """
        Sets the display_order of this Column.
        Specifies the display order of the column.


        :param display_order: The display_order of this Column.
        :type: int
        """
        self._display_order = display_order

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
