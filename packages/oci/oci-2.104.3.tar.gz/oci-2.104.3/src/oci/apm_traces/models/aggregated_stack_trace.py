# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AggregatedStackTrace(object):
    """
    A branching tree with aggregated stack trace.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AggregatedStackTrace object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param stack_trace_element:
            The value to assign to the stack_trace_element property of this AggregatedStackTrace.
        :type stack_trace_element: oci.apm_traces.models.StackTraceElement

        :param children:
            The value to assign to the children property of this AggregatedStackTrace.
        :type children: list[oci.apm_traces.models.AggregatedStackTrace]

        """
        self.swagger_types = {
            'stack_trace_element': 'StackTraceElement',
            'children': 'list[AggregatedStackTrace]'
        }

        self.attribute_map = {
            'stack_trace_element': 'stackTraceElement',
            'children': 'children'
        }

        self._stack_trace_element = None
        self._children = None

    @property
    def stack_trace_element(self):
        """
        Gets the stack_trace_element of this AggregatedStackTrace.

        :return: The stack_trace_element of this AggregatedStackTrace.
        :rtype: oci.apm_traces.models.StackTraceElement
        """
        return self._stack_trace_element

    @stack_trace_element.setter
    def stack_trace_element(self, stack_trace_element):
        """
        Sets the stack_trace_element of this AggregatedStackTrace.

        :param stack_trace_element: The stack_trace_element of this AggregatedStackTrace.
        :type: oci.apm_traces.models.StackTraceElement
        """
        self._stack_trace_element = stack_trace_element

    @property
    def children(self):
        """
        Gets the children of this AggregatedStackTrace.
        List of child aggregated stack trace to represent branches.


        :return: The children of this AggregatedStackTrace.
        :rtype: list[oci.apm_traces.models.AggregatedStackTrace]
        """
        return self._children

    @children.setter
    def children(self, children):
        """
        Sets the children of this AggregatedStackTrace.
        List of child aggregated stack trace to represent branches.


        :param children: The children of this AggregatedStackTrace.
        :type: list[oci.apm_traces.models.AggregatedStackTrace]
        """
        self._children = children

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
