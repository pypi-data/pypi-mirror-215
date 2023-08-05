# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .format_entry import FormatEntry
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SQLExpressionFormatEntry(FormatEntry):
    """
    The SQL Expression masking format uses a SQL expression to generate values
    that are used to replace the original data values. SQL expressions with
    dbms_lob and other user-defined functions can be used to mask columns of
    Large Object data type (LOB). To learn more, check SQL Expression in the
    Data Safe documentation.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SQLExpressionFormatEntry object with values from keyword arguments. The default value of the :py:attr:`~oci.data_safe.models.SQLExpressionFormatEntry.type` attribute
        of this class is ``SQL_EXPRESSION`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this SQLExpressionFormatEntry.
            Allowed values for this property are: "DELETE_ROWS", "DETERMINISTIC_SUBSTITUTION", "DETERMINISTIC_ENCRYPTION", "DETERMINISTIC_ENCRYPTION_DATE", "FIXED_NUMBER", "FIXED_STRING", "LIBRARY_MASKING_FORMAT", "NULL_VALUE", "POST_PROCESSING_FUNCTION", "PRESERVE_ORIGINAL_DATA", "RANDOM_DATE", "RANDOM_DECIMAL_NUMBER", "RANDOM_DIGITS", "RANDOM_LIST", "RANDOM_NUMBER", "RANDOM_STRING", "RANDOM_SUBSTITUTION", "REGULAR_EXPRESSION", "SHUFFLE", "SQL_EXPRESSION", "SUBSTRING", "TRUNCATE_TABLE", "USER_DEFINED_FUNCTION"
        :type type: str

        :param description:
            The value to assign to the description property of this SQLExpressionFormatEntry.
        :type description: str

        :param sql_expression:
            The value to assign to the sql_expression property of this SQLExpressionFormatEntry.
        :type sql_expression: str

        """
        self.swagger_types = {
            'type': 'str',
            'description': 'str',
            'sql_expression': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'description': 'description',
            'sql_expression': 'sqlExpression'
        }

        self._type = None
        self._description = None
        self._sql_expression = None
        self._type = 'SQL_EXPRESSION'

    @property
    def sql_expression(self):
        """
        **[Required]** Gets the sql_expression of this SQLExpressionFormatEntry.
        The SQL expression to be used to generate the masked values. It can
        consist of one or more values, operators, and SQL functions that
        evaluate to a value. It can also contain substitution columns from
        the same table. Specify the substitution columns within percent (%)
        symbols.


        :return: The sql_expression of this SQLExpressionFormatEntry.
        :rtype: str
        """
        return self._sql_expression

    @sql_expression.setter
    def sql_expression(self, sql_expression):
        """
        Sets the sql_expression of this SQLExpressionFormatEntry.
        The SQL expression to be used to generate the masked values. It can
        consist of one or more values, operators, and SQL functions that
        evaluate to a value. It can also contain substitution columns from
        the same table. Specify the substitution columns within percent (%)
        symbols.


        :param sql_expression: The sql_expression of this SQLExpressionFormatEntry.
        :type: str
        """
        self._sql_expression = sql_expression

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
