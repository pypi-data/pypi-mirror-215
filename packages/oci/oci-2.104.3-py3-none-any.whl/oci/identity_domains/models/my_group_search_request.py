# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyGroupSearchRequest(object):
    """
    Clients MAY execute queries without passing parameters on the URL by using the HTTP POST verb combined with the **.search** path extension. The inclusion of **.search** on the end of a valid SCIM endpoint SHALL be used to indicate the HTTP POST verb is intended to be a query operation. To create a new query result set, a SCIM client sends an HTTP POST request to the desired SCIM resource endpoint (ending in **.search**). The body of the POST request MAY include any of the parameters.
    """

    #: A constant which can be used with the attribute_sets property of a MyGroupSearchRequest.
    #: This constant has a value of "all"
    ATTRIBUTE_SETS_ALL = "all"

    #: A constant which can be used with the attribute_sets property of a MyGroupSearchRequest.
    #: This constant has a value of "always"
    ATTRIBUTE_SETS_ALWAYS = "always"

    #: A constant which can be used with the attribute_sets property of a MyGroupSearchRequest.
    #: This constant has a value of "never"
    ATTRIBUTE_SETS_NEVER = "never"

    #: A constant which can be used with the attribute_sets property of a MyGroupSearchRequest.
    #: This constant has a value of "request"
    ATTRIBUTE_SETS_REQUEST = "request"

    #: A constant which can be used with the attribute_sets property of a MyGroupSearchRequest.
    #: This constant has a value of "default"
    ATTRIBUTE_SETS_DEFAULT = "default"

    #: A constant which can be used with the sort_order property of a MyGroupSearchRequest.
    #: This constant has a value of "ASCENDING"
    SORT_ORDER_ASCENDING = "ASCENDING"

    #: A constant which can be used with the sort_order property of a MyGroupSearchRequest.
    #: This constant has a value of "DESCENDING"
    SORT_ORDER_DESCENDING = "DESCENDING"

    def __init__(self, **kwargs):
        """
        Initializes a new MyGroupSearchRequest object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param schemas:
            The value to assign to the schemas property of this MyGroupSearchRequest.
        :type schemas: list[str]

        :param attributes:
            The value to assign to the attributes property of this MyGroupSearchRequest.
        :type attributes: list[str]

        :param attribute_sets:
            The value to assign to the attribute_sets property of this MyGroupSearchRequest.
            Allowed values for items in this list are: "all", "always", "never", "request", "default"
        :type attribute_sets: list[str]

        :param filter:
            The value to assign to the filter property of this MyGroupSearchRequest.
        :type filter: str

        :param sort_by:
            The value to assign to the sort_by property of this MyGroupSearchRequest.
        :type sort_by: str

        :param sort_order:
            The value to assign to the sort_order property of this MyGroupSearchRequest.
            Allowed values for this property are: "ASCENDING", "DESCENDING"
        :type sort_order: str

        :param start_index:
            The value to assign to the start_index property of this MyGroupSearchRequest.
        :type start_index: int

        :param count:
            The value to assign to the count property of this MyGroupSearchRequest.
        :type count: int

        """
        self.swagger_types = {
            'schemas': 'list[str]',
            'attributes': 'list[str]',
            'attribute_sets': 'list[str]',
            'filter': 'str',
            'sort_by': 'str',
            'sort_order': 'str',
            'start_index': 'int',
            'count': 'int'
        }

        self.attribute_map = {
            'schemas': 'schemas',
            'attributes': 'attributes',
            'attribute_sets': 'attributeSets',
            'filter': 'filter',
            'sort_by': 'sortBy',
            'sort_order': 'sortOrder',
            'start_index': 'startIndex',
            'count': 'count'
        }

        self._schemas = None
        self._attributes = None
        self._attribute_sets = None
        self._filter = None
        self._sort_by = None
        self._sort_order = None
        self._start_index = None
        self._count = None

    @property
    def schemas(self):
        """
        **[Required]** Gets the schemas of this MyGroupSearchRequest.
        The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. Query requests MUST be identified using the following URI: \"urn:ietf:params:scim:api:messages:2.0:SearchRequest\" REQUIRED.


        :return: The schemas of this MyGroupSearchRequest.
        :rtype: list[str]
        """
        return self._schemas

    @schemas.setter
    def schemas(self, schemas):
        """
        Sets the schemas of this MyGroupSearchRequest.
        The schemas attribute is an array of Strings which allows introspection of the supported schema version for a SCIM representation as well any schema extensions supported by that representation. Each String value must be a unique URI. Query requests MUST be identified using the following URI: \"urn:ietf:params:scim:api:messages:2.0:SearchRequest\" REQUIRED.


        :param schemas: The schemas of this MyGroupSearchRequest.
        :type: list[str]
        """
        self._schemas = schemas

    @property
    def attributes(self):
        """
        Gets the attributes of this MyGroupSearchRequest.
        A multi-valued list of strings indicating the names of resource attributes to return in the response overriding the set of attributes that would be returned by default. Attribute names MUST be in standard attribute notation (`Section 3.10`__) form. See (`additional retrieval query parameters`__). OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.10
        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.9


        :return: The attributes of this MyGroupSearchRequest.
        :rtype: list[str]
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this MyGroupSearchRequest.
        A multi-valued list of strings indicating the names of resource attributes to return in the response overriding the set of attributes that would be returned by default. Attribute names MUST be in standard attribute notation (`Section 3.10`__) form. See (`additional retrieval query parameters`__). OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.10
        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.9


        :param attributes: The attributes of this MyGroupSearchRequest.
        :type: list[str]
        """
        self._attributes = attributes

    @property
    def attribute_sets(self):
        """
        Gets the attribute_sets of this MyGroupSearchRequest.
        A multi-valued list of strings indicating the return type of attribute definition. The specified set of attributes can be fetched by the return type of the attribute. One or more values can be given together to fetch more than one group of attributes. If \"attributes\" query parameter is also available, union of the two is fetched. Valid values : all, always, never, request, default. Values are case-insensitive. OPTIONAL.

        Allowed values for items in this list are: "all", "always", "never", "request", "default"


        :return: The attribute_sets of this MyGroupSearchRequest.
        :rtype: list[str]
        """
        return self._attribute_sets

    @attribute_sets.setter
    def attribute_sets(self, attribute_sets):
        """
        Sets the attribute_sets of this MyGroupSearchRequest.
        A multi-valued list of strings indicating the return type of attribute definition. The specified set of attributes can be fetched by the return type of the attribute. One or more values can be given together to fetch more than one group of attributes. If \"attributes\" query parameter is also available, union of the two is fetched. Valid values : all, always, never, request, default. Values are case-insensitive. OPTIONAL.


        :param attribute_sets: The attribute_sets of this MyGroupSearchRequest.
        :type: list[str]
        """
        allowed_values = ["all", "always", "never", "request", "default"]

        if attribute_sets and attribute_sets is not NONE_SENTINEL:
            for value in attribute_sets:
                if not value_allowed_none_or_none_sentinel(value, allowed_values):
                    raise ValueError(
                        "Invalid value for `attribute_sets`, must be None or one of {0}"
                        .format(allowed_values)
                    )
        self._attribute_sets = attribute_sets

    @property
    def filter(self):
        """
        Gets the filter of this MyGroupSearchRequest.
        The filter string that is used to request a subset of resources. The filter string MUST be a valid filter expression. See `Section 3.4.2.2`__. OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.2


        :return: The filter of this MyGroupSearchRequest.
        :rtype: str
        """
        return self._filter

    @filter.setter
    def filter(self, filter):
        """
        Sets the filter of this MyGroupSearchRequest.
        The filter string that is used to request a subset of resources. The filter string MUST be a valid filter expression. See `Section 3.4.2.2`__. OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.2


        :param filter: The filter of this MyGroupSearchRequest.
        :type: str
        """
        self._filter = filter

    @property
    def sort_by(self):
        """
        Gets the sort_by of this MyGroupSearchRequest.
        A string that indicates the attribute whose value SHALL be used to order the returned responses. The sortBy attribute MUST be in standard attribute notation (`Section 3.10`__) form. See `Sorting section`__. OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.10
        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.3


        :return: The sort_by of this MyGroupSearchRequest.
        :rtype: str
        """
        return self._sort_by

    @sort_by.setter
    def sort_by(self, sort_by):
        """
        Sets the sort_by of this MyGroupSearchRequest.
        A string that indicates the attribute whose value SHALL be used to order the returned responses. The sortBy attribute MUST be in standard attribute notation (`Section 3.10`__) form. See `Sorting section`__. OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.10
        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.3


        :param sort_by: The sort_by of this MyGroupSearchRequest.
        :type: str
        """
        self._sort_by = sort_by

    @property
    def sort_order(self):
        """
        Gets the sort_order of this MyGroupSearchRequest.
        A string that indicates the order in which the sortBy parameter is applied. Allowed values are \"ascending\" and \"descending\". See (`Sorting Section`__). OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.3

        Allowed values for this property are: "ASCENDING", "DESCENDING"


        :return: The sort_order of this MyGroupSearchRequest.
        :rtype: str
        """
        return self._sort_order

    @sort_order.setter
    def sort_order(self, sort_order):
        """
        Sets the sort_order of this MyGroupSearchRequest.
        A string that indicates the order in which the sortBy parameter is applied. Allowed values are \"ascending\" and \"descending\". See (`Sorting Section`__). OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.3


        :param sort_order: The sort_order of this MyGroupSearchRequest.
        :type: str
        """
        allowed_values = ["ASCENDING", "DESCENDING"]
        if not value_allowed_none_or_none_sentinel(sort_order, allowed_values):
            raise ValueError(
                "Invalid value for `sort_order`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._sort_order = sort_order

    @property
    def start_index(self):
        """
        Gets the start_index of this MyGroupSearchRequest.
        An integer that indicates the 1-based index of the first query result. See `Pagination Section`__. OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.4


        :return: The start_index of this MyGroupSearchRequest.
        :rtype: int
        """
        return self._start_index

    @start_index.setter
    def start_index(self, start_index):
        """
        Sets the start_index of this MyGroupSearchRequest.
        An integer that indicates the 1-based index of the first query result. See `Pagination Section`__. OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.4


        :param start_index: The start_index of this MyGroupSearchRequest.
        :type: int
        """
        self._start_index = start_index

    @property
    def count(self):
        """
        Gets the count of this MyGroupSearchRequest.
        An integer that indicates the desired maximum number of query results per page. 1000 is the largest value that you can use. See the Pagination section of the System for Cross-Domain Identity Management Protocol specification for more information. (`Section 3.4.2.4`__). OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.4


        :return: The count of this MyGroupSearchRequest.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this MyGroupSearchRequest.
        An integer that indicates the desired maximum number of query results per page. 1000 is the largest value that you can use. See the Pagination section of the System for Cross-Domain Identity Management Protocol specification for more information. (`Section 3.4.2.4`__). OPTIONAL.

        __ https://tools.ietf.org/html/draft-ietf-scim-api-19#section-3.4.2.4


        :param count: The count of this MyGroupSearchRequest.
        :type: int
        """
        self._count = count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
