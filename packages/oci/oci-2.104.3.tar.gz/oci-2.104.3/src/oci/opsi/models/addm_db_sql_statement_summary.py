# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AddmDbSqlStatementSummary(object):
    """
    Details for a given SQL ID
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AddmDbSqlStatementSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AddmDbSqlStatementSummary.
        :type id: str

        :param sql_identifier:
            The value to assign to the sql_identifier property of this AddmDbSqlStatementSummary.
        :type sql_identifier: str

        :param sql_text:
            The value to assign to the sql_text property of this AddmDbSqlStatementSummary.
        :type sql_text: str

        :param is_sql_text_truncated:
            The value to assign to the is_sql_text_truncated property of this AddmDbSqlStatementSummary.
        :type is_sql_text_truncated: bool

        :param sql_command:
            The value to assign to the sql_command property of this AddmDbSqlStatementSummary.
        :type sql_command: str

        """
        self.swagger_types = {
            'id': 'str',
            'sql_identifier': 'str',
            'sql_text': 'str',
            'is_sql_text_truncated': 'bool',
            'sql_command': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'sql_identifier': 'sqlIdentifier',
            'sql_text': 'sqlText',
            'is_sql_text_truncated': 'isSqlTextTruncated',
            'sql_command': 'sqlCommand'
        }

        self._id = None
        self._sql_identifier = None
        self._sql_text = None
        self._is_sql_text_truncated = None
        self._sql_command = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this AddmDbSqlStatementSummary.
        The `OCID`__ of the Database insight.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this AddmDbSqlStatementSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AddmDbSqlStatementSummary.
        The `OCID`__ of the Database insight.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this AddmDbSqlStatementSummary.
        :type: str
        """
        self._id = id

    @property
    def sql_identifier(self):
        """
        **[Required]** Gets the sql_identifier of this AddmDbSqlStatementSummary.
        SQL identifier


        :return: The sql_identifier of this AddmDbSqlStatementSummary.
        :rtype: str
        """
        return self._sql_identifier

    @sql_identifier.setter
    def sql_identifier(self, sql_identifier):
        """
        Sets the sql_identifier of this AddmDbSqlStatementSummary.
        SQL identifier


        :param sql_identifier: The sql_identifier of this AddmDbSqlStatementSummary.
        :type: str
        """
        self._sql_identifier = sql_identifier

    @property
    def sql_text(self):
        """
        **[Required]** Gets the sql_text of this AddmDbSqlStatementSummary.
        First 3800 characters of the SQL text


        :return: The sql_text of this AddmDbSqlStatementSummary.
        :rtype: str
        """
        return self._sql_text

    @sql_text.setter
    def sql_text(self, sql_text):
        """
        Sets the sql_text of this AddmDbSqlStatementSummary.
        First 3800 characters of the SQL text


        :param sql_text: The sql_text of this AddmDbSqlStatementSummary.
        :type: str
        """
        self._sql_text = sql_text

    @property
    def is_sql_text_truncated(self):
        """
        **[Required]** Gets the is_sql_text_truncated of this AddmDbSqlStatementSummary.
        SQL identifier


        :return: The is_sql_text_truncated of this AddmDbSqlStatementSummary.
        :rtype: bool
        """
        return self._is_sql_text_truncated

    @is_sql_text_truncated.setter
    def is_sql_text_truncated(self, is_sql_text_truncated):
        """
        Sets the is_sql_text_truncated of this AddmDbSqlStatementSummary.
        SQL identifier


        :param is_sql_text_truncated: The is_sql_text_truncated of this AddmDbSqlStatementSummary.
        :type: bool
        """
        self._is_sql_text_truncated = is_sql_text_truncated

    @property
    def sql_command(self):
        """
        **[Required]** Gets the sql_command of this AddmDbSqlStatementSummary.
        SQL command name (such as SELECT, INSERT)


        :return: The sql_command of this AddmDbSqlStatementSummary.
        :rtype: str
        """
        return self._sql_command

    @sql_command.setter
    def sql_command(self, sql_command):
        """
        Sets the sql_command of this AddmDbSqlStatementSummary.
        SQL command name (such as SELECT, INSERT)


        :param sql_command: The sql_command of this AddmDbSqlStatementSummary.
        :type: str
        """
        self._sql_command = sql_command

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
