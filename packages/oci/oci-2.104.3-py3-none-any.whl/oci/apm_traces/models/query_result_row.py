# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class QueryResultRow(object):
    """
    Object that represents a single row of the query result.  It contains the queryResultRowData object that contains the actual data
    represented by the elements of the query result row, and a queryResultRowMetadata object that contains the metadata about the data contained in
    the query result row.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new QueryResultRow object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param query_result_row_data:
            The value to assign to the query_result_row_data property of this QueryResultRow.
        :type query_result_row_data: dict(str, object)

        :param query_result_row_metadata:
            The value to assign to the query_result_row_metadata property of this QueryResultRow.
        :type query_result_row_metadata: dict(str, object)

        """
        self.swagger_types = {
            'query_result_row_data': 'dict(str, object)',
            'query_result_row_metadata': 'dict(str, object)'
        }

        self.attribute_map = {
            'query_result_row_data': 'queryResultRowData',
            'query_result_row_metadata': 'queryResultRowMetadata'
        }

        self._query_result_row_data = None
        self._query_result_row_metadata = None

    @property
    def query_result_row_data(self):
        """
        **[Required]** Gets the query_result_row_data of this QueryResultRow.
        A map containing the actual data represented by a single row of the query result.
        The key is the column name or attribute specified in the show clause, or an aggregate function in the show clause.
        The value is the actual value of that attribute or aggregate function of the corresponding single row of the query result set.
        If an alias name is specified for an attribute or an aggregate function, then the key will be the alias name specified in the show
        clause.  If an alias name is not specified for the group by aggregate function in the show clause, then the corresponding key
        will be the appropriate aggregate_function_name_column_name (For example: count(traces) will be keyed as count_traces).  The datatype of the value
        is presented in the queryResultRowTypeSummaries list in the queryResultMetadata structure, where the i-th queryResultRowTypeSummary object
        represents the datatype of the i-th value when this map is iterated in order.


        :return: The query_result_row_data of this QueryResultRow.
        :rtype: dict(str, object)
        """
        return self._query_result_row_data

    @query_result_row_data.setter
    def query_result_row_data(self, query_result_row_data):
        """
        Sets the query_result_row_data of this QueryResultRow.
        A map containing the actual data represented by a single row of the query result.
        The key is the column name or attribute specified in the show clause, or an aggregate function in the show clause.
        The value is the actual value of that attribute or aggregate function of the corresponding single row of the query result set.
        If an alias name is specified for an attribute or an aggregate function, then the key will be the alias name specified in the show
        clause.  If an alias name is not specified for the group by aggregate function in the show clause, then the corresponding key
        will be the appropriate aggregate_function_name_column_name (For example: count(traces) will be keyed as count_traces).  The datatype of the value
        is presented in the queryResultRowTypeSummaries list in the queryResultMetadata structure, where the i-th queryResultRowTypeSummary object
        represents the datatype of the i-th value when this map is iterated in order.


        :param query_result_row_data: The query_result_row_data of this QueryResultRow.
        :type: dict(str, object)
        """
        self._query_result_row_data = query_result_row_data

    @property
    def query_result_row_metadata(self):
        """
        **[Required]** Gets the query_result_row_metadata of this QueryResultRow.
        A map containing metadata or add-on data for the data presented in the queryResultRowData map.  Data required to present drill down
        information from the queryResultRowData is presented as key-value pairs.


        :return: The query_result_row_metadata of this QueryResultRow.
        :rtype: dict(str, object)
        """
        return self._query_result_row_metadata

    @query_result_row_metadata.setter
    def query_result_row_metadata(self, query_result_row_metadata):
        """
        Sets the query_result_row_metadata of this QueryResultRow.
        A map containing metadata or add-on data for the data presented in the queryResultRowData map.  Data required to present drill down
        information from the queryResultRowData is presented as key-value pairs.


        :param query_result_row_metadata: The query_result_row_metadata of this QueryResultRow.
        :type: dict(str, object)
        """
        self._query_result_row_metadata = query_result_row_metadata

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
