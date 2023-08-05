# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SqlTextSummary(object):
    """
    SQL Text details
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SqlTextSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param sql_identifier:
            The value to assign to the sql_identifier property of this SqlTextSummary.
        :type sql_identifier: str

        :param id:
            The value to assign to the id property of this SqlTextSummary.
        :type id: str

        :param database_id:
            The value to assign to the database_id property of this SqlTextSummary.
        :type database_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this SqlTextSummary.
        :type compartment_id: str

        :param sql_text:
            The value to assign to the sql_text property of this SqlTextSummary.
        :type sql_text: str

        """
        self.swagger_types = {
            'sql_identifier': 'str',
            'id': 'str',
            'database_id': 'str',
            'compartment_id': 'str',
            'sql_text': 'str'
        }

        self.attribute_map = {
            'sql_identifier': 'sqlIdentifier',
            'id': 'id',
            'database_id': 'databaseId',
            'compartment_id': 'compartmentId',
            'sql_text': 'sqlText'
        }

        self._sql_identifier = None
        self._id = None
        self._database_id = None
        self._compartment_id = None
        self._sql_text = None

    @property
    def sql_identifier(self):
        """
        **[Required]** Gets the sql_identifier of this SqlTextSummary.
        Unique SQL_ID for a SQL Statement.


        :return: The sql_identifier of this SqlTextSummary.
        :rtype: str
        """
        return self._sql_identifier

    @sql_identifier.setter
    def sql_identifier(self, sql_identifier):
        """
        Sets the sql_identifier of this SqlTextSummary.
        Unique SQL_ID for a SQL Statement.


        :param sql_identifier: The sql_identifier of this SqlTextSummary.
        :type: str
        """
        self._sql_identifier = sql_identifier

    @property
    def id(self):
        """
        **[Required]** Gets the id of this SqlTextSummary.
        The `OCID`__ of the database insight resource.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this SqlTextSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SqlTextSummary.
        The `OCID`__ of the database insight resource.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this SqlTextSummary.
        :type: str
        """
        self._id = id

    @property
    def database_id(self):
        """
        **[Required]** Gets the database_id of this SqlTextSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The database_id of this SqlTextSummary.
        :rtype: str
        """
        return self._database_id

    @database_id.setter
    def database_id(self, database_id):
        """
        Sets the database_id of this SqlTextSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param database_id: The database_id of this SqlTextSummary.
        :type: str
        """
        self._database_id = database_id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this SqlTextSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this SqlTextSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this SqlTextSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this SqlTextSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def sql_text(self):
        """
        **[Required]** Gets the sql_text of this SqlTextSummary.
        SQL Text


        :return: The sql_text of this SqlTextSummary.
        :rtype: str
        """
        return self._sql_text

    @sql_text.setter
    def sql_text(self, sql_text):
        """
        Sets the sql_text of this SqlTextSummary.
        SQL Text


        :param sql_text: The sql_text of this SqlTextSummary.
        :type: str
        """
        self._sql_text = sql_text

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
